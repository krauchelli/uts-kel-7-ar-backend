from flask import Flask
from tensorflow.keras.models import load_model
from config import model_path

model = None # Initialize model variable

def create_app():
    """Application factory function."""
    global model
    
    app = Flask(__name__, template_folder='../templates')

    # Load the AI model once when the app is created
    print("Loading Keras model...")
    model = load_model(model_path)
    print("Model loaded successfully.")

    # Register routes
    from . import routes
    app.register_blueprint(routes.bp)

    # Register error handlers (middleware)
    from . import middleware
    middleware.register_error_handlers(app)

    return app