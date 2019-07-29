import csv
import json
import grequests

from urllib.parse import urlencode



geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json?{}' \
              '&key=AIzaSyDVVAh1A6H2wjgB6JEHpAhu3BDaD1_Jjr0'
address_keys = 'Address City State Zipcode'.split()
_semaphore = 100


def csv_to_json(filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        processed = (convert_propnames(row) for row in reader)
        return list(processed)


def convert_propnames(restaurant):
    return {'name': restaurant['Restaurant Name'],
            'tags': restaurant['Type of food'].split(','),
            'phone_number': restaurant['Phone'],
            'website': restaurant['Website'],
            'price': restaurant['Price Range'].count('$'),
            'address': get_address(restaurant)}


def get_test_restaurants(filename):
    with open(filename) as jsonfile:
        return json.load(jsonfile)


def get_address(restaurant):
    return '{}\n{}, {}. {}'.format(*[restaurant[key] for key in address_keys])


def geocode_addresses(addresses):
    urls = [geocode_url.format(urlencode({'address': address}))
            for address in addresses]
    l = urls
    n = _semaphore
    chunks = [l[i:i + n] for i in range(0, len(l), n)]
    for chunk in chunks:
        rs = (grequests.get(u) for u in chunk)
        res = grequests.map(rs)
        results.extend([process_georesponse(r.json()) for r in res])
        with open('results.json', 'w') as jsonfile:
            json.dump(results, jsonfile)
            print('saved {}'.format(len(chunk)))
    return results


def geocode_locations(locations):
    coordinates = geocode_addresses([l['address'] for l in locations])
    return (dict(location=coord, **location) for location, coord
            in zip(locations, coordinates) if coord is not None)


def process_georesponse(res):
    try:
        geopt = res['results'][0]['geometry']['location']
        return [geopt['lat'], geopt['lng']]
    except (KeyError, IndexError):
        return None


with open('geocoded.json', 'w') as jsonfile:
    json.dump(list(geocode_locations(get_test_restaurants('30k.json'))),
              jsonfile)

