from unittest.mock import Mock, patch
import pytest
from services.weather_service import WeatherServiceError, get_current_weather

CONFIG = {"WEATHER_API_KEY": "key", "WEATHER_BASE_URL": "https://example.test", "REQUEST_TIMEOUT_SECONDS": 5}

@patch("services.weather_service.requests.get")
def test_current_weather_is_normalized(mock_get):
    response = Mock(ok=True, status_code=200)
    response.json.return_value = {"name": "Delhi", "sys": {"country": "IN"}, "main": {"temp": 30.4, "feels_like": 33, "humidity": 60, "pressure": 1005}, "weather": [{"main": "Clouds", "description": "scattered clouds", "icon": "03d"}], "wind": {"speed": 3.1, "deg": 120}, "visibility": 9000}
    mock_get.return_value = response
    weather = get_current_weather("Delhi", CONFIG)
    assert weather["city"] == "Delhi" and weather["visibility_km"] == 9.0

@patch("services.weather_service.requests.get")
def test_missing_city_returns_404_error(mock_get):
    mock_get.return_value = Mock(ok=False, status_code=404)
    with pytest.raises(WeatherServiceError, match="City not found") as error: get_current_weather("missing", CONFIG)
    assert error.value.status_code == 404
