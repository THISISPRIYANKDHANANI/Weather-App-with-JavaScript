// Weather App - Main JavaScript
// Interactive weather application with smooth animations
// Made with care for a great user experience

let currentWeatherData = null;
let currentUnits = 'metric';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Set up event listeners
    document.getElementById('locationInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            getWeather();
        }
    });
    
    document.getElementById('unitsSelect').addEventListener('change', function() {
        currentUnits = this.value;
        if (currentWeatherData) {
            // Refresh weather data with new units
            const location = document.getElementById('locationInput').value;
            if (location) {
                getWeather();
            }
        }
    });
    
    // Add input validation
    const locationInput = document.getElementById('locationInput');
    locationInput.addEventListener('input', validateLocationInput);
    
    console.log('🌤️ Weather app ready to go!');
}

function validateLocationInput() {
    const input = document.getElementById('locationInput');
    const value = input.value.trim();
    
    // Remove invalid characters
    const cleanValue = value.replace(/[^a-zA-Z0-9\s,.\'-]/g, '');
    if (cleanValue !== value) {
        input.value = cleanValue;
    }
    
    // Visual feedback
    if (value.length >= 2) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    } else if (value.length > 0) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
    } else {
        input.classList.remove('is-invalid', 'is-valid');
    }
}

function showLoading() {
    document.getElementById('loadingSpinner').style.display = 'block';
    document.getElementById('weatherDisplay').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loadingSpinner').style.display = 'none';
}

function showError(message) {
    hideLoading();
    const errorDiv = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    errorText.textContent = message;
    errorDiv.style.display = 'block';
    
    // Auto-hide error after 5 seconds
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

function showWeatherData(data) {
    hideLoading();
    document.getElementById('errorMessage').style.display = 'none';
    
    currentWeatherData = data;
    const weatherDisplay = document.getElementById('weatherDisplay');
    
    // Create weather display HTML
    const weatherHTML = createWeatherHTML(data);
    weatherDisplay.innerHTML = weatherHTML;
    weatherDisplay.style.display = 'block';
    
    // Add fade-in animation
    weatherDisplay.classList.add('fade-in');
    
    // Add pulse animation to temperature
    setTimeout(() => {
        const tempElement = weatherDisplay.querySelector('.temperature-display');
        if (tempElement) {
            tempElement.classList.add('pulse-animation');
        }
    }, 500);
}

function createWeatherHTML(data) {
    const tempUnit = currentUnits === 'metric' ? '°C' : '°F';
    const speedUnit = currentUnits === 'metric' ? 'm/s' : 'mph';
    
    return `
        <div class="weather-card">
            <div class="row">
                <div class="col-md-6">
                    <h2><i class="fas fa-map-marker-alt"></i> ${data.location}</h2>
                    <p class="mb-1"><i class="fas fa-clock"></i> ${data.timestamp}</p>
                    <p><i class="fas fa-globe"></i> ${data.coordinates}</p>
                </div>
                <div class="col-md-6 text-end">
                    <div class="units-toggle">
                        <button onclick="switchUnits('metric')" class="${currentUnits === 'metric' ? 'active' : ''}">°C</button>
                        <button onclick="switchUnits('imperial')" class="${currentUnits === 'imperial' ? 'active' : ''}">°F</button>
                    </div>
                </div>
            </div>
            
            <div class="text-center">
                <div class="weather-icon">${data.emoji}</div>
                <div class="temperature-display">${data.temperature}</div>
                <h4>${data.description}</h4>
                <p>Feels like ${data.feels_like}</p>
                <p>High: ${data.temp_max} | Low: ${data.temp_min}</p>
            </div>
            
            <div class="weather-details">
                <div class="detail-card">
                    <div class="detail-icon"><i class="fas fa-tint"></i></div>
                    <h5>Humidity</h5>
                    <p>${data.humidity}</p>
                </div>
                
                <div class="detail-card">
                    <div class="detail-icon"><i class="fas fa-thermometer-half"></i></div>
                    <h5>Pressure</h5>
                    <p>${data.pressure}</p>
                </div>
                
                <div class="detail-card">
                    <div class="detail-icon"><i class="fas fa-wind"></i></div>
                    <h5>Wind Speed</h5>
                    <p>${data.wind_speed}</p>
                </div>
                
                <div class="detail-card">
                    <div class="detail-icon"><i class="fas fa-compass"></i></div>
                    <h5>Wind Direction</h5>
                    <p>${data.wind_direction}</p>
                </div>
                
                <div class="detail-card">
                    <div class="detail-icon"><i class="fas fa-eye"></i></div>
                    <h5>Visibility</h5>
                    <p>${data.visibility}</p>
                </div>
                
                <div class="detail-card">
                    <div class="detail-icon"><i class="fas fa-cloud"></i></div>
                    <h5>Cloudiness</h5>
                    <p>${data.cloudiness}</p>
                </div>
                
                <div class="detail-card">
                    <div class="detail-icon"><i class="fas fa-sun"></i></div>
                    <h5>Sunrise</h5>
                    <p>${data.sunrise}</p>
                </div>
                
                <div class="detail-card">
                    <div class="detail-icon"><i class="fas fa-moon"></i></div>
                    <h5>Sunset</h5>
                    <p>${data.sunset}</p>
                </div>
            </div>
        </div>
    `;
}

function switchUnits(units) {
    if (units !== currentUnits) {
        currentUnits = units;
        document.getElementById('unitsSelect').value = units;
        
        // Refresh weather data with new units
        const location = document.getElementById('locationInput').value;
        if (location && currentWeatherData) {
            getWeather();
        }
    }
}

async function getWeather() {
    const location = document.getElementById('locationInput').value.trim();
    
    if (!location) {
        showError('Please enter a location!');
        return;
    }
    
    if (location.length < 2) {
        showError('Location must be at least 2 characters long!');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`/api/weather?location=${encodeURIComponent(location)}&units=${currentUnits}`);
        const result = await response.json();
        
        if (result.success) {
            showWeatherData(result.data);
        } else {
            showError(result.error || 'Failed to fetch weather data');
        }
    } catch (error) {
        console.error('Weather API Error:', error);
        showError('Network error. Please check your connection and try again.');
    }
}

