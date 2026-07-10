# run_tests.py
#!/usr/bin/env python
"""Test runner for AI Personal Farming Assistant"""

import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_all_tests():
    """Run all test suites"""
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_specific_test(test_module):
    """Run specific test module"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(f'tests.{test_module}')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run tests for AI Farming Assistant')
    parser.add_argument('--test', type=str, help='Specific test module to run')
    parser.add_argument('--coverage', action='store_true', help='Run with coverage')
    
    args = parser.parse_args()
    
    if args.coverage:
        try:
            import coverage
            cov = coverage.Coverage()
            cov.start()
            
            success = run_all_tests()
            
            cov.stop()
            cov.save()
            cov.report()
        except ImportError:
            print("Coverage package not installed. Run: pip install coverage")
            success = run_all_tests()
    elif args.test:
        success = run_specific_test(args.test)
    else:
        success = run_all_tests()
    
    sys.exit(0 if success else 1)