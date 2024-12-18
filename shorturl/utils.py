import string
import random
from geoip2.database import Reader

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def get_geo_info(ip):
    """Получить информацию о стране и городе по IP."""
    try:
        reader = Reader('geoip/GeoLite2-City.mmdb')
        response = reader.city(ip)
        country = response.country.name
        city = response.city.name
        return country, city
    except Exception:
        return None, None