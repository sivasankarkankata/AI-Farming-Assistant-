# app.py - Complete Working Version
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
import random
from datetime import datetime, timedelta
import base64
from io import BytesIO
from PIL import Image
import traceback
import sys

app = Flask(__name__)
app.secret_key = 'farming_assistant_secret_key_2026'
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Complete Crop Database with all details
CROPS = {
    'wheat': {
        'name': 'Wheat',
        'soil_type': 'Loamy',
        'water_need': 'Moderate',
        'season': 'Winter',
        'yield': '4-5 tons/ha',
        'description': 'High-yield wheat variety suitable for temperate climates',
        'duration': '120-150 days',
        'temperature': '15-25°C',
        'profit': 'High'
    },
    'rice': {
        'name': 'Rice',
        'soil_type': 'Clay',
        'water_need': 'High',
        'season': 'Monsoon',
        'yield': '6-7 tons/ha',
        'description': 'Premium rice variety with excellent grain quality',
        'duration': '90-120 days',
        'temperature': '20-35°C',
        'profit': 'High'
    },
    'maize': {
        'name': 'Maize',
        'soil_type': 'Sandy Loam',
        'water_need': 'Moderate',
        'season': 'Summer',
        'yield': '8-9 tons/ha',
        'description': 'High-yield hybrid maize for grain and silage',
        'duration': '100-120 days',
        'temperature': '18-30°C',
        'profit': 'Medium'
    },
    'cotton': {
        'name': 'Cotton',
        'soil_type': 'Black',
        'water_need': 'Low',
        'season': 'Summer',
        'yield': '2-3 tons/ha',
        'description': 'Long-staple cotton variety with high fiber quality',
        'duration': '150-180 days',
        'temperature': '20-35°C',
        'profit': 'High'
    },
    'sugarcane': {
        'name': 'Sugarcane',
        'soil_type': 'Loamy',
        'water_need': 'High',
        'season': 'Year-round',
        'yield': '80-100 tons/ha',
        'description': 'High-sucrose sugarcane variety for sugar production',
        'duration': '300-365 days',
        'temperature': '20-35°C',
        'profit': 'High'
    },
    'tomato': {
        'name': 'Tomato',
        'soil_type': 'Sandy Loam',
        'water_need': 'Moderate',
        'season': 'Summer',
        'yield': '20-25 tons/ha',
        'description': 'Disease-resistant tomato variety with high yield',
        'duration': '60-80 days',
        'temperature': '18-27°C',
        'profit': 'High'
    },
    'potato': {
        'name': 'Potato',
        'soil_type': 'Sandy Loam',
        'water_need': 'Moderate',
        'season': 'Winter',
        'yield': '15-20 tons/ha',
        'description': 'High-yield potato variety with good storage quality',
        'duration': '90-120 days',
        'temperature': '15-20°C',
        'profit': 'Medium'
    },
    'onion': {
        'name': 'Onion',
        'soil_type': 'Loamy',
        'water_need': 'Low',
        'season': 'Winter',
        'yield': '12-15 tons/ha',
        'description': 'High-yield onion variety with good keeping quality',
        'duration': '100-120 days',
        'temperature': '13-25°C',
        'profit': 'Medium'
    },
    'soybean': {
        'name': 'Soybean',
        'soil_type': 'Loamy',
        'water_need': 'Moderate',
        'season': 'Summer',
        'yield': '2.5-3.5 tons/ha',
        'description': 'High-protein soybean variety for oil and meal',
        'duration': '90-120 days',
        'temperature': '20-30°C',
        'profit': 'Medium'
    },
    'groundnut': {
        'name': 'Groundnut',
        'soil_type': 'Sandy',
        'water_need': 'Low',
        'season': 'Summer',
        'yield': '1.5-2.5 tons/ha',
        'description': 'High-oil groundnut variety with good shelling percentage',
        'duration': '120-150 days',
        'temperature': '25-35°C',
        'profit': 'Medium'
    }
}

SOIL_TYPES = ['General', 'Loamy', 'Sandy', 'Clay', 'Sandy Loam', 'Black', 'Red', 'Laterite']
SEASONS = ['Any', 'Summer', 'Winter', 'Monsoon', 'Year-round']
WATER_NEEDS = ['Any', 'Low', 'Moderate', 'High']

