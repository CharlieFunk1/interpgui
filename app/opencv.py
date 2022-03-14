import cv2
import math
from app import db
from app.models import Strip, Configure

def opencv_draw(strips):
    image = cv2.imread('./app/static/resolutions.png')
    for strip in strips:
        i = 0
        strip_xy = set_strip(strip)
        while i < len(strip_xy):
            start = (strip_xy[i][0], strip_xy[i][1])
            end = (strip_xy[i][0], strip_xy[i][1])
            cv2.line(image, start, end, (strip.line_color_b, strip.line_color_g, strip.line_color_r), 5)
            i += 1
    cv2.imwrite('./app/static/display.png', image)        


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
