#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import json
import pandas as pd
from datetime import datetime
from config import imd_raw_folder, imd_output_excel

def process_imd_data(imd_raw_folder, imd_output_excel):
    """
    Process IMD AWS JSON files stored in daily subfolders
    and update Excel file with the latest data.
    """
    rows = []
    for subfolder in os.listdir(imd_raw_folder):
        folder_path = os.path.join(imd_raw_folder, subfolder)
        if os.path.isdir(folder_path):
            try:
                folder_date = datetime.strptime(subfolder, "%Y-%m-%d").date()
                json_file = os.path.join(folder_path, "city_weather_forecast.json")

                if os.path.exists(json_file):
                    with open(json_file, "r") as f:
                        data = json.load(f)

                    if isinstance(data, list) and len(data) > 0:
                        record = data[0]
                        rainfall = record.get("Past_24_hrs_Rainfall", None)
                        station = record.get("Station_Name", None)
                    else:
                        rainfall, station = None, None

                    rows.append([folder_date, station, rainfall])
            except Exception as e:
                print(f"⚠️ Skipped {subfolder}: {e}")

    # Convert to DataFrame
    df_new = pd.DataFrame(rows, columns=["Date", "Station_Name", "Past_24_hrs_Rainfall"]).sort_values("Date")
    if df_new.empty:
        print("⚠️ No data found in subfolders.")
        return None

    # Keep only the latest date's data
    last_date = df_new["Date"].max()
    df_latest = df_new[df_new["Date"] == last_date]

    # Merge with existing Excel if it exists
    if os.path.exists(imd_output_excel):
        df_existing = pd.read_excel(imd_output_excel)
        df_existing["Date"] = pd.to_datetime(df_existing["Date"]).dt.date
        df_existing = df_existing[df_existing["Date"] != last_date]
        df_final = pd.concat([df_existing, df_latest], ignore_index=True)
    else:
        df_final = df_latest

    # Save final DataFrame
    df_final["Date"] = pd.to_datetime(df_final["Date"]).dt.date
    df_final.to_excel(imd_output_excel, index=False)

    print(f"✅ Updated Excel with data from {last_date}! Saved to {imd_output_excel}")
    return df_final

