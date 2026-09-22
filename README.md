# 👶 Provisional 2025 CDC Natality & Birth Count Dashboard

An interactive, educational Streamlit dashboard designed for **undergraduate business analytics students** to explore spatial, temporal, and demographic patterns in provisional 2025 U.S. live birth counts.

---

## 📌 Project Overview

This application visualizes provisional 2025 U.S. live birth data published by the **Centers for Disease Control and Prevention (CDC)** and the **National Center for Health Statistics (NCHS)**.

### Key Features
- **Interactive Sidebar Filtering:** Filter by 50 U.S. states + District of Columbia, chronological months (Jan–Dec), and infant sex (Female, Male, All) with one-click **Select All** and **Reset** controls.
- **Dynamic KPI Metrics Cards:** Live summaries of total selected births, national coverage percentages, monthly averages, peak birth geography, and peak birth month.
- **5 Dashboard Tabs:**
  1. **📊 Overview:** Executive summary, monthly trends, and biological sex comparison charts.
  2. **🗺️ Geographic Analysis:** Interactive U.S. choropleth map, dynamic state rankings, and volume disparity comparison (Top 5 vs. Bottom 5 geographies).
  3. **📈 Monthly & Sex Trends:** State-by-month birth density heatmap and monthly distribution variance boxplots.
  4. **📋 Data Table & Download:** Searchable, sortable data table with one-click CSV export capability.
  5. **ℹ️ About the Data:** Complete data dictionary, CDC metadata, methodology background, and student analytics exercises.

---

## ⚠️ Analytical Rule: Birth Counts vs. Birth Rates

In business analytics and epidemiology, it is critical to distinguish between **absolute counts** and **rates**:
- **Birth Counts (\(N\)):** The exact number of live births recorded in a jurisdiction. High-population states (e.g., California, Texas, Florida) naturally produce higher birth counts simply because they have larger populations.
- **Birth Rates (Per Capita):** The ratio of births relative to total population size or female population of childbearing age (e.g., crude birth rate per 1,000 residents).

> **Note:** This dataset contains **birth counts only**. All visualizations and KPI cards are strictly framed around live birth counts.

---

## 🛠️ Project Structure

```
cdc-natality-dashboard/
├── data/
│   └── Provisional_Natality_2025_CDC.xlsx  # Original CDC workbook (Read-only)
├── src/
│   ├── __init__.py
│   ├── data_loader.py       # Data ingestion, @st.cache_data, validation checks, state abbr mapping
│   ├── filters.py           # Sidebar filter UI and session state management
│   ├── kpis.py              # KPI card calculation and rendering
│   └── charts.py            # Plotly interactive visualizations
├── app.py                   # Main Streamlit application entrypoint
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation and student guide
```

---

## 🚀 How to Run Locally

### 1. Prerequisites
Ensure Python 3.10+ is installed on your machine.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Streamlit App
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 🧪 Data Audit & Validation Summary

| Metric | Validated Value | Benchmark | Status |
| :--- | :--- | :--- | :--- |
| **Total Observations** | 1,224 | 1,224 | ✅ Verified |
| **Unique Geographies** | 51 (50 States + DC) | 51 | ✅ Verified |
| **Unique Months** | 12 (January–December) | 12 | ✅ Verified |
| **Infant Sex Categories** | 2 (Female, Male) | 2 | ✅ Verified |
| **Missing Values** | 0 | 0 | ✅ Verified |
| **Duplicate Rows** | 0 | 0 | ✅ Verified |
| **Total Live Births** | 3,604,640 | 3,604,640 | ✅ Verified |

---

## 📜 License & Data Attribution
Data sourced from the **Centers for Disease Control and Prevention (CDC)** / NCHS Provisional Natality Files (2025). Built for educational and analytical study.
