# 🏬 Retail Sales Forecasting with LSTM & Executive Decision Support System (DSS)

> **Repositori Kode Sumber Tugas Akhir (Skripsi)**  
> **Penulis:** Fikran Naufal (NIM: 10122097)  
> **Dataset:** [Kaggle: Store Sales - Time Series Forecasting (Corporación Favorita)](https://www.kaggle.com/competitions/store-sales-time-series-forecasting)

---

## 📌 Ringkasan Proyek (Overview)

Repositori ini berisi kode sumber penelitian Tugas Akhir mengenai peramalan penjualan ritel (*retail sales forecasting*) menggunakan arsitektur **Long Short-Term Memory (LSTM)** dengan studi kasus data transaksi multi-toko dan multi-kategori dari **Corporación Favorita** (3+ juta transaksi).

Penelitian ini mencakup:
1. **Analisis Deret Waktu & Clustering**: Eksplorasi perilaku data, dekomposisi deret waktu, dan pengelompokan pola penjualan menggunakan *K-Means Clustering*.
2. **Eksperimen Pemodelan LSTM**: Perbandingan pendekatan pemodelan (*Individual LSTM* per kategori vs *Global LSTM* multi-kategori), serta teknik optimasi (*smoothing*, *feature engineering*, dan *hyperparameter tuning*).
3. **Executive Decision Support System (DSS)**: Aplikasi dashboard interaktif berbasis **Streamlit** untuk menerjemahkan metrik teknis Machine Learning (RMSLE, MAE, RMSE) ke dalam dampak bisnis nyata (*Business Impact*, *Inventory Cost*, *ROI*, dan *Safety Stock / Reorder Point Advisor*).

---

## 📂 Struktur Direktori

```text
sales-forecasting-lstm/
│
├── TA-1/                                    # Eksperimen Tugas Akhir Tahap 1 (Seminar 1)
│   ├── notebook-utama-seminar1.ipynb        # Notebook utama data pipeline, EDA, & baseline LSTM
│   ├── eksperimen_sales_forecast.ipynb      # Eksperimen peramalan awal
│   └── notebook-lstm-improvement.ipynb      # Eksperimen peningkatan model awal
│
├── TA-2/                                    # Eksperimen Tugas Akhir Tahap 2 (Lanjutan)
│   ├── notebook-eksperimen-ta2.ipynb        # Eksperimen pemodelan lanjutan
│   ├── notebook-statistika-deskriptif.ipynb # Analisis statistika deskriptif data
│   ├── kmeans.ipynb                         # Segmentasi pola penjualan dengan K-Means
│   ├── lstm-model-experiment-all-category.ipynb # Eksperimen Global LSTM (all categories)
│   ├── lstm-model-experiment-smooth.ipynb   # Eksperimen LSTM dengan target smoothing
│   ├── individual-lstm-experiment-1.ipynb   # Eksperimen model individual kategori 1
│   ├── individual-lstm-experiment-2.ipynb   # Eksperimen model individual kategori 2
│   ├── individual-lstm-experiment-3.ipynb   # Eksperimen model individual kategori 3
│   ├── individual-lstm-experiment-4.ipynb   # Eksperimen model individual kategori 4
│   ├── univariate-model-notebook.ipynb      # Eksperimen univariate benchmark
│   ├── comparison_4_experiments_summary.csv # Ringkasan evaluasi 4 skenario eksperimen
│   └── descriptive_stats_all_combinations.csv
│
├── dashboard/                               # Aplikasi Executive Decision Support System (DSS)
│   ├── app.py                               # Entry point aplikasi Streamlit multi-page
│   ├── requirements_dashboard.txt           # Dependensi khusus untuk menjalankan dashboard
│   ├── pages/
│   │   ├── 1_💰_Business_Impact_&_ROI.py    # Modul simulasi dampak finansial, ROI, & holding cost
│   │   ├── 2_📊_The_Kaizen_Story.py         # Modul visualisasi evolusi performa eksperimen
│   │   └── 3_📦_Demand_Pattern_&_Reorder_Advisor.py # Modul analisis pola & rekomendasi Reorder Point
│   ├── utils/                               # Helper modul (data loader, metrik, i18n, visualisasi)
│   │   ├── data_loader.py
│   │   ├── metrics_calc.py
│   │   ├── plot_helpers.py
│   │   ├── prepare_data.py
│   │   └── i18n.py
│   └── data/                                # Data ringkasan hasil inferensi untuk dashboard
│       ├── category_experiments_summary.csv
│       ├── target_experiments_summary.csv
│       ├── sample_timeseries_target.csv
│       └── descriptive_stats.csv
│
├── datasets/                                # Folder dataset mentah (diabaikan oleh git)
└── .gitignore
```

---

## 📊 Modul Dashboard (Executive DSS)

Dashboard dirancang untuk memberikan sudut pandang manajerial dan praktis dari model prediktif yang dibangun:

1. **💰 Dampak Bisnis & ROI (`1_Business_Impact_&_ROI.py`)**:
   - Menghitung efisiensi modal kerja (*working capital*) dan estimasi penghematan biaya *overstock* vs *stockout*.
   - Simulasi interaktif parameter margin kotor (*gross margin*), biaya simpan (*holding cost rate*), dan biaya penalti kehilangan penjualan (*stockout penalty*).
2. **📈 Cerita Kaizen / Kaizen Story (`2_The_Kaizen_Story.py`)**:
   - Melacak evolusi perbaikan model secara terstruktur (Baseline $\rightarrow$ Feature Engineering $\rightarrow$ Hyperparameter Tuning $\rightarrow$ Smoothing & Global Model).
   - Menampilkan perbandingan metrik evaluasi (RMSLE, MAE, WAPE) lintas iterasi eksperimen.
3. **📦 Rekomendasi Reorder & Pola Permintaan (`3_Demand_Pattern_&_Reorder_Advisor.py`)**:
   - Mengelompokkan item berdasarkan volatilitas dan tingkat permintaan.
   - Menghitung rekomendasi kuantitatif untuk *Safety Stock*, *Lead Time Demand*, dan *Reorder Point (ROP)* dengan *service level* yang dapat disesuaikan.

---

## 🚀 Panduan Menjalankan Dashboard

### 1. Prasyarat
- Python 3.9 s.d. 3.11 disarankan.
- Manajer paket `pip`.

### 2. Setup Virtual Environment
Buka terminal / PowerShell di direktori proyek:
```bash
# Buat virtual environment
python -m venv .venv

# Aktifkan virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate
```

### 3. Instalasi Dependensi Dashboard
```bash
pip install -r dashboard/requirements_dashboard.txt
```

### 4. Jalankan Aplikasi Streamlit
```bash
streamlit run dashboard/app.py
```
Aplikasi secara otomatis dapat diakses melalui browser di `http://localhost:8501`.

---

## 📦 Informasi Dataset

Dataset penelitian ini menggunakan data publik dari kompetisi **Store Sales - Time Series Forecasting** di Kaggle. File dataset mentah berukuran besar (> 100 MB) tidak disertakan di dalam repositori Git sesuai batasan ukuran file GitHub.

Jika ingin menjalankan notebook pelatihan dari awal:
1. Unduh dataset dari [Kaggle Store Sales](https://www.kaggle.com/competitions/store-sales-time-series-forecasting/data).
2. Ekstrak seluruh file CSV ke dalam direktori `datasets/`:
   - `datasets/train.csv`
   - `datasets/test.csv`
   - `datasets/stores.csv`
   - `datasets/oil.csv`
   - `datasets/holidays_events.csv`
   - `datasets/transactions.csv`

> **Catatan:** Dashboard eksekutif (`dashboard/app.py`) **tidak memerlukan** file `train.csv` mentah karena telah menggunakan data hasil agregasi dan inferensi yang tersimpan di `dashboard/data/`. Dashboard dapat langsung dijalankan setelah menginstal dependensi.

---

## 🛠️ Teknologi yang Digunakan

- **Pemodelan & Analisis Data**: Python, TensorFlow / Keras, Scikit-learn, Pandas, NumPy, Statsmodels.
- **Visualisasi & Aplikasi Web**: Streamlit, Plotly, Seaborn, Matplotlib.
- **Lingkungan Riset**: Jupyter Notebook / VS Code.

---

## 👤 Kontak & Lisensi

- **Peneliti**: Fikran Naufal
- **NIM**: 10122097
- **Institusi**: Program Studi Matematika Institut Teknologi Bandung
