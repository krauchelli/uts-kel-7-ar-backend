import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    MODEL_PATH = 'model/model.h5'
    
    # Face detection settings
    FACE_CASCADE_PATH = None  # Will use default OpenCV cascade
    FACE_SCALE_FACTOR = 1.1
    FACE_MIN_NEIGHBORS = 4
    
    # Model preprocessing settings
    TARGET_IMAGE_SIZE = (64, 64)  # Adjust based on your model requirements
    
    # API settings
    MAX_FACES_PER_IMAGE = 10  # Limit number of faces to process

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Production-specific settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for production environment")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}