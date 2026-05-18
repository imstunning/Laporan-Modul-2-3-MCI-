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





# VISUALISASI

1. Orders by Day of Week

  <img width="760" height="796" alt="image" src="https://github.com/user-attachments/assets/4ad22587-dcd5-4f1f-9250-cdee7def66f3" />

  Query ini digunakan untuk menghitung jumlah order berdasarkan hari dalam seminggu.

  Kolom order_dow yang awalnya berupa angka 0–6 diubah menjadi nama hari menggunakan CASE WHEN agar lebih mudah dibaca pada visualisasi. Setelah itu, data dikelompokkan menggunakan GROUP BY lalu dihitung total ordernya menggunakan COUNT(*).
  
  Visualisasi menunjukkan bahwa jumlah order tertinggi terjadi pada hari Senin, sedangkan jumlah order paling sedikit terjadi pada hari Minggu dan Kamis. Hal ini menunjukkan bahwa aktivitas pemesanan cenderung meningkat di awal minggu dibanding pertengahan minggu.

2. Orders by Hour of Day

  <img width="730" height="508" alt="image" src="https://github.com/user-attachments/assets/89d8baa1-25cc-46e1-a832-da492baf08be" />

  Query ini digunakan untuk melihat distribusi jumlah order berdasarkan jam.

  Data dikelompokkan berdasarkan order_hour_of_day, lalu dihitung jumlah order pada setiap jam menggunakan COUNT(*).
  
  Jumlah order paling banyak terjadi pada rentang siang hingga sore hari, terutama sekitar pukul 10.00–16.00. Hal ini menunjukkan bahwa pengguna lebih aktif melakukan pembelian pada jam produktif atau jam setelah aktivitas pagi.

3. Top 10 Most Ordered Products

  <img width="716" height="544" alt="image" src="https://github.com/user-attachments/assets/d34568b0-a62f-440b-adc0-573f76c8bade" />

  Query ini digunakan untuk mencari 10 produk yang paling sering dipesan.

  Data dikelompokkan berdasarkan nama produk menggunakan GROUP BY, kemudian jumlah pemesanannya dihitung menggunakan COUNT(*). Hasilnya diurutkan dari jumlah terbesar ke terkecil menggunakan ORDER BY DESC lalu dibatasi hanya 10 data teratas menggunakan LIMIT 10.

  Produk yang paling sering dipesan adalah Banana, diikuti Bag of Organic Bananas dan Organic Strawberries. Mayoritas produk teratas berasal dari kategori buah dan produk organik, menunjukkan preferensi pelanggan terhadap makanan segar dan sehat.

4. Top 5 Departments by Orders

  <img width="702" height="580" alt="image" src="https://github.com/user-attachments/assets/3606f139-a437-4ffa-8400-7a8e2f9497ea" />

  Query ini digunakan untuk mengetahui department dengan jumlah order terbanyak.

  Data dengan nilai `NULL` pada kolom department diabaikan menggunakan `WHERE` department `IS NOT NULL`. Selanjutnya data dikelompokkan berdasarkan department dan dihitung jumlah ordernya.

  Department dengan jumlah order tertinggi adalah produce, disusul dairy eggs dan beverages. Hal ini menunjukkan bahwa produk kebutuhan harian dan bahan makanan segar menjadi kategori yang paling sering dibeli pelanggan.

5. Top 10 Products by Reorder Rate

  <img width="1194" height="652" alt="image" src="https://github.com/user-attachments/assets/438704e1-49bb-4634-b70f-784b6478e0af" />

  Query ini digunakan untuk menghitung tingkat reorder suatu produk.
    - COUNT(*) digunakan untuk menghitung total pemesanan produk.
    - SUM(reordered) digunakan untuk menghitung berapa kali produk dibeli ulang.

   Fungsi ROUND(..., 2) digunakan agar hasil persentase hanya memiliki 2 angka desimal.

  HAVING total_ordered > 1 digunakan agar hanya produk yang pernah dipesan lebih dari satu kali yang dihitung reorder rate-nya.
  
  Beberapa produk seperti Organic Romaine Leaf, Organic Yellow Onion, dan Organic Baby Spinach memiliki reorder rate mencapai 100%. Hal ini menunjukkan bahwa produk-produk tersebut memiliki tingkat loyalitas pelanggan yang tinggi dan sering dibeli kembali.

6. Average Items per Order by Day

  <img width="1064" height="1012" alt="image" src="https://github.com/user-attachments/assets/b4a29616-afd6-4cf0-a5a7-cdcaf43de0cd" />

   Query ini digunakan untuk menghitung rata-rata jumlah item dalam setiap order berdasarkan hari.

   Digunakan untuk menghitung jumlah item pada setiap order. Kemudian hasilnya digabungkan dengan tabel orders menggunakan JOIN berdasarkan order_id. Setelah itu, rata-rata jumlah item dihitung menggunakan AVG(item_count) lalu dibulatkan menjadi 2 angka desimal menggunakan ROUND().
   
  Rata-rata jumlah item per order tertinggi terjadi pada Thursday, sedangkan Wednesday memiliki rata-rata item paling rendah. Ini menunjukkan bahwa meskipun jumlah order tidak selalu tinggi, pelanggan pada hari tertentu cenderung membeli lebih banyak produk dalam satu transaksi.
   
KESIMPULAN KESELURUHAN VISUALISASI

Berdasarkan keseluruhan dashboard, pola pembelian pelanggan didominasi oleh produk kebutuhan harian, terutama buah, sayuran, dan produk organik. Aktivitas order cenderung meningkat pada awal minggu dan pada jam siang hingga sore hari.

Selain itu, tingginya reorder rate pada beberapa produk menunjukkan adanya pola pembelian berulang, yang mengindikasikan loyalitas pelanggan terhadap produk tertentu. Secara keseluruhan, analisis ini dapat membantu bisnis memahami perilaku pelanggan, menentukan strategi stok barang, serta mengoptimalkan promosi berdasarkan waktu dan kategori produk yang paling diminati.




