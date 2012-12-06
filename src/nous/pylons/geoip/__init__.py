import os
import pygeoip
from threading import Lock

GEOIP_DB_PATH = os.path.join(os.path.dirname(__file__), 'GeoLiteCity.dat')
gi = pygeoip.GeoIP(GEOIP_DB_PATH)
gi_lock = Lock()

def get_record(user_ip):
    try:
        gi_lock.acquire()
        record = gi.record_by_addr(user_ip)
    except pygeoip.GeoIPError:
        record = {}
    finally:
        gi_lock.release()

    return record if record is not None else {}

def get_city_and_country(user_ip):
    record = get_record(user_ip)
    if not record:
        return '', ''

    country_code = record.get('country_code')
    city = unicode(record.get('city', ''), 'iso-8859-1')
    return country_code, city
