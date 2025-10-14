# 1️⃣ Base image
FROM python:3.10-slim

# 2️⃣ Çalışma dizini oluştur
WORKDIR /app

# 3️⃣ Gereksinimleri yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ Kodları kopyala
COPY . .

# 5️⃣ Flask uygulamasını başlat
CMD ["python", "app.py"]
