#Takes a 3 element array [r,g,b] and converts it to hex color code (#000000)
def decimal_to_hex(color_decimal):
    red = hex(color_decimal[0])
    if len(red) == 3:
        red = "0x0" + red[2]
    green = hex(color_decimal[1])
    if len(green) == 3:
        green = "0x0" + green[2]
    blue = hex(color_decimal[2])
    if len(blue) == 3:
        blue = "0x0" + blue[2]
    color_hex = "#" + blue[2] + blue[3] + green[2] + green[3] + red[2] + red[3]
    return color_hex

#Takes a hex color code (#000000) and converts it into a 3 element array [r,g,b]
def hex_to_decimal(color_hex):
    color_decimal = [int(color_hex[5] + color_hex[6], 16), int(color_hex[3] + color_hex[4], 16), int(color_hex[1] + color_hex[2], 16)]
    return color_decimal
    










