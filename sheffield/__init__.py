from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy, document
from utils import start_end_date, start_end_time
app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'test'
db = MongoAlchemy(app)


class Event(db.Document):
    """Model representing Event's happening in Sheffield. The data we're storing
    here is currently collected from EventSheffield. The fields we're storing are
    limited due to this. However we expect to extend this API.
    """
    name = db.StringField()
    start_time = db.StringField(required=False)
    end_time = db.StringField(required=False)
    start_date = db.DateTimeField(required=False)
    end_date = db.DateTimeField(required=False)
    venue_id = db.IntField(required=False)
    detail_description = db.StringField(required=False)
    detail_url = db.StringField(required=False)
    venue = db.StringField(required=False)
    venue_contact = db.StringField(required=False)
    venue_location = db.ListField(db.FloatField(), required=False)

    name_start_date = document.Index().ascending(
            'name').ascending('start_date').unique(drop_dups=True)

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
            e['venue_location'] = map(float, list(eval(ob['coords'])))
        return self(**e)
