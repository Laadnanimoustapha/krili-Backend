import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'mysql-10c55d3e-linsovivo-e979.e.aivencloud.com')
    DB_PORT = int(os.getenv('DB_PORT', 16369))
    DB_USER = os.getenv('DB_USER', 'avnadmin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'AVNS_zu414cqfwi1ZzcSuSga')
    DB_NAME = os.getenv('DB_NAME', 'defaultdb')
    DB_SSL_DISABLED = False
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:3001').split(',')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
