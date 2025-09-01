#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import pandas as pd
from config import zomato_folder, zomato_output

def list_csv_files(folder_path):
    return [f for f in os.listdir(folder_path) if f.endswith('.csv')]

def read_and_process_csv(file_path):
    df = pd.read_csv(file_path)
    df['device_date_time'] = pd.to_datetime(df['device_date_time'], errors='coerce')
    return df

def load_all_data(folder_path):
    csv_files = list_csv_files(folder_path)
    df_list = [read_and_process_csv(os.path.join(folder_path, f)) for f in csv_files]
    return pd.concat(df_list, ignore_index=True)

def process_zomato_data():
    df = load_all_data(zomato_folder)
    pivot_df = df.pivot_table(
        index='device_date_time',
        columns='locality_name',
        values='rain_intensity',
        aggfunc='mean'
    ).sort_index()

    daily_df = pivot_df.resample('D').sum().iloc[13:, :]
    daily_df['Ahmedabad_City'] = daily_df.mean(axis=1)

    daily_df = daily_df.reset_index()
    daily_df['DateTime'] = pd.to_datetime(daily_df['device_date_time']).dt.strftime("%Y-%m-%d")
    daily_df = daily_df.set_index('DateTime')

    if os.path.exists(zomato_output):
        existing_df = pd.read_excel(zomato_output, index_col=0)
        existing_df.index = pd.to_datetime(existing_df.index).strftime("%Y-%m-%d")
        daily_df = daily_df[~daily_df.index.isin(existing_df.index)]
        updated_df = pd.concat([existing_df, daily_df])
    else:
        updated_df = daily_df

    updated_df.to_excel(zomato_output)
    print(f"✅ Updated Zomato Excel")
    return updated_df

