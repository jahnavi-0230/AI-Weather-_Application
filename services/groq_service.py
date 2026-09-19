"""Groq integration for grounded weather explanations."""
from groq import Groq


class GroqServiceError(Exception):
    """Expected AI-provider failure safe to display."""


def generate_weather_explanation(weather_data, config):
    api_key = config.get("GROQ_API_KEY", "")
    if not api_key:
        raise GroqServiceError("AI explanation is unavailable because Groq is not configured.")
    facts = (f"Location: {weather_data['city']}, {weather_data['country']}. Temperature: {weather_data['temperature']}°C "
             f"(feels like {weather_data['feels_like']}°C). Condition: {weather_data['description']}. "
             f"Humidity: {weather_data['humidity']}%. Wind: {weather_data['wind_speed']} m/s. Visibility: {weather_data['visibility_km']} km.")
    try:
        completion = Groq(api_key=api_key).chat.completions.create(
            model=config["GROQ_MODEL"], temperature=0.3, max_completion_tokens=120,
            messages=[{"role": "system", "content": "Give a concise weather explanation in 2–3 sentences. Use only the provided current-weather facts; do not forecast. Include one practical, non-medical suggestion."}, {"role": "user", "content": facts}])
        content = completion.choices[0].message.content
    except Exception as exc:
        raise GroqServiceError("AI explanation is temporarily unavailable.") from exc
    if not content or not content.strip():
        raise GroqServiceError("AI explanation was empty. Please try again.")
    return content.strip()
