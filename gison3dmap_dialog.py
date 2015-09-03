# -*- coding: utf-8 -*-
"""
/***************************************************************************
 gison3dmapDialog
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

from lxml import etree as ET

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'gison3dmap_dialog_base.ui'))


class gison3dmapDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(gison3dmapDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.commands_dict = self.get_commands_dict()
        self.import_commands_list()

        # UI CONNECTORS
        self.comboBox.editTextChanged.connect(self.update_syntax)

    def import_commands_list(self):
        """ Populate comboBox with commands from help files"""
        self.comboBox.addItem('')
        for key in sorted(self.commands_dict.keys()):
            self.comboBox.addItem(key)

    def get_commands_dict(self):
        """ Fetchs Commands and their help and parameters strings"""
        # Read XML file with all commands help and parameters
        xml_commands_file = os.path.join(os.path.dirname(__file__), 'help/ComandosClienteGisOn3dMap.resx')
        tree = ET.parse(xml_commands_file)
        root = tree.getroot()

        # Make a dictionary with the structure {COMMAND_NAME: [HELP,PARAMETERS]
        commands_dict = dict()
        for chield in root.findall('data'):
            m = re.match(r"(\w+)_(\w+)", chield.get("name"))
            command_name = m.group(1).upper()
            if not command_name in commands_dict:
                commands_dict[command_name] = [None,None]
            if m.group(2).lower() == 'help':
                commands_dict[command_name][0] = chield[0].text
            elif m.group(2).lower() == 'parameters':
                commands_dict[command_name][1] = chield[0].text

        return commands_dict

    def update_syntax(self):
        """ Update syntax"""
        # get command name from combobox inputs
        m = re.match(r"^(\w*)(\s|$)",self.comboBox.currentText())

        if m:
            key = m.group(1).upper()
            # If command string matches one of the dictionary key show syntax text
            if key in self.commands_dict:
                # FIXME::newlines inside string are not considered
                text = u"{0}\n\nParâmetros:\n{1}".format(self.commands_dict[key][0], self.commands_dict[key][1])
            else:
                text = ''
        else:
            text = ''
        self.textBrowser.setText(text)

