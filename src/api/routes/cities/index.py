from src.api.utils.Result import OK
from src.api.utils.dictify import dictify_city
from src.city.CityService import CityService


def post():
    cities = CityService.get_all()

    cities_data = [dictify_city(c) for c in cities]

    return OK({"cities": cities_data})
