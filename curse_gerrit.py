#!/usr/bin/python

import collections
import getpass
import logging
import os
import threading
import time

import Queue

from datetime import datetime

from gerritlib import gerrit
import urwid

logging.basicConfig(level=logging.DEBUG, filename='output.log')
LOG = logging.getLogger(__name__)

### DEFAULT SETTINGS

GERRIT_HOST = 'review.openstack.org'
GERRIT_PORT = 29418
CONNECT_ATTEMPTS = 5
MAX_LIST_LEN = 50
TRUNCATE_LEN = 47  # 3 for the ...
ALARM_FREQ = 0.5

### GUI CONSTANTS

PALETTE = (
    ('body', urwid.WHITE, urwid.BLACK, 'standout'),
    ('merged', urwid.LIGHT_GREEN, urwid.BLACK, 'standout'),
    ('approved', urwid.LIGHT_GREEN, urwid.BLACK, 'standout'),
    ('rejected', urwid.LIGHT_RED, urwid.BLACK, 'standout'),
    ('succeeded', urwid.LIGHT_GREEN, urwid.BLACK, 'standout'),
)
COLUMNS = (
    'Username',
    "Topic",
    "Url",
    "Project",
    'Subject',
    'Created On',
    'Status',
    'Comment',
)
COLUMN_ATTRIBUTES = {
    'Created On': (urwid.WEIGHT, 0.5),
    'Status': (urwid.FIXED, 9),
    'Username': (urwid.FIXED, 10),
    'Project': (urwid.WEIGHT, 0.5),
    'Topic': (urwid.WEIGHT, 0.33),
    'Url': (urwid.WEIGHT, 1.0),
    'Subject': (urwid.WEIGHT, 1.0),
    'Comment': (urwid.WEIGHT, 0.7),
}

### HELPERS


class ExponentialBackoff(object):
    """An iterable object that will yield back an exponential delay sequence
    provided an exponent and a number of items to yield. This object may be
    iterated over multiple times (yielding the same sequence each time).
    """
    def __init__(self, attempts, exponent=2):
        self.attempts = int(attempts)
        self.exponent = exponent

    def __iter__(self):
        if self.attempts <= 0:
            raise StopIteration()
        for i in xrange(0, self.attempts):
            yield self.exponent ** i

    def __str__(self):
        return "ExponentialBackoff: %s" % ([str(v) for v in self])


def _get_key_path():
    home_dir = os.path.expanduser("~")
    ssh_dir = os.path.join(home_dir, ".ssh")
    if not os.path.isdir(ssh_dir):
        return None
    for k in ('id_rsa', 'id_dsa'):
        path = os.path.join(ssh_dir, k)
        if os.path.isfile(path):
            return path
    return None


def _get_now():
    dt = datetime.now()
    return dt.strftime('%I:%M:%S %p %m/%d/%Y')


def _get_date(k, row):
    v = _get_key(k, row)
    if not v:
        return ''
    try:
        dt = datetime.fromtimestamp(int(v))
        return dt.strftime('%I:%M %p %m/%d/%Y')
    except (ValueError, TypeError):
        return ''


def _trunc(text):
    if len(text) > TRUNCATE_LEN:
        text = text[0:TRUNCATE_LEN] + "..."
    return text


def _get_key(k, row, truncate=False):
    if k not in row:
        return ""
    v = str(row[k])
    if truncate:
        v = _trunc(v)
    return v


class GerritWatcher(threading.Thread):
    def __init__(self, queue, **config):
        super(GerritWatcher, self).__init__()
        self.queue = queue
        self.keyfile = config.get('keyfile', _get_key_path())
        self.port = int(config.get('port', GERRIT_PORT))
        self.server = str(config.get('server', GERRIT_HOST))
        self.connected = False
        self.daemon = True
        self.username = config.get('username', getpass.getuser())
        self.gerrit = None

    def _connect(self):
        try:
            self.gerrit = gerrit.Gerrit(self.server, self.username,
                                        self.port, self.keyfile)
            self.gerrit.startWatching()
            LOG.info('Start watching gerrit event stream.')
            self.connected = True
        except Exception:
            LOG.exception('Exception while connecting to gerrit')
            self.connected = False

    def _ensure_connected(self):
        if self.connected:
            return
        for i in ExponentialBackoff(CONNECT_ATTEMPTS):
            self._connect()
            if not self.connected:
                LOG.info("Trying connection again in %s seconds", i)
                time.sleep(i)
            else:
                break
        if not self.connected:
            raise IOError("Could not connect to '%s' on port %s"
                          % (self.server, self.port))

    def _handle_event(self, event):
        LOG.info('Placing event on producer queue: %s', event)
        self.queue.put(event)

    def _consume(self):
        try:
            event = self.gerrit.getEvent()
            self._handle_event(event)
        except Exception:
            LOG.exception('Exception encountered in event loop')
            if not self.gerrit.watcher_thread.is_alive():
                self.gerrit = None
                self.connected = False

    def run(self):
        while True:
            self._ensure_connected()
            self._consume()


