# ☀️ TFT + TDA Solar Energy Forecasting Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://solar-power-forecasting-tft-cgjvjsfv4rnxes4tmobhdq.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![PyTorch Forecasting](https://img.shields.io/badge/Model-Temporal%20Fusion%20Transformer-orange.svg)

An interactive web dashboard and probabilistic forecasting framework for **short-term solar power generation**, combining **Temporal Fusion Transformers (TFT)**, **Topological Data Analysis (TDA)**, and **Conformal Prediction**.

🔗 **Live Demo:** [Launch the Solar Energy Forecasting Dashboard](https://solar-power-forecasting-tft-cgjvjsfv4rnxes4tmobhdq.streamlit.app)

---

## 🎯 Why This Project Matters
Standard solar forecasting models (such as XGBoost or Random Forest) achieve high average accuracy (~96%) on clear, sunny days but fail during sudden weather volatility—and only output single-number point estimates. Real-world power grids need to know the **margin of risk** to dispatch backup battery storage safely.

This architecture solves that gap through three core components:
* **Topological Data Analysis (TDA):** Extracts geometric weather volatility features ($H_0$ and $H_1$ persistence entropy) over sliding time windows to flag sudden cloud cover and atmospheric turbulence early.
* **Temporal Fusion Transformer (TFT):** Uses Multi-Head Attention to dynamically shift feature weights toward turbulent weather variables during volatile conditions while maintaining full feature interpretability.
* **Conformal Prediction:** Generates mathematically calibrated **90% Confidence Intervals** (5th and 95th percentiles) that widen dynamically during weather chaos and tighten during clear skies.

---

## ✨ Dashboard Features
* **Selectable Forecast Horizons:** Toggle between **1-Week** and **1-Month** high-resolution (5-minute interval) solar generation forecasts.
* **Probabilistic Visualization:** Interactive active power output charts plotting the TFT median forecast alongside shaded 90% Conformal Prediction bounds.
* **Daily Energy Yield Breakdown:** Automated day-by-day summary table calculating projected energy output in **kWh**.
* **System KPIs:** Real-time overview of peak expected generation, cumulative energy yield, and maximum plant capacity.

---

## 🛠️ Tech Stack
* **Deep Learning & Forecasting:** PyTorch Forecasting (Temporal Fusion Transformer), Conformal Prediction
* **Feature Engineering:** Topological Data Analysis (`ripser` / Vietoris-Rips persistence diagrams)
* **Frontend & Deployment:** Streamlit, Streamlit Community Cloud
* **Data & Visualization:** Pandas, NumPy, Matplotlib

---

## 📂 Repository Structure
```text
solar-power-forecasting-tft/
├── app.py               # Streamlit web dashboard application
├── requirements.txt     # Python dependencies for cloud/local deployment
└── README.md            # Project documentation
