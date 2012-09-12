#!/usr/bin/env python
# -*- coding: utf-8 -*-

# mkdirs.py by:
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

"""A simple script for create directories and description files"""

__date__ = "18/04/12"
__author__ = "Agustin Zubiaga"

from widgets import SUBJECTS, GROUPS

import os
import shutil

GROUPS = list(GROUPS)
SUBJECTS = list(SUBJECTS)

GROUPS.remove(GROUPS[0])
SUBJECTS.remove(SUBJECTS[0])

TOTAL_COUNT = len(SUBJECTS) * len(GROUPS)


def mkdirs():
    """Makes groups (and subject) directories."""
    os.chdir('/home/servidor')
    os.mkdir("Groups")
    for g in GROUPS:
        os.mkdir("Groups/" + g)
        for s in SUBJECTS:
            os.mkdir("Groups/" + g + "/" + s)
            os.mkdir("Groups/" + g + "/" + s + "/" + '.homeworks')
            os.system('chmod 777 %s' % ("Groups/" + g + "/" + s + "/" +\
                                                                  '.homeworks'))


def make_desc_files():
    """Makes description files."""
    count = 0
    for g in GROUPS:
        for s in SUBJECTS:
            shutil.copyfile("/usr/share/antipapel/.desc", "Groups/" +\
                            g + "/" + s + "/.desc")
            shutil.copyfile("/usr/share/antipapel/.hdesc", "Groups/" +\
                            g + "/" + s + "/.homeworks/.desc")
            os.system('chmod 777 %s' % "Groups/" + g + "/" + s +\
                      "/.homeworks/.desc")
            os.system("clear")

            count += 1
            print "Creando directorios y archivos: " + str(
                                                count * 100 / TOTAL_COUNT) + "%"

    print "Listo!"

if __name__ == "__main__":
    mkdirs()
    make_desc_files()
