from flask import request, jsonify
import base64
import io
from PIL import Image
import numpy as np
import cv2
from . import services

def handle_api_predict():
    """Controller untuk endpoint /api/predict dengan logika yang benar dan format respon standar."""
    try:
        data = request.get_json()
        if not data or 'image_data' not in data:
            # Menggunakan abort untuk memicu error handler 400 secara eksplisit
            from flask import abort
            abort(400, description="Payload JSON harus berisi field 'image_data'.")
        
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
        
        # Panggil service untuk deteksi wajah
        faces = services.detect_faces(image_np)
        
        if len(faces) == 0:
            # Format respon error spesifik jika tidak ada wajah
            return jsonify({
                "statusCode": 400,
                "message": "Tidak ada wajah yang terdeteksi di dalam gambar.",
                "data": None
            }), 400
            
        # Ambil wajah terbesar untuk diprediksi
        faces_with_area = [(face, face[2] * face[3]) for face in faces]
        faces_with_area.sort(key=lambda x: x[1], reverse=True)
        largest_face = faces_with_area[0][0]
        
        x, y, w, h = largest_face
        face_img = image_np[y:y+h, x:x+w]
        
        # Panggil service untuk prediksi gender
        gender, confidence = services.predict_gender(face_img)
        
        if gender is None:
            # Ini adalah error server, jadi kita lemparkan agar ditangani middleware 500
            raise RuntimeError("Gagal memprediksi gender setelah wajah terdeteksi.")
            
        # Format respon sukses dengan struktur baru
        response = {
            "statusCode": 200,
            "message": "Prediksi berhasil dilakukan.",
            "data": {
                "prediction": gender.lower(),
                "confidence": round(confidence, 3)
            }
        }
        return jsonify(response), 200

    except Exception as e:
        # Semua error lain akan ditangkap di sini dan dilemparkan ke middleware 500
        print(f"Internal server error: {e}")
        raise e
    
    # --- Controller untuk rute /upload ---
def handle_upload():
    """Menangani upload gambar dari form HTML dan mengembalikan hasil deteksi lengkap."""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Tidak ada file gambar yang disediakan'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400

        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        image_np = np.array(image)
        
        # Konversi RGB ke BGR untuk OpenCV
        if len(image_np.shape) == 3 and image_np.shape[2] == 3:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        faces = services.detect_faces(image_np)
        
        results = []
        for (x, y, w, h) in faces:
            face_img = image_np[y:y+h, x:x+w]
            gender, confidence = services.predict_gender(face_img)
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
        return jsonify({'error': f'Error memproses gambar: {str(e)}'}), 500

# --- Controller untuk rute /predict_base64 ---
def handle_predict_base64():
    """Menangani data gambar base64 (biasanya dari webcam) dan mengembalikan hasil deteksi lengkap."""
    try:
        data = request.get_json()
        if 'image' not in data:
            return jsonify({'error': 'Tidak ada data gambar yang disediakan'}), 400
        
        image_data = data['image'].split(',')[1] # Hapus prefix
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        image_np = np.array(image)
        
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        faces = services.detect_faces(image_np)
        
        results = []
        for (x, y, w, h) in faces:
            face_img = image_np[y:y+h, x:x+w]
            gender, confidence = services.predict_gender(face_img)
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
        return jsonify({'error': f'Error memproses gambar: {str(e)}'}), 500