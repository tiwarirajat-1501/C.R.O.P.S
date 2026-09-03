"""
Weather Service module for C.R.O.P.S.
Provides live weather fetching via OpenWeatherMap API with realistic agronomic
offline presets for major agricultural hubs, ensuring flawless exhibition demos.
"""

import requests
from typing import Dict, Any, Optional

# Realistic agricultural regional climate profiles
# Tailored for demonstrations and offline fallback
REGIONAL_CLIMATE_PROFILES = {
    "Punjab (Ludhiana)": {
        "temperature": 28.5,
        "humidity": 62.0,
        "rainfall": 120.0,
        "description": "Semi-arid continental climate, optimal for wheat, maize, and cotton.",
        "state": "Punjab"
    },
    "Maharashtra (Nashik / Vidarbha)": {
        "temperature": 31.0,
        "humidity": 55.0,
        "rainfall": 85.0,
        "description": "Tropical wet-and-dry climate, suitable for grapes, onions, and pulses.",
        "state": "Maharashtra"
    },
    "Uttar Pradesh (Varanasi / Lucknow)": {
        "temperature": 29.0,
        "humidity": 70.0,
        "rainfall": 160.0,
        "description": "Humid subtropical Gangetic plains, ideal for rice, pulses, and sugarcane.",
        "state": "Uttar Pradesh"
    },
    "Karnataka (Bengaluru / Mandya)": {
        "temperature": 25.5,
        "humidity": 68.0,
        "rainfall": 110.0,
        "description": "Moderate plateau climate, ideal for coffee, maize, and fruit cultivation.",
        "state": "Karnataka"
    },
    "Andhra Pradesh (Guntur / Krishna)": {
        "temperature": 33.0,
        "humidity": 78.0,
        "rainfall": 140.0,
        "description": "Coastal deltaic climate, rich for rice, cotton, and blackgram.",
        "state": "Andhra Pradesh"
    },
    "West Bengal (Hooghly / Burdwan)": {
        "temperature": 29.5,
        "humidity": 84.0,
        "rainfall": 210.0,
        "description": "High humidity alluvial basin, excellent for rice, jute, and papaya.",
        "state": "West Bengal"
    },
    "Kerala (Wayanad / Palakkad)": {
        "temperature": 26.0,
        "humidity": 88.0,
        "rainfall": 250.0,
        "description": "Tropical monsoon rainforest belt, ideal for coconut, coffee, and banana.",
        "state": "Kerala"
    },
    "Gujarat (Anand / Saurashtra)": {
        "temperature": 32.5,
        "humidity": 50.0,
        "rainfall": 75.0,
        "description": "Arid to semi-arid, suitable for cotton, groundnut, and mothbeans.",
        "state": "Gujarat"
    },
    "California (Central Valley, USA)": {
        "temperature": 24.0,
        "humidity": 45.0,
        "rainfall": 60.0,
        "description": "Mediterranean climate with intensive irrigation, suitable for grapes and orange.",
        "state": "California"
    }
}

def get_weather(location_query: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch weather data for a given location or fallback to offline climate profile.
    
    Args:
        location_query: City or predefined region name.
        api_key: Optional OpenWeatherMap API key.
        
    Returns:
        dict: Weather attributes (temperature, humidity, rainfall, description, is_live, source).
    """
    # Check if exact match in regional profiles
    if location_query in REGIONAL_CLIMATE_PROFILES and not api_key:
        profile = REGIONAL_CLIMATE_PROFILES[location_query]
        return {
            "region": location_query,
            "temperature": profile["temperature"],
            "humidity": profile["humidity"],
            "rainfall": profile["rainfall"],
            "description": profile["description"],
            "is_live": False,
            "source": f"Agronomic Climate Database ({profile['state']})"
        }
    
    # Try Live OpenWeatherMap API if key is supplied
    if api_key and api_key.strip():
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": location_query,
                "appid": api_key.strip(),
                "units": "metric"
            }
            resp = requests.get(url, params=params, timeout=4)
            if resp.status_code == 200:
                data = resp.json()
                temp = float(data["main"]["temp"])
                humidity = float(data["main"]["humidity"])
                
                # Estimate 24h rainfall or default to typical value
                rainfall = 100.0
                if "rain" in data:
                    rainfall = float(data["rain"].get("1h", data["rain"].get("3h", 10.0)) * 10)
                
                desc = data["weather"][0]["description"].capitalize()
                return {
                    "region": f"{data.get('name', location_query)}, {data.get('sys', {}).get('country', '')}",
                    "temperature": round(temp, 1),
                    "humidity": round(humidity, 1),
                    "rainfall": round(rainfall, 1),
                    "description": f"Live Weather: {desc}",
                    "is_live": True,
                    "source": "OpenWeatherMap Live API"
                }
        except Exception:
            pass  # Fall back to matching profile or general default

    # Fuzzy match or fallback
    for name, prof in REGIONAL_CLIMATE_PROFILES.items():
        if location_query.lower() in name.lower() or name.lower() in location_query.lower():
            return {
                "region": name,
                "temperature": prof["temperature"],
                "humidity": prof["humidity"],
                "rainfall": prof["rainfall"],
                "description": prof["description"],
                "is_live": False,
                "source": f"Agronomic Climate Database ({prof['state']})"
            }

    # Generic realistic fallback
    return {
        "region": location_query,
        "temperature": 27.0,
        "humidity": 65.0,
        "rainfall": 115.0,
        "description": "Standard temperate-subtropical climate profile.",
        "is_live": False,
        "source": "Default Agricultural Baseline"
    }

def get_available_regions():
    """Return list of predefined exhibition regions."""
    return list(REGIONAL_CLIMATE_PROFILES.keys())
