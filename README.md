# Backend Service for UTS Augmented Reality - Kelompok 8

Ini adalah layanan backend yang dibangun menggunakan Python dan Flask untuk mendukung aplikasi Augmented Reality (AR) dalam proyek UTS. Layanan ini berfungsi sebagai otak dari aplikasi, menerima data gambar dari aplikasi Unity, memprosesnya menggunakan model *Machine Learning*, dan mengembalikan hasil klasifikasi.

## Deskripsi Proyek

Tujuan utama dari layanan ini adalah menyediakan REST API yang mampu:
1.  Menerima *request* HTTP yang berisi gambar wajah dalam format Base64.
2.  Mengubah data Base64 kembali menjadi gambar.
3.  Melakukan pra-pemrosesan pada gambar agar sesuai dengan input model.
4.  Menjalankan inferensi menggunakan model TensorFlow untuk mengklasifikasikan gender.
5.  Mengirimkan kembali hasil prediksi dalam format JSON ke aplikasi Unity.

---

## Prasyarat

Sebelum memulai, pastikan perangkat Anda telah terinstal:
* **Python 3.10**
* `pip` (biasanya sudah terinstal bersama Python)
* `git`

---

## Panduan Setup Lokal

Ikuti langkah-langkah berikut untuk menjalankan server di mesin lokal Anda.

### 1. Clone Repositori
```bash
git clone [https://github.com/user/uts-kel-8-ar-backend.git](https://github.com/user/uts-kel-8-ar-backend.git)
cd uts-kel-8-ar-backend
```

### 2. Buat dan Aktifkan Virtual Environment (venv)

Sangat disarankan untuk menggunakan *virtual environment* agar dependensi proyek tidak tercampur dengan instalasi Python global Anda.

**Untuk Windows (Command Prompt atau PowerShell):**
```powershell
# Buat venv (pastikan Anda menggunakan interpreter Python 3.10)
py -3.10 -m venv venv

# Aktifkan venv
.\venv\Scripts\activate
```

**Untuk macOS / Linux:**
```bash
# Buat venv (pastikan Anda menggunakan interpreter Python 3.10)
python3.10 -m venv venv

# Aktifkan venv
source venv/bin/activate
```
Setelah aktif, Anda akan melihat `(venv)` di awal baris terminal Anda.

### 3. Instalasi Dependensi
Setelah *virtual environment* aktif, instal semua paket yang dibutuhkan dengan satu perintah:
```bash
pip install -r requirements.txt
```

### 4. Menjalankan Server
Untuk menjalankan server Flask secara lokal, gunakan perintah berikut:
```bash
flask run
```
Server akan berjalan secara default di `http://127.0.0.1:5000`.

---
## Struktur API

### Endpoint: `POST /classify`

* **Deskripsi:** Endpoint utama untuk klasifikasi gambar.
* **Request Body:**
    ```json
    {
        "image_data": "string_base64_dari_gambar_disini"
    }
    ```
* **Success Response (200 OK):**
    ```json
    {
        "prediction": "male",
        "confidence": 0.95
    }
    ```

---
## Cara Pengujian

Anda dapat menguji *endpoint* ini tanpa memerlukan aplikasi Unity dengan menggunakan *tools* seperti **Postman** atau **Insomnia**. Cukup kirim *request* `POST` ke URL server lokal Anda dengan *body* JSON yang sesuai.