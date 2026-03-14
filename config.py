import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///youtube_filter.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # YouTube API
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    CLIENT_SECRETS_FILE = os.getenv('CLIENT_SECRETS_FILE', 'client_secret.json')
    
    # OAuth
    SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
    REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:5000/oauth2callback')
    
    # Security
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Video sync settings
    VIDEO_SYNC_MAX = int(os.getenv('VIDEO_SYNC_MAX', '1000'))  # Maximum videos to sync
    CACHE_DURATION_HOURS = int(os.getenv('CACHE_DURATION_HOURS', '24'))  # Cache duration


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    REDIRECT_URI = 'http://localhost:5000/oauth2callback'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # HTTPS için zorunlu
    # Production'da REDIRECT_URI environment variable'dan gelecek
    # ÖNEMLİ: Production'da OAUTHLIB_INSECURE_TRANSPORT tanımlı OLMAMALI veya 0 olmalı


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

