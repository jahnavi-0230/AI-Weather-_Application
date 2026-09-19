# AI Weather App

A Flask app that gets current weather from OpenWeatherMap and uses Groq to write a short practical explanation.

## Setup

Install Python 3.10+, get an [OpenWeatherMap key](https://openweathermap.org/api) and a [Groq key](https://console.groq.com/keys), then run:

```powershell
cd ai-weather-app
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Set `WEATHER_API_KEY` and `GROQ_API_KEY` in `.env`, then start it:

```powershell
python app.py
```

Visit `http://127.0.0.1:5000`. Run tests with `pytest`.

`POST /api/weather` accepts `{"city":"Delhi"}`. OpenWeatherMap uses metric units. API keys stay on the server.