def get_crop_recommendations(soil_type, season, water_availability):
    """
    Get crop recommendations based on soil type, season, and water availability
    """
    try:
        recommendations = []
        
        for crop_id, crop_data in CROPS.items():
            score = 0
            reasons = []
            match_criteria = []
            
            # Check soil type match
            if soil_type == 'General':
                score += 2
                reasons.append("Suitable for various soil types")
                match_criteria.append("Soil: Any")
            elif crop_data['soil_type'] == soil_type:
                score += 3
                reasons.append(f"Perfect match for {soil_type} soil")
                match_criteria.append(f"Soil: {soil_type}")
            else:
                score += 1
                reasons.append("Can adapt to different soils")
                match_criteria.append("Soil: Adaptable")
            
            # Check season match
            if season == 'Any':
                score += 2
                reasons.append("Can be grown in multiple seasons")
                match_criteria.append("Season: Any")
            elif crop_data['season'] == season:
                score += 3
                reasons.append(f"Optimal for {season} season")
                match_criteria.append(f"Season: {season}")
            else:
                score += 1
                reasons.append("Can be grown in different seasons")
                match_criteria.append("Season: Adaptable")
            
            # Check water availability
            if water_availability == 'Any':
                score += 2
                reasons.append("Adaptable water requirements")
                match_criteria.append("Water: Any")
            elif crop_data['water_need'] == water_availability:
                score += 3
                reasons.append(f"Matches {water_availability} water availability")
                match_criteria.append(f"Water: {water_availability}")
            else:
                score += 1
                reasons.append("Can adapt to different water conditions")
                match_criteria.append("Water: Adaptable")
            
            # Calculate match percentage
            match_percentage = min(100, int((score / 9) * 100))
            
            # Add to recommendations if score is good
            if score >= 4:
                recommendations.append({
                    'id': crop_id,
                    'name': crop_data['name'],
                    'soil_type': crop_data['soil_type'],
                    'water_need': crop_data['water_need'],
                    'season': crop_data['season'],
                    'yield': crop_data['yield'],
                    'description': crop_data['description'],
                    'duration': crop_data['duration'],
                    'temperature': crop_data['temperature'],
                    'profit': crop_data['profit'],
                    'score': score,
                    'reasons': reasons,
                    'match_criteria': match_criteria,
                    'match_percentage': match_percentage
                })
        
        # Sort by score (highest first)
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        # Return top 6 recommendations
        return recommendations[:6]
        
    except Exception as e:
        print(f"Error in crop recommendation: {str(e)}")
        print(traceback.format_exc())
        return []

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/crop-recommendation', methods=['GET', 'POST'])
def crop_recommendation():
    """Crop recommendation module"""
    recommendations = []
    selected_soil = 'General'
    selected_season = 'Any'
    selected_water = 'Any'
    error_message = None
    show_results = False
    
    if request.method == 'POST':
        try:
            # Get form data
            soil_type = request.form.get('soil_type', 'General')
            season = request.form.get('season', 'Any')
            water_availability = request.form.get('water_availability', 'Any')
            
            # Store selections for display
            selected_soil = soil_type
            selected_season = season
            selected_water = water_availability
            
            # Get recommendations
            recommendations = get_crop_recommendations(soil_type, season, water_availability)
            show_results = True
            
            if not recommendations:
                error_message = "No crops found matching your criteria. Try selecting 'General' or 'Any' for broader results."
                
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            print(f"Error: {traceback.format_exc()}")
    
    return render_template(
        'crop_recommendation.html',
        recommendations=recommendations,
        soil_types=SOIL_TYPES,
        seasons=SEASONS,
        water_needs=WATER_NEEDS,
        selected_soil=selected_soil,
        selected_season=selected_season,
        selected_water=selected_water,
        error_message=error_message,
        show_results=show_results
    )

@app.route('/weather-forecast')
def weather_forecast():
    location = request.args.get('location', 'Farm Location')
    forecast = get_weather_forecast(location)
    return render_template('weather_forecast.html', forecast=forecast, location=location)

@app.route('/soil-analysis', methods=['GET', 'POST'])
def soil_analysis():
    analysis = None
    if request.method == 'POST':
        try:
            nitrogen = float(request.form.get('nitrogen', 30))
            phosphorus = float(request.form.get('phosphorus', 20))
            potassium = float(request.form.get('potassium', 25))
            ph = float(request.form.get('ph', 6.5))
            analysis = analyze_soil(nitrogen, phosphorus, potassium, ph)
        except ValueError:
            analysis = {'status': 'Error', 'recommendations': ['Please enter valid numeric values']}
    return render_template('soil_analysis.html', analysis=analysis)

