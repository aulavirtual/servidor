# -*- coding: utf-8 -*-

"""AulaVirtual-Server (aulavirtual.wordpress.com)"""

__prj__ = "av-server"
__author__ = "The AulaVirtual Team"
__mail__ = "antipapel at gmail dot com"
__url__ = "http://antipapel.wordpress.com"
__source__ = "https://github.com/aulavirtual/servidor"
__version__ = "1.7"
__license__ = "GPLv3"


def setup_and_run():
    import gtk
    from window import Window

    window = Window()
    window._do_gui()
    gtk.main()
