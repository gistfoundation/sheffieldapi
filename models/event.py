from mongoalchemy.document import Document
from mongoalchemy import fields


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
    venue_location = fields.ListField(fields.FloatField(), require=False)

