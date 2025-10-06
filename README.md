# Layanan Backend untuk UTS Augmented Reality - Kelompok 7

Ini adalah layanan backend untuk proyek UTS Augmented Reality, dibangun dengan struktur Flask yang modular dan skalabel. Layanan ini menyediakan REST API yang berfungsi sebagai "otak" AI untuk aplikasi Unity, menangani deteksi wajah dan klasifikasi gender.

## ✨ Fitur

* **Arsitektur Modular**: Logika dipisahkan secara bersih ke dalam *routes*, *controllers*, dan *services*, terinspirasi dari pola *framework* web modern.
* **Logika AI Dua Tahap**: Mengimplementasikan alur kerja deteksi wajah terlebih dahulu menggunakan OpenCV, baru kemudian melakukan klasifikasi pada area wajah yang terdeteksi.
* **Penanganan Error Terpusat**: Menggunakan *middleware* global untuk menangani error dari sisi klien (400) dan sisi server (500) dengan format respons JSON yang konsisten.
* **Fasilitas Pengujian Lengkap**: Menyertakan antarmuka web sederhana untuk pengujian mudah melalui unggah file (`/`) dan webcam langsung (`/webcam`).

---

## 📂 Struktur Proyek

Proyek ini menggunakan pola *application factory* untuk organisasi yang lebih baik:

```
uts-kel-7-ar-backend/
├── app/                  # Paket aplikasi utama
│   ├── __init__.py       # Menginisialisasi aplikasi Flask (App Factory)
│   ├── routes.py         # Mendefinisikan semua rute API dan halaman
│   ├── controllers.py    # Menangani logika request/response
│   ├── services.py       # Berisi logika bisnis inti (deteksi, prediksi)
│   └── middleware.py     # Logika penanganan error global
├── config.py             # File konfigurasi terpusat
├── model/
│   └── model.h5          # Model Keras yang sudah dilatih
├── templates/            # File HTML untuk pengujian
├── run.py                # Titik masuk (entry point) untuk memulai server
└── requirements.txt      # Daftar dependensi Python
```

---

## 🚀 Memulai

Ikuti langkah-langkah berikut untuk melakukan setup dan menjalankan server di komputer lokal Anda.

### Prasyarat

* **Python 3.10**
* `pip` (manajer paket Python)
* `git`

### 1. Clone Repositori
```bash
git clone [https://github.com/your-username/uts-kel-7-ar-backend.git](https://github.com/your-username/uts-kel-7-ar-backend.git)
cd uts-kel-7-ar-backend
```

### 2. Buat dan Aktifkan Virtual Environment (venv)

Menggunakan *virtual environment* sangat penting untuk menjaga agar dependensi proyek tetap terisolasi.

**Untuk Windows (Command Prompt / PowerShell):**
```powershell
# Buat virtual environment
py -3.10 -m venv venv

# Aktifkan
.\venv\Scripts\activate
```

**Untuk macOS / Linux:**
```bash
# Buat virtual environment
python3.10 -m venv venv

# Aktifkan
source venv/bin/activate
```
*(Anda sekarang seharusnya melihat `(venv)` di awal baris terminal Anda.)*

### 3. Instalasi Dependensi
Dengan venv yang aktif, instal semua paket yang dibutuhkan dari `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Jalankan Server
Gunakan perintah standar `flask run` untuk memulai server pengembangan.
```bash
flask run
```
Server akan berjalan, memuat model AI, dan akan tersedia di `http://127.0.0.1:5000`.

---

## 🧪 Dokumentasi API

Berikut adalah daftar *endpoint* yang tersedia.

### Endpoint Utama untuk Unity

#### `POST /api/predict`
Endpoint ini dirancang khusus untuk aplikasi Unity dengan format respons yang disederhanakan.

* **Request Body:**
    ```json
    {
        "image_data": "string_base64_gambar_anda"
    }
    ```
* **Respon Sukses (200 OK):**
    ```json
    {
        "statusCode": 200,
        "message": "Prediksi berhasil dilakukan.",
        "data": {
            "prediction": "male",
            "confidence": 0.987
        }
    }
    ```

### Endpoint untuk Pengujian Internal

#### `POST /upload`
Menerima unggahan file gambar dari form HTML.

#### `POST /predict_base64`
Menerima data gambar Base64 dari *frontend tester* (webcam).

* **Respon (untuk `/upload` dan `/predict_base64`):**
    ```json
    {
        "success": true,
        "faces_detected": 1,
        "results": [
            {
                "gender": "Male",
                "confidence": 0.987,
                "bbox": {"x": 120, "y": 80, "width": 250, "height": 250}
            }
        ]
    }
    ```

---
title: Uts Kel 7 Ar Backend
emoji: 💻
colorFrom: indigo
colorTo: indigo
sdk: docker
pinned: false
short_description: backend service to serve AR project
---