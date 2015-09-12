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

from PyQt4.QtCore import QSettings

class config:
    """QGIS Plugin Implementation."""

    def __init__(self):
        """Constructor."""
        s = QSettings()
        self.num_drive_map = s.value("gison3dmap/NumDriveMap","0")
        self.controller = s.value("gison3dmap/Controller","localhost")
        self.log = s.value("gison3dmap/Log",False) == 'true'
        self.log_erros = s.value("gison3dmap/LogErros",False) == 'true'
        self.transparencia = s.value("gison3dmap/Transparencia",False) == 'true'
        self.symbol_scale = float(s.value("gison3dmap/SymbolScale",1))
        self.clear_before_draw_map = s.value("gison3dmap/ClearBeforeDrawMap",True) == 'true'
        self.display_multimedia = s.value("gison3dmap/DisplayMultimedia","dword:00000000")
        self.host_multimedia = s.value("gison3dmap/HostMultimedia","localhost")
        self.log_path = s.value("gison3dmap/LogPath","")


    def storeSettings(self):
        """
        Saves plugin current user settings in System native way to store settings,
        that is — registry (on Windows), .plist file (on Mac OS X) or .ini file (on Unix).
        """
        s = QSettings()

        # s.setValue("gison3dmap/NumDriveMap", self.num_drive_map)
        s.setValue("gison3dmap/Controller", self.controller)
        s.setValue("gison3dmap/Log", self.log)
        s.setValue("gison3dmap/LogErros", self.log_erros)
        s.setValue("gison3dmap/Transparencia", self.transparencia)
        s.setValue("gison3dmap/SymbolScale", self.symbol_scale)
        s.setValue("gison3dmap/ClearBeforeDrawMap", self.clear_before_draw_map)
        s.setValue("gison3dmap/DisplayMultimedia",self.display_multimedia)
        s.setValue("gison3dmap/HostMultimedia",  self.host_multimedia)
        s.setValue("gison3dmap/LogPath", self.log_path)

shared = config()