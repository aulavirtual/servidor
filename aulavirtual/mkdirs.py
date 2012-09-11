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


def make_desc_files():
    """Makes description files."""
    count = 0
    for g in GROUPS:
        for s in SUBJECTS:
            shutil.copyfile("/usr/share/antipapel/.desc", "Groups/" + g +"/" + s +"/.desc")
            shutil.copyfile("/usr/share/antipapel/.desc", "Groups/" + g +"/" + s +"/.homeworks/.desc")
            os.system("clear")

            count += 1
            print "Creando directorios y archivos: " + str(count * 100 / TOTAL_COUNT) + "%"


    print "Listo!"

if __name__ == "__main__":
    mkdirs()
    make_desc_files()

