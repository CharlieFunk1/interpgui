#add brightness control to rust.  Already in UI.
#finish run from shell script to start program
#changed paths to absolute in json and opencv modules in rust.  change back maybe?

from flask import render_template, flash, redirect, url_for, request, make_response
from app import app
from app import db
from app.forms import StripForm, ConfigForm, LinkForm, StripConfigureForm
from app.models import Strip, Configure, Link, StripConfigure
from app.opencv import opencv_draw
from app.json_and_run import write_json, run_program

@app.route('/', methods=['GET', 'POST'])
def slash():
    #try:
    #    config = Configure.query.get(1)
    #    
    #    if str(config.num_strips).isdigit() == True:
    #        print("Data Present")
    #        
    #except:
    #    print("No data in table.  Adding basic setup info")
    #    configure = Configure(num_strips = 1,
    #                          rust_path = "/",
    #                          brightness = 100)
    #   
    #    db.session.add(configure)
    #    db.session.commit()

    return redirect('/config')

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    form = StripForm()
    configure = Configure.query.get(1)
    strip = Strip.query.all()
    strips = Strip.query.all()
    opencv_draw(strips)

    if form.validate_on_submit():
        strip = Strip(strip_num = form.strip_num.data,
                      link_to_last = form.link_to_last.data,
                      links_in_strip = form.links_in_strip.data,
                      link_num = form.link_num.data,
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
        
        return redirect('/setup/' + str(form.strip_num.data) + ',' + str(form.link_num.data + ',' + str(form.links_in_strip.data)))
    
    return render_template('setup.html', title='Interp Setup', form=form, configure=configure, strip=strip)

@app.route('/setup/<strip_number>,<link_number>,<links_in_the_strip>', methods=['GET', 'POST'])
def setup2(strip_number,link_number,links_in_the_strip):
    form = StripForm()
    if int(links_in_the_strip) > 0:
        strip = Strip(strip_num = 1,
                      link_to_last = 0,
                      links_in_strip = links_in_the_strip,
                      link_num = link_number,
                      num_pixels = 1,
                      start_pos_x = 0,
                      start_pos_y = 0,
                      angle = 0,
                      length = 0,
                      line_color_r = 0,
                      line_color_g = 0,
                      line_color_b = 0,
                      zig_zags = 1,
                      zag_distance = 0,
                      ip = "000.000.0.000")

        db.session.add(strip)
        db.session.commit()
    configure = Configure.query.get(1)
    strip = Strip.query.filter_by(strip_num=strip_number, link_num=link_number).first()
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
                      link_to_last = form.link_to_last.data,
                      links_in_strip = form.links_in_strip.data,
                      link_num = form.link_num.data,
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
        return redirect('/setup/' + str(form.strip_num.data) + ',' + str(form.link_num.data) + "," + str(form.links_in_strip.data))
    try:
        if str(strip.strip_num).isdigit() == True:
        
            form.strip_num.data = strip.strip_num
            form.link_to_last.data = strip.link_to_last
            form.links_in_strip.data = strip.links_in_strip
            form.link_num.data = strip.link_num
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

    return render_template('setup.html', title='Interp Setup', form=form, configure=configure, strip=strip, links_in_strip=form.links_in_strip.data)

    
@app.route('/config', methods=['GET', 'POST'])
def config():
    form1 = ConfigForm()
    
    if form1.validate_on_submit():
        configure = Configure(num_strips = form1.num_strips.data,
                              rust_path = form1.rust_path.data,
                              brightness = form1.brightness.data)
        db.session.add(configure)
        db.session.commit()
        flash('Config Data Submitted.  Set {} strips'.format(
            form1.num_strips.data))
        return redirect(url_for('config_strips'))
    
    try:
        configure = Configure.query.all()
        num_strips = configure.num_strips.data
        print("Data present in Configure")
        return redirect(url_for('config_strips'))
    
    except:
        print("No data present in config")
        
    return render_template('configure.html', title='Interp Config', form1=form1)

@app.route('/config/strips', methods=['GET', 'POST'])
def config_strips():
    form1 = ConfigForm()
    form2 = StripConfigureForm()
    strip_configure = StripConfigure.query.all()
    config = Configure.query.get(1)
    configure = Configure.query.all()
    num_strips = config.num_strips
        
    if form1.validate_on_submit():
        for c in configure:
            db.session.delete(c)
            db.session.commit()
            configure = Configure(num_strips = form1.num_strips.data,
                                  rust_path = form1.rust_path.data,
                                  brightness = form1.brightness.data)
            db.session.add(configure)
            db.session.commit()
            flash('Config Data Submitted.  Set {} strips'.format(
                form1.num_strips.data))
            return redirect(url_for('config_strips'))
    try:
        if str(num_strips).isdigit() == True:
            form1.num_strips.data = config.num_strips
            form1.rust_path.data = config.rust_path
            form1.brightness.data = config.brightness
    except:
        print("No data present in config")
    
    if form2.validate_on_submit():
        try:
            for i in range(1, num_strips+1):
                try:
                    stripconfigure = StripConfigure(strip_num = i,
                                                    strip_type = form2.strip_type.data,
                                                    links_in_strip = form2.links_in_strip.data)
                except:
                    stripconfigure = StripConfigure(strip_num = i,
                                                    strip_type = form2.strip_type.data)
                db.session.add(stripconfigure)
                db.session.commit()

        except:
            print("could not write form2 to StripConfigure")
        
    return render_template('config_strips.html', title='Interp Config', form1=form1, form2=form2, num_strips=num_strips)

@app.route('/running', methods=['GET', 'POST'])
def running():
    configure = Configure.query.get(1)
    rust_path = configure.rust_path
    write_json(rust_path)
    run_program(rust_path)
    return render_template('running.html', title='running')
