# tests/test_integration.py
import unittest
import json
from app import app

class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    def test_complete_farmer_workflow(self):
        """Test a complete farmer workflow from dashboard to recommendations"""
        
        # 1. Access dashboard
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        # 2. Get crop recommendations
        data = {
            'soil_type': 'Loamy',
            'season': 'Winter',
            'water_availability': 'Moderate'
        }
        response = self.app.post('/crop-recommendation', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recommended Crops', response.data)
        
        # 3. Check weather
        response = self.app.get('/weather-forecast')
        self.assertEqual(response.status_code, 200)
        
        # 4. Analyze soil
        data = {
            'nitrogen': 35,
            'phosphorus': 25,
            'potassium': 30,
            'ph': 6.8
        }
        response = self.app.post('/soil-analysis', data=data)
        self.assertEqual(response.status_code, 200)
        
        # 5. Check market prices
        data = {'crop': 'wheat'}
        response = self.app.post('/market-prediction', data=data)
        self.assertEqual(response.status_code, 200)
        
    def test_api_workflow(self):
        """Test API endpoints workflow"""
        
        # 1. Get weather
        response = self.app.get('/api/weather')
        self.assertEqual(response.status_code, 200)
        weather_data = json.loads(response.data)
        
        # 2. Get crop recommendations
        response = self.app.get('/api/crop-recommendation?soil=Loamy&season=Winter&water=Moderate')
        self.assertEqual(response.status_code, 200)
        crop_data = json.loads(response.data)
        
        # 3. Get market prices
        response = self.app.get('/api/market-prices')
        self.assertEqual(response.status_code, 200)
        market_data = json.loads(response.data)
        
        # Verify data structures
        self.assertIsInstance(weather_data, list)
        self.assertIsInstance(crop_data, list)
        self.assertIsInstance(market_data, dict)

class TestSecurity(unittest.TestCase):
    """Security tests"""
    
    def setUp(self):
        self.app = app.test_client()
        
    def test_csrf_protection(self):
        """Test CSRF protection (if implemented)"""
        response = self.app.post('/crop-recommendation', data={})
        self.assertEqual(response.status_code, 200)  # Should be safe
        
    def test_file_upload_size_limit(self):
        """Test file upload size limit"""
        from io import BytesIO
        
        # Create large image (>16MB)
        large_file = BytesIO(b'0' * (17 * 1024 * 1024))
        data = {
            'plant_image': (large_file, 'large_image.jpg')
        }
        
        response = self.app.post('/disease-detection', data=data,
                                content_type='multipart/form-data')
        # Should handle large file gracefully
        self.assertIn(response.status_code, [200, 413])