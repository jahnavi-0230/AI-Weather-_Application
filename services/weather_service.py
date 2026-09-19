"""OpenWeatherMap current-weather integration."""
import requests


class WeatherServiceError(Exception):
    def __init__(self, message, status_code=502):
        super().__init__(message)
        self.status_code = status_code


def get_current_weather(city, config):
    """Return normalized current weather in metric units."""
    api_key = config.get("WEATHER_API_KEY", "")
    if not api_key:
        raise WeatherServiceError("Weather service is not configured.", 503)
    try:
        response = requests.get(config["WEATHER_BASE_URL"], params={"q": city.strip(), "appid": api_key, "units": "metric"}, timeout=config["REQUEST_TIMEOUT_SECONDS"])
    except requests.RequestException as exc:
        raise WeatherServiceError("Could not reach the weather service.") from exc
    if response.status_code == 404:
        raise WeatherServiceError("City not found. Check the city name and try again.", 404)
    if response.status_code in (401, 403):
        raise WeatherServiceError("Weather service authentication failed.", 503)
    if response.status_code == 429:
        raise WeatherServiceError("Weather service rate limit reached. Try again shortly.", 429)
    if not response.ok:
        raise WeatherServiceError("Weather service is temporarily unavailable.")
    try:
        data = response.json(); condition = data["weather"][0]; main = data["main"]
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise WeatherServiceError("Weather service returned an unexpected response.") from exc
    wind = data.get("wind", {})
    return {"city": data.get("name", city.strip()), "country": data.get("sys", {}).get("country", ""), "temperature": main.get("temp"), "feels_like": main.get("feels_like"), "humidity": main.get("humidity"), "pressure": main.get("pressure"), "condition": condition.get("main", "Unknown"), "description": condition.get("description", "No description available"), "icon": condition.get("icon", ""), "wind_speed": wind.get("speed", 0), "wind_direction": wind.get("deg"), "visibility_km": round(data.get("visibility", 0) / 1000, 1), "unit": "C"}
