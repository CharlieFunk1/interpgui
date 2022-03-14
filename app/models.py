from app import db

class Strip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strip_num = db.Column(db.Integer, index=True, unique=True)
    num_pixels = db.Column(db.Integer, index=True)
    start_pos_x = db.Column(db.Integer)
    start_pos_y = db.Column(db.Integer)
    angle = db.Column(db.Integer)
    length = db.Column(db.Integer)
    line_color_r = db.Column(db.Integer)
    line_color_g = db.Column(db.Integer)
    line_color_b = db.Column(db.Integer)
    zig_zags = db.Column(db.Integer)
    zag_distance = db.Column(db.Integer)
    ip = db.Column(db.String(15), index=True, unique=True)

    def __repr__(self):
        return '<Strip Number {}>'.format(self.strip_num)

class StripSnake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strip_num = db.Column(db.Integer, index=True, unique=True)
    strip_segments = db.Column(db.Integer)
    start_pos_x = db.Column(db.Integer)
    start_pos_y = db.Column(db.Integer)
    line_color_r = db.Column(db.Integer)
    line_color_g = db.Column(db.Integer)
    line_color_b = db.Column(db.Integer)
    ip = db.Column(db.String(15), index=True, unique=True)
    segments = db.relationship('StripSnakeSegment', backref='strip_num', lazy='dynamic')

class StripSnakeSegment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    segment_number = db.Column(db.Integer, index=True)
    num_pixels = db.Column(db.Integer)
    angle = db.Column(db.Integer)
    length = db.Column(db.Integer)
    segment_strip_num = db.Column(db.Integer, db.ForeignKey('stripsnake.strip_num'))

class Configure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_strips = db.Column(db.Integer, index=True)
    rust_path = db.Column(db.String(64))
    brightness = db.Column(db.Integer)
    
    
