# Weather Application - Core Services
# Created: December 2024
# Description: Weather and location services for web interface

import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class WeatherService:
    """Handles weather API interactions and data processing"""

    def __init__(self):
        # Using OpenWeatherMap API (free tier)
        self.api_key = os.getenv('WEATHER_API_KEY', '')
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
        self.icon_url = "http://openweathermap.org/img/wn"
        self.geocoding_url = "http://api.openweathermap.org/geo/1.0"

        # Weather condition emojis for better display
        self.weather_emojis = {
            'clear sky': '☀️',
            'few clouds': '🌤️',
            'scattered clouds': '⛅',
            'broken clouds': '☁️',
            'overcast clouds': '☁️',
            'shower rain': '🌦️',
            'rain': '🌧️',
            'thunderstorm': '⛈️',
            'snow': '❄️',
            'mist': '🌫️',
            'fog': '🌫️',
            'haze': '🌫️',
            'dust': '💨',
            'sand': '💨',
            'smoke': '💨'
        }
        
    def get_api_key(self):
        """Get API key from environment, .env file, or user input"""
        # First try environment variable
        api_key = os.getenv('WEATHER_API_KEY')

        # If not found, try .env file
        if not api_key:
            try:
                if os.path.exists('.env'):
                    with open('.env', 'r') as f:
                        for line in f:
                            if line.startswith('WEATHER_API_KEY='):
                                api_key = line.split('=', 1)[1].strip()
                                break
            except Exception:
                pass

        # If still not found, try hardcoded fallback (for development)
        if not api_key:
            # You can temporarily set your API key here for testing
            api_key = "eadd8028ae3041f819b0f4068e02a02c"  # Your API key

        if api_key and len(api_key) > 10:
            self.api_key = api_key
            return True
        else:
            print("\n🌤️  Weather App Setup")
            print("=" * 40)
            print("To use this app, you need a free API key from OpenWeatherMap.")
            print("1. Visit: https://openweathermap.org/api")
            print("2. Sign up for a free account")
            print("3. Get your API key")
            print("4. Set it as environment variable: WEATHER_API_KEY")
            print("   Or enter it below (temporary for this session)")
            print("-" * 40)
            api_key = input("Enter your API key: ").strip()
            if api_key:
                self.api_key = api_key
                return True
            return False
    
    def get_current_weather(self, location, units='metric'):
        """Fetch current weather data for a location"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': units
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch weather data: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("Invalid response from weather service")
    
    def get_forecast(self, location, units='metric'):
        """Fetch 5-day weather forecast"""
        try:
            url = self.forecast_url
            params = {
                'q': location,
                'appid': self.api_key,
                'units': units
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch forecast data: {str(e)}")

    def get_weather_by_coordinates(self, lat: float, lon: float, units='metric'):
        """Fetch weather data using coordinates"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': units
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch weather data: {str(e)}")

    def get_air_quality(self, lat: float, lon: float):
        """Fetch air quality data"""
        try:
            url = f"{self.base_url}/air_pollution"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch air quality data: {str(e)}")

    def geocode_location(self, location: str):
        """Convert location name to coordinates"""
        try:
            url = f"{self.geocoding_url}/direct"
            params = {
                'q': location,
                'limit': 1,
                'appid': self.api_key
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            if data:
                return data[0]
            return None
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to geocode location: {str(e)}")
    
    def format_weather_data(self, data, units='metric'):
        """Format weather data for display"""
        if not data:
            return None

        temp_unit = "°C" if units == 'metric' else "°F"
        speed_unit = "m/s" if units == 'metric' else "mph"
        pressure_unit = "hPa"

        # Get weather emoji
        description = data['weather'][0]['description'].lower()
        emoji = self.weather_emojis.get(description, '🌤️')

        # Calculate additional info
        temp_min = data['main'].get('temp_min', data['main']['temp'])
        temp_max = data['main'].get('temp_max', data['main']['temp'])

        weather_info = {
            'location': f"{data['name']}, {data['sys']['country']}",
            'coordinates': f"{data['coord']['lat']:.2f}, {data['coord']['lon']:.2f}",
            'temperature': f"{data['main']['temp']:.1f}{temp_unit}",
            'temp_min': f"{temp_min:.1f}{temp_unit}",
            'temp_max': f"{temp_max:.1f}{temp_unit}",
            'feels_like': f"{data['main']['feels_like']:.1f}{temp_unit}",
            'description': data['weather'][0]['description'].title(),
            'emoji': emoji,
            'humidity': f"{data['main']['humidity']}%",
            'pressure': f"{data['main']['pressure']} {pressure_unit}",
            'wind_speed': f"{data['wind']['speed']} {speed_unit}",
            'wind_direction': f"{data['wind'].get('deg', 0)}°",
            'wind_gust': f"{data['wind'].get('gust', 0)} {speed_unit}" if 'gust' in data['wind'] else None,
            'visibility': f"{data.get('visibility', 0) / 1000:.1f} km",
            'cloudiness': f"{data['clouds']['all']}%",
            'icon': data['weather'][0]['icon'],
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
            'timezone': data.get('timezone', 0),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'raw_data': data  # Keep raw data for advanced processing
        }

        return weather_info

    def convert_temperature(self, temp: float, from_unit: str, to_unit: str) -> float:
        """Convert temperature between Celsius and Fahrenheit"""
        if from_unit == to_unit:
            return temp

        if from_unit.lower() == 'celsius' and to_unit.lower() == 'fahrenheit':
            return (temp * 9/5) + 32
        elif from_unit.lower() == 'fahrenheit' and to_unit.lower() == 'celsius':
            return (temp - 32) * 5/9
        else:
            raise ValueError("Unsupported temperature units")

    def get_weather_emoji(self, description: str) -> str:
        """Get appropriate emoji for weather condition"""
        return self.weather_emojis.get(description.lower(), '🌤️')

class LocationService:
    """Handles location detection and validation"""

    def __init__(self):
        self.current_location = None
        self.location_history = []

    def get_location_by_ip(self):
        """Get location using IP geolocation"""
        try:
            import geocoder
            g = geocoder.ip('me')
            if g.ok:
                location = f"{g.city}, {g.country}"
                self.current_location = {
                    'name': location,
                    'lat': g.latlng[0] if g.latlng else None,
                    'lon': g.latlng[1] if g.latlng else None,
                    'method': 'ip_detection'
                }
                return location
            return None
        except ImportError:
            print("💡 Tip: Install 'geocoder' package for automatic location detection")
            print("   Run: pip install geocoder")
            return None
        except Exception as e:
            print(f"⚠️  Location detection failed: {e}")
            return None

    def get_location_by_gps(self):
        """Get location using GPS (placeholder for mobile implementation)"""
        # This would be implemented for mobile apps
        print("📱 GPS location detection not available in desktop version")
        return None

    def validate_location(self, location):
        """Validate location input"""
        if not location or len(location.strip()) < 2:
            return False, "Location must be at least 2 characters long"

        # Remove extra spaces
        location = ' '.join(location.split())

        # Basic validation - allow letters, numbers, spaces, commas, hyphens, apostrophes
        import re
        if not re.match(r'^[a-zA-Z0-9\s,.\'-]+$', location):
            return False, "Location contains invalid characters"

        # Check for common location patterns
        valid_patterns = [
            r'^[a-zA-Z\s]+$',  # City name only
            r'^[a-zA-Z\s]+,\s*[a-zA-Z\s]+$',  # City, Country
            r'^[a-zA-Z\s]+,\s*[A-Z]{2}$',  # City, State Code
            r'^\d{5}$',  # ZIP code (US)
            r'^[a-zA-Z]\d[a-zA-Z]\s*\d[a-zA-Z]\d$',  # Postal code (Canada)
        ]

        if any(re.match(pattern, location) for pattern in valid_patterns):
            return True, "Valid location"

        # If no pattern matches but basic validation passed, still allow it
        return True, "Location format accepted"

    def add_to_history(self, location):
        """Add location to search history"""
        if location not in self.location_history:
            self.location_history.append(location)
            # Keep only last 10 locations
            if len(self.location_history) > 10:
                self.location_history.pop(0)

    def get_location_suggestions(self, partial_location):
        """Get location suggestions based on history"""
        if not partial_location:
            return self.location_history[-5:]  # Return last 5 locations

        suggestions = []
        partial_lower = partial_location.lower()

        for location in self.location_history:
            if partial_lower in location.lower():
                suggestions.append(location)

        return suggestions[:5]  # Return max 5 suggestions

# This module provides WeatherService and LocationService classes
# for the web interface to use
