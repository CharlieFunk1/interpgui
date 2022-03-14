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
        dictionary ={
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
        diclist.append(dictionary)
        i += 1
    json_object = json.dumps(diclist, indent = 4)
    with open(rust_path + "stripdata.json", "w") as outfile:
        outfile.write(json_object)

def run_program(rust_path):
    #os.system(rust_path + "cargo" + " run")
    Popen([rust_path + "target/debug/interprust"])
    #subprocess.run([rust_path, "cargo", " run"])
