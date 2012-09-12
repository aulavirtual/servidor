#!/usr/bin/env python
# -*- coding: utf-8 -*-

# window.py by:
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

import os
import sys
import gtk
import json
import magic
import shutil
import widgets
import logexplorer

from widgets import GROUPS, SUBJECTS

GROUPS_DIR = os.path.join('/home/servidor', 'Groups')

if not os.path.exists(GROUPS_DIR):
    import mkdirs
    mkdirs.mkdirs()
    mkdirs.make_desc_files()


class Window(gtk.Window):

    def __init__(self):
        gtk.Window.__init__(self)

        self.set_title('Aula Virtual')
        self.set_border_width(10)
        self.set_property('deletable', False)
        self.resize(800, 600)
        self.connect('destroy', lambda w: sys.exit(0))

        self._path = None

        self.show_all()

    def _do_gui(self):
        notebook = gtk.Notebook()
        self.add(notebook)

        main_container = gtk.VBox()
        main_container.set_border_width(10)
        notebook.append_page(main_container, gtk.Label('Documentos'))

        topbox = gtk.HBox()
        main_container.pack_start(topbox, False, False, 0)

        self._title = widgets.Entry('Escriba el titulo aqui')
        topbox.pack_start(self._title, True, True, 0)

        open_btn = gtk.Button(stock=gtk.STOCK_OPEN)
        open_btn.connect('clicked', lambda w: widgets.FileChooser(self))
        topbox.pack_end(open_btn, False, True, 5)

        label = gtk.Label('Descripcion y/o Resumen:')
        main_container.pack_start(label, False, True, 10)

        self._description = gtk.TextView()
        self._description.set_property('wrap-mode', gtk.WRAP_WORD)
        main_container.pack_start(self._description, True, True, 5)

        bottom = gtk.HBox()
        main_container.pack_end(bottom, False, True, 5)

        self._teacher_name = widgets.Entry('Escriba su nombre aqui')
        main_container.pack_end(self._teacher_name, False, True, 0)

        self._subject_selector = widgets.SubjectChooser()
        bottom.pack_start(self._subject_selector, False, True, 5)

        self._groups_selector = widgets.GroupChooser()
        bottom.pack_start(self._groups_selector, False, True, 0)

        save = gtk.Button(stock=gtk.STOCK_SAVE)
        save.connect('clicked', self.save_cb)
        bottom.pack_end(save, False, True, 0)

        main_container.show_all()

        lexplorer = logexplorer.Canvas()
        notebook.append_page(lexplorer, gtk.Label('Registro'))

        lexplorer.show_all()
        notebook.show_all()
        notebook.set_current_page(0)

    def set_file(self, path):
        self._path = path
        self._title.set_text(os.path.split(path)[1])

    def save_cb(self, widget):
        title = self._title.get_text()

        _buffer = self._description.get_buffer()
        start = _buffer.get_start_iter()
        end = _buffer.get_end_iter()
        description = _buffer.get_text(start, end, True)

        teacher = self._teacher_name.get_text()

        group_id = self._groups_selector.get_active()
        group = GROUPS[group_id]

        subject_id = self._subject_selector.get_active()
        subject = SUBJECTS[subject_id]

        if subject_id == 0 or group_id == 0:
            dialog = gtk.MessageDialog(type=gtk.MESSAGE_ERROR)
            dialog.set_markup(
                       '<b>%s</b>' % 'No se ha elejido el grupo y/o la materia')
            dialog.format_secondary_text('Por favor elija uno')
            dialog.add_buttons(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
            dialog.run()
            dialog.destroy()

        else:
            save_dir = os.path.join(GROUPS_DIR, group, subject)
            desc_file = open(os.path.join(save_dir, '.desc'))
            mimetype = magic.from_file(self._path, mime=True)

            try:
                desc_dict = json.load(desc_file)
            finally:
                desc_file.close()

            desc_dict[title] = (description, teacher, mimetype)

            desc_file = open(os.path.join(save_dir, '.desc'), 'w')
            json.dump(desc_dict, desc_file)
            desc_file.close()

            shutil.copyfile(self._path, os.path.join(save_dir, title))

            # Question:
            dialog = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION)
            dialog.set_markup('<b>%s</b>' % '¡Documento guardado!')
            dialog.format_secondary_text(
                               '¿Desea enviar el mismo documento a más grupos?')
            dialog.add_buttons(gtk.STOCK_YES, gtk.RESPONSE_YES,
                               gtk.STOCK_NO, gtk.RESPONSE_NO)
            response = dialog.run()

            if response == gtk.RESPONSE_NO:
                self.clear()

            dialog.destroy()

    def clear(self):
        self._path = None
        self._title.set_text('')
        self._description.get_buffer().set_text('')
        self._teacher_name.set_text('')
        self._groups_selector.set_active(0)
        self._subject_selector.set_active(0)


if __name__ == '__main__':
    window = Window()
    window._do_gui()
    gtk.main()
