import cv2
import math
from app import db
from app.models import Strip, Configure
from app.decimal_hex import decimal_to_hex, hex_to_decimal

def opencv_draw(strips):
    image = cv2.imread('./app/static/images/resolutions.png')
    for strip in strips:
        decimal_color = hex_to_decimal(strip.line_color_hex)
        i = 0
        if strip.enable_poly == False:
            strip_xy = set_strip(strip)
        else:
            strip_xy = set_strip_poly(strip)
        while i < len(strip_xy):
            start = (strip_xy[i][0], strip_xy[i][1])
            end = (strip_xy[i][0], strip_xy[i][1])
            cv2.line(image, start, end, (decimal_color[0], decimal_color[1], decimal_color[2]), 5)
            i += 1
    cv2.imwrite('./app/static/images/display.png', image)        


def set_strip(strip):
    strip_xy = []
    i = 1
    k = 1
    j = 1
    x_start = strip.start_pos_x
    y_start = strip.start_pos_y
    strip_xy.append((x_start, y_start))
    while i <= strip.zig_zags:
        while j < (strip.num_pixels/strip.zig_zags):
            x = round(((strip.length/(strip.num_pixels/strip.zig_zags) * (j)) * (math.cos(math.radians(strip.angle * -1))) * k) + x_start)
            y = round(((strip.length/(strip.num_pixels/strip.zig_zags) * (j)) * (math.sin(math.radians(strip.angle * -1))) * k) + y_start)
            strip_xy.append((x, y))
            j += 1
        if i == strip.zig_zags:
            break
        k = k * -1
        x_start = round(((strip.zag_distance) * math.cos(math.radians((strip.angle * -1) - (-90)))) + (strip_xy[((j * i) - 1)][0]))
        y_start = round(((strip.zag_distance) * math.sin(math.radians((strip.angle * -1) - (-90)))) + (strip_xy[((j * i) - 1)][1]))
        strip_xy.append((x_start, y_start))
        i += 1
        j = 1
    return strip_xy

def set_strip_poly(strip):
    strip_xy = []
    i = 1
    j = 1
    angle = strip.angle
    x_start = strip.start_pos_x
    y_start = strip.start_pos_y
    strip_xy.append((x_start, y_start))
    while i <= strip.num_angles:
        while j < (strip.num_pixels/strip.num_angles):
            x = round((strip.length/(strip.num_pixels/strip.num_angles) * (j)) * (math.cos(math.radians(angle * -1))) + x_start)
            y = round((strip.length/(strip.num_pixels/strip.num_angles) * (j)) * (math.sin(math.radians(angle * -1))) + y_start)
            strip_xy.append((x, y))
            j += 1
        x_start = strip_xy[-1][0]
        y_start = strip_xy[-1][1]
        if (angle + (angle * 2)) >= 360:
            angle = angle + (360/strip.num_angles)
            angle = angle - 360
        else:
            angle = angle + (360/strip.num_angles)
        i += 1
        j = 1
    return strip_xy
