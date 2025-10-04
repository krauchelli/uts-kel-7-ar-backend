from flask import Blueprint, render_template, jsonify
from . import controllers

bp = Blueprint('main', __name__)

# Rute untuk frontend pengujian
@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/webcam')
def webcam():
    return render_template('webcam.html')

# Rute API Utama untuk Unity
@bp.route('/api/predict', methods=['POST'])
def api_predict_route():
    return controllers.handle_api_predict()

# Rute API lain dari file asli (bisa diimplementasikan controllernya jika perlu)
@bp.route('/upload', methods=['POST'])
def upload_route():
    # Logika untuk handle_upload()
    pass

@bp.route('/predict_base64', methods=['POST'])
def predict_base64_route():
    # Logika untuk handle_predict_base64()
    pass

# Rute untuk health check
@bp.route('/health')
def health_check():
    from . import model
    model_status = "loaded" if model is not None else "not_loaded"
    response = {
        "statusCode": 200,
        "message": "Server is healthy.",
        "data": {
            "status": "healthy",
            "model_status": model_status
        }
    }
    return jsonify(response), 200