async function autoDetectLocation() {
    showLoading();
    
    try {
        const response = await fetch('/api/location');
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('locationInput').value = result.location;
            // Automatically get weather for detected location
            setTimeout(() => {
                getWeather();
            }, 500);
        } else {
            hideLoading();
            showError('Could not detect your location automatically. Please enter your location manually.');
        }
    } catch (error) {
        console.error('Location Detection Error:', error);
        hideLoading();
        showError('Location detection failed. Please enter your location manually.');
    }
}

// Add some fun interactive features
function addInteractiveFeatures() {
    // Add hover effects to detail cards
    document.addEventListener('mouseover', function(e) {
        if (e.target.closest('.detail-card')) {
            e.target.closest('.detail-card').style.transform = 'translateY(-5px) scale(1.02)';
        }
    });
    
    document.addEventListener('mouseout', function(e) {
        if (e.target.closest('.detail-card')) {
            e.target.closest('.detail-card').style.transform = 'translateY(0) scale(1)';
        }
    });
}

// Initialize interactive features when DOM is loaded
document.addEventListener('DOMContentLoaded', addInteractiveFeatures);

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to search
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        getWeather();
    }
    
    // Ctrl/Cmd + L to focus location input
    if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
        e.preventDefault();
        document.getElementById('locationInput').focus();
    }
});

// Add weather tips based on conditions
function getWeatherTip(weatherData) {
    const temp = parseFloat(weatherData.temperature);
    const humidity = parseFloat(weatherData.humidity);
    const windSpeed = parseFloat(weatherData.wind_speed);
    
    let tips = [];
    
    if (temp < 0) {
        tips.push("🧥 It's freezing! Dress warmly and watch for icy conditions.");
    } else if (temp < 10) {
        tips.push("🧥 It's quite cold. Don't forget your jacket!");
    } else if (temp > 30) {
        tips.push("☀️ It's hot! Stay hydrated and seek shade when possible.");
    }
    
    if (humidity > 80) {
        tips.push("💧 High humidity today. It might feel warmer than it is.");
    }
    
    if (windSpeed > 10) {
        tips.push("💨 It's windy! Secure loose items and be careful outdoors.");
    }
    
    if (weatherData.description.toLowerCase().includes('rain')) {
        tips.push("☔ Don't forget your umbrella!");
    }
    
    return tips;
}

console.log('🌤️ Weather app JavaScript loaded and ready!');
