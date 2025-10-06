# Menggunakan image dasar Python 3.9 atau 3.10
FROM python:3.10-slim

# Menambahkan user non-root untuk keamanan (praktik terbaik)
RUN useradd -m -u 1000 user
USER user

# Mengatur environment variables
ENV PATH="/home/user/.local/bin:$PATH"
WORKDIR /app

# Menginstal dependensi sistem yang dibutuhkan oleh OpenCV
# Kita perlu beralih ke root sementara untuk instalasi ini
USER root
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0
USER user

# Salin file requirements dan instal dependensi
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Salin seluruh kode aplikasi
COPY --chown=user . /app

# Buka port 7860 sesuai syarat dari Hugging Face Spaces
EXPOSE 7860

# Perintah untuk menjalankan aplikasi saat kontainer dimulai
# Gunicorn akan menjalankan 'app' dari file 'run.py' di port 7860
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "run:app"]