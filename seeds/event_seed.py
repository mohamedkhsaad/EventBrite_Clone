import os
import random
import string
import datetime
from pymongo import MongoClient
import uuid
import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
client = MongoClient()
db = client['eventbrite-db']


media_root = 'media/'
events_dir = os.path.join(media_root, 'events')
if not os.path.exists(events_dir):
    os.makedirs(events_dir)

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventbrite.settings')
# if not settings.configured:
#     settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')
#     if not settings_module:
#         raise ImproperlyConfigured(
#             "You must either set the DJANGO_SETTINGS_MODULE environment variable or call settings.configure() before accessing settings."
#         )
#     settings.configure()

# create a directory for event images if it doesn't exist
events_dir = os.path.join(media_root, 'events')
if not os.path.exists(events_dir):
    os.makedirs(events_dir)


def random_image_url():
    response = requests.get('https://picsum.photos/800/600')
    return response.url


def random_string(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


categories = ['Technology', 'Music', 'Sports', 'Arts']
sub_categories = {
    'Technology': ['Web', 'Mobile', 'AI', 'Deep Learning'],
    'Music': ['Rock', 'Jazz', 'Hip Hop', 'Pop'],
    'Sports': ['Football', 'Basketball', 'Tennis', 'Swimming'],
    'Arts': ['Painting', 'Sculpture', 'Photography', 'Architecture']
}
for i in range(50):
    image_url = random_image_url()
    filename = str(uuid.uuid4()) + '.jpg'
    full_path = os.path.join(media_root, 'events', filename)
    with open(full_path, 'wb') as f:
        f.write(requests.get(image_url).content)

    event = {
        "id": str(uuid.uuid4()),
        "ID": str(uuid.uuid4()),
        "User_id": None,
        "Title": random_string(10),
        "organizer": random_string(8),
        "Summary": random_string(50),
        "Description": random_string(100),
        "type": "Seminar",
        "category_name": str(random.choice(categories)),
        "sub_Category": random.choice(sub_categories[random.choice(categories)]),
        "venue_name": random_string(10),
        "ST_DATE": datetime.datetime(2023, 4, 17),
        "END_DATE": datetime.datetime(2023, 4, 17),
        "ST_TIME": "08:15:15",
        "END_TIME": "12:15:15",
        "online": "True",
        "CAPACITY": random.randint(50, 200),
        "PASSWORD": None,
        "STATUS": "Draft",
        "image": full_path
    }
    db.event_event.insert_one(event)
print('MEDIA_ROOT:', settings.MEDIA_ROOT)
print('full_path:', full_path)

# import requests
# import uuid
# image_url = 'https://picsum.photos/800/600'
# filename = str(uuid.uuid4()) + '.jpg'
# full_path = '/Users/ismailtawfik/Downloads/EventBrite_Clone_Backend-19/eventbrite/media/events' + filename
# with open(full_path, 'wb') as f:
#     f.write(requests.get(image_url).content)


# "export DJANGO_SETTINGS_MODULE=eventbrite.settings"
