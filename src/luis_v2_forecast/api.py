from .config import API_BASE_URL
from datetime import datetime, timedelta
import requests

def fetch_air_data(station: int, component: int, days: int) -> dict:
    """Get air data from the API"""
    try:

        data = {
            "station": station,
            "components": [component],
            "startDate": str((datetime.now() - timedelta(days=days)).date()),
            "endDate": str((datetime.now() - timedelta(days=1)).date()),
            "average": 1,
            "interpolate": False,
            "fileFormat": "json"
        }

        response = requests.post(API_BASE_URL + '/api/data', json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Data API-Error: {e}")
        return {}
    
def fetch_available_stations() -> dict:
    """Get available stations from the API"""
    try:
        response = requests.get(API_BASE_URL + '/api/station')
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Station API-Error: {e}")
        return {}
    
def fetch_available_components(station_id: int) -> dict:
    """Get available components from the API"""
    try:
        response = requests.get(API_BASE_URL + "/api/station/" + str(station_id) + '/component')
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Component API-Error: {e}")
        return {}