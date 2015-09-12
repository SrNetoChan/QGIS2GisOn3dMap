# -*- coding: utf-8 -*-
"""
/***************************************************************************
 configDialog
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

import os, re

from PyQt4 import QtGui, uic
import tools.config as config

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'config_dialog_base.ui'))

class configDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(configDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.display_multimedia.addItems(["0","1","2","3","4"])

        # Save reference from shared configuration instance
        self.cfg = config.shared

        # UI CONNECTORS

    def settingsToDialog(self):
        self.controller.setText(self.cfg.controller)
        self.num_drive_map = "0" # ::FIXME
        self.log.setChecked(self.cfg.log)
        self.log_erros.setChecked(self.cfg.log_erros)
        self.transparencia.setChecked(self.cfg.transparencia)
        self.symbol_scale.setText(str(self.cfg.symbol_scale))
        self.clear_before_draw_map.setChecked(self.cfg.clear_before_draw_map)
        self.host_multimedia.setText(self.cfg.host_multimedia)
        self.log_path.setText(self.cfg.log_path)

        index = self.display_multimedia.findText(self.cfg.display_multimedia)
        if index >= 0:
            self.display_multimedia.setCurrentIndex(index)

    def dialogToSettings(self):
        """
        Get values from configuration dialog widgets
        pass them to the settings varaibles and store them for future use
        """

        # give dialog values to corresponding settings variables
        # self.num_drive_map = "0"
        self.cfg.controller = self.controller.text()
        self.cfg.log = self.log.isChecked()
        self.cfg.log_erros = self.log_erros.isChecked()
        self.cfg.transparencia = self.transparencia.isChecked()
        self.cfg.symbol_scale = float(self.symbol_scale.text())
        self.cfg.clear_before_draw_map = self.clear_before_draw_map.isChecked()
        self.cfg.display_multimedia = self.display_multimedia.currentText()
        self.cfg.host_multimedia = self.host_multimedia.text()
        self.cfg.log_path = self.log_path.text()
        self.cfg.storeSettings()

        # self.num_drive_map = "0"
        # self.config_dlg.controller.setText(self.controller)
        # self.config_dlg.log = self.log
        # self.config_dlg.log_erros = self.log_erros
        # self.config_dlg.transparencia = self.transparencia
        # self.config_dlg.symbol_scale = self.symbol_scale
        # self.config_dlg.clear_antes_draw_map = self.clear_antes_draw_map
        # self.config_dlg.display_multimedia = self.display_multimedia
        # self.config_dlg.host_multimedia = self.host_multimedia
        # self.config_dlg.log_path = self.log_path

        # call function to store the settings in OS registry


        # # Get new settings from dialog widget's values
        # self.num_drive_map = "0"
        # self.controller = self.config_dlg.controller.text()
        # self.log = self.config_dlg.log
        # self.log_erros = self.config_dlg.log_erros
        # self.transparencia = self.config_dlg.transparencia
        # self.symbol_scale =self.config_dlg.symbol_scale
        # self.clear_antes_draw_map = self.config_dlg.clear_antes_draw_map
        # self.display_multimedia = "dword:00000000"
        # self.host_multimedia = self.config_dlg.host_multimedia
        # self.log_path = self.config_dlg.log_path
        #
        # # and Save settings to system