@app.route('/disease-detection', methods=['GET', 'POST'])
def disease_detection():
    result = None
    image_preview = None
    
    if request.method == 'POST':
        if 'plant_image' in request.files:
            file = request.files['plant_image']
            if file.filename != '':
                try:
                    img = Image.open(file.stream)
                    buffered = BytesIO()
                    img.save(buffered, format="JPEG")
                    image_preview = base64.b64encode(buffered.getvalue()).decode()
                    result = analyze_plant_image()
                except Exception as e:
                    result = {'error': f'Error processing image: {str(e)}'}
    
    return render_template('disease_detection.html', result=result, image_preview=image_preview)

@app.route('/irrigation-management', methods=['GET', 'POST'])
def irrigation_management():
    schedule = None
    if request.method == 'POST':
        try:
            soil_moisture = int(request.form.get('soil_moisture', 50))
            crop_type = request.form.get('crop_type', 'wheat')
            weather = request.form.get('weather', 'Normal')
            schedule = get_irrigation_schedule(soil_moisture, crop_type, weather)
        except ValueError:
            schedule = {'error': 'Please enter a valid moisture value'}
    return render_template('irrigation_management.html', schedule=schedule, crops=CROPS.keys())

@app.route('/market-prediction', methods=['GET', 'POST'])
def market_prediction():
    prediction = None
    if request.method == 'POST':
        crop = request.form.get('crop')
        if crop:
            prediction = get_market_prediction(crop)
    return render_template('market_prediction.html', prediction=prediction)

@app.route('/voice-assistant', methods=['GET', 'POST'])
def voice_assistant():
    response = None
    if request.method == 'POST':
        voice_input = request.form.get('voice_input', '')
        if voice_input:
            response = process_voice_command(voice_input)
    return render_template('voice_assistant.html', response=response)

# Helper functions
def get_weather_forecast(location=None):
    """Generate mock weather forecast"""
    today = datetime.now()
    forecast = []
    conditions = ['Sunny', 'Partly Cloudy', 'Rainy', 'Cloudy', 'Thunderstorm', 'Clear']
    for i in range(5):
        date = today + timedelta(days=i)
        temp = random.randint(15, 35)
        condition = random.choice(conditions)
        forecast.append({
            'date': date.strftime('%Y-%m-%d'),
            'day': date.strftime('%A'),
            'temp': temp,
            'condition': condition,
            'humidity': random.randint(40, 85),
            'wind_speed': random.randint(5, 25)
        })
    return forecast

def analyze_soil(nitrogen, phosphorus, potassium, ph):
    """Analyze soil nutrients and provide recommendations"""
    analysis = {
        'status': 'Good',
        'recommendations': [],
        'deficiencies': []
    }
    
    # Nitrogen analysis
    if nitrogen < 20:
        analysis['deficiencies'].append('Nitrogen')
        analysis['recommendations'].append('Apply nitrogen-rich fertilizer (Urea, DAP) at 50-60 kg/ha')
    elif nitrogen > 80:
        analysis['recommendations'].append('Reduce nitrogen application to prevent overgrowth')
    else:
        analysis['recommendations'].append('Nitrogen levels are optimal')
    
    # Phosphorus analysis
    if phosphorus < 10:
        analysis['deficiencies'].append('Phosphorus')
        analysis['recommendations'].append('Apply phosphorus fertilizer (Superphosphate) at 40-50 kg/ha')
    elif phosphorus > 50:
        analysis['recommendations'].append('Reduce phosphorus application')
    else:
        analysis['recommendations'].append('Phosphorus levels are optimal')
    
    # Potassium analysis
    if potassium < 15:
        analysis['deficiencies'].append('Potassium')
        analysis['recommendations'].append('Apply potassium fertilizer (MOP) at 30-40 kg/ha')
    elif potassium > 60:
        analysis['recommendations'].append('Reduce potassium application')
    else:
        analysis['recommendations'].append('Potassium levels are optimal')
    
    # pH analysis
    if ph < 5.5:
        analysis['recommendations'].append('Add lime (2-3 tons/ha) to increase soil pH')
        analysis['status'] = 'Needs Attention'
    elif ph > 7.5:
        analysis['recommendations'].append('Add sulfur (500-1000 kg/ha) to decrease soil pH')
        analysis['status'] = 'Needs Attention'
    elif 6.0 <= ph <= 7.0:
        analysis['recommendations'].append('Soil pH is ideal for most crops')
    
    # Overall status
    if not analysis['deficiencies']:
        if len(analysis['recommendations']) <= 3:
            analysis['status'] = 'Excellent'
    elif len(analysis['deficiencies']) >= 2:
        analysis['status'] = 'Poor'
    
    return analysis

