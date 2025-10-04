# Layanan Backend untuk UTS Augmented Reality - Kelompok 7

Ini adalah layanan backend untuk proyek UTS Augmented Reality, dibangun dengan struktur Flask yang modular dan skalabel. Layanan ini menyediakan REST API yang berfungsi sebagai "otak" AI untuk aplikasi Unity, menangani pemrosesan gambar dan klasifikasi gender.

## ✨ Fitur

* **Arsitektur Modular**: Logika dipisahkan secara bersih ke dalam *routes*, *controllers*, dan *services*, terinspirasi dari pola *framework* web modern.
* **Konfigurasi Terpusat**: Semua parameter kunci seperti path model dan dimensi gambar dikelola dalam satu file `config.py`.
* **Penanganan Error yang Tangguh**: Mengimplementasikan *middleware* global untuk menangani error dari sisi klien (400) dan sisi server (500) dengan baik.
* **Fasilitas Pengujian Lengkap**: Menyertakan antarmuka web sederhana untuk pengujian mudah melalui unggah file atau webcam langsung.

---

## 📂 Struktur Proyek

Proyek ini menggunakan pola *application factory* untuk organisasi yang lebih baik:

```
uts-kel-7-ar-backend/
├── app/                  # Paket aplikasi utama
│   ├── __init__.py       # Menginisialisasi aplikasi Flask (App Factory)
│   ├── routes.py         # Mendefinisikan semua rute API dan halaman
│   ├── controllers.py    # Menangani logika request/response
│   ├── services.py       # Berisi logika bisnis inti (pemrosesan gambar, prediksi)
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
Gunakan perintah standar `flask run` untuk memulai server pengembangan. Titik masuknya ditangani oleh `run.py`.
```bash
flask run
```
Server akan berjalan, memuat model AI, dan akan tersedia di `http://12.0.0.1:5000`.

---

## 🧪 Pengujian API

Setelah server berjalan, Anda dapat mengujinya dengan beberapa cara:

* **Tes Webcam (Real-time):** Buka `http://127.0.0.1:5000/webcam` di browser Anda.
* **Tes Unggah File:** Buka `http://127.0.0.1:5000/` di browser Anda.
* **Postman:** Gunakan file `Gender_Detection_API.postman_collection.json` yang tersedia untuk mengirim *request* ke *endpoint* `/predict`.

### Endpoint API: `POST /predict`

* **Deskripsi:** *Endpoint* utama untuk klasifikasi gambar.
* **Request Body:**
    ```json
    {
        "image_data": "string_base64_gambar_anda"
    }
    ```
* **Respon Sukses (200 OK):**
    ```json
    {
        "success": true,
        "prediction": "male",
        "confidence": 0.95
    }
    ```