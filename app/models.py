from app import db

class Strip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strip_num = db.Column(db.Integer, index=True)
    num_pixels = db.Column(db.Integer)
    start_pos_x = db.Column(db.Integer)
    start_pos_y = db.Column(db.Integer)
    angle = db.Column(db.Integer)
    length = db.Column(db.Integer)
    line_color_r = db.Column(db.Integer)
    line_color_g = db.Column(db.Integer)
    line_color_b = db.Column(db.Integer)
    zig_zags = db.Column(db.Integer)
    zag_distance = db.Column(db.Integer)
    ip = db.Column(db.String(15), index=True)
    links_in_strip = db.Column(db.Integer)
    strip_type = db.Column(db.String(10))
    links = db.relationship('Link', backref='strip_num', lazy='dynamic')

    def __repr__(self):
        return '<Strip Number {}>'.format(self.strip_num)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link_num = db.Column(db.Integer, index=True)
    num_pixels = db.Column(db.Integer)
    start_pos_x = db.Column(db.Integer)
    start_pos_y = db.Column(db.Integer)
    angle = db.Column(db.Integer)
    length = db.Column(db.Integer)
    origin_strip = db.Column(db.Integer, db.ForeignKey('strip.strip_num'))

    def __repr__(self):
        return '<Link Number {}>'.format(self.link_num)
    
class Configure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_strips = db.Column(db.Integer, index=True)
    rust_path = db.Column(db.String(64))
    brightness = db.Column(db.Integer)
    
class StripConfigure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strip_num = db.Column(db.Integer, index=True)
    strip_type = db.Column(db.String(10))
    links_in_strip = db.Column(db.Integer)
    
