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
        self.num_drive_map = s.value("gison3dmap/NumDriveMap","")
        self.controller = s.value("gison3dmap/Controller","localhost")
        self.log = s.value("gison3dmap/Log",False) == 'true'
        self.log_erros = s.value("gison3dmap/LogErros",False) == 'true'
        self.transparencia = s.value("gison3dmap/Transparencia",False) == 'true'
        self.symbol_scale = float(s.value("gison3dmap/SymbolScale",1))
        self.clear_before_draw_map = s.value("gison3dmap/ClearBeforeDrawMap",True) == 'true'
        self.display_multimedia = s.value("gison3dmap/DisplayMultimedia","dword:00000000")
        self.host_multimedia = s.value("gison3dmap/HostMultimedia","localhost")
        self.log_path = s.value("gison3dmap/LogPath","")
        self.file_map = s.value("gison3dmap/FileMap",None)

    def storeSettings(self):
        """
        Saves plugin current user settings in System native way to store settings,
        that is — registry (on Windows), .plist file (on Mac OS X) or .ini file (on Unix).
        """
        s = QSettings()

        s.setValue("gison3dmap/Controller", self.controller)
        s.setValue("gison3dmap/Log", self.log)
        s.setValue("gison3dmap/LogErros", self.log_erros)
        s.setValue("gison3dmap/Transparencia", self.transparencia)
        s.setValue("gison3dmap/SymbolScale", self.symbol_scale)
        s.setValue("gison3dmap/ClearBeforeDrawMap", self.clear_before_draw_map)
        s.setValue("gison3dmap/DisplayMultimedia",self.display_multimedia)
        s.setValue("gison3dmap/HostMultimedia",  self.host_multimedia)
        s.setValue("gison3dmap/LogPath", self.log_path)
        s.setValue("gison3dmap/FileMap", self.file_map)

    def do_file_mapping(self, source):
        """
        Function to replace source path by remote path
        :param source: String
        :return: String
        """
        remote_source = source
        # For each row on File Mapping configuration try to match and replace
        # origin strings (at [0]) by destination string (at [1])
        if self.file_map:
            for pair in self.file_map:
                remote_source = remote_source.replace(pair[0],pair[1])

        # Revert dashes in case client is unix based
        remote_source = remote_source.replace('/','\\')
        return remote_source

# Initialize a instance to share with other modules as import
shared = config()