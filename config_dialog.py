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

        # Prepare file mapping table
        header = ['Origem','Destino']
        self.model = QtGui.QStandardItemModel(0,2)
        self.model.setHorizontalHeaderLabels(header)
        self.filemap_tv.setModel(self.model)
        self.filemap_tv.verticalHeader().setVisible(False)
        self.filemap_tv.horizontalHeader().setStretchLastSection(True)

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

        #File mapping
        if self.cfg.file_map:
            for row in self.cfg.file_map:
                input_row = [QtGui.QStandardItem(item) for item in row]
                self.model.appendRow(input_row)


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

        #Get Values from file mapping table
        temp_array = []
        for i in range(self.model.rowCount()):
            temp_list = []
            for j in range(self.model.columnCount()):
                temp_list.append(self.model.item(i,j).text())
            temp_array.append(temp_list)

        # If table is empty
        if len(temp_array) == 0:
            temp_array = None

        self.cfg.file_map = temp_array

        #Call function to store settings in system
        self.cfg.storeSettings()
