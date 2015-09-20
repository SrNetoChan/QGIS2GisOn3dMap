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

import random
import config

def rgba2argb(rgba,alpha_factor):
    """
    Function to convert RGBA color values (red, green, blue, alpha)
    to ARGB (alpha, red, green, blue)

    :param rgba: RGBA string with integers (0-255) separated by commas
    :type rgba: string
    :returns: ARGB string with integers (0-255) separated by commas
    :rtype: string
    """

    # Create a list with the values inside the string
    band_values = rgba.split(',')
    # Remove alpha values of the end of the list and append it in the beginning
    alpha = band_values.pop()
    band_values.insert(0,alpha)
    # Check is Transparencies are allowed, if not, set alpha value to no transparency
    # Else apply alpha_factor resulting from layer alpha and symbol alpha
    if not config.shared.transparencia:
        band_values[0] = "255"
    else:
        band_values[0] = str(int(int(band_values[0]) * alpha_factor))
    # Convert list back to comma separated string
    argb = ",".join(band_values)
    return argb


def mm2px(mm_value):
    """
    Function to convert units from milimiter to pixels
    Uses configuration settings Scale Symbols to scale the values

    :param mm_value: value in milimeter (Double)
    :type mm_value: string
    :returns: Float value in pixels (Float)
    :rtype: string
    """

    # Assuming 72 resolution, means that 1 mm = 2.85 pixels
    FACTOR = 2.85
    px_value = str(int(int(float(mm_value) * FACTOR + 0.5) * config.shared.symbol_scale))

    return px_value


def random_color():
    """
    Function to create random colors

    :returns: a color according to gison3dmap syntax
    :rtype: string
    """
    # The color is completly opaque, thus the 255 at the alpha band
    color = ['255','','','']
    for i in range(1,4):
        # start at 100 to return bright colors
        color[i] = str(random.randint(100,255))
    color = ",".join(color)
    return color

def stringToArray(array_string):
    """
    Converts a string representing an array of strings
    Lines are separated by semicolons and elements separated by colons
    :param array_string: String
    :return: array of Strings
    """
    if len(array_string) > 0:
        array = array_string.split(';')
        array = [line.split(',') for line in array]
        return array
    else:
        return None

def arrayToString(array):
    """
    Converts an array os strings in a string representation
    :param array: Array
    :return: String
    """
    array_string = [','.join(line) for line in array]
    array_string = ';'.join(array_string)
    return array_string

#testing
if __name__ == '__main__':
    print rgba2argb('101,102,103,127')
    print mm2px('0.54')
    print random_color()