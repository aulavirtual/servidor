#!/usr/bin/env python
# -*- coding: utf-8 -*-

# logexplorer.py by:
#    Agustin Zubiaga <aguz@sugarlabs.org>
#    Cristhofer Travieso <cristhofert97@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gtk
import time
import os
import json

LOGFILE = os.path.join('/home', 'servidor', 'log.txt')
SERIAL_NUMBERS_FILE = os.path.join('/home', 'servidor', 'serial_numbers.txt')
SERIAL_NUMBERS = json.load(open(SERIAL_NUMBERS_FILE))


def get_name(serial):
    '''devuelve el nombre'''
    try:
        name, group = SERIAL_NUMBERS[serial]
        name = "%s %s" % (name, group)
    except IndexError:
        name = 'Desconocido'

    return name


def num(_num):
    '''Numero'''
    number = str(_num)
    if len(number) == 1:
        number = "0" + number

    return number


class LogExplorer(gtk.TreeView):
    '''Registro del explorador'''
    def __init__(self, parent):
        super(LogExplorer, self).__init__()

        self._parent = parent
        self._log = None
        self._model = gtk.TreeStore(str, str)
        self.set_model(self._model)

        log = gtk.CellRendererText()
        index = gtk.CellRendererText()
        index.props.visible = False

        col = gtk.TreeViewColumn('Registro')
        col.pack_start(log, True)
        col.pack_start(index, False)
        col.add_attribute(log, 'text', 0)
        col.add_attribute(index, 'text', 1)

        self.append_column(col)

        self.refresh_log()

        self.show_all()

    def _get_log(self):
        '''Devuelve el registro'''
        try:
            global SERIAL_NUMBERS
            SERIAL_NUMBERS = json.load(open(SERIAL_NUMBERS_FILE))
            lfile = open(LOGFILE)
            log = []
            for line in lfile.readlines():
                ltime, serial, action = line.split(' - ')
                gmtime = time.gmtime(float(ltime))
                date = '%s/%s/%s' % (num(gmtime.tm_mday),
                                     num(gmtime.tm_mon),
                                     num(gmtime.tm_year))

                hour = '%s:%s:%s' % (num(gmtime.tm_hour),
                                     num(gmtime.tm_min),
                                     num(gmtime.tm_sec))

                item = {'date': date,
                        'hour': hour,
                        'serial-number': serial,
                        'name': get_name(serial),
                        'type': action}
                log.append(item)

            return log
        except Exception:
            print "There are not any log."
            return []

    def _get_days(self):
        '''Devuelve los dias'''
        days = {}
        _days = []
        for i in self._log:
            date = i['date']
            if not date in _days:
                day = self._model.append(None, [date, -1])
                connections = self._model.append(day, ['Conexiones', -1])
                downloads = self._model.append(day, ['Descargas', -1])
                days[date] = (connections, downloads)
                _days.append(date)

        return days

    def refresh_log(self):
        '''Recarga el registro'''
        self._model.clear()
        self._log = self._get_log()
        days = self._get_days()

        index = 0

        for i in self._log:
            connections, downloads = days[i['date']]
            _type = i['type'].split("\n")[0]
            if _type == 'Connecting':
                item = "%s  %s" % (i['hour'], i['name'])
                self._model.append(connections, [item, index])

            elif 'Saving' in _type:
                document = i['type'].split(': ')[-1].split('\n')[0]
                item = "%s  %s - %s" % (i['hour'], i['name'], document)
                self._model.append(downloads, [item, index])

            index += 1


class Canvas(gtk.VBox):
    '''Clase del canvas'''
    def __init__(self):
        super(Canvas, self).__init__()

        main = gtk.ScrolledWindow()
        main.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        explorer = LogExplorer(self)

        main.add(explorer)

        toolbar = gtk.Toolbar()
        self.pack_start(toolbar, False, True, 0)

        refresh = gtk.ToolButton()
        refresh.connect('clicked', lambda w: explorer.refresh_log())
        refresh.set_stock_id('gtk-refresh')
        toolbar.insert(refresh, -1)

        self.pack_end(main, True, True, 0)

        self.show_all()

if __name__ == '__main__':
    window = gtk.Window()
    window.resize(400, 300)
    window.add(Canvas())
    window.show_all()
    gtk.main()
