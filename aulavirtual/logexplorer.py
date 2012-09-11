#!/usr/bin/env python

import gtk
import time
import os
import json
import gobject

LOGFILE = os.path.join('/home', 'servidor', 'log.txt')
SERIAL_NUMBERS_FILE = os.path.join('/home', 'servidor', 'serial_numbers.txt')
SERIAL_NUMBERS = json.load(open(SERIAL_NUMBERS_FILE))


def get_name(serial):
    try:
        name, group = SERIAL_NUMBERS[serial]
	name = "%s %s" % (name, group)
    except IndexError:
        name = 'Desconocido'

    return name


def num(_num):
    number = str(_num)
    if len(number) == 1:
        number = "0" + number

    return number


class LogExplorer(gtk.TreeView):

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

    def __init__(self):
        super(Canvas, self).__init__()

        main = gtk.ScrolledWindow()
        main.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC )
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
