import json
import requests

json_filename = 'new_restaurants.json'
server = 'https://buena-comida.appspot.com'

with open(json_filename) as jsonfile:
    restaurants = json.load(jsonfile)

user_key = 'me'
_session = None


def logged_in_session():
    s = requests.Session()
    r = requests.post(server + '/users/login', json={'user_name': 'rtorres',
                                                    'password': 'swagdmin'})
    s.headers['cookie'] = r.headers['set-cookie']
    global user_key
    user_key = r.json()['id']
    return s


def get_session():
    global _session
    if not _session:
        _session = logged_in_session()
    return _session


def process_old_restaurant(restaurant):
    return {'name': restaurant['nombre'],
            'address': restaurant['direccion'],
            'city': restaurant['ciudad'],
            'images': [restaurant['imagen']],
            'website': restaurant['link'],
            'phone_number': restaurant['telefono'],
            'location': restaurant['coord']}

def with_owner(entities):
    for entity in entities:
        entity['owner'] = user_key
        yield entity


def uplodad_restaurants(restaurants):
    s = get_session()
    r = s.post(server + '/restaurants', json=list(with_owner(restaurants)))
    print(r.json())


