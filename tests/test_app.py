# tests/test_app.py
import unittest
import json
import os
import sys
from io import BytesIO
from PIL import Image
from flask import Flask

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestFarmingAssistant(unittest.TestCase):
    """Test cases for AI Personal Farming Assistant"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
        self.app.secret_key = 'test_secret_key'
        
    def test_home_page(self):
        """Test home page loads successfully"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AI Personal Farming Assistant', response.data)
        
    def test_crop_recommendation_page(self):
        """Test crop recommendation page"""
        response = self.app.get('/crop-recommendation')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Crop Recommendation', response.data)
        
    def test_crop_recommendation_post(self):
        """Test crop recommendation form submission"""
        data = {
            'soil_type': 'Loamy',
            'season': 'Winter',
            'water_availability': 'Moderate'
        }
        response = self.app.post('/crop-recommendation', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recommended Crops', response.data)
        
    def test_weather_forecast_page(self):
        """Test weather forecast page"""
        response = self.app.get('/weather-forecast')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Weather Forecast', response.data)
        
    def test_soil_analysis_page(self):
        """Test soil analysis page"""
        response = self.app.get('/soil-analysis')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Soil Analysis', response.data)
        
    def test_soil_analysis_post(self):
        """Test soil analysis form submission"""
        data = {
            'nitrogen': 30,
            'phosphorus': 20,
            'potassium': 25,
            'ph': 6.5
        }
        response = self.app.post('/soil-analysis', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Analysis Results', response.data)
        
    def test_disease_detection_page(self):
        """Test disease detection page"""
        response = self.app.get('/disease-detection')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Disease', response.data)
        
    def test_disease_detection_post(self):
        """Test disease detection with image upload"""
        # Create test image
        img = Image.new('RGB', (100, 100), color='red')
        img_io = BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        
        data = {
            'plant_image': (img_io, 'test_plant.jpg')
        }
        response = self.app.post('/disease-detection', data=data, 
                                content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        
    def test_irrigation_management_page(self):
        """Test irrigation management page"""
        response = self.app.get('/irrigation-management')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Irrigation', response.data)
        
    def test_irrigation_management_post(self):
        """Test irrigation management form submission"""
        data = {
            'soil_moisture': 50,
            'crop_type': 'wheat',
            'weather': 'Normal'
        }
        response = self.app.post('/irrigation-management', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Irrigation Schedule', response.data)
        
    def test_market_prediction_page(self):
        """Test market prediction page"""
        response = self.app.get('/market-prediction')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Market', response.data)
        
    def test_market_prediction_post(self):
        """Test market prediction form submission"""
        data = {'crop': 'wheat'}
        response = self.app.post('/market-prediction', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Market Analysis', response.data)
        
    def test_voice_assistant_page(self):
        """Test voice assistant page"""
        response = self.app.get('/voice-assistant')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Voice Assistant', response.data)
        
    def test_voice_assistant_post(self):
        """Test voice assistant form submission"""
        data = {'voice_input': 'What is the weather today?'}
        response = self.app.post('/voice-assistant', data=data)
        self.assertEqual(response.status_code, 200)
        
    def test_api_weather(self):
        """Test weather API endpoint"""
        response = self.app.get('/api/weather')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('date', data[0])
        self.assertIn('temp', data[0])
        
    def test_api_crop_recommendation(self):
        """Test crop recommendation API endpoint"""
        response = self.app.get('/api/crop-recommendation?soil=Loamy&season=Winter&water=Moderate')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        
    def test_api_market_prices(self):
        """Test market prices API endpoint"""
        response = self.app.get('/api/market-prices')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('wheat', data)
        self.assertIn('rice', data)
        
    def test_404_page(self):
        """Test 404 page for non-existent route"""
        response = self.app.get('/non-existent-page')
        self.assertEqual(response.status_code, 404)

class TestUtils(unittest.TestCase):
    """Test utility functions"""
    
    def test_validate_image_file(self):
        """Test image file validation"""
        from utils import validate_image_file
        self.assertTrue(validate_image_file('photo.jpg'))
        self.assertTrue(validate_image_file('image.png'))
        self.assertFalse(validate_image_file('document.pdf'))
        self.assertFalse(validate_image_file('file.exe'))
        
    def test_format_date(self):
        """Test date formatting"""
        from utils import format_date
        result = format_date('2026-01-15')
        self.assertIn('January', result)
        self.assertIn('2026', result)
        
    def test_get_season_emoji(self):
        """Test season emoji function"""
        from utils import get_season_emoji
        self.assertEqual(get_season_emoji('Summer'), '☀️')
        self.assertEqual(get_season_emoji('Winter'), '❄️')
        self.assertEqual(get_season_emoji('Monsoon'), '🌧️')
        
    def test_format_currency(self):
        """Test currency formatting"""
        from utils import format_currency
        self.assertEqual(format_currency(1000), '₹1,000.00')
        self.assertEqual(format_currency(2500.50), '₹2,500.50')

class TestModels(unittest.TestCase):
    """Test database models (if SQLAlchemy is configured)"""
    
    def setUp(self):
        """Set up test database"""
        from models import db
        self.db = db
        
    def test_user_model(self):
        """Test user model creation"""
        from models import User
        user = User(username='testuser', email='test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')

if __name__ == '__main__':
    # Run with coverage if available
    try:
        import coverage
        cov = coverage.Coverage()
        cov.start()
        
        unittest.main()
        
        cov.stop()
        cov.save()
        cov.report()
    except:
        unittest.main()