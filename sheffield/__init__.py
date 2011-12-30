from mongoalchemy.document import Document, Index
from mongoalchemy import fields
from utils import start_end_date, start_end_time


class Event(Document):
    """Model representing Event's happening in Sheffield. The data we're storing
    here is currently collected from EventSheffield. The fields we're storing are
    limited due to this. However we expect to extend this API.
    """
    name = fields.StringField()
    start_time = fields.StringField(required=False)
    end_time = fields.StringField(required=False)
    start_date = fields.DateTimeField(required=False)
    end_date = fields.DateTimeField(required=False)
    venue_id = fields.IntField(required=False)
    detail_description = fields.StringField(required=False)
    detail_url = fields.StringField(required=False)
    venue = fields.StringField(required=False)
    venue_contact = fields.StringField(required=False)
    venue_location = fields.ListField(fields.FloatField(), required=False)

    name_start_date = Index().ascending('name').ascending('start_date').unique(True)

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
