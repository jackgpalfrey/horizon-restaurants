from src.api.utils.Result import OK
from src.city.CityService import CityService


def post():
    cities = CityService.get_all()

    cities_data = [{"id": c.get_id(),
                    "name": c.get_name()} for c in cities]

    return OK({"cities": cities_data})
