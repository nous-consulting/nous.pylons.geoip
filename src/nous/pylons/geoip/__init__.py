import os
import pygeoip
from threading import Lock

GEOIP_DB_PATH = os.path.join(os.path.dirname(__file__), 'GeoIPCity.dat')
gi = pygeoip.GeoIP(GEOIP_DB_PATH)
gi_lock = Lock()

def get_city_and_country(user_ip):
    try:
        gi_lock.acquire()
        record = gi.record_by_addr(user_ip)
    except pygeoip.GeoIPError:
        return '', ''
    finally:
        gi_lock.release()

    if record is None:
        return '', ''

    country_code = record.get('country_code')
    city = unicode(record.get('city', ''), 'iso-8859-1')
    return country_code, city
