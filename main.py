#!/usr/bin/env python3
"""
Simple Weather App
A beginner-friendly weather application

Features:
- Real-time weather data from OpenWeatherMap API
- Easy location search (city names or ZIP codes)
- Temperature in Celsius or Fahrenheit
- Beautiful web interface with animations
- Automatic location detection
- Detailed weather information including humidity, wind, etc.
"""

import os

def check_dependencies():
    """Check if required packages are installed"""
    missing_packages = []

    try:
        import requests
    except ImportError:
        missing_packages.append("requests")

    try:
        import flask
    except ImportError:
        missing_packages.append("flask")

    if missing_packages:
        print("⚠️  Missing Dependencies:")
        print("The following packages need to be installed:")
        for package in missing_packages:
            print(f"   - {package}")
        print()
        print("📦 To install dependencies, run:")
        print("   pip install -r requirements.txt")
        print()
        return False

    return True

def setup_api_key():
    """Help user set up API key"""
    print("🔑 API Key Setup")
    print("=" * 30)
    print()
    print("To use this weather app, you need a free API key from OpenWeatherMap:")
    print()
    print("📋 Steps to get your API key:")
    print("   1. Visit: https://openweathermap.org/api")
    print("   2. Click 'Sign Up' and create a free account")
    print("   3. After login, go to 'API keys' section")
    print("   4. Copy your API key")
    print()
    print("🔧 How to set your API key:")
    print("   Option 1: Set environment variable")
    print("     Windows: set WEATHER_API_KEY=your_key_here")
    print("     Linux/Mac: export WEATHER_API_KEY=your_key_here")
    print()
    print("   Option 2: Create .env file in project folder")
    print("     Add line: WEATHER_API_KEY=your_key_here")
    print()

def launch_web():
    """Launch web interface"""
    try:
        print("🌤️" + "=" * 50 + "🌤️")
        print("        WEATHER APP - WEB INTERFACE")
        print("🌤️" + "=" * 50 + "🌤️")
        print()
        print("🚀 Starting Weather App...")
        print("🌐 Initializing server... Please wait...")

        # Check dependencies first
        if not check_dependencies():
            print("\n📦 Please install dependencies first:")
            print("   pip install -r requirements.txt")
            return

        # Import and run the Flask app
        from server import app
        print("✅ Server ready!")
        print("📍 Open your browser and go to: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 50)

        app.run(debug=False, host='0.0.0.0', port=5000)

    except ImportError as e:
        print(f"❌ Error importing web module: {e}")
        print("💡 Make sure Flask is installed: pip install flask")
    except Exception as e:
        print(f"❌ Error launching web app: {e}")

def main():
    """Main application launcher"""
    try:
        print("🌤️ Welcome to Weather App!")
        print("🌐 Starting web interface...")
        print()

        # Show API key setup info
        api_key = os.getenv('WEATHER_API_KEY')
        if not api_key:
            print("⚠️  API Key not found!")
            setup_api_key()
            print()

        launch_web()

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for using Weather App!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("🔧 Please check your installation and try again.")

if __name__ == "__main__":
    main()
