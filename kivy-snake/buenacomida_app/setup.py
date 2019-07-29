from distutils.core import setup
from setuptools import find_packages

options = {'apk': {'debug': None,  # use None for arguments that don't pass a value
                   'requirements': 'kivy,openssl,requests,futures,android',
                   'android-api': 19,
                   'dist-name': 'python2',
                   'package': 'mx.buenacomida.buenacomida',
                   'orientation': 'portrait',
                   'arch': 'armeabi-v7a',
                   'permissions': 'INTERNET ACCESS_FINE_LOCATION'.split(),
                   'window': None,
                   'release': None,
                   'presplash': 'apk_files/presplash.png',
                   # 'presplash-color': '#0a496eff',
                   'icon': 'apk_files/app_icon.png'}}

packages = find_packages()
maxpathlen = max(len(package.split('.')) for package in packages)
extensions = '*.py *.ttf *.ttfs *.png *.atlas *.json *.kv *.zip'.split()
res = {'app' + ('/*' * num): extensions for num in range(maxpathlen)}

setup(
    name='Buena Comida',
    version='0.91',
    description='all of mexicos food in one place',
    author='Rodolfo Torres',
    author_email='rtorresware@gmail.com',
    packages=packages,
    options=options,
    package_data=res
)
