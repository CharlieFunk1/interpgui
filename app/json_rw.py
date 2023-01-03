import json
import os
import subprocess
from subprocess import Popen
from app import db
from app.models import Strip, Configure
from app.decimal_hex import hex_to_decimal, decimal_to_hex

def write_json(path):
    configure = Configure.query.get(1)
    diclist = []
    i = 1
    while i <= configure.num_strips:
        strip = Strip.query.filter_by(strip_num=i).first()
        decimal_color = hex_to_decimal(strip.line_color_hex)
        strip_dictionary ={
            "strip_num" : strip.strip_num,
            "num_pixels" : strip.num_pixels,
            "start_pos" : (strip.start_pos_x, strip.start_pos_y),
            "angle" : strip.angle,
            "length" : strip.length,
            "line_color" : (decimal_color[0], decimal_color[1], decimal_color[2]),
            "zig_zags" : strip.zig_zags,
            "zag_distance" : strip.zag_distance,
            "num_angles" : strip.num_angles,
            "enable_poly" : strip.enable_poly,
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
    with open(path + "stripdata.json", "w") as outfile:
        outfile.write(strip_json_object)
    with open(path + "configdata.json", "w") as outfile:
        outfile.write(config_json_object)


        
def read_json(path, config_name):
    if config_name != None:
        c = open(path + config_name + "/configdata.json")
        s = open(path + config_name + "/stripdata.json")
        configuration = json.load(c)
        strips = json.load(s)
        db_strips = Strip.query.all()
        db_config = Configure.query.all()
        all_strips = []
        for strip in strips:
            all_strips.append(strip)
            
        for strip in db_strips:
            db.session.delete(strip)
                
        for config in db_config:
            db.session.delete(config)
                    
        db.session.commit()

        for strip in all_strips:
            hex_color = decimal_to_hex(strip["line_color"])
            strip_add = Strip(strip_num = strip["strip_num"],
                              num_pixels = strip["num_pixels"],
                              start_pos_x = strip["start_pos"][0],
                              start_pos_y = strip["start_pos"][1],
                              angle = strip["angle"],
                              length = strip["length"],
                              line_color_hex = hex_color,
                              zig_zags = strip["zig_zags"],
                              zag_distance = strip["zag_distance"],
                              num_angles = strip["num_angles"],
                              enable_poly = strip["enable_poly"],
                              ip = strip["ip"])
        
            db.session.add(strip_add)
        db.session.commit()
        config_add = Configure(num_strips = configuration["num_strips"],
                               rust_path = configuration["rust_path"],
                               brightness = configuration["brightness"],
                               mode = configuration["mode"],
                               video_stream_ip = configuration["video_stream_ip"])
        db.session.add(config_add)
        db.session.commit()
    
    
