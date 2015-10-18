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

from qgis.core import *

import xml.etree.ElementTree as ET
import re
import utils, config

# Get current settings from the config module
cfg = config.shared

def get_layer_legend(layer):
    """
    Converts Layer's Symbols and Labels properties to gison3dmap XML

    :param layer: Vector Layer
    :type layer: QgsVectorLayer

    :returns: XML with all needed information about the layer
    :rtype: String
    """
    renderer = layer.rendererV2()

    # Check if render is supported by gison3dmap
    if renderer.type() not in ('singleSymbol', 'categorizedSymbol', 'graduatedSymbol', 'RuleRenderer'):
        # If renderer is not supported
        return None
    else:
        # Creates basic XML structure
        layer_legend = ET.Element('LayerLegend')
        vector_layer_legend = ET.SubElement(layer_legend, 'VectorLayerLegend')
        legend = ET.SubElement(vector_layer_legend, 'Legend')

        # Getting layer's transparency to further use in feature's colors
        layer_alpha = 1.0 - layer.layerTransparency()/100.0

        if renderer.type() == 'singleSymbol':
            symbol = renderer.symbol()
            alpha_factor = symbol.alpha() * layer_alpha
            symbol_layer = symbol.symbolLayers()[0]  # only considers first layer of symbol
            set_legend(legend, alpha_factor, symbol_layer)

        elif renderer.type() in ('graduatedSymbol', 'categorizedSymbol' ):
            set_legend(legend, layer_alpha)
            legend.set('FieldName', renderer.classAttribute())

            if renderer.type() == 'categorizedSymbol':
                value_breaks = renderer.categories()
            else:
                value_breaks = renderer.ranges()

            for value_break in value_breaks:
                set_break(legend, value_break, layer_alpha)

        # TODO: Add support to RuleRenderer
        # elif renderer.type() == 'RuleRenderer':
        #     rule_list = []
        #     for children in renderer.rootRule().children():
        #         getRules(rule_list, children)
        #     rules = rule_list
        else:
            print "This renderer is not supported by gison3dmap"

        if layer.labelsEnabled():
            label_layer = ET.SubElement(layer_legend, 'LabelLayer')
            label_settings = QgsPalLayerSettings.fromLayer(layer)
            set_label(label_layer, layer.name(), label_settings)
        # FIXME::Need to add labels

        # create xml string from etree element and decode it to unicode for further processing
        xml_string = ET.tostring(layer_legend, encoding='UTF-8')
        xml_string = xml_string.decode('UTF-8')
        # all elements must be represented in on single line, so remove inconvenient end of line characters
        xml_string = xml_string.replace('\n', '')
        return xml_string



