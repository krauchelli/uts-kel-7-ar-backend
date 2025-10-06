# --- Tahap 1: Build Environment ---
# Menggunakan image Python yang lebih lengkap untuk menginstal dependensi,
# termasuk yang mungkin memerlukan kompilasi.
FROM python:3.10-slim as builder

# Menentukan direktori kerja di dalam kontainer
WORKDIR /usr/src/app

# Mencegah Python menulis file .pyc untuk menjaga image tetap kecil
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Menginstal dependensi sistem yang mungkin dibutuhkan oleh OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Menyalin file requirements.txt terlebih dahulu untuk caching
COPY requirements.txt .

# Menginstal semua dependensi Python
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


# --- Tahap 2: Production Environment ---
# Menggunakan image Python yang sangat ringan untuk hasil akhir
FROM python:3.10-slim

# Menentukan direktori kerja
WORKDIR /usr/src/app

# Menyalin dependensi yang sudah di-build dari tahap sebelumnya
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app /usr/src/app

# Menginstal dependensi dari "wheels" tanpa perlu men-download ulang
RUN pip install --no-cache /wheels/*

# Menyalin seluruh kode aplikasi ke dalam direktori kerja
COPY . .

# Memberi tahu Docker bahwa kontainer akan berjalan di port 5000
EXPOSE 5000

# Perintah untuk menjalankan aplikasi saat kontainer dimulai
# Menggunakan gunicorn sebagai server produksi yang lebih tangguh daripada server bawaan Flask
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]