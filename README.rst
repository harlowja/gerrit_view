**Gerrit & zuul viewers & tools for all**
=========================================

qgerrit
------------

Use `qgerrit` to find out what your friends have been up to::

    $ qgerrit -u 'harlowja'
    $ qgerrit -h
    
    Usage: qgerrit [options]
    
    Options:
      -h, --help            show this help message and exit
      -l USER, --login=USER
                            connect to gerrit with USER
      -u USER, --user=USER  gather information on given USER
      -s STATUS, --status=STATUS
                            gather information on given status
      -m MESSAGE, --message=MESSAGE
                            filter on message
      -p PROJECT, --project=PROJECT
                            gather information on given project
      -b BRANCH, --branch=BRANCH
                            filter on branch
      -a APPROVAL, --approval=APPROVAL
                            filter on approval value min %n [default: no filter]
      -k FILE, --keyfile=FILE
                            gerrit ssh keyfile [default: /home/josh/.ssh/id_rsa]
      -t SORT, --sort=SORT  sort order for results [default: createdOn]
      -f FIELD, --field=FIELD
                            display field in results [default: 'approvals',
                            'branch', 'createdOn', 'lastUpdated', 'owner',
                            'project', 'status', 'subject', 'topic', 'url']
    

cgerrit
------------

Use `cgerrit` to watch (in realtime) the reviews showing up (powered by
urwid_ and the curses_ library):

.. image:: https://github.com/harlowja/gerrit_view/raw/master/screenshots/screen1.png

::

    $ cgerrit
    $ cgerrit -h
    
    Usage: cgerrit [options]
    
    Options:
      -h, --help            show this help message and exit
      -u USER, --user=USER  gerrit user [default: harlowja]
      -s SERVER, --server=SERVER
                            gerrit server [default: review.openstack.org]
      -p PORT, --port=PORT  gerrit port [default: 29418]
      --prefetch=COUNT      prefetch amount [default: 50]
      -k FILE, --keyfile=FILE
                            gerrit ssh keyfile [default:
                            /home/harlowja/.ssh/id_rsa]
      --project=PROJECT     only show given projects reviews
      -i COUNT, --items=COUNT
                            how many items to keep visible [default: 50]

czuul
------------

Use `czuul` to watch the reviews zuul status (powered by
urwid_, curses_ library and the requests_ library):

.. image:: https://github.com/harlowja/gerrit_view/raw/master/screenshots/screen2.png

::

    $ czuul
    $ czuul -h
    
    Usage: czuul [options]
    
    Options:
      -h, --help            show this help message and exit
      -s URL, --server=URL  zuul server [default:
                            http://zuul.openstack.org/status.json]
      -p PIPELINE, --pipeline=PIPELINE
                            only show given pipelines reviews

.. _urwid: http://excess.org/urwid/
.. _curses: http://docs.python.org/2.7/library/curses.html
.. _requests: http://www.python-requests.org/
