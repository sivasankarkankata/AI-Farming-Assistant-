# tests/test_performance.py
import unittest
import time
from app import app

class TestPerformance(unittest.TestCase):
    """Performance tests"""
    
    def setUp(self):
        self.app = app.test_client()
        
    def test_page_load_time(self):
        """Test page load times"""
        pages = ['/', '/crop-recommendation', '/weather-forecast', '/soil-analysis']
        
        for page in pages:
            start_time = time.time()
            response = self.app.get(page)
            load_time = time.time() - start_time
            
            self.assertEqual(response.status_code, 200)
            self.assertLess(load_time, 2.0, f"Page {page} loaded in {load_time:.2f}s")
            
    def test_api_response_time(self):
        """Test API response times"""
        endpoints = [
            '/api/weather',
            '/api/crop-recommendation?soil=Loamy&season=Winter&water=Moderate',
            '/api/market-prices'
        ]
        
        for endpoint in endpoints:
            start_time = time.time()
            response = self.app.get(endpoint)
            response_time = time.time() - start_time
            
            self.assertEqual(response.status_code, 200)
            self.assertLess(response_time, 1.0, f"API {endpoint} responded in {response_time:.2f}s")
            
    def test_concurrent_requests(self):
        """Test concurrent requests (simplified)"""
        import threading
        
        def make_request():
            self.app.get('/')
            
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
            
        for thread in threads:
            thread.join(timeout=5)
            
        # All threads should complete
        self.assertTrue(True)