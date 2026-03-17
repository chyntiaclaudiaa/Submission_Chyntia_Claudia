# E-Commerce Public Dataset Analysis 📊

Dashboard ini adalah proyek akhir dari kelas "Belajar Analisis Data dengan Python" di Dicoding. Dashboard ini memberikan wawasan mendalam mengenai performa e-commerce melalui visualisasi tren penjualan, performa produk, dan segmentasi pelanggan menggunakan analisis RFM (Recency, Frequency, & Monetary).

## Link Dashboard Streamlit
Dashboard yang telah dideploy dapat diakses melalui tautan berikut:
[https://submissionchyntiaclaudia-hhsgmcmcbnoyxgbeccheny.streamlit.app/](https://submissionchyntiaclaudia-hhsgmcmcbnoyxgbeccheny.streamlit.app/)

## Struktur Proyek
- `dashboard/`: Direktori yang berisi file utama aplikasi.
  - `dashboard.py`: File utama untuk menjalankan aplikasi Streamlit.
  - `main_data.csv`: Dataset yang telah diproses untuk visualisasi.
- `notebook.ipynb`: File Jupyter Notebook yang berisi proses Exploratory Data Analysis (EDA).
- `requirements.txt`: Daftar pustaka (library) Python yang diperlukan.
- `README.md`: Dokumentasi petunjuk penggunaan ini.

## Menjalankan Dashboard Secara Lokal

### 1. Setup Environment - Anaconda
```shell
conda create --name ds-submission python=3.9
conda activate ds-submission
pip install -r requirements.txt
```

### 2. Setup Environment - Shell/Terminal (Python Virtual Environment)
```shell
mkdir submission_chyntia_claudia
cd submission_chyntia_claudia
pipenv install
pipenv shell
pip install -r requirements.txt
```

### 3. Menjalankan Aplikasi Streamlit
```Shell
streamlit run dashboard/dashboard.py
```
