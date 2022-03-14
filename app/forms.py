from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, IPAddress
from app.models import Strip, Configure

class StripForm(FlaskForm):
    strip_num = IntegerField('Strip Number', validators=[DataRequired(), NumberRange(min=1, max=None, message="There is no strip 0.  Must start with 1.")])
    num_pixels = IntegerField('Number of Pixels in Strip', validators=[DataRequired(), NumberRange(min=1, max=300, message="Must be 1-300")])
    start_pos_x = IntegerField('Start Position X Value', validators=[DataRequired()])
    start_pos_y = IntegerField('Start Position Y Value', validators=[DataRequired()])
    angle = IntegerField('Angle (In Degrees)', validators=[NumberRange(min=-359, max=359, message="Must be between -359 and 359 degrees")])
    length = IntegerField('Length (in Pixels)', validators=[DataRequired()])
    line_color_r = IntegerField('Strip Color Red (0-255)', validators=[NumberRange(min=0, max=255, message="Value needs to be 0-255")])
    line_color_g = IntegerField('Strip Color Green (0-255)', validators=[NumberRange(min=0, max=255, message="Value needs to be 0-255")])
    line_color_b = IntegerField('Strip Color Blue (0-255)', validators=[NumberRange(min=0, max=255, message="Value needs to be 0-255")])
    zig_zags = IntegerField('Number of Zig Zags (1 = None)', validators=[DataRequired()])
    zag_distance = IntegerField('Distance between Zig Zag lines (in Pixels)', validators=[DataRequired()])
    ip = StringField('IP address of Strip', validators=[IPAddress(message="Value needs to be a valid IP Address")])
    submit = SubmitField('Submit Values')
    
class ConfigForm(FlaskForm):
    num_strips = IntegerField('Number of Strips', validators=[DataRequired(), NumberRange(min=1, max=None, message="Can not have 0 strips")])
    rust_path = StringField('Path to Program (/home/path/to/rust/program/)', validators=[DataRequired()])
    brightness = IntegerField('Global Brightness Control', validators=[DataRequired()])
    submit = SubmitField('Submit Values')
    
    

