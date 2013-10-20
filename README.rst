**Gerrit viewers & tools for all**
==================================

query_gerrit
------------

Use `query_gerrit` to find out what your friends have been up to::

    $ query_gerrit -u 'harlowja'
    $ query_gerrit -h
    
    Usage: query_gerrit [options]
    
    Options:
      -h, --help            show this help message and exit
      -u USER, --user=USER  gather information on given USER

curse_gerrit
------------

Use `curse_gerrit` to watch (in realtime) the reviews showing up (powered by
urwid_ and the curses_ library)::

    $ curse_gerrit
    $ curse_gerrit -h
    
    Usage: curse_gerrit [options]
    
    Options:
      -h, --help            show this help message and exit
      -u USER, --user=USER  gerrit user [default: harlowja]
      -s SERVER, --server=SERVER
                            gerrit server [default: review.openstack.org]
      -p PORT, --port=PORT  gerrit port [default: 29418]
      -k FILE, --keyfile=FILE
                            gerrit ssh keyfile [default:
                            /home/harlowja/.ssh/id_rsa]

.. _urwid: http://excess.org/urwid/
.. _curses: http://docs.python.org/2.7/library/curses.html
