python-lirc-send
================

Lirc 0.9.2 supports sending IR via the C bindings. Sadly Lirc 0.9.2 isn't available natively in [Raspbian](http://www.raspbian.org/).

This library is intended to compliment [python-lirc](https://github.com/tompreston/python-lirc).

Use
===

The library supports connecting to both local UNIX or remote Lirc sockets.

    from lircsend import LircSend
    #Local socket, default path (/var/run/lirc/lircd)
    local_lirc = LircSend.create_local()
    #Local socket, custom path (/var/run/lirc/lircd2)
    local_lirc_2 = LircSend.create_local("/var/run/lirc/lircd2")
    
    #Remote socket, default host and port (127.0.0.1:8765)
    remote_lirc = LircSend.create_remote()
    #Remote socket, custom host and default port (10.0.2.98:8765)
    remote_lirc_2 = LircSend.create_remote("10.0.2.98")
    #Remote socket, custom host and port (10.0.2.98:10765)
    remote_lirc_3 = LircSend.create_remote("10.0.2.98", 10765)
