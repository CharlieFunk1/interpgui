#TODO Make brightness control constantly update strip.  JSON?
#TODO Add multistrip vew page with x,y,length and angle only.
#TODO Add colorpicker for strip color
#TODO Add polygon implementor length, number of angles, angle degrees

from flask import render_template, flash, redirect, url_for, request, make_response
from app import app
from app import db, socketio
from app.forms import StripForm, ConfigForm, LoadConfig, SaveConfig
from app.models import Strip, Configure
from app.opencv import opencv_draw
from app.save_load import save_config, load_config, query_saves
from app.json_rw import write_json, read_json
import subprocess
from subprocess import Popen
import os
import math
from flask_socketio import send, emit


@app.route('/', methods=['GET', 'POST'])
def slash():
    try:
        config = Configure.query.get(1)
        
        if str(config.num_strips).isdigit() == True:
            print("Data Present")
            
    except:
        print("No data in table.  Adding basic setup info")
        configure = Configure(num_strips = 1,
                              rust_path = "/",
                              brightness = 100,
                              mode = 1,
                              video_stream_ip = "0.0.0.0")
        db.session.add(configure)
        db.session.commit()

    return redirect('/setup/1')

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    form = StripForm()
    configure = Configure.query.get(1)
    strip = Strip.query.all()
    strips = Strip.query.all()
    opencv_draw(strips)

    if form.validate_on_submit():
        strip = Strip(strip_num = form.strip_num.data,
                      num_pixels = form.num_pixels.data,
                      start_pos_x = form.start_pos_x.data,
                      start_pos_y = form.start_pos_y.data,
                      angle = form.angle.data,
                      length = form.length.data,
                      line_color_r = form.line_color_r.data,
                      line_color_g = form.line_color_g.data,
                      line_color_b = form.line_color_b.data,
                      zig_zags = form.zig_zags.data,
                      zag_distance = form.zag_distance.data,
                      ip = form.ip.data)
        db.session.add(strip)
        db.session.commit()
        flash('Config Data Submitted for Strip {}'.format(
            form.strip_num.data))
        
        return redirect('/setup/' + str(form.strip_num.data))
    
    return render_template('setup.html', title='Interp Setup', form=form, configure=configure)

@app.route('/setup/<strip_number>', methods=['GET', 'POST'])
def setup2(strip_number):
    form = StripForm()
    configure = Configure.query.get(1)
    strip = Strip.query.filter_by(strip_num=strip_number).first()
    strips = Strip.query.all()
    opencv_draw(strips)

    if form.validate_on_submit():
        try:
            strip = Strip.query.filter_by(strip_num=form.strip_num.data).first()
            db.session.delete(strip)
            db.session.commit()
        except:
            print("No data to delete")
            
        strip = Strip(strip_num = form.strip_num.data,
            num_pixels = form.num_pixels.data,
            start_pos_x = form.start_pos_x.data,
            start_pos_y = form.start_pos_y.data,
            angle = form.angle.data,
            length = form.length.data,
            line_color_r = form.line_color_r.data,
            line_color_g = form.line_color_g.data,
            line_color_b = form.line_color_b.data,
            zig_zags = form.zig_zags.data,
            zag_distance = form.zag_distance.data,
            ip = form.ip.data)

        db.session.add(strip)
        db.session.commit()
        flash('Config Data Submitted for Strip {}'.format(
            form.strip_num.data))
        return redirect('/setup/' + str(form.strip_num.data))
    try:
        if str(strip.strip_num).isdigit() == True:
        
            form.strip_num.data = strip.strip_num
            form.num_pixels.data = strip.num_pixels
            form.start_pos_x.data = strip.start_pos_x
            form.start_pos_y.data = strip.start_pos_y
            form.angle.data = strip.angle
            form.length.data = strip.length
            form.line_color_r.data = strip.line_color_r
            form.line_color_g.data = strip.line_color_g
            form.line_color_b.data = strip.line_color_b
            form.zig_zags.data = strip.zig_zags
            form.zag_distance.data = strip.zag_distance
            form.ip.data = strip.ip
    except:
        print("No data present in strip")

    return render_template('setup.html', title='Interp Setup', form=form, configure=configure)

    
