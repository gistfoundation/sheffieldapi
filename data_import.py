import json
import urllib2
import logging

from sheffield import Event, db


# data = urllib2.urlopen("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=json&name=scrape_the_eventsheffield_dataset_1&query=select+*+from+`swdata`&apikey=")
data = open('scrape.json')
data = json.load(data)

events = []
for ob in data:
    try:
        events.append(Event.from_json(ob))
    except Exception as e:
        logging.error("Exception Raised: %s" % e)
        logging.error("NOT IMPORTED Event: %s" % ob)

print len(events)

def save_events():
    for ev in events:
        db.session.add(ev)
    db.session.commit()
