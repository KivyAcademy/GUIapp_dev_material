import requests
import json

server = 'https://buena-comida.appspot.com'

def login(user='rtorres', password='swagdmin', server='https://buena-comida.appspot.com'):
    session = requests.Session()
    r = requests.post(server + '/users/login', json={'user_name': user,
                                                     'password': password})
    session.headers['cookie'] = r.headers['set-cookie']
    return session, r.json()['id']

tags = json.load(open('tags2.json'))

upload_tags = tags

s, id_ = login()

s.post(server + '/tags', json=tags)