def set_legend(legend, alpha_factor, symbol_layer=None):
    """
    Function to fill legend attributes with values from the symbolLayer
    """
    # Set default values for the case that layer_symbol arguments is not declared
    legend.set('BackColor', '')
    legend.set('LineColor', '')
    legend.set('Width', '2')
    legend.set('ImagePath', '')
    legend.set('ImageScale', '1')
    legend.set('EnableHatch', 'False')
    legend.set('Hatch', '0')
    legend.set('FieldName', '')
    legend.set('DashPattern', '')  # FIXME Need to understand how dash Pattern is read in gison3dmap
    legend.set('CampoRotacao', '')
    legend.set('CorSel', '255,255,255,0')

    # Check the type of symbolLayer and fill the legend attributes according
    if symbol_layer:
        layer_type = symbol_layer.layerType()
        properties = symbol_layer.properties()

        if layer_type == 'SimpleFill':
            if properties['style'] != 'no':
                legend.set('BackColor', utils.rgba2argb(properties['color'],alpha_factor))

            if properties['style'] not in ('solid','no'):
                legend.set('EnableHatch', 'True')
                legend.set('Hatch', '0') # FIXME:: Hatchs in QGIS are different from gison3dmap

            if properties['outline_style'] != 'no':
                legend.set('LineColor', utils.rgba2argb(properties['outline_color'],alpha_factor))

            legend.set('Width', utils.mm2px(properties['outline_width']))
            legend.set('DashPattern', '')  # ??

        elif layer_type == 'SimpleMarker':
            print properties
            legend.set('BackColor', utils.rgba2argb(properties['color'],alpha_factor))

            if properties['outline_style'] != 'no':
                legend.set('LineColor', utils.rgba2argb(properties['outline_color'],alpha_factor))

            legend.set('Width', utils.mm2px(properties['size']))
            legend.set('DashPattern', '')  # ??

        elif layer_type == 'SimpleLine':
            if properties['line_style'] != 'no':
                legend.set('LineColor', utils.rgba2argb(properties['line_color'],alpha_factor))
            legend.set('Width', utils.mm2px(properties['line_width']))
            legend.set('DashPattern', '')  # ??

        elif layer_type == 'ImageFill':
            legend.set('ImagePath', properties['imageFile'])
            legend.set('ImageScale', '1')
        else:
            legend.set('BackColor', utils.random_color())
            legend.set('LineColor', utils.random_color())
            # ::FIXME Pass this message to interface
            print "It was not possible to Render the layer's Symbol. " \
                  "Only Simple Marker,Simple Fill, Simple Line and Image fill are suported." \
                  "A random style was used instead"


def set_break(legend, value_break, layer_alpha):
    """
    Create legend's breaks to represent categories or ranges

    :param value_break: range or category object
    """
    symbol = value_break.symbol()
    alpha_factor = symbol.alpha() * layer_alpha

    symbol_layer = symbol.symbolLayers()[0]
    layer_type = symbol_layer.layerType()
    properties = symbol_layer.properties()

    # Create a new break sub-element in legend
    legend_break = ET.SubElement(legend, 'Break')

    # setting default values
    color = ''
    line_color = ''
    if layer_type == 'SimpleMarker' or layer_type == 'SimpleFill':
        if properties['style'] != 'no':
            color = utils.rgba2argb(properties['color'],alpha_factor)
        if properties['outline_style'] != 'no':
            line_color = utils.rgba2argb(properties['outline_color'],alpha_factor)
        line_width = properties['outline_width']

    elif layer_type == 'SimpleLine':
        if properties['line_style'] != 'no':
            line_color = utils.rgba2argb(properties['line_color'],alpha_factor)
        line_width = properties['line_width']
    else:
        color = utils.random_color()
        line_color = '255,0,0,0'
        line_width = '1'
        print "Not possible to render the symbol properly a default was used instead"

    legend_break.set('EndColor', color)
    legend_break.set('StartColor', color)
    legend_break.set('OutlineEndColor', line_color)
    legend_break.set('OutlineStartColor', line_color)

    # Check if value_break has a single value or a lower and upper value
    # This is the only difference between graduated ranges and categorized categories
    try:
        # This will run for graduated layers
        legend_break.set('StartText', "{:.9f}".format(value_break.lowerValue()))
        legend_break.set('EndText', "{:.9f}".format(value_break.upperValue()))
    except AttributeError:
        # This will run for categorized layers
        value = value_break.value()
        # Convert to string in case of non string values
        if not isinstance(value, basestring):
            value = unicode(value)
        legend_break.set('StartText', value) # FIXME::Must check if values are always strings
        legend_break.set('EndText', value)

    legend_break.set('Rotulo', value_break.label())
    legend_break.set('Imagem', '')
    legend_break.set('Width', str(utils.mm2px(line_width)))


