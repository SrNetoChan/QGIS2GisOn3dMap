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


def conConfig(ip='192.168.56.1',port=9992):
    tcp_ip = ip
    tcp_port = port


def sendCommand(command):
    s.send(command)


def send_messages(messages=[], ip_port=('127.0.0.1',9991)):
    """
    messages is a list of strings
    ip_port is a tupple composed by string (ip) and a integer (port)
    The function iterate the list of strings and send them to the
    Configurated Socket connection
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(ip_port)
    print messages
    for message in messages:
        s.send(message)
        print 'Sent command: ', message #
    s.close()
    return None

if __name__ == '__main__':

    TCP_IP = '192.168.56.101'
    TCP_PORT = 9991
    BUFFER_SIZE = 1024
    MESSAGE = "map_props"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)

    data = s.recv(BUFFER_SIZE)
    s.close()

    print "received data:", data