import requests

def extract_weather_data():
    url = "https://api.open-meteo.com/v1/forecast?latitude=54.90&longitude=23.90&current_weather=true"
    response = requests.get(url)
    return response.json()