#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.


# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Setup for AulaVirtual-Server (aulavirtual.wordpress.com)"""

from distutils.core import setup
import aulavirtual

params = {
    "name": aulavirtual.__prj__,
    "version": aulavirtual.__version__,
    "description": aulavirtual.__doc__,
    "author": aulavirtual.__author__,
    "author_email": aulavirtual.__mail__,
    "url": aulavirtual.__url__,
    "license": aulavirtual.__license__,
    "packages": ['aulavirtual'],
    "scripts": ['av-server'],
    "data_files": [('/usr/share/antipapel', ['resources/.desc',
                                             'resources/log.txt',
                                             'resources/serial_numbers.txt']),
                   ('/usr/share/icons/gnome/48x48/apps/',
                    ['resources/aulavirtual.png']),
                   ('/usr/share/applications',
                    ['resources/aulavirtual.desktop'])]
}


setup(**params)

if __name__ == '__main__':
    print(__doc__)
