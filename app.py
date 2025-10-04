from flask import Flask, render_template, request, jsonify, Response
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import base64
import io
from PIL import Image
import os

app = Flask(__name__)

# Load the model
MODEL_PATH = 'model/model.h5'
model = None

def load_gender_model():
    """Load the gender detection model"""
    global model
    try:
        model = load_model(MODEL_PATH)
        print("Model loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def preprocess_face(face_img, target_size=(64, 64)):
    """Preprocess face image for model prediction"""
    # Resize image
    face_img = cv2.resize(face_img, target_size)
    
    # Convert to RGB if needed
    if len(face_img.shape) == 3:
        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
    
    # Normalize pixel values
    face_img = face_img.astype('float32') / 255.0
    
    # Add batch dimension
    face_img = np.expand_dims(face_img, axis=0)
    
    return face_img

def detect_faces(image):
    """Detect faces in image using OpenCV"""
    # Load face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    return faces

def predict_gender(face_img):
    """Predict gender from face image"""
    if model is None:
        return None, 0.0
    
    try:
        # Preprocess the face
        processed_face = preprocess_face(face_img)
        
        # Make prediction
        prediction = model.predict(processed_face)[0][0]
        
        # Convert to gender label
        if prediction > 0.5:
            gender = "Female"
            confidence = prediction
        else:
            gender = "Male" 
            confidence = 1 - prediction
            
        return gender, float(confidence)
    except Exception as e:
        print(f"Error in prediction: {e}")
        return None, 0.0

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload and predict gender"""
    try:
        # Check if image is provided
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Read image
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        image_np = np.array(image)
        
        # Convert PIL RGB to OpenCV BGR if needed
        if len(image_np.shape) == 3 and image_np.shape[2] == 3:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        # Detect faces
        faces = detect_faces(image_np)
        
        if len(faces) == 0:
            return jsonify({'error': 'No face detected in the image'}), 400
        
        results = []
        
        # Process each detected face
        for (x, y, w, h) in faces:
            # Extract face region
            face_img = image_np[y:y+h, x:x+w]
            
            # Predict gender
            gender, confidence = predict_gender(face_img)
            
            if gender:
                results.append({
                    'gender': gender,
                    'confidence': confidence,
                    'bbox': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)}
                })
        
        return jsonify({
            'success': True,
            'faces_detected': len(faces),
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

@app.route('/webcam')
def webcam():
    """Webcam page"""
    return render_template('webcam.html')

@app.route('/predict_base64', methods=['POST'])
def predict_base64():
    """Handle base64 image from webcam"""
    try:
        data = request.get_json()
        
        if 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Decode base64 image
        image_data = data['image'].split(',')[1]  # Remove data:image/jpeg;base64,
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        image_np = np.array(image)
        
        # Convert RGB to BGR for OpenCV
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        # Detect faces
        faces = detect_faces(image_np)
        
        results = []
        
        # Process each detected face
        for (x, y, w, h) in faces:
            # Extract face region
            face_img = image_np[y:y+h, x:x+w]
            
            # Predict gender
            gender, confidence = predict_gender(face_img)
            
            if gender:
                results.append({
                    'gender': gender,
                    'confidence': confidence,
                    'bbox': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)}
                })
        
        return jsonify({
            'success': True,
            'faces_detected': len(faces),
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    API endpoint for gender prediction with simplified response format
    Request Body: { "image_data": "base64_string" }
    Response Body: { "prediction": "male/female", "confidence": 0.95 }
    """
    try:
        data = request.get_json()
        
        if not data or 'image_data' not in data:
            return jsonify({'error': 'image_data field is required'}), 400
        
        image_data = data['image_data']
        
        # Handle different base64 formats
        if image_data.startswith('data:image'):
            # Remove data URL prefix if present
            image_data = image_data.split(',')[1]
        
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(image)
        except Exception as e:
            return jsonify({'error': 'Invalid base64 image data'}), 400
        
        # Convert RGB to BGR for OpenCV if needed
        if len(image_np.shape) == 3 and image_np.shape[2] == 3:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        # Detect faces
        faces = detect_faces(image_np)
        
        if len(faces) == 0:
            return jsonify({'error': 'No face detected in the image'}), 400
        
        # Get the first (largest) face for prediction
        # Sort faces by area (width * height) and take the largest
        faces_with_area = [(face, face[2] * face[3]) for face in faces]
        faces_with_area.sort(key=lambda x: x[1], reverse=True)
        largest_face = faces_with_area[0][0]
        
        x, y, w, h = largest_face
        face_img = image_np[y:y+h, x:x+w]
        
        # Predict gender
        gender, confidence = predict_gender(face_img)
        
        if gender is None:
            return jsonify({'error': 'Failed to predict gender'}), 500
        
        # Format response according to requirements
        prediction = gender.lower()  # Convert to lowercase (male/female)
        
        return jsonify({
            'prediction': prediction,
            'confidence': round(confidence, 3)
        })
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    model_status = "loaded" if model is not None else "not_loaded"
    return jsonify({
        'status': 'healthy',
        'model_status': model_status
    })

if __name__ == '__main__':
    # Load model on startup
    if load_gender_model():
        print("Starting Flask app...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Failed to load model. Please check the model file.")