def analyze_plant_image():
    """Mock plant disease detection"""
    diseases = {
        'aphids': {
            'name': 'Aphids', 
            'type': 'Pest', 
            'symptoms': 'Yellowing leaves, sticky residue, curled leaves', 
            'treatment': 'Apply neem oil (2 ml/L water) or insecticidal soap weekly'
        },
        'rust': {
            'name': 'Leaf Rust', 
            'type': 'Disease', 
            'symptoms': 'Orange-brown powdery spots on leaves', 
            'treatment': 'Apply fungicide (Propiconazole 0.05%) every 7-10 days'
        },
        'blight': {
            'name': 'Blight', 
            'type': 'Disease', 
            'symptoms': 'Brown to black spots, wilting leaves', 
            'treatment': 'Remove infected parts, apply copper-based fungicide every 7 days'
        },
        'mildew': {
            'name': 'Powdery Mildew', 
            'type': 'Disease', 
            'symptoms': 'White powdery coating on leaves', 
            'treatment': 'Apply sulfur spray (3g/L) or potassium bicarbonate solution'
        }
    }
    
    detected = random.choice(list(diseases.keys()))
    confidence = random.randint(75, 98)
    
    return {
        'detected': detected,
        'name': diseases[detected]['name'],
        'type': diseases[detected]['type'],
        'symptoms': diseases[detected]['symptoms'],
        'treatment': diseases[detected]['treatment'],
        'confidence': f"{confidence}%"
    }

def get_irrigation_schedule(soil_moisture, crop_type, weather):
    """Generate irrigation recommendations"""
    schedule = {
        'urgency': 'Normal',
        'recommendation': '',
        'water_amount': '',
        'frequency': '',
        'soil_moisture': soil_moisture
    }
    
    # Get crop water need
    crop_data = CROPS.get(crop_type.lower(), None)
    crop_water_need = crop_data['water_need'] if crop_data else 'Moderate'
    
    # Weather factor
    weather_factor = 1.0
    if weather == 'Hot':
        weather_factor = 1.5
    elif weather == 'Rainy':
        weather_factor = 0.5
    elif weather == 'Cold':
        weather_factor = 0.7
    elif weather == 'Windy':
        weather_factor = 1.3
    
    # Adjust thresholds based on crop water need
    if crop_water_need == 'High':
        threshold_critical = 30
        threshold_high = 50
        threshold_normal = 70
    elif crop_water_need == 'Low':
        threshold_critical = 15
        threshold_high = 35
        threshold_normal = 60
    else:  # Moderate
        threshold_critical = 25
        threshold_high = 45
        threshold_normal = 65
    
    # Calculate effective moisture
    effective_moisture = soil_moisture * weather_factor
    
    if effective_moisture < threshold_critical:
        schedule['urgency'] = 'Critical'
        schedule['recommendation'] = 'Immediate irrigation required - plant stress critical'
        schedule['water_amount'] = 'High (3-4 inches)'
        schedule['frequency'] = 'Daily until moisture improves'
    elif effective_moisture < threshold_high:
        schedule['urgency'] = 'High'
        schedule['recommendation'] = 'Irrigation needed within 24 hours'
        schedule['water_amount'] = 'Moderate (1-2 inches)'
        schedule['frequency'] = 'Every 2-3 days'
    elif effective_moisture < threshold_normal:
        schedule['urgency'] = 'Normal'
        schedule['recommendation'] = 'Maintain regular irrigation schedule'
        schedule['water_amount'] = 'Moderate (1-2 inches)'
        schedule['frequency'] = 'Every 3-4 days'
    else:
        schedule['urgency'] = 'Low'
        schedule['recommendation'] = 'Delay irrigation - optimal soil moisture'
        schedule['water_amount'] = 'Low (0.5-1 inch)'
        schedule['frequency'] = 'Weekly or as needed'
    
    return schedule

