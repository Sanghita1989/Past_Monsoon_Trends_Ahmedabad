# Past_Monsoon_Trends_Ahmedabad
Statistical Downscaling Model+WRF_Hydro+IMD_AWS+Zomato_AWS (Comparison Plots)

Ahmedabad_Monsoon_Project/
│── config.py # Global paths & settings
│── main.py # Orchestration script
│
│── parsers/
│ ├── imd_parser.py # IMD AWS JSON → Excel
│ ├── zomato_parser.py # Zomato AWS Station Data Processing (Daily Data)
│ ├── file_loader.py # Build combined dataframe with model outputs (Statistical Downscaling+WRF), Zomato_AWS and IMD_AWS
│
│── analysis/
│ ├── metrics.py # Recall / Precision / F1 Score
│ ├── plotting.py # Time-series & metrics plots
│
│── data/ # Raw IMD JSON / Zomato CSV/ Model Outputs (Past Data), WRF Outputs (Past Data)
│── output/ # Plots
│── README.md # Documentation

# 🌧️ Rainfall Prediction & Verification (Ahmedabad)

This project processes **AWS data (IMD & Zomato)**, combines it with **WRF model outputs** and **Statistical downscaling model predictions**, and evaluates model performance using **event-based metrics (Recall, Precision, F1 Score)**.  
It also generates **time-series comparison plots** and **metrics plots** for rainfall events.

---

## 🚀 Features
- **IMD AWS Data Preprocessing**  
  - Reads daily JSON files from IMD AWS folders  
  - Extracts rainfall & station info  
  - Updates `IMD_Rainfall_Data.xlsx`

- **Zomato AWS Data Preprocessing**  
  - Reads multiple CSV files from Zomato AWS  
  - Aggregates rainfall data into daily sums  
  - Computes Ahmedabad City average  
  - Updates `DailyRain_Ahmedabad.xlsx`

- **Data Integration**  
  - Combines Statistical model predictions, AWS, IMD, and WRF Hydro outputs  
  - Produces a unified dataframe for analysis

- **Performance Metrics**  
  - Calculates Recall, Precision, and F1-score for rainfall events above a configurable threshold  
  - Compares Statistical vs WRF models

- **Visualization**  
  - 📈 Time-series plots: Predictions vs Observed (AWS, IMD, WRF)  
  - 📊 Metrics bar plots with side-by-side comparison  

---

## 📂 Project Structure
