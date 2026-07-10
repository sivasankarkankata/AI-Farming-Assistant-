# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-2026'
    DEBUG = True
    TESTING = False
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.jpeg']
    
    # API keys (for real services)
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', '')
    MARKET_API_KEY = os.environ.get('MARKET_API_KEY', '')
    
    # Database (if needed)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///farming.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}