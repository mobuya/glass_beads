from openpyxl.styles import PatternFill

def convert_for_xlsx(dominant_colors):
    rgb_colors = []
    cell_fills = []

    first_col = dominant_colors[0]
    second_col = dominant_colors[1]
    third_col = dominant_colors[2]

    rgb_color1 = f"({first_col[0]}, {first_col[1]}, {first_col[2]})"
    rgb_color2 = f"({second_col[0]}, {second_col[1]}, {second_col[2]})"
    rgb_color3 = f"({third_col[0]}, {third_col[1]}, {third_col[2]})"

    rgb_colors.append(rgb_color1)
    rgb_colors.append(rgb_color2)
    rgb_colors.append(rgb_color3)

    color_hex1 = f"{first_col[0]:02X}{first_col[1]:02X}{first_col[2]:02X}"
    color_hex2 = f"{second_col[0]:02X}{second_col[1]:02X}{second_col[2]:02X}"
    color_hex3 = f"{third_col[0]:02X}{third_col[1]:02X}{third_col[2]:02X}"

    color_fill1 = PatternFill(start_color=color_hex1, end_color=color_hex1, fill_type="solid")
    color_fill2 = PatternFill(start_color=color_hex2, end_color=color_hex2, fill_type="solid")
    color_fill3 = PatternFill(start_color=color_hex3, end_color=color_hex3, fill_type="solid")

    cell_fills.append(color_fill1)
    cell_fills.append(color_fill2)
    cell_fills.append(color_fill3)

    return rgb_colors, cell_fills