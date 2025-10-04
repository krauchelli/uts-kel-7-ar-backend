import cv2
import numpy as np
from app import model # Impor model yang sudah dimuat dari __init__.py

def preprocess_face(face_img, target_size=(64, 64)):
    """Melakukan pra-pemrosesan pada gambar wajah untuk prediksi model."""
    # Ubah ukuran gambar
    face_img = cv2.resize(face_img, target_size)
    
    # Konversi ke RGB jika perlu
    if len(face_img.shape) == 3:
        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
    
    # Normalisasi nilai piksel
    face_img = face_img.astype('float32') / 255.0
    
    # Tambahkan dimensi batch
    face_img = np.expand_dims(face_img, axis=0)
    
    return face_img

def detect_faces(image_np):
    """Mendeteksi wajah pada gambar menggunakan OpenCV."""
    # Muat classifier cascade wajah
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Konversi ke grayscale untuk deteksi wajah
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    
    # Deteksi wajah
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    return faces

def predict_gender(face_img):
    """Memprediksi gender dari gambar wajah."""
    if model is None:
        raise RuntimeError("Model AI belum dimuat.")
    
    # Pra-pemrosesan wajah
    processed_face = preprocess_face(face_img)
    
    # Lakukan prediksi
    prediction = model.predict(processed_face)[0][0]
    
    # Konversi ke label gender
    if prediction > 0.5:
        gender = "Female"
        confidence = prediction
    else:
        gender = "Male"
        confidence = 1 - prediction
        
    return gender, float(confidence)