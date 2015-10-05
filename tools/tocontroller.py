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
    s.settimeout(5.0)
    # FIXME:: Try connect, if connection not available inform the user
    if cfg.log:
        global f
        f = open(cfg.log_path,'a+')

    try:
        s.connect(ip_port)
        for message in messages:
            message = (message)  + u'\n'
            s.send(message)
            report(u'CMD: '+ message)

    except UnicodeDecodeError as e:
        error_msg = u"UnicodeDecodeError: %s \n" % str(e)
        print error_msg
        report(error_msg)

    except socket.error as e:
        error_msg = u"Socket Error: %s \n" % str(e)
        print error_msg
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
        now = datetime.datetime.now()
        log_line = now.strftime('%Y-%m-%d %H:%M:%S ') + message
        f.write(log_line.encode('UTF-8'))
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

