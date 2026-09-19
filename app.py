"""Flask application for current weather and an AI weather explanation."""
from flask import Flask, jsonify, render_template, request
from config.config import Config
from services.groq_service import GroqServiceError, generate_weather_explanation
from services.weather_service import WeatherServiceError, get_current_weather
from utils.validators import validate_city


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/api/weather")
    def weather():
        payload = request.get_json(silent=True) or {}
        valid, error = validate_city(payload.get("city", ""))
        if not valid:
            return jsonify({"error": error}), 400
        try:
            weather_data = get_current_weather(payload["city"], app.config)
        except WeatherServiceError as exc:
            return jsonify({"error": str(exc)}), exc.status_code
        try:
            explanation = generate_weather_explanation(weather_data, app.config)
            ai_error = None
        except GroqServiceError as exc:
            explanation, ai_error = None, str(exc)
        response = {"weather": weather_data, "ai_explanation": explanation}
        if ai_error:
            response["ai_error"] = ai_error
        return jsonify(response)

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Route not found."}), 404
    return app


app = create_app()
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=app.config["DEBUG"])
