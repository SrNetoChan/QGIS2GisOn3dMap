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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from gison3dmap_dialog import gison3dmapDialog
from config_dialog import configDialog
import os.path, sys, re
from tools.layersxml import get_layer_legend, define_layer, get_layer_filter
from tools import tocontroller, utils
import tools.config as config


class gison3dmap:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        # and other elements
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.tree_view = self.iface.layerTreeView()
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'gison3dmap_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialogs (after translation) and keep reference
        self.send_commands_dlg = gison3dmapDialog()
        self.config_dlg = configDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&gison3dmap')

        self.toolbar = self.iface.addToolBar(u'gison3dmap')
        self.toolbar.setObjectName(u'gison3dmap')

        # Save reference from shared configuration instance
        self.cfg = config.shared

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('gison3dmap', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        self.send_Selection_action = self.add_action(
            ':/plugins/gison3dmap/icons/cmdAddSelection.png',
            text=self.tr(u'Seleção'),
            callback=self.sendSelection,
            parent=self.iface.mainWindow(),
            enabled_flag=False)
        self.send_Layer_action = self.add_action(
            ':/plugins/gison3dmap/icons/cmdAddLayer.png',
            text=self.tr(u'Camada ou Grupo'),
            callback=self.sendLayer,
            parent=self.iface.mainWindow(),
            enabled_flag=False)
        self.send_Map_action = self.add_action(
            ':/plugins/gison3dmap/icons/cmdAllLayers.png',
            text=self.tr(u'Mapa'),
            callback=self.sendMap,
            parent=self.iface.mainWindow(),
            enabled_flag=False)
        self.add_action(
            ':/plugins/gison3dmap/icons/cmdClear.png',
            text=self.tr(u'Limpar'),
            callback=self.clear,
            parent=self.iface.mainWindow())
        self.add_action(
            ':/plugins/gison3dmap/icons/cmdComando.png',
            text=self.tr(u'Enviar comandos'),
            callback=self.sendCommands,
            parent=self.iface.mainWindow())
        self.add_action(
            ':/plugins/gison3dmap/icons/cmdConfig.png',
            text=self.tr(u'Configuração'),
            callback=self.configuration,
            parent=self.iface.mainWindow())

        # connect signals for button behavior
        self.iface.currentLayerChanged["QgsMapLayer *"].connect(self.toggle)
        self.canvas.selectionChanged.connect(self.toggle)
        self.canvas.mapCanvasRefreshed.connect(self.toggle)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&gison3dmap'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def toggle(self):
        """
        function to activate or deactivate the plugin buttons
        :return:
        """
        # disconnect all previously connect signals of the node
        try:
            self.current_node.visibilityChanged.disconnect(self.toggle)
        except:
            pass

        # get current active node
        self.current_node = self.tree_view.currentNode()

        if self.current_node is None:
            #No node is selected disable selection and layer buttons
            self.send_Selection_action.setEnabled(False)
            self.send_Layer_action.setEnabled(False)

        elif self.current_node.nodeType() == 1:
            #In this case the node is a QgsLayerTree
            layer = self.current_node.layer()

            # Check if it is possible to use selection command
            if layer.type() == layer.VectorLayer and layer.selectedFeatureCount() > 0:
                self.send_Selection_action.setEnabled(True)
            else:
                self.send_Selection_action.setEnabled(False)

            self.send_Layer_action.setEnabled(True)

        elif self.current_node.nodeType() == 0:
            #In this case the node is a QgsLayerGroup
            self.send_Selection_action.setEnabled(False)

            # Check if there are visible layers on the current node
            visible = False
            for layer in self.current_node.findLayers():
                if layer.isVisible():
                    visible = True
                    break

            if visible:
                self.send_Layer_action.setEnabled(True)
            else:
                self.send_Layer_action.setEnabled(False)

            # Create a slot waiting for visibility changes on any child layer in the node
            self.current_node.visibilityChanged.connect(self.toggle)

        # See if there are any visible layers on the map canvas
        if self.canvas.layerCount() > 0:
            self.send_Map_action.setEnabled(True)
        else:
            self.send_Map_action.setEnabled(False)

    def sendSelection(self):
        """Function to send selected features on the active layer to gison3dmap"""
        layer = self.canvas.currentLayer()

        if layer.type() == layer.VectorLayer and layer.selectedFeatureCount()>0:
            commands = list()

            if self.cfg.clear_before_draw_map:
                commands.append(u'CLEAR')

            # Try to get the legend form layer
            layer_legend = get_layer_legend(layer)

            if layer_legend:
                # Get IDs from selected Features
                ids = layer.selectedFeaturesIds()
                ids = [id + 1 for id in ids]
                #convert the list to a string to use in LAYERID command
                ids_str = ",".join(map(str,ids))

                # Replace all colors in legend by project selection color
                qcolor = self.canvas.mapSettings().selectionColor()
                s_color = ",".join(map(str,qcolor.getRgb()))
                s_color = utils.rgba2argb(s_color,1.0)
                layer_legend = re.sub(r'\d{1,3},\d{1,3},\d{1,3},\d{1,3}', s_color, layer_legend)

                commands.append(u'DEFINELAYER ' + define_layer(layer))
                commands.append(u'LEGEND ' + layer_legend)
                commands.append(u'LAYERID ' + layer.name() + "," + ids_str)

            commands.append(u'DRAW')

            if len(commands)>2:
                tocontroller.send_messages(commands)
            else:
                print "Invalid renderer for layer : ", layer.name()
        else:
            print "Please select a Vector or Raster Layer" #FIXME Use a warning message for this

        pass

    def sendLayer(self):
        """Function to send active layer or layer group to gison3dmap"""
        current_node = self.tree_view.currentNode()

        if current_node.nodeType() == 1:
            #In this case the node is a QgsLayerTree
            #One single layer will be projected
            layer = current_node.layer()
            group_layers = [layer]

        elif current_node.nodeType() == 0:
            #In this case the node is a QgsLayerGroup
            #All visible layers with the group should be projected
            layers_tree = current_node.findLayers()
            group_layers = [layer.layer() for layer in layers_tree if layer.isVisible()]

        else:
            group_layers = None

        commands = list()

        if self.cfg.clear_before_draw_map:
            commands.append(u'CLEAR')

        for layer in group_layers[::-1]: # [::-1] is used to reverse the order of layers to project
            # Try to get the legend form layer
            try:
                layer_legend = get_layer_legend(layer)
            except:
                layer_legend = None

            if layer.type() == layer.VectorLayer and layer_legend:
                commands.append(u'DEFINELAYER ' + define_layer(layer))
                commands.append(u'LEGEND ' + layer_legend)
                commands.append(u'LAYERSQL ' + layer.name() + u', ' + get_layer_filter(layer))

            elif layer.type() == layer.RasterLayer:
                commands.append(u'DEFINELAYER ' + define_layer(layer))
                commands.append(u'GRID ' + layer.name())
            else:
                print "Invalid renderer for layer : ", layer.name() #FIXME:: Use a warning message for this

            commands.append(u'DRAW')

            tocontroller.send_messages(commands)


    def sendMap(self):
        """Function to send all visible layers to gison3dmap"""
        visible_layers = self.canvas.layers()
        commands = list()

        if self.cfg.clear_before_draw_map:
            commands.append(u'CLEAR')

        # Since last defined layer will be projected above the other, we need to iterate the
        # Visible layer at the inverse order,i.e., bottom to top. That's why [::-1] was used
        for layer in visible_layers[::-1]:
            try:
                layer_legend = get_layer_legend(layer)
            except:
                layer_legend = None #FIXME:: To brode error

            if layer.type() == layer.VectorLayer and layer_legend:
                commands.append(u'DEFINELAYER ' + define_layer(layer))
                commands.append(u'LEGEND ' + layer_legend)
                commands.append(u'LAYERSQL ' + layer.name() + u', ' + get_layer_filter(layer))

            elif layer.type() == layer.RasterLayer:
                commands.append(u'DEFINELAYER ' + define_layer(layer))
                commands.append(u'GRID ' + layer.name())

            else:
                print "Could not project layer: ", layer.name()

        commands.append(u'DRAW')

        # Check if list of commands are more that just CLEAR and DRAW and a DEFINE LAYER
        # Meaning that there are no valid layers to project
        if len(commands)>2:
            tocontroller.send_messages(commands)
        else:
            print "No valid layers to print"

    def clear(self):
        """
        Function to clear all layers from gison3dmap
        """

        commands = [u'CLEAR',u'DRAW']
        tocontroller.send_messages(commands)

    def sendCommands(self):
        """Function to send single commands to gison3dmap"""
        # show the dialog
        self.send_commands_dlg.show()
        # Run the dialog event loop
        # result = self.dlg.exec_()
        # See if OK was pressed
        if self.send_commands_dlg.exec_():
            command = self.send_commands_dlg.comboBox.currentText()
            commands = [command]
            tocontroller.send_messages(commands)

    def configuration(self):
        """Function to execute configuration dialog"""
        # Update dialog values from settings
        self.config_dlg.settingsToDialog()
        # show the dialog
        self.config_dlg.show()
        # Run the dialog event loop
        result = self.config_dlg.exec_()

        # If OK was pressed save dialog values to settings
        if result:
            self.config_dlg.dialogToSettings()