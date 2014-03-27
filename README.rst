**A set of tools to query/view Gerrit patch reviews and their Zuul status**
===========================================================================

Current set of tools:

- ``qgerrit`` -- to query different projects' Gerrit reviews based on a set of criteria/filters.

- ``cgerrit`` -- to view (in real time) Gerrit reviews on CLI.

- ``czuul`` -- to view Gerrit reviews' Zuul (a pipeline oriented project gating and automation system) status on CLI.



qgerrit
------------

Use ``qgerrit`` to query different projects' Gerrit reviews
based on a set of criteria/filters::


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
                            gerrit ssh keyfile [default: attempt to use
                            local agent]
      -t SORT, --sort=SORT  sort order for results [default: createdOn]
      -f FIELD, --field=FIELD
                            display field in results [default: 'approvals',
                            'branch', 'createdOn', 'lastUpdated', 'owner',
                            'project', 'status', 'subject', 'topic', 'url']

########
Examples
########

1. To enumerate all reviews requests for openstack/nova which touch a
   file with libvirt in the name::

    $ qgerrit \
      -l harlowja \
      -f url -f branch -f owner -f subject:100 \
      -f lastUpdated -f createdOn -f approvals \
      --sort createdOn \
      --project openstack/nova \
      libvirt

2. Show reviews for neutron which does not have any negative karma, as
   those reviews are going to be resubmitted any way::

    $ qgerrit -l harlowja -a c0,v0 neutron

(Thanks to Daniel Berrange for the above two examples)


cgerrit
------------

Use ``cgerrit`` to watch (in realtime) the reviews showing up (powered by
urwid_ and the gerrit_ libraries):

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
                            gerrit ssh keyfile [default: attempt to use local
                            agent]
      --project=PROJECT     only show given projects reviews
      -v FILE, --verbose=FILE
                            run in verbose mode and log output to the given file
      -i COUNT, --items=COUNT
                            how many items to keep visible [default: 50]
      -r FILE, --record-file=FILE
                            record file to store past events (also used for
                            initial view population if provided)

##############
Keys supported
##############

* (S, s) - Change sort mode (default none)
* (q, Q, esc) - Quit   
* (up, down, page up, page down) - Scroll up/down

########
Examples
########

1. To view reviews (real-time) for a specific project::

    $ cgerrit -u harlowja --project=openstack/neutron

2. To view reviews (real-time) for all projects::

    $ cgerrit -u harlowja


czuul
------------

Use ``czuul`` to watch the reviews zuul status (powered by
urwid_ and the requests_ libraries):

.. image:: https://github.com/harlowja/gerrit_view/raw/master/screenshots/screen2.png

::

    $ czuul
    $ czuul -h
    Usage: czuul [options]
    
    Options:
      -h, --help            show this help message and exit
      -s URL, --server=URL  zuul server [default:
                            http://zuul.openstack.org/status.json]
      --split-screens=SCREENS
                            split screen count [default: 3]
      -p PIPELINE, --pipeline=PIPELINE
                            only show given pipelines reviews
      -r SECONDS, --refresh=SECONDS
                            refresh every X seconds [default: 30]
      --project=PROJECT     only show given projects reviews
      --details             fetch each reviews details [default: False]
      --detail-dir=CLONE_DIR
                            store git checkout locations at [default: /tmp/czuul]
      -v FILE, --verbose=FILE
                            run in verbose mode and log output to the given file
      --detail-git=GIT_SERVER
                            fetch git repositories from this git server [default:
                            git://git.openstack.org/]
      --detail-remote=REMOTE_SERVER
                            fetch review remotes from this gerrit server [default:
                            https://review.openstack.org/]

##############
Keys supported
##############

* (R, r) - Force refresh
* (q, Q, esc) - Quit
* (up, down, page up, page down) - Scroll up/down
* (left, right) - Scroll left/right
* (enter) - show job details


########
Examples
########

1. To get details about a project::

    $ czuul --project "openstack/nova"

2. To fetch review details (including git summary) about a specific
   project::

    $ czuul --details --project "openstack/nova"

3. To track all OpenStack project details in one go::

    $ czuul --details --project "openstack/*"


.. _urwid: http://excess.org/urwid/
.. _gerrit: https://pypi.python.org/pypi/gerritlib
.. _requests: http://www.python-requests.org/
