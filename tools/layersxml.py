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

import lxml.etree as ET
import random
import re
import utils


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

        if renderer.type() == 'singleSymbol':
            symbol_layer = renderer.symbol().symbolLayers()[0]  # only considers first layer of symbol
            set_legend(legend, symbol_layer)

        # elif renderer.type() == 'categorizedSymbol':
        #     set_legend(legend)
        #     categories = renderer.categories()
        #     for category in categories:
        #         symbol_layer = category.symbol().symbolLayers()[0].properties()
        #         set_break(legend, symbol_layer)

        elif renderer.type() in ('graduatedSymbol', 'categorizedSymbol' ):
            set_legend(legend)
            legend.set('FieldName', renderer.classAttribute())
            if renderer.type() == 'categorizedSymbol':
                value_breaks = renderer.categories()
            else:
                value_breaks = renderer.ranges()
            for value_break in value_breaks:
                set_break(legend, value_break)

        # TODO: Add support to RuleRenderer
        # elif renderer.type() == 'RuleRenderer':
        #     rule_list = []
        #     for children in renderer.rootRule().children():
        #         getRules(rule_list, children)
        #     rules = rule_list
        else:
            print "This renderer is not supported by gison3dmap"

        if layer.hasLabelsEnabled(): #FIXME:: this is depreaced need to update for 2.10 labelsEnabled()
            label_layer = ET.SubElement(layer_legend, 'LabelLayer')
            label_settings = QgsPalLayerSettings.fromLayer(layer)
            set_label(label_layer, layer.name(), label_settings)
        # FIXME::Need to add labels


        # prepare xml string for output
        xml_string = ET.tostring(layer_legend, pretty_print=False, xml_declaration=True, encoding='utf 8')
        # Remove inconvenient end of line
        xml_string = xml_string.replace('\n', '')
        return xml_string


def set_legend(legend, symbol_layer=None):
    # backcolor='', linecolor='', width='', imagepath='', imagescale='1', enablehatch='False',
    # hatch='0', fieldname='', dashpattern='', camporotacao='', corset='255,255,255,0'):
    """
    Function to fill legend attributes with values from the symbolLayer
    """
    # Set default values for the case that layer_symbol arguments is not undeclared
    legend.set('BackColor', '')
    legend.set('LineColor', '')
    # FIXME:: Need to convert line width to pixels
    legend.set('Width', '')
    legend.set('ImagePath', '')
    legend.set('ImageScale', '1')
    legend.set('EnableHatch', 'False')
    # FIXME:: need to convert QGIS strings to similar Hatch
    legend.set('Hatch', '0')
    legend.set('FieldName', '')
    legend.set('DashPattern', '')  # ??
    legend.set('CampoRotacao', '')
    legend.set('CorSel', '255,255,255,0')

    # Check the type of symbolLayer and fill the legend attributes according
    if symbol_layer:
        layer_type = symbol_layer.layerType()
        properties = symbol_layer.properties()

        if layer_type == 'SimpleMarker' or layer_type == 'SimpleFill':
            legend.set('BackColor', utils.rgba2argb(properties['color']))
            legend.set('LineColor', utils.rgba2argb(properties['outline_color']))
            # FIXME:: Need to convert line width to pixels
            legend.set('Width', properties['outline_width'])
            legend.set('DashPattern', '')  # ??

        elif layer_type == 'SimpleLine':
            legend.set('LineColor', utils.rgba2argb(properties['line_color']))
            # FIXME:: Need to convert line width to pixels
            legend.set('Width', properties['line_width'])
            legend.set('DashPattern', '')  # ??

        elif layer_type == 'ImageFill':
            legend.set('ImagePath', properties['imageFile'])
            legend.set('ImageScale', '1')
            pass
        else:
            print "Not possible to render the symbol properly a default was used instead"


