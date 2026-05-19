# 📊 Capstone Project - Dashboard Analisis Pendidikan Indonesia

Dashboard Streamlit gabungan untuk 2 pertanyaan bisnis tentang pendidikan di Indonesia.

## 🎯 Pertanyaan Bisnis

### **Pertanyaan Satu: Estimasi Pelajar yang Dapat Dijangkau (3-6 Bulan)**
- **Tujuan**: Menjawab berapa banyak pelajar yang dapat dijangkau untuk menjadi pengguna platform dalam 3-6 bulan
- **Metrik Utama**: 
  - Pelajar aktif (total - putus sekolah)
  - Akses telepon seluler
  - Akses internet
  - Sinyal 4G/5G/LTE
- **Output**: 9 visualisasi (bar charts, heatmaps, scatter plots)

### **Pertanyaan Dua: Korelasi IPTI dengan Angka Partisipasi Sekolah (2020-2025)**
- **Tujuan**: Menganalisis hubungan antara pembangunan TIK dengan partisipasi sekolah
- **Metrik Utama**:
  - Indeks Pembangunan TIK (IPTIK) 2019-2024
  - Angka Partisipasi Sekolah (APS) per age group: 13-15, 16-18, 19-23
- **Output**: 11 visualisasi (bar charts, line plots, heatmap korelasi, scatter plots)

---
## 🚀 Cara Menjalankan

### **1. Setup Environment (First Time Only)**

```bash
# Install dependencies
pip install -r requirements.txt
```

### **2. Jalankan Streamlit**

```bash
# Pastikan berada di folder capstone-streamlit
cd capstone-streamlit

# Jalankan aplikasi
streamlit run app.py
```

Browser akan terbuka otomatis di `http://localhost:8501`

### **3. Gunakan Dashboard**

1. **Pilih Pertanyaan** di sidebar kiri
2. **Jelajahi Tab**:
   - Data Summary (tabel & metrik utama)
   - Visualisasi (grafik interaktif)
   - Analisis tambahan (insights spesifik)
3. **Klik gambar** untuk zoom/download
4. **Toggle sidebar** untuk full-width view

---
