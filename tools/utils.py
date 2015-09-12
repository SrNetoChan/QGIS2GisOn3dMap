import random
import config


def rgba2argb(rgba):
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

#testing
if __name__ == '__main__':
    print rgba2argb('101,102,103,127')
    print mm2px('0.54')
    print random_color()