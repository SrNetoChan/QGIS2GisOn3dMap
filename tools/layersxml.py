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
import re
import utils


def get_layer_legend(layer):
    """
    Converts Layer's Symbols and Labels properties to gison3dmap XML
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

        elif renderer.type() == 'categorizedSymbol':
            set_legend(legend)
            categories = renderer.categories()
            for category in categories:
                p = category.symbol().symbolLayers()[0].properties()
                set_break(legend)

        elif renderer.type() == 'graduatedSymbol':
            set_legend(legend)
            ranges = renderer.ranges()
            for each_range in ranges:
                p = each_range.symbol().symbolLayers()[0].properties()
                set_break(legend)

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
        type = symbol_layer.layerType()
        properties = symbol_layer.properties()

        if type == 'SimpleMarker' or type == 'SimpleFill':
            legend.set('BackColor', utils.rgba2argb(properties['color']))
            legend.set('LineColor', utils.rgba2argb(properties['outline_color']))
            # FIXME:: Need to convert line width to pixels
            legend.set('Width', properties['outline_width'])
            legend.set('DashPattern', '')  # ??

        elif type == 'SimpleLine':
            legend.set('LineColor', utils.rgba2argb(properties['line_color']))
            # FIXME:: Need to convert line width to pixels
            legend.set('Width', properties['line_width'])
            legend.set('DashPattern', '')  # ??

        elif type == 'ImageFill':
            legend.set('ImagePath', properties['imageFile'])
            legend.set('ImageScale', '1')
            pass

        else:
            print "Not possible to render the symbol properly a default was used instead"


def set_break(legend, endcolor='', startcolor='', outlineendcolor='',
              outlinestartcolor='', starttext='', endtext='', rotulo='', imagem='', width=''):
    """
    Create legend's breaks to represent categories or ranges

    :type width: object
    """
    legend_break = ET.SubElement(legend, 'Break')
    legend_break.set('EndColor', endcolor)
    legend_break.set('StartColor', startcolor)
    legend_break.set('OutlineEndColor', outlineendcolor)
    legend_break.set('OutlineStartColor', outlinestartcolor)
    legend_break.set('StartText', starttext)
    legend_break.set('EndText', endtext)
    legend_break.set('Rotulo', rotulo)
    legend_break.set('Imagem', imagem)
    legend_break.set('Width', width)


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
    fonte.set('Tamanho', "{:.3f}".format(lab_set.textFont.pointSizeF()))
    fonte.set('Nome', lab_set.textFont.family())
    fonte.set('StrickOut', str(lab_set.textFont.strikeOut()))
    fonte.set('Underline', str(lab_set.textFont.underline()))
    fonte.set('Bold', str(lab_set.textFont.bold()))
    fonte.set('Italic', str(lab_set.textFont.italic()))


def define_layer(layer):
    layer_name = layer.name()
    provider = layer.dataProvider()
    provider_type = provider.storageType()
    source = re.sub(r'(.*)\|layerid=\d+', r'\1', provider.dataSourceUri())
    # FIXME:: Must remake provider_type gison3map syntax
    return layer_name + ',' + provider_type + ',' + source


def get_layer_filter(layer):
    provider = layer.dataProvider()
    subset_string = provider.subsetString()
    if len(subset_string) == 0:
        return '1=1'
    else:
        # FIXME:: Must remake substring to the gison3dmap syntax
        return subset_string


if __name__ == '__main__':
    # Creates the XML structure to store layer symbols and labels
    layer_legend = ET.Element('LayerLegend')

    # Creates LayerLegend's child to store symbols
    vector_layer_legend = ET.SubElement(layer_legend, 'VectorLayerLegend')
    legend = ET.SubElement(vector_layer_legend, 'Legend')

    legend.set('BackColor', '')
    legend.set('LineColor', '')
    legend.set('Width', '')
    legend.set('ImagePath', '')
    legend.set('ImageScale', '')
    legend.set('EnableHatch', '')
    legend.set('Hatch', '')
    legend.set('FieldName', '')
    legend.set('DashPattern', '')
    legend.set('CampoRotacao', '')
    legend.set('CorSel', '')

    # Create legend's child to represent categories or ranges if necessary
    # FIXME::this only applyes to category and classes symbols
    # FIXME::This will need to Loop
    legend_break = ET.SubElement(legend, 'Break')
    legend_break.set('EndColor', '')
    legend_break.set('StartColor', '')
    legend_break.set('OutlineEndColor', '')
    legend_break.set('OutlineStartColor', '')
    legend_break.set('StartText', '')
    legend_break.set('EndText', '')
    legend_break.set('Rotulo', '')
    legend_break.set('Imagem', '')
    legend_break.set('Width', '')

    legend_break = ET.SubElement(legend, 'Break')
    legend_break.set('EndColor', '111')
    legend_break.set('StartColor', '')
    legend_break.set('OutlineEndColor', '')
    legend_break.set('OutlineStartColor', '')
    legend_break.set('StartText', '')
    legend_break.set('EndText', '')
    legend_break.set('Rotulo', '')
    legend_break.set('Imagem', '')
    legend_break.set('Width', '')

    # Creates LayerLegend's child to store labels
    label_layer = ET.SubElement(layer_legend, 'LabelLayer')
    label_layer.set('Nome', '')
    label_layer.set('ColunaText', '')
    label_layer.set('ExpressaoRotulo', '')
    label_layer.set('ColunaRotacao', '')
    label_layer.set('Prioridade', '')
    label_layer.set('CollisionDetectio', '')
    label_layer.set('Cor', '')
    label_layer.set('Activo', '')
    label_layer.set('ExpressaoActiva', '')
    label_layer.set('MaxRotuloVisible', '')
    label_layer.set('MinRotuloVisible', '')
    label_layer.set('CollisionBufferW', '')
    label_layer.set('CollisionBufferH', '')

    cor_fundo = ET.SubElement(label_layer, 'CorFundo')
    cor_fundo.set('Cor', '')

    offset = ET.SubElement(label_layer, 'Offset')
    offset.set('OffsetX', '0')
    offset.set('OffsetY', '0')

    fonte = ET.SubElement(label_layer, 'Fonte')
    fonte.set('Tamanho', '')
    fonte.set('Nome', '')
    fonte.set('StrickOut', 'False')
    fonte.set('Underline', 'False')
    fonte.set('Bold', 'False')
    fonte.set('Italic', 'False')

    string = ET.tostring(layer_legend, pretty_print=False, xml_declaration=True, encoding='utf 8')
    string = string.replace('\n', '')
    print string
