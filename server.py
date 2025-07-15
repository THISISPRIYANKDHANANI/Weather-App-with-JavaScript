# Weather App - Web Server
# A Flask web application for displaying weather information
# Built with love for weather enthusiasts

import os
import json
from flask import Flask, render_template, request, jsonify
from weather_app import WeatherService, LocationService
from datetime import datetime
import threading
import time

# Create Flask application
app = Flask(__name__)
app.secret_key = 'my-weather-app-secret-key-2024'

# Create weather and location service instances
weather_service = WeatherService()
location_service = LocationService()

def setup_api_key():
    """Set up the weather API key"""
    if not weather_service.get_api_key():
        # Use the API key - you can get your own from openweathermap.org
        api_key = "eadd8028ae3041f819b0f4068e02a02c"
        weather_service.api_key = api_key
        return True
    return True

# Initialize API key when server starts
setup_api_key()

@app.route('/')
def home():
    """Display the main weather app page"""
    return render_template('weather_index.html')

@app.route('/api/weather')
def get_weather():
    """API endpoint to get current weather"""
    location = request.args.get('location', '').strip()
    units = request.args.get('units', 'metric')

    if not location:
        return jsonify({'error': 'Location parameter is required'}), 400

    # Validate location
    is_valid, message = location_service.validate_location(location)
    if not is_valid:
        return jsonify({'error': message}), 400

    try:
        # Ensure API key is set
        if not weather_service.api_key:
            api_key = os.getenv('WEATHER_API_KEY') or "eadd8028ae3041f819b0f4068e02a02c"
            weather_service.api_key = api_key

        # Get weather data
        weather_data = weather_service.get_current_weather(location, units)
        formatted_data = weather_service.format_weather_data(weather_data, units)

        return jsonify({
            'success': True,
            'data': formatted_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/forecast')
def get_forecast():
    """API endpoint to get weather forecast"""
    location = request.args.get('location', '').strip()
    units = request.args.get('units', 'metric')

    if not location:
        return jsonify({'error': 'Location parameter is required'}), 400

    try:
        # Ensure API key is set
        if not weather_service.api_key:
            api_key = os.getenv('WEATHER_API_KEY') or "eadd8028ae3041f819b0f4068e02a02c"
            weather_service.api_key = api_key

        # Get forecast data
        forecast_data = weather_service.get_forecast(location, units)

        return jsonify({
            'success': True,
            'data': forecast_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/location')
def auto_detect_location():
    """API endpoint for automatic location detection"""
    try:
        location = location_service.get_location_by_ip()
        if location:
            return jsonify({
                'success': True,
                'location': location
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Could not detect location automatically'
            }), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather-history')
def get_weather_history():
    """API endpoint to get weather history (mock data for demo)"""
    location = request.args.get('location', '').strip()

    if not location:
        return jsonify({'error': 'Location parameter is required'}), 400

    # Mock historical data for demonstration
    import random
    from datetime import datetime, timedelta

    history = []
    for i in range(7):  # Last 7 days
        date = datetime.now() - timedelta(days=i)
        temp = random.randint(15, 30)
        history.append({
            'date': date.strftime('%Y-%m-%d'),
            'temperature': temp,
            'condition': random.choice(['Sunny', 'Cloudy', 'Rainy', 'Partly Cloudy']),
            'humidity': random.randint(40, 80)
        })

    return jsonify({
        'success': True,
        'location': location,
        'history': history
    })

if __name__ == '__main__':
    print("🌤️  Starting Weather App Web Server...")
    print("📍 Access the application at: http://localhost:5000")
    print("🔑 Make sure to set WEATHER_API_KEY environment variable")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
