'''
iOS GPS
-----------
'''

from pyobjus import autoclass, protocol
from pyobjus.dylib_manager import load_framework
from plyer.facades import GPS

load_framework('/System/Library/Frameworks/CoreLocation.framework')
CLLocationManager = autoclass('CLLocationManager')


class IosGPS(GPS):
    def _configure(self):
        if not hasattr(self, '_location_manager'):
            self._location_manager = CLLocationManager.alloc().init()

    def _start(self, **kwargs):
        self._location_manager.delegate = self

        self._location_manager.requestWhenInUseAuthorization()
        # NSLocationWhenInUseUsageDescription key must exist in Info.plist
        # file. When the authorization prompt is displayed your app goes
        # into pause mode and if your app doesn't support background mode
        # it will crash.
        self._location_manager.startUpdatingLocation()

    def _stop(self):
        self._location_manager.stopUpdatingLocation()

    @protocol('CLLocationManagerDelegate')
    def locationManager_didUpdateLocations_(self, manager, locations):
        location = manager.location
        description = location.description.UTF8String()
        lat, lon = [float(coord) for coord in description.split('<')[-1].split('>')[0].split(',')]
        acc = float(description.split(' +/- ')[-1].split('m ')[0])
        
        self.on_location(lat=lat, lon=lon, accuracy=acc)


def instance():
    return IosGPS()