def consume_queue(queue):
    events = []
    ev = None
    try:
        ev = queue.get(block=False)
    except Queue.Empty:
        pass
    if ev is not None:
        events.append(ev)
    return events


def _get_change_status(event):
    change_type = None
    for approval in event.get('approvals', []):
        if (approval['type'] == 'VRIF' and approval['value'] == '-2'):
            change_type = 'Failed'
        if (approval['type'] == 'VRIF' and approval['value'] == '2'):
            change_type = 'Succeeded'
        if (approval['type'] == 'CRVW' and approval['value'] == '-2'):
            change_type = 'Rejected'
        if (approval['type'] == 'CRVW' and approval['value'] == '2'):
            change_type = 'Approved'
    return change_type


###

def make_text(text):
    return urwid.Text(text, wrap='any', align='left')


def main():
    event_queue = Queue.Queue()
    gerrit_reader = GerritWatcher(event_queue)
    gerrit_details = collections.defaultdict(int)

    listwalker = urwid.SimpleListWalker([])
    listbox = urwid.ListBox(listwalker)
    table_header = []
    for col_name in COLUMNS:
        col_attrs = list(COLUMN_ATTRIBUTES[col_name])
        col_attrs.append(make_text(col_name))
        table_header.append(tuple(col_attrs))
    header_sep = urwid.AttrWrap(urwid.Divider('-'), 'body')
    footer_text = urwid.Text("Waiting for events...")
    table_header = urwid.AttrWrap(urwid.Columns(table_header, dividechars=1),
                                  'body')
    header_pile = urwid.Pile([table_header, header_sep])
    footer_details = urwid.Text('', align='right')
    footer = urwid.AttrWrap(urwid.Columns([footer_text, footer_details]),
                            'body')
    footer_sep = urwid.AttrWrap(urwid.Divider('-'), 'body')
    footer_pile = urwid.Pile([footer_sep, footer])
    frame = urwid.LineBox(urwid.Frame(urwid.AttrWrap(listbox, 'body'),
                          footer=footer_pile, header=header_pile))

    def exit_on_q(input):
        if input in ('q', 'Q', 'esc'):
            raise urwid.ExitMainLoop()

    def on_patchset_created(event):
        change = event['change']
        patch_set = event['patchSet']
        uploader = event['uploader']
        row = [
            _get_key('username', uploader),
            _get_key('topic', change),
            _get_key('url', change),
            _get_key('project', change),
            _get_key('subject', change, truncate=True),
            _get_date('createdOn', patch_set),
            "",  # status
            '',  # comment
        ]
        attr_row = []
        for (i, v) in enumerate(row):
            col_name = COLUMNS[i]
            col_attrs = list(COLUMN_ATTRIBUTES[col_name])
            col_attrs.append(make_text(v))
            attr_row.append(tuple(col_attrs))
        # The list is getting to big, shrink it.
        if len(listwalker) >= MAX_LIST_LEN:
            listwalker.pop()
        listwalker.append(urwid.Columns(attr_row, dividechars=1))

    def find_change(change):
        matched_c = None
        for c in listwalker:
            url = c.contents[COLUMNS.index('Url')]
            if url[0].text == change.get('url'):
                matched_c = c
                break
        return matched_c

    def set_status(match, text):
        if not text or match is None:
            return
        status_i = COLUMNS.index('Status')
        new_contents = list(match.contents[status_i])
        new_contents[0] = urwid.AttrWrap(make_text(text), text.lower())
        match.contents[status_i] = tuple(new_contents)

    def on_change_merged(event):
        change = event['change']
        match = find_change(change)
        if match is not None:
            set_status(match, 'Merged')

    def on_comment_added(event):
        change = event['change']
        match = find_change(change)
        if match is not None:
            comment = _trunc(event.get('comment', ''))
            if len(comment):
                comment_i = COLUMNS.index('Comment')
                match.contents[comment_i][0].set_text(comment)
            set_status(match, _get_change_status(event))

    def process_event(event):
        if not isinstance(event, (dict)) or not 'type' in event:
            return
        event_handlers = {
            'patchset-created': on_patchset_created,
            'comment-added': on_comment_added,
            'change-merged': on_change_merged,
        }
        event_type = str(event.get('type'))
        functor = event_handlers.get(event_type)
        if not functor:
            return
        gerrit_details[event_type] += 1
        functor(event)

    def process_gerrit():
        evs = consume_queue(event_queue)
        for e in evs:
            try:
                process_event(e)
            except Exception:
                LOG.exception("Failed handling event: %s", e)
        total_events = sum(gerrit_details.values())
        detail_text = "%s, %s events received" % (_get_now(), total_events)
        footer_details.set_text(detail_text)
        loop.event_loop.alarm(ALARM_FREQ, process_gerrit)

    loop = urwid.MainLoop(frame, PALETTE,
                          handle_mouse=False,
                          unhandled_input=exit_on_q)
    gerrit_reader.start()
    loop.event_loop.enter_idle(process_gerrit)
    loop.run()


if __name__ == "__main__":
    main()
