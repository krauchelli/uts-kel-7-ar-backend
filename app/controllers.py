from flask import request, jsonify
import base64
import io
from PIL import Image
import numpy as np
import cv2
from . import services

def handle_api_predict():
    """Controller untuk endpoint /api/predict yang dibutuhkan Unity."""
    try:
        data = request.get_json()
        if not data or 'image_data' not in data:
            return jsonify({'error': 'field image_data dibutuhkan'}), 400
        
        image_data = data['image_data']
        
        # Hapus prefix base64 jika ada
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]

        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        image_np = np.array(image)
        
        # Konversi RGB (dari PIL) ke BGR (untuk OpenCV)
        if len(image_np.shape) == 3 and image_np.shape[2] == 3:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        faces = services.detect_faces(image_np)
        
        if len(faces) == 0:
            return jsonify({'error': 'Tidak ada wajah yang terdeteksi'}), 400
            
        # Ambil wajah terbesar untuk diprediksi
        faces_with_area = [(face, face[2] * face[3]) for face in faces]
        faces_with_area.sort(key=lambda x: x[1], reverse=True)
        largest_face = faces_with_area[0][0]
        
        x, y, w, h = largest_face
        face_img = image_np[y:y+h, x:x+w]
        
        gender, confidence = services.predict_gender(face_img)
        
        if gender is None:
            return jsonify({'error': 'Gagal memprediksi gender'}), 500
            
        return jsonify({
            'prediction': gender.lower(),
            'confidence': round(confidence, 3)
        })

    except Exception as e:
        print(f"Internal server error: {e}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

# Anda bisa menambahkan controller lain untuk rute /upload dan /predict_base64 jika diperlukan