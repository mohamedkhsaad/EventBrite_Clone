from celery import Celery
from pymongo import MongoClient
from datetime import datetime, date

app = Celery('eventbrite', broker='mongodb://localhost:27017/eventbrite')

@app.task
def update_event_status():
    client = MongoClient('localhost', 27017)
    db = client['eventbrite']
    publish_info_collection = db['eventManagment_publish_info']
    today = date.today()

    publish_info_collection.update_many(
        {'Publication_Date': {'$lt': today}, 'Event_Status': 'Private'},
        {'$set': {'Event_Status': 'Public'}}
    )