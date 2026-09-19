"""Input validation utilities."""
import re

CITY_PATTERN = re.compile(r"^[\w\s,.'-]+$", re.UNICODE)


def validate_city(city):
    if not isinstance(city, str):
        return False, "City must be text."
    city = city.strip()
    if not city:
        return False, "Enter a city name."
    if len(city) > 100:
        return False, "City name must be 100 characters or fewer."
    if not CITY_PATTERN.fullmatch(city):
        return False, "City name contains unsupported characters."
    return True, ""
