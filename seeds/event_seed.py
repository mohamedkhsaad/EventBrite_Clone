import os
import random
import string
import datetime
from pymongo import MongoClient
import uuid
import requests






# client = MongoClient()
# db = client['eventbrite-db']

client = MongoClient("mongodb+srv://ismail:512002@cluster0.7bge3an.mongodb.net/?retryWrites=true&w=majority", username="ismail", password="512002")
db = client['event-us']

media_root = ''
events_dir = os.path.join(media_root, 'events/')
if not os.path.exists(events_dir):
    os.makedirs(events_dir)
user = {
    "id": "1190264",
    "email": "ismailtawfik@gmail.com",
    "password": "Password123*",
    "first_name": "Ismail",
    "last_name": "Tawfik",
    'username': "IsmailTawfik"
}
db.user_user.insert_one(user)


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


def generate_unique_id():
    while True:
        # Generate a random integer between 1 and 9999
        new_id = random.randint(1, 9999)
        # Check if an event with this ID already exists in the database
        if not db.event_event.find_one({"ID": new_id}):
            return new_id


for i in range(10):
    image_url = random_image_url()
    filename = str(uuid.uuid4()) + '.jpg'
    full_path = os.path.join(media_root, 'events', filename)
    with open(full_path, 'wb') as f:
        f.write(requests.get(image_url).content)
    event = {
        "id": uuid.uuid4().hex,
        "ID": str(generate_unique_id()),
        "User_id": user['id'],
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
        "STATUS": "Live",
        "image": full_path
    }
    db.event_event.insert_one(event)



# from djongo import settings
# from pymongo import MongoClient
# settings.configure(
#     DATABASES={
#         'default': {
#             'ENGINE': 'djongo',
#             'NAME': 'event-us',
#             'ENFORCE_SCHEMA': False,
#             'CLIENT': {
#                 'host': 'mongodb+srv://ismail:512002@cluster0.7bge3an.mongodb.net/?retryWrites=true&w=majority',
#             }
#         }
#     }
# )
# client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
# db = client[settings.DATABASES['default']['NAME']]