def set_label(label_layer, layer_name, lab_set):
    """
    Fills label attributes with values from the layers label object
    :param lab_set: Layer Label settings
    :type lab_set: QgsPalLayerSettings
    """
    label_layer.set('Nome', layer_name)
    # See if label is built by a single field or expression
    if lab_set.isExpression:
        field_name = ''
        is_exp_enable = 'True'
        expression = lab_set.getLabelExpression().dump() #FIXME:: Need to check Expressions syntax
    else:
        field_name = lab_set.fieldName
        is_exp_enable = 'False'
        expression = ''

    label_layer.set('ColunaTexto', field_name)
    label_layer.set('ExpressaoRotulo', expression)
    label_layer.set('ColunaRotacao', '')
    label_layer.set('Prioridade', str(10 * lab_set.priority))
    label_layer.set('CollisionDetection', 'True')
    # label_layer.set('Cor', lab_set.textColor)
    label_layer.set('Cor', '-16777216') # FIXME:: não tenho a certeza de qual a nomenclatura destas cores
    label_layer.set('Activo', 'True')
    label_layer.set('ExpressaoActiva', is_exp_enable)
    if lab_set.scaleVisibility:
        min_scale = str(lab_set.scaleMin)
        max_scale = str(lab_set.scaleMax)
    else:
        min_scale = '0'
        max_scale = '1.79769313486232E+308'

    label_layer.set('MaxRotuloVisible', max_scale)
    label_layer.set('MinRotuloVisible', min_scale)
    label_layer.set('CollisionBufferW', '0')
    label_layer.set('CollisionBufferH', '0')

    cor_fundo = ET.SubElement(label_layer, 'CorFundo')
    c = lab_set.textColor

    # Check if Background option is On
    if lab_set.shapeDraw:
        # Currently gison3dmap only supports Rectangular Shape
        if lab_set.shapeType == 0:
            #qglab_set.shapeFillColor # FIXME:: Need to convert to this kind of colors
            cor_fundo.set('Cor', '16777215') #hardcoded as White
        else:
            print "The label background type is not supported. Choose Rectangular instead."

    if lab_set.bufferDraw:
        halo = ET.SubElement(label_layer, 'halo')
        #halo.set('HaloCor', str(lab_set.bufferColor)) FIXME:: Need to convert color to
        halo.set('HaloCor', "16777215") # hardcoded as white
        halo.set('HaloTamanho', utils.mm2px(lab_set.bufferSize))

    offset = ET.SubElement(label_layer, 'Offset')
    # This assumes that we are using mm.
    offset.set('OffsetX', utils.mm2px(lab_set.xOffset))
    offset.set('OffsetY', utils.mm2px(lab_set.yOffset))

    fonte = ET.SubElement(label_layer, 'Fonte')
    fonte.set('Tamanho', "{:.1f}".format(lab_set.textFont.pointSizeF()))
    fonte.set('Nome', lab_set.textFont.family())
    fonte.set('StrikeOut', str(lab_set.textFont.strikeOut()))
    fonte.set('Underline', str(lab_set.textFont.underline()))
    fonte.set('Bold', str(lab_set.textFont.bold()))
    fonte.set('Italic', str(lab_set.textFont.italic()))


def define_layer(layer):
    layer_name = layer.name()
    provider = layer.dataProvider()
    source = re.sub(r'(.*)\|layerid=\d+', r'\1', provider.dataSourceUri())
    # case there is a subset definition remove it
    source = re.sub(r'(.*)\|subset.*', r'\1', source)

    # Call function to do file mapping between local source and remote source
    source = cfg.do_file_mapping(source)

    # If layer is vectorlayer get storage type
    if layer.type() == layer.VectorLayer:
        # provider_type = provider.storageType() #FIXME:: Make it work for other providers
        provider_type = u'SHP' # Hardcoded for shapefile only
        result = layer_name + u',' + provider_type + ',' + source
    else:
        result = layer_name + u',' + source

    return result


def get_layer_filter(layer):
    subset_string = layer.dataProvider().subsetString()
    if len(subset_string) == 0:
        return u'1=1'
    else:
        # Convert subset_string to gison3dmap syntax
        # replace double quotes by square brackets
        s = subset_string
        p = re.compile(r'"(.*?)"')
        s = p.sub(r'[\1]', s)

        s = s.replace("'" , u'"')
        s = s.replace('!=' , u'<>')
        return s