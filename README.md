# 🐄 Sistem Tracing Produk Peternakan Halal

Sistem pelacakan produk peternakan halal berbasis blockchain untuk memastikan integritas dan kepatuhan halal dari peternak hingga konsumen.

## ✨ Fitur Utama

- **📝 Input Data**: Input data tahapan produk dengan QR code otomatis
- **🔍 Tracing Produk**: Lacak riwayat produk berdasarkan ID atau scan QR code
- **⛓️ Blockchain**: Verifikasi integritas data dengan teknologi blockchain
- **📊 Dashboard**: Statistik real-time dan tingkat kepatuhan halal
- **📱 QR Code**: Generate dan scan QR code dengan data lengkap

## 🚀 Instalasi

1. Clone repository ini
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```bash
   streamlit run app.py
   ```

## 📋 Requirements

- Python 3.8+
- Webcam (untuk scanning QR code)
- Browser modern

## 🛠️ Teknologi

- **Frontend**: Streamlit
- **Database**: CSV file
- **Blockchain**: Implementasi SHA-256
- **QR Code**: qrcode & pyzbar
- **Image Processing**: OpenCV & Pillow

## 📖 Cara Penggunaan

1. **Input Data**: Pilih tahap produk dan isi data yang diperlukan
2. **Generate QR**: Sistem otomatis generate QR code dengan data lengkap
3. **Tracing**: Scan QR atau input ID untuk melihat riwayat produk
4. **Verifikasi**: Cek status halal dan integritas blockchain

## 🔒 Keamanan

- Data tersimpan dalam format CSV dengan backup otomatis
- Blockchain memastikan data tidak dapat diubah tanpa deteksi
- QR code mengandung data terenkripsi untuk verifikasi

## 📈 Fitur Kepatuhan Halal

- Tracking sertifikasi halal per tahap
- Kalkulasi tingkat kepatuhan otomatis
- Alert untuk produk tidak patuh
- Dashboard compliance real-time

## 🤝 Kontribusi

Untuk pengembangan lebih lanjut atau pertanyaan, silakan hubungi tim pengembang.

## 📄 Lisensi

Sistem ini dikembangkan untuk keperluan traceability produk halal.