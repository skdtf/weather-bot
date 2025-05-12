from typing import Dict, Optional
from rapidfuzz import process

WEATHER_DATA: Dict[str, str] = {
    "New York": "Breezy, 15°C",
    "London": "Snowy, 23°C",
    "Paris": "Drizzly, 5°C",
    "Tokyo": "Windy, -10°C",
    "Delhi": "Windy, 20°C",
    "Mumbai": "Hot, 34°C",
    "Beijing": "Humid, 31°C",
    "Shanghai": "Foggy, 10°C",
    "Los Angeles": "Drizzly, 27°C",
    "Chicago": "Humid, 20°C",
    "Houston": "Foggy, 4°C",
    "Phoenix": "Humid, 26°C",
    "Philadelphia": "Sunny, 29°C",
    "San Antonio": "Humid, 25°C",
    "San Diego": "Stormy, 13°C",
    "Dallas": "Drizzly, 4°C",
    "San Jose": "Humid, -9°C",
    "Austin": "Hot, 31°C",
    "Jacksonville": "Rainy, 27°C",
    "Fort Worth": "Breezy, 17°C",
    "Columbus": "Rainy, -5°C",
    "San Francisco": "Breezy, 40°C",
    "Charlotte": "Drizzly, 22°C",
    "Indianapolis": "Sunny, 16°C",
    "Seattle": "Breezy, 36°C",
    "Denver": "Dry, 33°C",
    "Washington": "Hot, 34°C",
    "Boston": "Rainy, -10°C",
    "El Paso": "Dry, 40°C",
    "Nashville": "Breezy, 37°C",
    "Detroit": "Stormy, -1°C",
    "Oklahoma City": "Breezy, 17°C",
    "Portland": "Rainy, 13°C",
    "Las Vegas": "Dry, 13°C",
    "Memphis": "Breezy, 5°C",
    "Louisville": "Rainy, 3°C",
    "Baltimore": "Drizzly, -9°C",
    "Milwaukee": "Snowy, -5°C",
    "Albuquerque": "Snowy, 1°C",
    "Tucson": "Cold, 29°C",
    "Fresno": "Drizzly, 32°C",
    "Sacramento": "Hot, 14°C",
    "Kansas City": "Drizzly, 12°C",
    "Long Beach": "Hot, 2°C",
    "Mesa": "Sunny, 25°C",
    "Atlanta": "Cold, 13°C",
    "Colorado Springs": "Drizzly, 35°C",
    "Virginia Beach": "Foggy, 8°C",
    "Raleigh": "Foggy, 33°C",
    "Omaha": "Windy, 6°C",
    "Miami": "Rainy, 1°C",
    "Oakland": "Windy, 40°C",
    "Minneapolis": "Humid, -5°C",
    "Tulsa": "Snowy, 27°C",
    "Wichita": "Cloudy, 17°C",
    "New Orleans": "Sunny, 30°C",
    "Arlington": "Rainy, 10°C",
    "Cleveland": "Cloudy, 33°C",
    "Bakersfield": "Windy, -1°C",
    "Tampa": "Breezy, 7°C",
    "Aurora": "Humid, 14°C",
    "Honolulu": "Drizzly, 8°C",
    "Anaheim": "Snowy, 14°C",
    "Santa Ana": "Windy, 2°C",
    "Corpus Christi": "Cloudy, 36°C",
    "Riverside": "Rainy, 10°C",
    "Lexington": "Cloudy, 5°C",
    "St. Louis": "Cloudy, -7°C",
    "Stockton": "Snowy, 30°C",
    "Pittsburgh": "Stormy, -7°C",
    "Saint Paul": "Sunny, 14°C",
    "Cincinnati": "Drizzly, 23°C",
    "Anchorage": "Foggy, 17°C",
    "Henderson": "Foggy, -5°C",
    "Greensboro": "Cold, -8°C",
    "Plano": "Stormy, 4°C",
    "Newark": "Rainy, 12°C",
    "Lincoln": "Drizzly, 26°C",
    "Toledo": "Cold, 14°C",
    "Orlando": "Drizzly, -9°C",
    "Chula Vista": "Dry, 10°C",
    "Irvine": "Cold, 26°C",
    "Fort Wayne": "Rainy, 28°C",
    "Jersey City": "Cold, 16°C",
    "Durham": "Foggy, 15°C",
    "St. Petersburg": "Hot, 0°C",
    "Laredo": "Dry, 23°C",
    "Buffalo": "Cloudy, 19°C",
    "Madison": "Cold, 11°C",
    "Lubbock": "Humid, 5°C",
    "Chandler": "Dry, 34°C",
    "Scottsdale": "Hot, 29°C",
    "Reno": "Sunny, 6°C",
    "Glendale": "Foggy, 22°C",
    "Norfolk": "Windy, -9°C",
    "Winston–Salem": "Breezy, 30°C",
    "North Las Vegas": "Hot, 40°C",
    "Irving": "Foggy, 30°C",
    "Chesapeake": "Sunny, 17°C",
    "Gilbert": "Rainy, -7°C"
}

def normalize_city_name(city: str) -> str:
    return city.strip().title()

def get_closest_city(user_input: str, city_data: Dict[str, str]) -> Optional[str]:
    cities = list(city_data.keys())
    print(f'user_input: {user_input}')
    best_match, score, index = process.extractOne(user_input, cities)
    
    if score >= 80:
        return best_match
    else:
        return None

def get_weather(city: str) -> str:
    if not city:
        return "Please provide a city name."
    
    # Normalize the city name
    normalized_city = normalize_city_name(city)
    
    # Try exact match first
    if normalized_city in WEATHER_DATA:
        return WEATHER_DATA[normalized_city]
    
    # Try fuzzy matching
    closest_city = get_closest_city(normalized_city, WEATHER_DATA)
    if closest_city:
        return WEATHER_DATA[closest_city]
    
    return "Sorry, I don't have data for that city." 