@app.route('/config', methods=['GET', 'POST'])
def config():
    form1 = ConfigForm()
    config = Configure.query.get(1)
    configure = Configure.query.all()
    num_strips = config.num_strips
        
    if form1.validate_on_submit():
        for c in configure:
            db.session.delete(c)
        db.session.commit()
        configure = Configure(num_strips = form1.num_strips.data,
                              rust_path = form1.rust_path.data,
                              brightness = form1.brightness.data,
                              mode = form1.mode.data,
                              video_stream_ip = form1.video_stream_ip.data)
        db.session.add(configure)
        db.session.commit()
        flash('Config Data Submitted.  Set {} strips'.format(
            form1.num_strips.data))
        return redirect(url_for('config'))
    try:
        if str(num_strips).isdigit() == True:
            form1.num_strips.data = config.num_strips
            form1.rust_path.data = config.rust_path
            form1.brightness.data = config.brightness
            form1.mode.data = config.mode
            form1.video_stream_ip.data = config.video_stream_ip
    except:
        print("No data present in config")
        
    return render_template('configure.html', title='Interp Config', form1=form1)


@app.route('/running', methods=['GET', 'POST'])
def running():
    configure = Configure.query.get(1)
    rust_path = configure.rust_path
    path = rust_path + "target/debug/interprust"
    write_json(rust_path)
    proc = subprocess.Popen(path, shell=True)
        
    if request.method == 'POST':
        if request.form.get("close_program"):
            done = os.system("killall interprust")
            return redirect('/setup/1')
      
    return render_template('running.html', title='running')

@app.route('/load', methods=['GET', 'POST'])
def load():
    form1 = LoadConfig()
    saves = query_saves()

    if form1.validate_on_submit():
        load_config(form1.load_file.data)
        return redirect('/setup/1')
    
    return render_template('load.html', title='load', saves=saves, form1=form1)

@app.route('/save', methods=['GET', 'POST'])
def save():
    form = SaveConfig()
    saves = query_saves()

    if form.validate_on_submit():
        save_config(form.save_file.data)
        return redirect('/setup/1')
    
    return render_template('save.html', title='save', saves=saves, form=form)

@app.route('/drawstripstart/<strip_n>', methods=['GET', 'POST'])
def drawstripstart(strip_n):
    
    return render_template('drawstripstart.html', title='drawstripstart', strip_n = strip_n)

@socketio.on('start_point_rec')
def start_point(data):
    #print('received message: ')
    #print(data)
    strip_number = data[2]
    strip = Strip.query.filter_by(strip_num=strip_number).first()
    #print(strip.start_pos_x, strip.start_pos_y, strip.angle)
    strip.start_pos_x = data[0]
    strip.start_pos_y = data[1]
    #print(strip.start_pos_x, strip.start_pos_y, strip.angle) 
    db.session.add(strip)
    db.session.commit()
    strips = Strip.query.all()
    opencv_draw(strips)
    destination = '/drawstripstart/' + str(data[2])
    emit('redirect', destination)
    
@app.route('/drawstripend/<strip_n>', methods=['GET', 'POST'])
def drawstripend(strip_n):
    
    return render_template('drawstripend.html', title='drawstripend', strip_n = strip_n)

@socketio.on('end_point_rec')
def end_point(data):
    #print('received message: ')
    #print(data)
    strip_number = data[2]
    strip = Strip.query.filter_by(strip_num=strip_number).first()
    length = round(math.sqrt(((data[0] - strip.start_pos_x) ** 2) + ((data[1] - strip.start_pos_y) ** 2)))
    angle = round(math.degrees(math.atan2((data[1] - strip.start_pos_y), (data[0] - strip.start_pos_x))) * -1)
    #print("length: " + str(length))
    #print("angle:" + str(angle))
    strip.length = length
    strip.angle = angle
    db.session.add(strip)
    db.session.commit()
    strips = Strip.query.all()
    opencv_draw(strips)
    destination = '/drawstripend/' + str(data[2])
    emit('redirect', destination)
