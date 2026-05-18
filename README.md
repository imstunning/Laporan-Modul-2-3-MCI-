# Laporan-Modul-3-MCI

# TASK 1

Script `fetch_orders.py` bertugas mengambil data orders dari API lalu menyimpannya ke dalam format .parquet sebagai raw data sebelum diproses lebih lanjut pada tahap transformasi.

1. Setup & Konfigurasi

  <img width="1252" height="652" alt="image" src="https://github.com/user-attachments/assets/b8acfc0f-6a3a-4689-87bc-364a36521f15" />

  Bagian ini berfungsi sebagai setup awal program sebelum proses ingestion dijalankan. Selain itu, logging dikonfigurasi menggunakan level INFO agar setiap proses penting seperti keberhasilan maupun error dapat tercatat dengan jelas. disini kami menggunakan format parquet karena dirasa lebih efisien untuk pemrosesan big data dan kompatibel dengan Apache Spark.

2. Fungsi Mengambil dan Menyimpan Data Orders

  <img width="1610" height="940" alt="image" src="https://github.com/user-attachments/assets/6bbc7db9-2541-4523-b68e-35305b8fd4e0" />

  Fungsi ini bertugas mengambil data orders dari API lalu menyimpannya ke dalam format .parquet sebagai raw data.

  Data diambil menggunakan requests.get(), kemudian diubah menjadi DataFrame Pandas sebelum disimpan ke lokasi output. Script juga memastikan folder penyimpanan tersedia terlebih dahulu menggunakan os.makedirs().

  Jika proses berhasil, sistem akan mencatat jumlah data yang berhasil disimpan. Namun jika terjadi error, pesan error akan dicatat ke log dan pipeline dihentikan agar Airflow mendeteksi task sebagai gagal.

3. Menjalankan Fungsi Utama

  <img width="672" height="364" alt="image" src="https://github.com/user-attachments/assets/b1588022-189e-4aee-ac76-0bc86dcfc14a" />

  Bagian ini digunakan untuk menjalankan fungsi `fetch_orders()` secara otomatis saat file Python dieksekusi oleh Airflow maupun terminal.

# TASK 2

Script orders_pipeline.py` bertugas mengatur alur workflow pipeline menggunakan Apache Airflow, mulai dari proses pengambilan data, transformasi data, hingga memuat data ke ClickHouse.

1. Import Library

  <img width="976" height="400" alt="image" src="https://github.com/user-attachments/assets/9ba3584f-ce5b-4097-ae0e-2f8fe81756dd" />

  Bagian ini mengimpor library yang dibutuhkan untuk membuat workflow pipeline di Apache Airflow.
  DAG digunakan untuk mendefinisikan pipeline, sedangkan `BashOperator` digunakan untuk menjalankan script Python melalui command terminal.

2. Setup DAG Config

   <img width="860" height="508" alt="image" src="https://github.com/user-attachments/assets/2d8eec0b-dc3d-48fd-b296-01b7eb317e83" />

  Bagian ini berisi konfigurasi default untuk DAG seperti owner pipeline, tanggal mulai scheduler, jumlah retry jika task gagal, serta jeda retry selama 5 menit sebelum task dijalankan ulang.

3. Membuat DAG Pipeline

   <img width="1092" height="580" alt="image" src="https://github.com/user-attachments/assets/9e8b4a87-12de-4f69-a1d6-88d03a93e575" />

   Bagian ini membuat DAG bernama `orders_pipeline` yang menjadi workflow utama pipeline.
   Pipeline dijadwalkan berjalan setiap hari menggunakan @daily. Selain itu:
    - `catchup=False` digunakan agar Airflow tidak menjalankan task lama,
    - `max_active_runs=1` memastikan hanya satu pipeline berjalan dalam satu waktu.

5. Menjalankan Proses Fetch Orders

  <img width="1294" height="436" alt="image" src="https://github.com/user-attachments/assets/2a37d438-04a4-4727-974b-dc7a1d2dff0d" />

  Bagian ini menjalankan script `fetch_orders.py` untuk mengambil data orders dari API lalu menyimpannya sebagai raw data dalam format `.parquet`.

5. Menjalankan Proses Transformasi Data

   <img width="1380" height="436" alt="image" src="https://github.com/user-attachments/assets/a9318b02-32ab-455d-b3a2-898def6c9d6b" />

  Bagian `transform_orders` menjalankan script `transform_orders.py` untuk melakukan transformasi data seperti flattening nested data dan membersihkan data sebelum dimuat ke ClickHouse.

6. Menjalankan Proses Load ke ClickHouse

   <img width="1294" height="436" alt="image" src="https://github.com/user-attachments/assets/024f2dd3-74b6-438a-89ff-ed6259ebc012" />

   Bagian `load_to_clickhouse` bertugas menjalankan script `load_orders.py` untuk memuat hasil transformasi data ke dalam database ClickHouse.

7. Mengatur Urutan Eksekusi Task Pipeline

  <img width="1076" height="328" alt="image" src="https://github.com/user-attachments/assets/94019f7b-5037-4bcf-bbb7-d62956be2d25" />

  Bagian ini menentukan urutan eksekusi task pada pipeline menggunakan dependency Airflow.







   
    



