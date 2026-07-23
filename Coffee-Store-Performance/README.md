# ☕ Coffee Shop Sales & Spatial Analytics Dashboard

## 🛠️ Project Workflow

Proyek ini dikerjakan melalui beberapa tahapan analisis data secara end-to-end, mulai dari pengolahan data hingga visualisasi dashboard.

| Tahapan | Tools | Deskripsi |
|---------|-------|-----------|
| **Data Cleaning** | Microsoft Excel | Melakukan pemeriksaan kualitas data, menghapus data duplikat, memeriksa missing values, mengubah format data, membuat kolom Revenue, serta menambahkan koordinat Latitude dan Longitude menggunakan XLOOKUP. |
| **Data Analysis** | SQLite | Melakukan analisis data menggunakan SQL untuk menghitung KPI, menganalisis performa penjualan, produk, outlet, serta tren penjualan berdasarkan waktu. |
| **Spatial Analysis** | Python | Memvisualisasikan lokasi setiap outlet menggunakan koordinat geografis dan menganalisis distribusi revenue berdasarkan lokasi (Spatial Analysis). |
| **Dashboard Development** | Power BI | Membangun dashboard interaktif yang menyajikan KPI, tren penjualan, performa outlet, performa produk, analisis spasial, serta fitur filter interaktif untuk mendukung pengambilan keputusan bisnis. |

## 📌 Business Problem

Coffee shop memiliki beberapa outlet di wilayah New York, namun belum memiliki dashboard yang mampu memberikan gambaran menyeluruh mengenai performa bisnis. Oleh karena itu, diperlukan analisis untuk menjawab beberapa pertanyaan berikut:

- Outlet mana yang menghasilkan revenue tertinggi?
- Produk apa yang paling diminati pelanggan?
- Kategori produk mana yang memberikan kontribusi revenue terbesar?
- Bagaimana tren penjualan dari waktu ke waktu?
- Bagaimana distribusi performa penjualan berdasarkan lokasi outlet?

---

## 🎯 Project Objectives

Proyek ini bertujuan untuk membangun dashboard Business Intelligence yang interaktif guna:

- Menganalisis performa penjualan berdasarkan indikator utama (KPI).
- Mengidentifikasi outlet dengan performa terbaik berdasarkan revenue.
- Menentukan produk terlaris berdasarkan jumlah penjualan (quantity sold).
- Menganalisis kategori produk yang memberikan kontribusi revenue terbesar.
- Memvisualisasikan performa outlet menggunakan analisis spasial (Spatial Analysis).
- Mendukung pengambilan keputusan bisnis yang lebih efektif berdasarkan data.

---

## 📊 Key Insights

- Coffee shop menghasilkan **Total Revenue sebesar 698,81K** dari sekitar **149 ribu transaksi** dengan **214 ribu produk terjual**.
- Penjualan tertinggi terjadi pada **bulan Juni**, sedangkan bulan Februari memiliki performa penjualan terendah.
- **Hell's Kitchen** merupakan outlet dengan revenue tertinggi dibandingkan outlet lainnya.
- Produk terlaris diidentifikasi berdasarkan **Total Quantity Sold**, sehingga dapat diketahui produk yang paling banyak diminati pelanggan.
- Kategori **Coffee** memberikan kontribusi revenue terbesar dibandingkan kategori produk lainnya.
- Analisis spasial menunjukkan bahwa performa ketiga outlet relatif seimbang, meskipun terdapat satu outlet dengan performa sedikit lebih tinggi.

---

## 💡 Business Recommendations

- Memprioritaskan ketersediaan stok untuk produk dengan tingkat penjualan tertinggi.
- Menerapkan strategi promosi pada bulan dengan penjualan rendah untuk meningkatkan revenue.
- Menjadikan outlet dengan performa terbaik sebagai acuan dalam evaluasi operasional outlet lainnya.
- Memfokuskan strategi pemasaran pada kategori produk dengan kontribusi revenue terbesar, sekaligus meningkatkan promosi pada kategori yang masih rendah.
- Memanfaatkan hasil analisis spasial sebagai dasar dalam menentukan strategi ekspansi dan evaluasi lokasi outlet di masa mendatang.

<img width="1845" height="1044" alt="image" src="https://github.com/user-attachments/assets/3bd43180-8fd5-4a7b-be49-07dc87e25513" />

