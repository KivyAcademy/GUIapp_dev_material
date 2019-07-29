from kivy.uix.screenmanager import Screen
from kivy import properties as kp

from kivyrt.input_group import InputGroup
from kivyrt.forms import FormBehavior, is_email, mark_as_required
from kivyrt.subclasses import HeightlessBox


class LoginScreen(Screen):
    pass


default_args = {'user_name': {'error': False},
                'password': {'error': False}}


class LoginForm(FormBehavior, HeightlessBox):
    defaults = default_args

    def on_input(self, data, defaults):
        defaults['user_name']['text'] = ''.join(data['user_name'].lower().split())
        defaults['password']['text'] = ''.join(data['password'].split())

    def verify_data(self, data, defaults):
        defaults.update(mark_as_required(list(data), data, error=True,
                                         error_code='required'))
        if data['user_name'] and data['password']:
            return data


signup_defaults = {'user_name': {'error': False},
                   'email': {'error': False},
                   'password': {'error': False},
                   'verify': {'error': False}}


class SignupForm(FormBehavior, HeightlessBox):
    defaults = signup_defaults

    def on_input(self, data, defaults):
        defaults['user_name']['text'] = ''.join(data['user_name'].lower().split())
        defaults['password']['text'] = ''.join(data['password'].split())

        if ' ' in data['password']:
            defaults['password']['error_code'] = 'no_spaces'
            defaults['password']['error'] = True

        if data['verify'] and data['password'] != data['verify']:
            defaults['verify']['error_code'] = 'passwords_dont_match'
            defaults['verify']['error'] = True

        if data['email'] and not is_email(data['email']):
            defaults['email']['error_code'] = 'not_an_email'
            defaults['email']['error'] = True

        if ' ' in data['user_name']:
            defaults['user_name']['error_code'] = 'no_spaces'
            defaults['user_name']['error'] = True

    def verify_data(self, data, defaults):
        defaults.update(mark_as_required(list(data), data, error=True,
                                         error_code='required'))
        if (len(data['user_name']) > 5 and
            is_email(data['email']) and
            len(data['password']) > 5 and
            data['verify'] == data['password']):
            data.pop('verify')
            return data

