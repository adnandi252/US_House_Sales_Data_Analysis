# **Laporan Analisis Pasar Properti**
Laporan ini menyajikan analisis mendalam mengenai pasar properti berdasarkan data yang divisualisasikan. Analisis ini dilakukan pada data sintetis yang berisi 3.000 listing properti residensial yang dimodelkan seperti data penjualan rumah riil di Amerika Serikat (dalam format gaya Zillow).Setiap baris mewakili properti unik dan mencakup 16 fitur utama yang umum digunakan oleh agen real estat, investor, dan analis. Data ini mencakup beberapa negara bagian dan kota di AS, dengan nilai yang realistis untuk harga, luas persegi, jumlah kamar tidur/kamar mandi, tipe properti, dan banyak lagi.Analisis mencakup harga, efisiensi penjualan, preferensi pasar, performa agen, dan tren berdasarkan usia bangunan. Setiap visualisasi dibuat untuk menjawab 5 pertanyaan bisnis.

**Sumber Dataset:** [USA House Sales Data by Abdul Wadood from Kaggle](https://www.kaggle.com/datasets/abdulwadood11220/usa-house-sales-data)
**Link Live Dashboard:** [Dashboard analytics US House Sales Data](https://ushousesalesdataanalysis-fg6ymkkoqdjwfcvevtjc7k.streamlit.app/)

## **Ringkasan Umum Pasar:**
* Total Properti Dianalisis: 3,000
* Rata-rata Harga Properti: $810,859
* Rata-rata Hari di Pasar: 61 hari
* Tingkat Terjual: 34.8%

## **1. Analisis Harga Pasar**
Bagian ini menjawab pertanyaan: Bagaimana distribusi harga properti di berbagai negara bagian dan kota? Mana yang paling mahal dan mana yang paling terjangkau?
* Distribusi Harga per Negara Bagian:
    * Berdasarkan grafik batang "Rata-rata Harga Properti per Negara Bagian", harga properti menunjukkan konsistensi yang tinggi di lima negara bagian teratas (FL, IL, CA, NY, TX).
    * Rata-rata harga di kelima negara bagian ini sangat berdekatan, berada di rentang $800k hingga $830k. Florida (FL) dan Illinois (IL) menunjukkan rata-rata harga sedikit lebih tinggi dibandingkan California (CA), New York (NY), dan Texas (TX), meskipun perbedaannya tidak signifikan.
* Kota Termahal:
    * Grafik "Top 10 Kota Termahal" menyoroti kota-kota dengan rata-rata harga tertinggi.
    * Fresno, IL menempati posisi puncak sebagai kota termahal dengan rata-rata harga mendekati $880k.
    * Diikuti oleh San Diego, FL dan Fresno, CA di posisi kedua dan ketiga.
    * Tidak ada informasi mengenai kota yang paling terjangkau dari visualisasi yang ada, karena data hanya menampilkan "Top 10 Termahal".
**Kesimpulan:** Harga properti secara umum tinggi dan relatif seragam di tingkat negara bagian. Namun, terdapat perbedaan signifikan di tingkat kota, dengan Fresno, IL menjadi lokasi paling premium dalam dataset ini.


## **2. Efisiensi Penjualan**
Bagian ini menjawab pertanyaan: Berapa rata-rata waktu properti berada di pasar (Days on Market) berdasarkan tipe properti, lokasi, dan rentang harga?
* Berdasarkan Tipe Properti:
    * Grafik "Hari di Pasar berdasarkan Tipe Properti" menunjukkan bahwa efisiensi penjualan sangat mirip untuk semua tipe properti (Apartment, Condo, Multi-Family, Single Family, Townhouse).
    * Baik nilai rata-rata maupun median waktu penjualan untuk semua tipe properti berada di sekitar 61-62 hari. Ini menandakan bahwa tipe properti bukanlah faktor utama yang membedakan kecepatan penjualan di pasar ini.

* Berdasarkan Kategori Harga:
    * Box plot "Distribusi Hari di Pasar berdasarkan Kategori Harga" menunjukkan tren yang jelas:
    * Properti <$200k: Terjual paling cepat. Median waktu penjualan berada di sekitar 50 hari.
    * Properti $200k - $600k: Memiliki waktu penjualan yang moderat, dengan median sekitar 60 hari.
    * Properti >$1M: Cenderung memakan waktu paling lama untuk terjual. Meskipun mediannya tidak jauh berbeda, rentang kuartilnya (kotak pada plot) lebih tinggi, menunjukkan bahwa sebagian besar properti di kategori ini membutuhkan waktu lebih lama di pasar.
**Kesimpulan:** Efisiensi penjualan lebih dipengaruhi oleh harga daripada tipe properti. Properti dengan harga lebih rendah cenderung terjual lebih cepat, sementara properti mewah (di atas $1M) membutuhkan waktu pemasaran yang lebih lama.

## **3. Preferensi Pasar**
Bagian ini menjawab pertanyaan: Bagaimana hubungan antara jumlah kamar tidur, kamar mandi, dan luas bangunan terhadap harga jual?
* Analisis Korelasi:
    * Matriks korelasi menunjukkan hubungan yang sangat lemah antara fitur utama properti dan harga. Nilai korelasinya adalah sebagai berikut:
    * Harga vs. Kamar Tidur: -0.0215 (hampir tidak ada korelasi)
    * Harga vs. Kamar Mandi: 0.0094 (hampir tidak ada korelasi)
    * Harga vs. Luas Bangunan: -0.0320 (hampir tidak ada korelasi)
    * Nilai yang mendekati nol ini menunjukkan bahwa penambahan kamar tidur, kamar mandi, atau luas bangunan tidak secara langsung menyebabkan kenaikan atau penurunan harga yang signifikan dalam dataset ini.

* Hubungan Luas Bangunan vs Harga:
    * Scatter plot "Hubungan Luas Bangunan vs Harga" mengkonfirmasi temuan dari matriks korelasi. Titik-titik data tersebar secara acak tanpa membentuk pola yang jelas. Properti dengan luas bangunan yang besar tidak selalu memiliki harga yang lebih tinggi, dan sebaliknya.
    * Warna titik yang merepresentasikan jumlah kamar tidur juga tersebar, yang menegaskan bahwa jumlah kamar tidur bukan pendorong utama harga.

**Kesimpulan:** Berdasarkan data ini, preferensi pasar tidak ditentukan oleh fitur fisik standar seperti jumlah kamar atau luas bangunan. Faktor-faktor lain yang tidak ditampilkan (misalnya, lokasi spesifik, kondisi properti, pemandangan, atau fasilitas lingkungan) kemungkinan memiliki pengaruh yang jauh lebih besar terhadap harga.

## **4. Analisis Performa Agen**
Bagian ini menjawab pertanyaan: Siapa agen terbaik berdasarkan jumlah properti yang berhasil dijual dan rata-rata waktu penjualan?

* Berdasarkan Jumlah Properti (Volume):
    * Grafik "Top Agen Berdasarkan Jumlah Properti" menunjukkan bahwa Alex Johnson adalah agen dengan volume properti terbanyak, diikuti sangat tipis oleh Jane Smith. Keduanya menangani lebih dari 600 properti.
    * Emily Davis berada di urutan ketiga dengan 594 properti.

* Berdasarkan Efisiensi (Tingkat Penjualan vs. Waktu):
    * Scatter plot "Performa Agen" memberikan gambaran efisiensi. Agen ideal berada di kiri bawah (tingkat penjualan tinggi, hari di pasar rendah) yaitu Emily Davis.
    * Terdapat sekelompok agen (Alex Jhonson, dan Jane Smith) yang memiliki tingkat penjualan tertinggi (sekitar 36-36.5%) dengan rata-rata waktu penjualan 61-62 hari.
    * Ada satu agen (jhon Doe) yang menonjol dengan tingkat penjualan tinggi (36.5%) dan waktu penjualan yang lebih cepat (60.5 hari), menjadikannya salah satu agen paling efisien.
    * Sebaliknya, ada agen di kanan bawah (Mike Lee) yang memiliki waktu penjualan paling lama (63 hari) dan tingkat penjualan terendah (32%), menunjukkan performa yang kurang optimal.

**Kesimpulan:** Alex Johnson dan Jane Smith adalah pemimpin pasar dari segi volume. Namun, dalam hal efisiensi (kombinasi kecepatan dan tingkat keberhasilan penjualan), agen yang berada di cluster kiri-atas pada scatter plot adalah yang terbaik. Tanpa nama yang terhubung di kedua grafik, tidak dapat dipastikan apakah Alex Johnson dan Jane Smith termasuk agen yang paling efisien.

## **5. Tren Pasar Berdasarkan Usia Bangunan**
Bagian ini menjawab pertanyaan: Bagaimana hubungan antara tahun dibangun dengan harga jual dan daya tarik pasar?

* Hubungan Usia Bangunan dengan Harga:
    * Grafik "Rata-rata Harga berdasarkan Usia Bangunan" menunjukkan bahwa usia bangunan tidak memiliki dampak signifikan terhadap rata-rata harga jual.
    * Semua kategori usia, dari yang terbaru (0-10 tahun) hingga yang tertua (50+ tahun), memiliki rata-rata harga yang sangat stabil di sekitar $800k - $820k. Menariknya, properti tertua (50+ tahun) memiliki rata-rata harga yang sedikit lebih tinggi, mungkin karena lokasinya yang premium di area yang sudah mapan.

* Hubungan Usia Bangunan dengan Daya Tarik Pasar (Waktu Penjualan):
    * Box plot "Distribusi Hari di Pasar berdasarkan Usia Bangunan" menunjukkan hubungan yang jelas:
    * Properti Baru (0-10 tahun): Paling cepat terjual, dengan median waktu penjualan terendah (sekitar 55 hari).
    * Properti Menengah (11-30 tahun): Terjual dengan kecepatan moderat.
    * Properti Tua (31+ tahun): Membutuhkan waktu paling lama untuk terjual. Median dan sebaran waktu penjualan untuk kategori 31-50 tahun dan 50+ tahun deutlich lebih tinggi.

**Kesimpulan:** Meskipun harga properti tetap tinggi tanpa memandang usianya, daya tarik pasar (kecepatan penjualan) sangat dipengaruhi oleh usia bangunan. Pembeli menunjukkan preferensi yang kuat untuk properti yang lebih baru, yang terjual secara signifikan lebih cepat daripada properti yang lebih tua.
