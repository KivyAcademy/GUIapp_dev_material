from kivyrt.rating_label import rating_to_stars


def marker_interface(restaurant):
    return {'lat': restaurant['location'][0],
            'lon': restaurant['location'][1],
            'key': restaurant['id'],
            'source': 'res/logo.png'}


def quickview_presenter(restaurant):
    _tags = restaurant['tags']
    tags = _tags[:len(_tags)/2]
    return {'name': restaurant['name'],
            'rating': '{0:2.1f}'.format(5),
            'stars': rating_to_stars(5),
            'price': '$' * (restaurant['price'] or 2),
            'address': restaurant['address'],
            'tags': ', '.join(tags),
            'thumbnail': (restaurant['images'] + [''])[0],
            'key': restaurant['id']}


def detail_interface(restaurant):
    _tags = restaurant['tags']
    tags = _tags[:len(_tags)/2]
    return {'name': restaurant['name'],
            'rating': '{0:2.1f}'.format(5),
            'stars': rating_to_stars(5),
            'address': restaurant['address'],
            'phone_number': restaurant['phone_number'],
            'website': restaurant['website'],
            'price': '$' * (restaurant['price'] or 2),
            'tags': ', '.join(tags),
            'images': restaurant['images'] * 3,
            'key': restaurant['id']}


def comment_interface(comment):
    return {'commenter': comment['commenter'],
            'text': comment['text'],
            'key': comment['id'],
            'created': str(comment['created']),
            'stars': rating_to_stars(comment['rating'])}


