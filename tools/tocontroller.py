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

import socket, config, datetime

# Get current settings from the config module
cfg = config.shared

def send_messages(messages=[], ip_port=('127.0.0.1',9991)):
    """
    messages is a list of strings
    ip_port is a tupple composed by string (ip) and a integer (port)
    The function iterate the list of strings and send them to the
    Configurated Socket connection
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # FIXME:: Try connect, if connection not available inform the user
    if cfg.log:
        f = open(cfg.log_path,'a+')
        print f

    try:
        s.connect(ip_port)
        for message in messages:
            message = (message + u'\n').encode('UTF-8')
            s.send(message)
            report(f,'CMD: '+ message)

    except UnicodeDecodeError as e:
        error_msg = u"UnicodeDecodeError: %s \n" % str(e)
        report(f,error_msg)

    except socket.error as e:
        error_msg = u"Socket Error: %s \n" % str(e)
        print error_msg
        report(f,error_msg)

    finally:
        s.close()
        if cfg.log:
            f.close()


def report(file,message):
    if cfg.log:
        now = datetime.datetime.now()
        file.write(now.strftime('%Y-%m-%d %H:%M:%S ') + message)
    print message

# Tests
if __name__ == '__main__':

    TCP_IP = "192.168.1.69"
    TCP_PORT = 9991
    BUFFER_SIZE = 256
    MESSAGE = "DRAW"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)

    data = s.recv(BUFFER_SIZE)
    print "received data:", data
    s.close()

