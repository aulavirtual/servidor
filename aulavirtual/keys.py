# -*- coding: utf-8 -*-

# keys.py by:
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
import os
import json
import widgets

try:
    import checkpasswd32 as checkpasswd

except ImportError:
    import checkpasswd64 as checkpasswd

AUTHORIZED_KEYS = 'authorized_keys.py'


class KeysConfiguration(gtk.VBox):

    def __init__(self):
        super(KeysConfiguration, self).__init__()

        toolbar = gtk.Toolbar()
        self.pack_start(toolbar, False, True, 0)

        add = gtk.ToolButton()
        add.connect('clicked', self._add_key)
        add.set_stock_id(gtk.STOCK_ADD)
        toolbar.insert(add, -1)

        remove = gtk.ToolButton()
        remove.connect('clicked', self._remove_key)
        remove.set_stock_id(gtk.STOCK_REMOVE)
        toolbar.insert(remove, -1)

        self._liststore = gtk.ListStore(str, str)
        treeview = gtk.TreeView(self._liststore)
        self.pack_start(treeview, True, True, 0)

        self._selection = treeview.get_selection()

        name = gtk.CellRendererText()
        mac = gtk.CellRendererText()

        col = gtk.TreeViewColumn('Nombre')
        col.pack_start(name, True)
        col.set_attributes(name, text=0)
        treeview.append_column(col)

        col = gtk.TreeViewColumn('Dirección MAC')
        col.pack_start(mac, True)
        col.set_attributes(mac, markup=1)
        treeview.append_column(col)

        self._keys = {}

        self.refresh()

        self.show_all()

    def refresh(self):
        self._liststore.clear()
        keys = open(AUTHORIZED_KEYS, 'r')
        for key in keys.read().split('# '):
            line = key.split('\n')[:-2]
            try:
                name, rsakey = line
                name, mac = name.split(': ')
                self._keys[name] = (mac, rsakey)
                macmark = ''
                for c in mac:
                    if c == ':':
                        macmark += c
                    else:
                        macmark +=\
                                  '<span foreground="grey"><b>%s</b></span>' % c
                if name:
                    self._liststore.append([name, macmark])
            except:
                pass

        keys.close()

    def _check_password(self):
        dialog = gtk.Dialog()
        dialog.set_size_request(250, 110)
        dialog.set_title('Administración Aula Virtual')
        dialog.set_border_width(5)
        dialog.add_buttons(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                           gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dialog.set_default_response(gtk.RESPONSE_ACCEPT)
        label = gtk.Label('Contraseña:')
        lbox = gtk.HBox()
        lbox.pack_start(label, False, True, 0)
        dialog.vbox.pack_start(lbox)
        password = gtk.Entry()
        password.set_visibility(False)
        dialog.vbox.add(password)
        password.show()
        lbox.show_all()
        response = dialog.run()
        spassword = password.get_text()
        dialog.destroy()

        if response == gtk.RESPONSE_ACCEPT:
            return checkpasswd.check(spassword)
        else:
            return False

    def _remove_answer(self, name):
        dialog = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION)
        dialog.set_markup(
                   '<b>%s</b>' % '¿Está seguro?')
        dialog.format_secondary_text(
                             '¿Desea eliminar la clave de acceso de %s?' % name)
        dialog.add_buttons(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                           gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        response = dialog.run()
        dialog.destroy()

        return response == gtk.RESPONSE_ACCEPT

    def _remove_key(self, widget):
        model, _iter = self._selection.get_selected()
        name = model.get_value(_iter, 0)
        if self._remove_answer(name) and self._check_password():
            del self._keys[name]
            self._save_keys()

    def _add_key(self, widget):
        filechooser = widgets.FileChooser(None, 'Seleccione una clave')
        if filechooser.file_path and self._check_password():
            desc_path = os.path.join(os.path.dirname(filechooser.file_path),
                                     '.desc')
            desc_file = open(desc_path, 'r')
            desc = json.load(desc_file)
            desc_file.close()

            name = os.path.split(filechooser.file_path)[1].\
                                              replace('_', ' ').split('.pub')[0]
            mac = desc[name]

            rsakey_file = open(filechooser.file_path)
            rsakey = rsakey_file.read()
            rsakey_file.close()
            self._keys[name] = (mac, rsakey)

            self._save_keys()

    def _save_keys(self):
        keys = open(AUTHORIZED_KEYS, 'w')
        count = 0
        for name in self._keys.keys():
            mac, rsakey = self._keys[name]
            keys.write('# %s: %s\n' % (name, mac))
            keys.write(rsakey)
            count += 1
            keys.write('\n\n')

        keys.close()
        self.refresh()

if __name__ == '__main__':
    w = gtk.Window()
    w.resize(800, 500)
    w.connect('destroy', lambda w: gtk.main_quit())
    w.add(KeysConfiguration())
    w.show_all()
    gtk.main()
