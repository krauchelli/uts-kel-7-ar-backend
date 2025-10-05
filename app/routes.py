from flask import Blueprint, render_template, jsonify
from . import controllers

bp = Blueprint('main', __name__)

# --- Rute Halaman (untuk frontend pengujian) ---
@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/webcam')
def webcam():
    return render_template('webcam.html')

# --- Rute API ---

@bp.route('/upload', methods=['POST'])
def upload_route():
    """Rute untuk menangani upload file dari form."""
    return controllers.handle_upload()

@bp.route('/predict_base64', methods=['POST'])
def predict_base64_route():
    """Rute untuk menangani prediksi dari data base64 (webcam)."""
    return controllers.handle_predict_base64()

@bp.route('/api/predict', methods=['POST'])
def api_predict_route():
    """Rute utama untuk client Unity dengan respon sederhana."""
    return controllers.handle_api_predict()

@bp.route('/health')
def health_check():
    """Rute untuk memeriksa kesehatan server dan status model."""
    from . import model
    model_status = "loaded" if model is not None else "not_loaded"
    response = {"statusCode": 200, "message": "Server is healthy.", "data": {"status": "healthy", "model_status": model_status}}
    return jsonify(response), 200