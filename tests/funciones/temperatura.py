import openmeteo_requests
import requests_cache
from retry_requests import retry
from datetime import datetime, timedelta

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

def obtener_temperatura_por_intervalo(url, params, intervalo_horas=5):
    # Llamada a la API
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # Verificar que la respuesta contiene datos horarios
    if not hasattr(response, 'Hourly') or response.Hourly() is None:
        print("Error: No se encontraron datos horarios en la respuesta de la API")
        return

    hourly = response.Hourly()
    if hourly is None or not hasattr(hourly, 'Variables') or hourly.Variables(0) is None:
        print("Error: No se encontraron datos horarios en la respuesta de la API")
        return

    hourly_temperature = hourly.Variables(0).ValuesAsNumpy()

    # Verificar si hourly.Time() es una lista o un solo valor
    times = hourly.Time()
    if isinstance(times, int):
        times = [times]  # Convertir un solo valor en una lista
    elif not isinstance(times, list):
        print("Error: Formato de tiempo inesperado en la respuesta de la API")
        return

    # Convertir los tiempos desde el formato string a datetime
    times = [datetime.utcfromtimestamp(t) for t in times]

    # Filtrar los datos solo para el día actual
    today = datetime.utcnow().date()
    temperatures_today = [(time, temp) for time, temp in zip(times, hourly_temperature) if time.date() == today]

    if not temperatures_today:
        print("No hay datos para el día actual")
        return

    # Redondear los tiempos al inicio del intervalo y agrupar
    intervalos = {}
    for time, temp in temperatures_today:
        intervalo_inicio = time.replace(minute=0, second=0, microsecond=0)
        intervalo_inicio -= timedelta(hours=intervalo_inicio.hour % intervalo_horas)
        if intervalo_inicio not in intervalos:
            intervalos[intervalo_inicio] = []
        intervalos[intervalo_inicio].append(temp)

    # Calcular la temperatura media, mínima y máxima por intervalo e imprimir resultados
    for intervalo_inicio, temperaturas in sorted(intervalos.items()):
        intervalo_fin = intervalo_inicio + timedelta(hours=intervalo_horas)
        temperatura_media = sum(temperaturas) / len(temperaturas)
        temperatura_min = min(temperaturas)
        temperatura_max = max(temperaturas)
        print(f"Intervalo: {intervalo_inicio} a {intervalo_fin}")
        print(f"  Temperatura media: {temperatura_media:.2f} °C")
        print(f"  Temperatura mínima: {temperatura_min:.2f} °C")
        print(f"  Temperatura máxima: {temperatura_max:.2f} °C")

# Parámetros para la API
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 36.7202,
    "longitude": -4.4203,
    "hourly": "temperature_2m"
}

# Obtener e imprimir la temperatura media, mínima y máxima por intervalos de 5 horas
obtener_temperatura_por_intervalo(url, params)
