# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                   gison3dmap
                                 A QGIS plugin
 Client for gison3dmap to project gis data in a physical terrain model
                              -------------------
        begin                : 2015-07-24
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Alexandre Neto (for CCC Geomática)
        email                : alex.f.neto@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import socket
import os
import datetime

import gison3dmap.tools.config as config

# Get current settings from the config module
cfg = config.shared

def send_messages(messages=[]):
    """
    messages is a list of strings
    ip_port is a tupple composed by string (ip) and a integer (port)
    The function iterate the list of strings and send them to the
    Configurated Socket connection
    """
    ip_port = (cfg.controller, 9991)

    if cfg.log:
        global f

        #Compose filename from current date
        now = datetime.datetime.now()
        file_name = now.strftime('%Y-%m-%d.txt')

        f = open(os.path.join(cfg.log_path,file_name),'a+')

    for message in messages:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        try:
            s.connect(ip_port)
            s.send(message.encode('utf-16'))
            report(message)
        except UnicodeDecodeError as e:
            error_msg = 'UnicodeDecodeError: {}'.format(str(e))
            report(error_msg)

        except socket.error as e:
            error_msg = 'Socket Error: {}'.format(str(e))
            report(error_msg)

        finally:
            s.close()

    if cfg.log:
        f.close()


def report(message):
    """
    :param message: string
    :return:
    """
    if cfg.log:
        log_line = message + '\n'
        f.write(log_line.encode('UTF-8'))

    # Try print commands into th console. Usefull for commands debugging
    try:
        print(message)
    except:
        pass

# Tests
if __name__ == '__main__':

    TCP_IP = '192.168.56.1'
    TCP_PORT = 9991
    BUFFER_SIZE = 256
    MESSAGE = 'traço'.encode('utf-16')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)

    #data = s.recv(BUFFER_SIZE)
    #print "received data:", data
    s.close()
