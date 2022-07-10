import json
import os
import subprocess
from subprocess import Popen
from app import db
from app.models import Strip, Configure

def write_json(rust_path):
    configure = Configure.query.get(1)
    diclist = []
    i = 1
    while i <= configure.num_strips:
        strip = Strip.query.filter_by(strip_num=i).first()
        strip_dictionary ={
            "strip_num" : strip.strip_num,
            "num_pixels" : strip.num_pixels,
            "start_pos" : (strip.start_pos_x, strip.start_pos_y),
            "angle" : strip.angle,
            "length" : strip.length,
            "line_color" : (strip.line_color_r, strip.line_color_g, strip.line_color_b),
            "zig_zags" : strip.zig_zags,
            "zag_distance" : strip.zag_distance,
            "ip" : strip.ip
        }
        diclist.append(strip_dictionary)
        i += 1
    
    config_dictionary ={
        "num_strips" : configure.num_strips,
        "rust_path" : configure.rust_path,
        "brightness" : configure.brightness,
        "mode" : configure.mode,
        "video_stream_ip" : configure.video_stream_ip
    }
    config_json_object = json.dumps(config_dictionary, indent = 4)
    strip_json_object = json.dumps(diclist, indent = 4)
    with open(rust_path + "stripdata.json", "w") as outfile:
        outfile.write(strip_json_object)
    with open(rust_path + "configdata.json", "w") as outfile:
        outfile.write(config_json_object)

