from flask import Blueprint, render_template
from . import controllers

# Using Blueprint is the Flask way to create modular route handlers
bp = Blueprint('main', __name__)

# --- API Routes ---
@bp.route('/predict', methods=['POST'])
def predict_route():
    return controllers.handle_prediction()

# --- Page Routes (for testing frontend) ---
@bp.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@bp.route('/webcam', methods=['GET'])
def webcam_page():
    return render_template('webcam.html')