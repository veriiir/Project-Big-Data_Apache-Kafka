# Project-Big-Data_Apache-Kafka

**Nama**: Veri Rahman
**NRP**: 5027231088

## Deskripsi
Sistem ini dirancang untuk memantau kondisi gudang penyimpanan yang menyimpan barang-barang sensitif seperti makanan, obat-obatan, dan peralatan elektronik secara real-time. Dengan memanfaatkan Apache Kafka sebagai platform streaming data dan PySpark Structured Streaming untuk pemrosesan data, sistem ini mampu mendeteksi kondisi berbahaya seperti suhu dan kelembaban ekstrem secara instan.

## Fitur
Simulasi Data Sensor – Data suhu & kelembaban dihasilkan setiap detik untuk 3 gudang (G1, G2, G3).
Deteksi Anomali – Sistem memberikan peringatan jika:
- Suhu melebihi 80°C (Risiko Kebakaran/Kerusakan Barang).
- Kelembaban melebihi 70% (Risiko Jamur/Kerusakan Elektronik).
- Kondisi Kritis jika kedua parameter melebihi batas aman secara bersamaan.
  - Integrasi Data – Menggabungkan data suhu & kelembaban berdasarkan ID Gudang dan window waktu 10 detik.
 
## Komponen
1. Apache Kafka
- Fungsi: Sebagai pusat pengumpulan data real-time dari sensor.

- Topik yang Digunakan:

  - sensor-suhu-gudang → Menerima data suhu.

  - sensor-kelembaban-gudang → Menerima data kelembaban.

2. Kafka Producer
producer_suhu.py → Mengirim data suhu ke Kafka dalam format JSON, contoh:

{"gudang_id": "G1", "suhu": 82}
producer_kelembaban.py → Mengirim data kelembaban ke Kafka, contoh:

{"gudang_id": "G2", "kelembaban": 75}
