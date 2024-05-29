import requests
import requests_cache
from retrying import retry
from datetime import datetime

# Setup the session with caching and retry mechanism
requests_cache.install_cache('.cache', expire_after=3600)

@retry(stop_max_attempt_number=5, wait_exponential_multiplier=200)
def get_weather_data(url, params):
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Define the URL and parameters for the API request
url = "https://air-quality-api.open-meteo.com/v1/air-quality"
params = {
    "latitude": 36.7202,
    "longitude": -4.4203,
    "current": ["dust", "olive_pollen"],
    "hourly": ["pm10", "pm2_5", "olive_pollen"]
}

# Fetch the weather data
response = get_weather_data(url, params)

# Extract the necessary data from the response
current_data = response.get('current', {})
hourly_data = response.get('hourly', {})

# Function to classify levels
def classify_olive_pollen(value):
    if value is None:
        return "No Data"
    if value <= 30:
        return "Bajo"
    elif value <= 60:
        return "Moderado"
    elif value <= 120:
        return "Alto"
    else:
        return "Muy Alto"

def classify_pm10(value):
    if value <= 54:
        return "Bajo"
    elif value <= 154:
        return "Moderado"
    elif value <= 254:
        return "Alto"
    else:
        return "Muy Alto"

def classify_pm2_5(value):
    if value <= 12:
        return "Bajo"
    elif value <= 35:
        return "Moderado"
    elif value <= 55:
        return "Alto"
    else:
        return "Muy Alto"

# Get today's date in ISO 8601 format
today = datetime.utcnow().date()

# Filter hourly data for today
hourly_times = hourly_data.get('time', [])
hourly_pm10 = hourly_data.get('pm10', [])
hourly_pm2_5 = hourly_data.get('pm2_5', [])
hourly_olive_pollen = hourly_data.get('olive_pollen', [])

# Initialize an empty list to store the grouped data
grouped_data = []

# Group data in intervals of 4 hours
for i in range(0, len(hourly_times), 4):
    interval_times = hourly_times[i:i+4]
    interval_pm10 = hourly_pm10[i:i+4]
    interval_pm2_5 = hourly_pm2_5[i:i+4]
    interval_olive_pollen = hourly_olive_pollen[i:i+4]
    
    interval_start_date = datetime.fromisoformat(interval_times[0]).date()
    if interval_start_date == today:
        if any(pollen is not None for pollen in interval_olive_pollen):
            max_olive_pollen = max(filter(lambda x: x is not None, interval_olive_pollen))
            olive_pollen_level = classify_olive_pollen(max_olive_pollen)
        else:
            olive_pollen_level = "No Data"
        
        grouped_data.append({
            'start_time': interval_times[0],
            'end_time': interval_times[-1],
            'pm10': interval_pm10,
            'pm2_5': interval_pm2_5,
            'olive_pollen': interval_olive_pollen,
            'olive_pollen_level': olive_pollen_level
        })


def airQuality():
    print("\nGrouped data for today (in intervals of 4 hours):")
    for interval in grouped_data:
        interval_start = interval['start_time']
        interval_end = interval['end_time']
        olive_pollen_level = interval['olive_pollen_level']
        print(f"Interval: {interval_start} to {interval_end}, Olive pollen level: {olive_pollen_level}")
