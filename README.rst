**Gerrit viewers & tools for all**
==================================

qgerrit
------------

Use `qgerrit` to find out what your friends have been up to::

    $ qgerrit -u 'harlowja'
    $ qgerrit -h
    
    Usage: qgerrit [options]
    
    Options:
      -h, --help            show this help message and exit
      -u USER, --user=USER  gather information on given USER
      -k FILE, --keyfile=FILE
                            gerrit ssh keyfile [default:
                            /homes/harlowja/.ssh/id_rsa]

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


.. _urwid: http://excess.org/urwid/
.. _curses: http://docs.python.org/2.7/library/curses.html
