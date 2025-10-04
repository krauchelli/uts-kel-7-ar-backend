# Backend Service for UTS Augmented Reality - Kelompok 7

**REST API untuk deteksi gender menggunakan deep learning model dengan Flask untuk aplikasi Augmented Reality (AR).**

Ini adalah layanan backend yang dibangun menggunakan Python dan Flask untuk mendukung aplikasi Augmented Reality (AR) dalam proyek UTS. Layanan ini berfungsi sebagai otak dari aplikasi, menerima data gambar dari aplikasi Unity, memprosesnya menggunakan model _Machine Learning_, dan mengembalikan hasil klasifikasi.

---

## Deskripsi Proyek

Tujuan utama dari layanan ini adalah menyediakan REST API yang mampu:

1. Menerima _request_ HTTP yang berisi gambar wajah dalam format Base64.
2. Mengubah data Base64 kembali menjadi gambar.
3. Melakukan pra-pemrosesan pada gambar agar sesuai dengan input model.
4. Menjalankan inferensi menggunakan model TensorFlow untuk mengklasifikasikan gender.
5. Mengirimkan kembali hasil prediksi dalam format JSON ke aplikasi Unity.

---

## Prasyarat

Sebelum memulai, pastikan perangkat Anda telah terinstal:

- **Python 3.10**
- `pip` (biasanya sudah terinstal bersama Python)
- `git`

---

## Setup dan Instalasi

### Opsi 1: Quick Setup (Disarankan)

```powershell
# Setup lengkap dan langsung jalankan aplikasi
.\quick_setup.bat
```

**Ini akan otomatis:**

1. Buat virtual environment
2. Install dependencies
3. Jalankan Flask app di http://localhost:5000

### Opsi 2: Setup Manual

```powershell
# 1. Setup environment
.\setup.bat

# 2. Jalankan aplikasi
.\run.bat
```

### Opsi 3: Setup Manual Virtual Environment

**Untuk Windows (Command Prompt atau PowerShell):**

```powershell
# Buat venv (pastikan Anda menggunakan interpreter Python 3.10)
py -3.10 -m venv venv

# Aktifkan venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Jalankan server
flask run
```

**Untuk macOS / Linux:**

```bash
# Buat venv (pastikan Anda menggunakan interpreter Python 3.10)
python3.10 -m venv venv

# Aktifkan venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Jalankan server
flask run
```

**Aplikasi akan berjalan di: `http://localhost:5000`**

---

## Setup dan Instalasi

### Opsi 1: Quick Setup (Recommended)

```powershell
# Setup lengkap dan langsung jalankan aplikasi
.\quick_setup.bat
```

**Ini akan otomatis:**

1. Buat virtual environment
2. Jalankan virtual environment
3. Install dependencies
4. Jalankan Flask app di http://localhost:5000

### Opsi 2: Manual Setup

```powershell
# 1. Setup environment
.\setup.bat

# 2. Jalankan aplikasi
.\run.bat
```

**Aplikasi akan berjalan di: `http://localhost:5000`**

---

## API Endpoints

### **1. POST `/api/predict` (Primary Endpoint)**

**Gender detection dari base64 image:**

**Request:**

```json
{
  "image_data": "base64_encoded_image_string"
}
```

**Response (Success):**

```json
{
  "prediction": "male",
  "confidence": 0.95
}
```

**Response (Error):**

```json
{
  "error": "No face detected in the image",
  "status": "error"
}
```

### **2. POST `/classify` (Unity Endpoint)**

**Endpoint khusus untuk aplikasi Unity:**

**Request:**

```json
{
  "image_data": "string_base64_dari_gambar_disini"
}
```

**Response (Success):**

```json
{
  "prediction": "male",
  "confidence": 0.95
}
```

### **3. GET `/health`**

**Check API status:**

**Response:**

```json
{
  "status": "healthy",
  "model_status": "loaded"
}
```

---

## Convert Image ke Base64

**Gunakan script converter:**

```python
# Convert gambar ke base64
python image_to_base64.py path/to/your/image.jpg
```

---

## Cara Pengujian

### Testing dengan Postman

Anda dapat menguji _endpoint_ ini tanpa memerlukan aplikasi Unity dengan menggunakan _tools_ seperti **Postman** atau **Insomnia**.

**Setup Request:**

1. **Method:** POST
2. **URL:** `http://localhost:5000/api/predict` atau `http://localhost:5000/classify`
3. **Headers:** `Content-Type: application/json`
4. **Body (raw JSON):**
   ```json
   {
     "image_data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
   }
   ```

### Testing dengan Unity

Kirim _request_ `POST` ke URL server lokal dengan _body_ JSON yang sesuai dari aplikasi Unity Anda.
