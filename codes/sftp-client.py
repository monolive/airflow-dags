#!/usr/bin/env python

# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.

# based on code provided by raymond mosteller (thanks!)

import base64
import getpass
import os
import socket
import sys
import traceback
import argparse

import paramiko
from paramiko.py3compat import input
from datetime import datetime

def parsing_args():
    # Read arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', action='store', dest='server', default="beefy", help='server to connect to')
    parser.add_argument('-p', '--port', action='store', dest='port', default=22, type=int, help='port to connect to')
    parser.add_argument('-u', '--user', action='store', dest='user', default="orenault", help='user to connect as')
    parser.add_argument('-k', '--key', action='store', dest='key', default=".ssh/id_rsa", help='RSAkey to authenticate user')
    parser.add_argument('-d', '--directory', action='store', dest='directory', help='directory containing the files')
    try:
        results = parser.parse_args()
    except SystemExit as err:
        if err.code == 2:
            parser.print_help()
        sys.exit(0)
    return results

def connect(server, port, user, key):
    try:
        key = paramiko.RSAKey.from_private_key_file(key)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname = server,
            port = port,
            username = user,
            pkey = key,
        )
        sftp = client.open_sftp()
    except Exception as e:
        print("*** Caught exception: %s: %s" % (e.__class__, e))
        traceback.print_exc()
        try:
            t.close()
        except:
            pass
        sys.exit(1)

    return sftp

def main():
    arguments = parsing_args()
    # setup logging
    paramiko.util.log_to_file(arguments.server + datetime.now().strftime('_%Y_%m_%d-%H_%M_%S.log'))
    # Connect and use paramiko Transport to negotiate SSH2 across the connection
    sftp = connect(arguments.server, arguments.port, arguments.user, arguments.key)


    # dirlist on remote host
    dirlist = sftp.listdir(arguments.directory)
    print("Dirlist: %s" % dirlist)

    """
    # copy this demo onto the server
    try:
        sftp.mkdir("demo_sftp_folder")
    except IOError:
        print("(assuming demo_sftp_folder/ already exists)")
    with sftp.open("demo_sftp_folder/README", "w") as f:
        f.write("This was created by demo_sftp.py.\n")
    with open("demo_sftp.py", "r") as f:
        data = f.read()
    sftp.open("demo_sftp_folder/demo_sftp.py", "w").write(data)
    print("created demo_sftp_folder/ on the server")

    # copy the README back here
    with sftp.open("demo_sftp_folder/README", "r") as f:
        data = f.read()
    with open("README_demo_sftp", "w") as f:
        f.write(data)
    print("copied README back here")

    # BETTER: use the get() and put() methods
    sftp.put("demo_sftp.py", "demo_sftp_folder/demo_sftp.py")
    sftp.get("demo_sftp_folder/README", "README_demo_sftp")

    t.close()
    """

if __name__ == '__main__':
    main()