def set_break(legend, value_break):
    """
    Create legend's breaks to represent categories or ranges

    :param value_break: range or category object
    """
    symbol_layer = value_break.symbol().symbolLayers()[0]
    type = symbol_layer.layerType()
    properties = symbol_layer.properties()

    # Create a new break sub-element in legend
    legend_break = ET.SubElement(legend, 'Break')

    if type == 'SimpleMarker' or type == 'SimpleFill':
        color = utils.rgba2argb(properties['color'])
        line_color = utils.rgba2argb(properties['outline_color'])
        line_width = properties['outline_width']

    elif type == 'SimpleLine':
        color = utils.rgba2argb(properties['line_color'])
        line_color = utils.rgba2argb(properties['line_color'])
        line_width = properties['line_width']
    else:
        color = utils.random_color()
        line_color = '255,0,0,0'
        line_width = '1'
        print "Not possible to render the symbol properly a default was used instead"

    legend_break.set('EndColor', color)
    legend_break.set('StartColor', line_color)
    legend_break.set('OutlineEndColor', line_color)
    legend_break.set('OutlineStartColor', line_color)

    # Check if value_break has a single value or a lower and upper one
    # This is the only difference between ranges and categories
    try:
        legend_break.set('StartText', "{:.9f}".format(value_break.lowerValue()))
        legend_break.set('EndText', "{:.9f}".format(value_break.upperValue()))
    except:

        # Convert to string in case of non string values
        value = value_break.value()
        if not isinstance(value, basestring):
            value = str(value)
        legend_break.set('StartText', value) # FIXME::Must check if values are always strings
        legend_break.set('EndText', value)
    legend_break.set('Rotulo', value_break.label())
    legend_break.set('Imagem', '')
    legend_break.set('Width', str(line_width))


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
        expression_enable = 'True'
        expression = lab_set.getLabelExpression().dump() #FIXME:: Need to check Expressions syntax
    else:
        field_name = lab_set.fieldName
        expression_enable = 'False'
        expression =''
    label_layer.set('ColunaText', field_name)
    label_layer.set('ExpressaoRotulo', expression)
    label_layer.set('ColunaRotacao', '')
    label_layer.set('Prioridade', str(lab_set.priority)) #FIXME rever valores pode ir de 0 a 100
    label_layer.set('CollisionDetectio', 'True')
    label_layer.set('Cor', '-16777216') # FIXME:: não tenho a certeza
    label_layer.set('Activo', 'True')
    label_layer.set('ExpressaoActiva', expression_enable)
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
    cor_fundo.set('Cor', str(lab_set.textColor.rgb())) #::FIXME:: this color does not work...

    if lab_set.bufferDraw:
        halo = ET.SubElement(label_layer, 'CorFundo')
        halo.set('HaloCor', str(lab_set.bufferColor))
        halo.set('HaloCor', str(lab_set.bufferSize))

    offset = ET.SubElement(label_layer, 'Offset')
    offset.set('OffsetX', "{:.3f}".format(lab_set.xOffset)) # FIXME:: What are the units of the offset?
    offset.set('OffsetY', "{:.3f}".format(lab_set.yOffset))

    fonte = ET.SubElement(label_layer, 'Fonte')
    fonte.set('Tamanho', "{:.1f}".format(lab_set.textFont.pointSizeF()))
    fonte.set('Nome', lab_set.textFont.family())
    fonte.set('StrickOut', str(lab_set.textFont.strikeOut()))
    fonte.set('Underline', str(lab_set.textFont.underline()))
    fonte.set('Bold', str(lab_set.textFont.bold()))
    fonte.set('Italic', str(lab_set.textFont.italic()))


def define_layer(layer):
    layer_name = layer.name()
    provider = layer.dataProvider()
    source = re.sub(r'(.*)\|layerid=\d+', r'\1', provider.dataSourceUri())

    # If layer is vectorlayer get storage type
    if isinstance(provider, QgsVectorLayer):
        provider_type = provider.storageType()
        result = layer_name + ',' + provider_type + ',' + source
    else:
        result = layer_name + ',SHP,' + source

    # FIXME:: Must remake provider_type gison3map syntax
    return result


def get_layer_filter(layer):
    provider = layer.dataProvider()
    subset_string = provider.subsetString()
    if len(subset_string) == 0:
        return ',1=1'
    else:
        # FIXME:: Must remake substring to the gison3dmap syntax
        return subset_string