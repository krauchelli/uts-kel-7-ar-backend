from flask import Flask
from tensorflow.keras.models import load_model

# Definisikan variabel global untuk model
model = None

def create_app():
    """Application factory function."""
    global model
    
    app = Flask(__name__, template_folder='../templates')

    # Muat model saat startup
    try:
        # Gunakan path absolut untuk keamanan
        import os
        basedir = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.join(basedir, '..', 'model', 'model.h5')
        
        model = load_model(model_path)
        print("Model AI berhasil dimuat!")
    except Exception as e:
        print(f"ERROR: Gagal memuat model AI: {e}")

    # Registrasi Blueprints (rute)
    from . import routes
    app.register_blueprint(routes.bp)

    return app