def get_market_prediction(crop):
    """Get market price prediction for crops"""
    market_prices = {
        'wheat': 2200,
        'rice': 2800,
        'maize': 1800,
        'cotton': 5500,
        'sugarcane': 3500,
        'tomato': 1200,
        'potato': 900,
        'onion': 1500,
        'soybean': 4000,
        'groundnut': 4500
    }
    
    if crop.lower() in market_prices:
        base_price = market_prices[crop.lower()]
        trend = random.choices(['Rising', 'Stable', 'Declining'], weights=[40, 35, 25])[0]
        trend_percent = random.randint(5, 20)
        
        if trend == 'Rising':
            predicted_price = base_price * (1 + trend_percent / 100)
        elif trend == 'Declining':
            predicted_price = base_price * (1 - trend_percent / 100)
        else:
            predicted_price = base_price
            trend_percent = random.randint(1, 5)
        
        return {
            'crop': crop,
            'current_price': base_price,
            'predicted_price': int(predicted_price),
            'trend': trend,
            'change_percent': trend_percent,
            'best_time': 'Next 2-3 weeks' if trend == 'Rising' else 'Wait for market recovery' if trend == 'Declining' else 'Current season',
            'suggestion': 'Sell now for best returns' if trend == 'Rising' else 'Hold and monitor market' if trend == 'Declining' else 'Sell as per regular schedule',
            'confidence': random.randint(70, 95)
        }
    return None

def process_voice_command(command):
    """Process voice commands with better responses"""
    command_lower = command.lower()
    
    # Weather commands
    if any(word in command_lower for word in ['weather', 'temperature', 'rain', 'sunny', 'cloud']):
        return "Today's weather is partly cloudy with temperature around 28°C. There's a 20% chance of rain. Perfect for farming activities."
    
    # Crop recommendation commands
    elif any(word in command_lower for word in ['crop', 'recommend', 'plant', 'grow', 'suggest']):
        recommendations = get_crop_recommendations('General', 'Any', 'Any')
        if recommendations:
            crop_names = [c['name'] for c in recommendations[:3]]
            return f"Based on general conditions, I recommend planting {', '.join(crop_names)}. These crops would perform well in your region."
        return "I recommend wheat or rice for your region. Both have good yield and market demand."
    
    # Disease commands
    elif any(word in command_lower for word in ['disease', 'pest', 'bug', 'infection', 'sick']):
        return "Please upload a photo of the affected plant for AI-powered disease detection. I can identify diseases like rust, blight, or mildew, and suggest organic treatments."
    
    # Irrigation commands
    elif any(word in command_lower for word in ['irrigation', 'water', 'moisture', 'irrigate']):
        return "Current soil moisture is at optimal levels. Maintain regular irrigation schedule of 2-3 days gap. Avoid overwatering to prevent root diseases."
    
    # Market commands
    elif any(word in command_lower for word in ['market', 'price', 'sell', 'profit', 'cost']):
        return "Current market prices: Wheat ₹2200/quintal, Rice ₹2800/quintal, Tomato ₹1200/quintal. Prices are showing an upward trend in the coming weeks."
    
    # General commands
    elif any(word in command_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm your AI Farming Assistant. How can I help you today? You can ask me about crops, weather, diseases, irrigation, or market prices."
    
    elif any(word in command_lower for word in ['help', 'support']):
        return "I can help you with crop recommendations, weather forecasts, disease detection, irrigation scheduling, and market predictions. Just tell me what you need!"
    
    else:
        return "I'm here to help you with farming! You can ask me about weather, crop recommendations, disease detection, irrigation, or market prices. Try saying 'crop recommendation' or 'weather'."

# API endpoints
@app.route('/api/weather')
def api_weather():
    location = request.args.get('location', 'Farm')
    return jsonify(get_weather_forecast(location))

@app.route('/api/crop-recommendation')
def api_crop_recommendation():
    soil = request.args.get('soil', 'General')
    season = request.args.get('season', 'Any')
    water = request.args.get('water', 'Any')
    return jsonify(get_crop_recommendations(soil, season, water))

@app.route('/api/market-prices')
def api_market_prices():
    market_prices = {
        'wheat': 2200,
        'rice': 2800,
        'maize': 1800,
        'cotton': 5500,
        'sugarcane': 3500,
        'tomato': 1200,
        'potato': 900,
        'onion': 1500,
        'soybean': 4000,
        'groundnut': 4500
    }
    return jsonify(market_prices)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
if __name__ == '__main__':
    # This works with ALL network configurations
    app.run(
        debug=True, 
        host='0.0.0.0',  # Allows connections from any device
        port=5000        # Standard port
    )