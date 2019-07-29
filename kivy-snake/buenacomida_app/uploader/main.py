from kivyrt.network.datastore import DatastoreModel, ConfiguratorModel
from kivyrt.storage.autosavestore import AutosaveStore
from kivy.app import App


class Uploader(App):
    def __init__(self, **kwargs):
        super(Uploader, self).__init__(**kwargs)
        self.users = ConfiguratorModel('https://buena-comida.appspot.com')
        self.storage = AutosaveStore('storage.json', ['headers', 'cache'], self.users)
        self.restaurants = DatastoreModel(self.users, 'restaurants')
        self.restaurants.get()

Uploader().run()

