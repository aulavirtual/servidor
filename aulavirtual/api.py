# -*- coding: utf-8 -*-

# api.py by:
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

import sys
import os
import magic

sys.path.insert(0, 'lib')

import paramiko
import json

SERVER = '192.168.1.100'
USERNAME = 'profesores'
RSAKEY = os.path.join(os.getenv('HOME'), '.ssh', 'id_rsa')
GROUPS_DIR = '/home/servidor/Groups'
AUTHORIZED_KEYS = '/home/%s/.ssh/authorized_keys' % USERNAME
SERIAL_NUMBERS = os.path.join('/home', 'servidor', 'serial_numbers.txt')
LOGFILE = os.path.join('/home', 'servidor', 'log.txt')


def connect_to_server():
    """Connects to sftp server"""
    transport = paramiko.Transport((SERVER, 22))
    rsakey = paramiko.RSAKey.from_private_key_file(RSAKEY, password='')
    transport.connect(username=USERNAME, pkey=rsakey)

    sftp = paramiko.SFTPClient.from_transport(transport)

    return sftp


def save_document(sftp, uri, name, group, subject, title, description):
    """Saves a document in the server"""
    sftp.chdir(os.path.join(GROUPS_DIR, group, subject))
    local_file = open(uri)
    remote_file = sftp.open(title, 'w')
    remote_file.write(local_file.read())
    local_file.close()
    remote_file.close()

    desc = sftp.open('.desc', 'r')
    info = json.load(desc)
    desc.close()
    mime_type = magic.from_file(uri, mime=True)

    #FIXME: Save the mime type
    info[title] = (description, name, mime_type)

    desc = sftp.open('.desc', 'w')
    json.dump(info, desc)
    desc.close()


def get_authorized_keys(sftp, mode):
    """Return authorized keys python file"""
    return sftp.open(AUTHORIZED_KEYS, mode)


def install_ssh_key(path):
    """Install the ssh key in the main server"""
    os.system('ssh-copy-id -i %s %s@%s' % (path, USERNAME, SERVER))


def get_serial_numbers(sftp):
    _file = sftp.open(SERIAL_NUMBERS)
    try:
        return json.load(_file)
    finally:
        _file.close()


def get_log_file(sftp):
    return sftp.open(LOGFILE, 'r')