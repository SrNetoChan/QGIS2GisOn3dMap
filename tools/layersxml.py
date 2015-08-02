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

import lxml.etree as ET

# Creates the XML structure to store layer symbols and labels
layer_legend = ET.Element('LayerLegend')

# Creates LayerLegend's child to store symbols
vector_layer_legend = ET.SubElement(layer_legend, 'VectorLayerLegend')
legend = ET.SubElement(vector_layer_legend, 'Legend')

legend.set('BackColor', '')
legend.set('Width', '')
legend.set('ImagePath','')
legend.set('ImageScale','')
legend.set('EnableHatch','')
legend.set('Hatch','')
legend.set('FieldName','')
legend.set('DashPattern','')
legend.set('CampoRotacao','')
legend.set('CorSel','')

# Create legend's child to represent categories or ranges if necessary
# FIXME::this only applyes to category and classes symbols
# FIXME::This will need to Loop
legend_break = ET.SubElement(legend,'Break')
legend_break.set('EndColor', '')
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
label_layer.set('Nome','')
label_layer.set('ColunaText','')
label_layer.set('ExpressaoRotulo','')
label_layer.set('ColunaRotacao','')
label_layer.set('Prioridade','')
label_layer.set('CollisionDetectio','')
label_layer.set('Cor','')
label_layer.set('Activo','')
label_layer.set('ExpressaoActiva','')
label_layer.set('MaxRotuloVisible','')
label_layer.set('MinRotuloVisible','')
label_layer.set('CollisionBufferW','')
label_layer.set('CollisionBufferH','')

cor_fundo = ET.SubElement(label_layer, 'CorFundo')
cor_fundo.set('Cor','')

offset = ET.SubElement(label_layer, 'Offset')
offset.set('OffsetX','0')
offset.set('OffsetY','0')

fonte = ET.SubElement(label_layer, 'Fonte')
fonte.set('Tamanho','')
fonte.set('Nome','')
fonte.set('StrickOut','False')
fonte.set('Underline','False')
fonte.set('Bold','False')
fonte.set('Italic','False')


print ET.tostring(layer_legend,pretty_print = True,xml_declaration=True, encoding='utf 8')
