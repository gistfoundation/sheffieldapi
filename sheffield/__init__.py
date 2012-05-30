from flask import Flask
from utils import start_end_date, start_end_time
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)

# SQLite backend for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# This is safer than using eval()
from ast import literal_eval

class Event(db.Model):
    """Model representing Events happening in Sheffield. The data we're storing
    here is currently collected from EventSheffield. The fields we're storing are
    limited due to this. However we expect to extend this API.
    """
    # For SQLAlchemy
    __tablename__ = 'Event'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    start_time = db.Column(db.String)
    end_time = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    venue_id = db.Column(db.Integer)
    detail_description = db.Column(db.String)
    detail_url = db.Column(db.String)
    venue = db.Column(db.String)
    venue_contact = db.Column(db.String)
    venue_lat = db.Column(db.Float)
    venue_long = db.Column(db.Float)
    
    def __init__(self, name, **kwargs):
        self.name = name
        for field, val in kwargs.items():
            setattr(self, field, val)
    
    def __repr__(self):
        return "<Event: %r>" % self.name

    #TODO: Figure out how to make index with SQLAlchemy
    #name_start_date = document.Index().ascending(
    #        'name').ascending('start_date').unique(drop_dups=True)

    @classmethod
    def from_json(self, ob):
        e = dict()
        start_time, end_time = start_end_time(ob['event_time'])
        start_date, end_date = start_end_date(ob['event_date'])
        e['name'] = ob['event_name'].strip()
        e['start_date'] = start_date
        if end_date: e['end_date'] = end_date
        e['start_time'] = start_time
        if end_time: e['end_time'] = end_time
        e['venue_id'] = int(ob['venue'].strip())
        e['detail_description'] = ob['details_text'].strip()
        e['detail_url'] = ob['details_url'].strip()
        e['venue'] = ob['event_venue'].strip()
        e['venue_contact'] = ob['event_contact'].strip()
        if ob['coords']:
            lat, long = literal_eval(ob['coords'])
            e['venue_lat'] = float(lat)
            e['venue_long'] = float(long)
        return self(**e)
