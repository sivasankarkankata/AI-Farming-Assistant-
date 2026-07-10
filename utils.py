# utils.py
import re
import json
from datetime import datetime, timedelta
import random

def validate_image_file(filename):
    """Validate if the uploaded file is an image"""
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def format_date(date_str):
    """Format date string to readable format"""
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%d %B %Y')
    except:
        return date_str

def get_season_emoji(season):
    """Get emoji for season"""
    emojis = {
        'Summer': '☀️',
        'Winter': '❄️',
        'Monsoon': '🌧️',
        'Year-round': '🔄'
    }
    return emojis.get(season, '🌱')

def get_weather_icon(condition):
    """Get weather icon class"""
    icons = {
        'Sunny': 'fa-sun',
        'Partly Cloudy': 'fa-cloud-sun',
        'Rainy': 'fa-cloud-rain',
        'Cloudy': 'fa-cloud',
        'Thunderstorm': 'fa-bolt',
        'Snow': 'fa-snowflake',
        'Windy': 'fa-wind'
    }
    return icons.get(condition, 'fa-cloud')

def format_currency(amount):
    """Format amount in Indian Rupees"""
    return f"₹{amount:,.2f}"

def get_random_advice():
    """Get random farming advice"""
    advices = [
        "Water deeply and less frequently for stronger roots.",
        "Test soil pH every 6 months for optimal crop health.",
        "Rotate crops to prevent soil depletion and pest buildup.",
        "Use organic compost to improve soil structure.",
        "Monitor weather forecasts to plan irrigation schedules.",
        "Plant companion crops to naturally deter pests.",
        "Harvest early morning for best crop quality.",
        "Store seeds in cool, dry place for better germination."
    ]
    return random.choice(advices)

def crop_suitability_score(crop_data, soil_type, season, water):
    """Calculate crop suitability score"""
    score = 0
    if crop_data['soil_type'] == soil_type or soil_type == 'General':
        score += 2
    if crop_data['season'].lower() == season.lower() or season == 'Any':
        score += 2
    if crop_data['water_need'].lower() == water.lower() or water == 'Any':
        score += 1
    return score

# Data validation functions
def validate_soil_data(n, p, k, ph):
    """Validate soil nutrient values"""
    errors = []
    if not (0 <= n <= 100):
        errors.append("Nitrogen should be between 0 and 100")
    if not (0 <= p <= 100):
        errors.append("Phosphorus should be between 0 and 100")
    if not (0 <= k <= 100):
        errors.append("Potassium should be between 0 and 100")
    if not (0 <= ph <= 14):
        errors.append("pH should be between 0 and 14")
    return errors