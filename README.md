# Project-Big-Data_Apache-Kafka

**Nama**: Veri Rahman

**NRP**: 5027231088

## **Deskripsi**

Sistem ini dirancang untuk memantau kondisi gudang penyimpanan yang menyimpan barang-barang sensitif seperti makanan, obat-obatan, dan peralatan elektronik secara real-time. Dengan memanfaatkan Apache Kafka sebagai platform streaming data dan PySpark Structured Streaming untuk pemrosesan data, sistem ini mampu mendeteksi kondisi berbahaya seperti suhu dan kelembaban ekstrem secara instan.

## **Fitur**

Simulasi Data Sensor – Data suhu & kelembaban dihasilkan setiap detik untuk 3 gudang (G1, G2, G3).

Deteksi Anomali – Sistem memberikan peringatan jika:

- Suhu melebihi 80°C (Risiko Kebakaran/Kerusakan Barang).
  
- Kelembaban melebihi 70% (Risiko Jamur/Kerusakan Elektronik).
  
- Kondisi Kritis jika kedua parameter melebihi batas aman secara bersamaan.
  
  - Integrasi Data – Menggabungkan data suhu & kelembaban berdasarkan ID Gudang dan window waktu 10 detik.
 
## **Komponen**

1. **Apache Kafka**

- Fungsi: Sebagai pusat pengumpulan data real-time dari sensor.

- Topik yang Digunakan:

  - *sensor-suhu-gudang* → Menerima data suhu.

  - *sensor-kelembaban-gudang* → Menerima data kelembaban.

2. **Kafka Producer**
   
producer_suhu.py → Mengirim data suhu ke Kafka dalam format JSON, contoh:
```bash
{"gudang_id": "G1", "suhu": 82}
```

producer_kelembaban.py → Mengirim data kelembaban ke Kafka, contoh:
```bash
{"gudang_id": "G2", "kelembaban": 75}
```

3. **PySpark Structured Streaming**

- Fungsi: Membaca data dari Kafka, melakukan analisis, dan menghasilkan alert.

- Proses yang Dilakukan:

  - Filtering → Mendeteksi suhu >80°C dan kelembaban >70%.

  - Stream Join → Menggabungkan data suhu & kelembaban berdasarkan gudang_id dan window waktu 10 detik.

  - Output → Menampilkan status gudang (Normal/Peringatan/Kritis) di konsol.

## **Panduan Menjalankan Sistem**

**1. Menjalankan Kafka**

```bash
bin/kafka-server-start.sh config/kraft/server.properties
```
![Cuplikan layar 2025-05-22 225931](https://github.com/user-attachments/assets/f88b0891-4d46-4412-a265-1d3db21a7119)
![Cuplikan layar 2025-05-22 225943](https://github.com/user-attachments/assets/bdbf3ef1-e0f0-4803-9f62-3ec6a2685b99)

**2. Membuat Topik Kafka**

```bash
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic sensor-suhu-gudang --partitions 1 --replication-factor 1
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic sensor-kelembaban-gudang --partitions 1 --replication-factor 1
```
![Cuplikan layar 2025-05-22 193851](https://github.com/user-attachments/assets/cc587f3c-87f2-4f16-a1f2-013ecd12755b)
![Cuplikan layar 2025-05-22 193902](https://github.com/user-attachments/assets/e300eca3-5b5d-488e-8607-7eb08ab4683b)

**3. Menjalankan Producer**

```bash
python producer_suhu.py  
python producer_kelembaban.py  
```
![Cuplikan layar 2025-05-22 221335](https://github.com/user-attachments/assets/c927e88b-5b9b-4c12-96d6-1ed7c21d89d8)
![Cuplikan layar 2025-05-22 221345](https://github.com/user-attachments/assets/4c7698c6-d818-4588-89ea-6dec200c8cd0)


**4. Menjalankan Pyspark Comsumer**

```bash
spark-submit consumer_spark.py  
```

## **Struktur Folder**

```bash
real-time-gudang-monitoring/  
├── consumer_spark.py          # Pemrosesan data dengan PySpark 
├── producer_kelembaban.py     # Simulator data kelembaban  
├── producer_suhu.py           # Simulator data suhu 
├── topics.sh                  # Script Topik 
└── README.md                  # Dokumentasi proyek
```
