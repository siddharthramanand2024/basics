#  Weather Dataset & Analytics

A production-quality weather data analytics application built with
**Python**, **Faker**, **Pandas**, and **Streamlit**.

This project generates a large synthetic weather dataset,
performs comprehensive data analysis, and provides an interactive
dashboard for exploring weather patterns across Indian cities.

---

##  Project Overview

| Component | Description |
|-----------|-------------|
| **Dataset Generator** | OOP-based synthetic data using Faker (~8,760 records) |
| **Pandas Analysis** | Comprehensive notebook with 13 analysis sections |
| **Streamlit Dashboard** | Interactive web dashboard with charts and search |

---

##  Project Structure

```
basics/
│
├── app/                              # Previous Weather CLI (merged)
├── datasets/
│   ├── weather_dataset.csv           # Generated synthetic dataset
│   └── weather_dataset_cleaned.csv   # Cleaned & enriched dataset
│
├── generate_weather_dataset.py       # OOP dataset generator
├── streamlit_app.py                  # Streamlit dashboard
├── weather_analysis.ipynb            # Pandas analysis notebook
├── pyproject.toml                    # Project config & dependencies
├── README.md
└── uv.lock
```

---

##  Getting Started

### Prerequisites

You only need [uv](https://docs.astral.sh/uv/) installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation

```bash
git clone https://github.com/siddharthramanand2024/basics.git
cd basics
uv sync
```

### Generate the Dataset

```bash
uv run python generate_weather_dataset.py
```

This creates `datasets/weather_dataset.csv` with ~8,760 hourly
weather observations.

### Run the Streamlit Dashboard

```bash
uv run streamlit run streamlit_app.py
```

### Run the Jupyter Notebook

```bash
uv run jupyter notebook weather_analysis.ipynb
```

---

##  Dataset Details

| Field | Description | Example |
|-------|-------------|---------|
| `date` | Observation date | 2025-04-10 |
| `time` | Hour of observation | 13:00 |
| `city` | Indian city | Hyderabad |
| `temperature` | Temperature (°C) | 34.6 |
| `humidity` | Humidity (%) | 57 |
| `wind_speed` | Wind speed (km/h) | 12.3 |
| `pressure` | Atmospheric pressure (hPa) | 1008.4 |
| `rainfall` | Rainfall (mm) | 0.0 |
| `uv_index` | UV index (0–12) | 8 |
| `air_quality` | Air Quality Index | 72 |

**Cities:** Hyderabad, Mumbai, Delhi, Bangalore, Chennai

**Date Range:** January 1, 2025 – December 31, 2025

---

##  Analysis Notebook Sections

1. **Reading** — `read_csv()`
2. **Inspection** — `head()`, `tail()`, `sample()`, `shape`,
   `columns`, `dtypes`, `info()`, `describe()`
3. **Cleaning** — missing values, duplicates, `fillna()`,
   `astype()`, `rename()`
4. **Feature Engineering** — daily averages, temperature categories,
   month, weekday
5. **Filtering** — by temperature, humidity, rainfall, city, month
6. **Statistics** — mean, median, mode, variance, std, min, max
7. **Percentiles** — P90, P95, P99
8. **Ranking** — 7th highest (`nlargest`), 3rd lowest (`nsmallest`)
9. **GroupBy** — monthly averages by metric
10. **Pivot Table** — temperature by month and city
11. **Sorting** — hottest and coldest records
12. **Dynamic Queries** — reusable functions for date and
    date+time lookup
13. **Export** — cleaned dataset to CSV

---

##  Streamlit Dashboard

The dashboard provides five interactive sections:

- **Dataset Overview** — Browse and filter the full dataset
- **Search** — Look up daily averages or exact records
- **Statistics** — Descriptive stats and percentiles (P90/P95/P99)
- **Ranking** — 7th highest and 3rd lowest temperature records
- **Charts** — Temperature, humidity, and rainfall trends;
  monthly comparisons; histograms

---

## Technologies

- **Python 3.14**
- **Faker** — Synthetic data generation
- **Pandas** — Data manipulation and analysis
- **NumPy** — Numerical operations
- **Streamlit** — Interactive dashboard
- **Plotly** — Data visualization
- **Jupyter** — Notebook environment
- **uv** — Package management

---
