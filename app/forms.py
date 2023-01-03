from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired, NumberRange, IPAddress, InputRequired
from app.models import Strip, Configure

class StripForm(FlaskForm):
    strip_num = IntegerField('Strip Number', validators=[DataRequired(), NumberRange(min=1, max=None, message="There is no strip 0.  Must start with 1.")])
    num_pixels = IntegerField('Number of Pixels in Strip', validators=[DataRequired(), NumberRange(min=1, max=300, message="Must be 1-300")])
    start_pos_x = IntegerField('Start Position X Value', validators=[DataRequired()])
    start_pos_y = IntegerField('Start Position Y Value', validators=[DataRequired()])
    angle = IntegerField('Angle (In Degrees)', validators=[NumberRange(min=-359, max=359, message="Must be between -359 and 359 degrees")])
    length = IntegerField('Length (In Pixels)', validators=[DataRequired()])
    line_color_hex = StringField('Strip Color', validators=[DataRequired()])
    zig_zags = IntegerField('Number of Zig Zags (1 = None)', validators=[DataRequired()])
    zag_distance = IntegerField('Distance between Zig Zag lines (in Pixels)(Negative to Zag Other Direction)', validators=[DataRequired()])
    num_angles = IntegerField('Number of angles in polygon(Negative to daw in other direction)', validators=[InputRequired()])
    enable_poly = BooleanField('Enable Polygon Mode', default=[False])
    ip = StringField('IP address of Strip', validators=[IPAddress(message="Value needs to be a valid IP Address")])
    submit = SubmitField('Submit Values')
    
class ConfigForm(FlaskForm):
    num_strips = IntegerField('Number of Strips', validators=[DataRequired(), NumberRange(min=1, max=None, message="Can not have 0 strips")])
    rust_path = StringField('Path to Program (/home/path/to/rust/program/)', validators=[DataRequired()])
    brightness = IntegerField('Global Brightness Control', validators=[DataRequired()])
    mode = IntegerField('Mode: 1)Video 2)Camera time sub 3)Camera static sub 4)IP', validators=[NumberRange(min=1, max=4, message="Must be 1, 2, 3, or 4")])
    video_stream_ip = StringField('IP address of streaming video', validators=[IPAddress(message="Value needs to be a valid IP Address")])
    submit = SubmitField('Submit Values')

class LoadConfig(FlaskForm):
    load_file = StringField('Name of project to load:')
    submit = SubmitField('Submit Values')

class SaveConfig(FlaskForm):
    save_file = StringField('Name of project to save:')
    submit = SubmitField('Submit Values')
 
