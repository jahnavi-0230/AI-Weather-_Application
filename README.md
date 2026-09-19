# AI-Weather-_Application

A Flask web application that displays current city weather and uses Groq to provide a practical AI weather explanation.

## Setup

Install Python 3.10+, get an [OpenWeatherMap key](https://openweathermap.org/api) and a [Groq key](https://console.groq.com/keys), then run:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Set `WEATHER_API_KEY` and `GROQ_API_KEY` in `.env`, then start the application:

```powershell
python app.py
```

Visit `http://127.0.0.1:5000`. Run automated tests with `pytest`.

`POST /api/weather` accepts `{"city":"Delhi"}`. OpenWeatherMap uses metric units and API keys remain server-side.
