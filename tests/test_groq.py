from unittest.mock import Mock, patch
import pytest
from services.groq_service import GroqServiceError, generate_weather_explanation

WEATHER = {"city": "Delhi", "country": "IN", "temperature": 30, "feels_like": 32, "description": "clear sky", "humidity": 40, "wind_speed": 2, "visibility_km": 10}
CONFIG = {"GROQ_API_KEY": "key", "GROQ_MODEL": "test-model"}

@patch("services.groq_service.Groq")
def test_generates_trimmed_explanation(mock_groq):
    mock_groq.return_value.chat.completions.create.return_value = Mock(choices=[Mock(message=Mock(content="  Clear and warm. Wear light clothing.  "))])
    assert generate_weather_explanation(WEATHER, CONFIG) == "Clear and warm. Wear light clothing."

def test_missing_key_is_a_clear_error():
    with pytest.raises(GroqServiceError, match="not configured"): generate_weather_explanation(WEATHER, {"GROQ_API_KEY": ""})
