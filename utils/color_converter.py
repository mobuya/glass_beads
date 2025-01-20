from openpyxl.styles import PatternFill



def convert_for_xlsx(dominant_colors):
    '''
    Converts an array of RGB color values into two formats suitable for use in an Excel (.xlsx) file:
    a list of RGB string representations and a list of `PatternFill` objects for cell coloring.

    Parameters
    ----------
    dominant_colors : list of tuples
        A list of RGB color tuples, where each tuple contains three integers (R, G, B) ranging from 0 to 255.

    Returns
    -------
    rgb_colors : list of str
        A list of RGB color values formatted as strings, e.g., "(255, 0, 0)" for red.

    cell_fills : list of openpyxl.styles.PatternFill
        A list of `PatternFill` objects with solid fills corresponding to each color, used for Excel cell formatting.
    '''

    rgb_colors = []
    cell_fills = []

    for color in dominant_colors:
        rgb_value = f"({color[0]}, {color[1]}, {color[2]})"
        rgb_colors.append(rgb_value)

        hex_value = f"{color[0]:02X}{color[1]:02X}{color[2]:02X}"
        color_value = PatternFill(start_color=hex_value, end_color=hex_value, fill_type="solid")
        cell_fills.append(color_value)

    return rgb_colors, cell_fills