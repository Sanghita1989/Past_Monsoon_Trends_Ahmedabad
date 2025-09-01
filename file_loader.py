#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import pandas as pd
import numpy as np
from config import data_folder, imd_output_excel, wrf_file, files

def load_and_clean_excel(file, col_idx):
    """Safely load excel file and extract one column series."""
    df = pd.read_excel(file, index_col=0)
    df.index = pd.to_datetime(df.index, errors='coerce')
    df = df[~df.index.isna()]
    df = df.groupby(df.index).mean()
    col_series = df.iloc[:, col_idx]
    return col_series

def load_statistical_and_aws():
    """Load statistical model predictions + AWS observations."""
    files = sorted([os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith('.xlsx')])

    col_1 = load_and_clean_excel(files[0], 0).iloc[1:]
    col_2 = load_and_clean_excel(files[1], 0).iloc[1:]
    col_3 = load_and_clean_excel(files[2], 0).iloc[1:]
    col_4 = load_and_clean_excel(files[3], 15)  # Zomato_AWS

    combined_df = pd.concat([col_1, col_2, col_3, col_4], axis=1)
    combined_df.columns = ['Predicted_Lead Day_1', 'Predicted_Lead Day_2', 'Predicted_Lead Day_3', 'AWS']
    combined_df.index.name = 'Datetime'
    combined_df = combined_df[combined_df["AWS"].notna()]
    combined_df = combined_df.sort_index().reset_index()
    return combined_df

def load_imd():
    """Load IMD Excel file and clean NIL values."""
    imd_df = pd.read_excel(imd_output_excel, sheet_name="Sheet1")
    imd_df["Date"] = pd.to_datetime(imd_df["Date"], errors="coerce")
    imd_df["Past_24_hrs_Rainfall"] = pd.to_numeric(imd_df["Past_24_hrs_Rainfall"].replace("NIL", np.nan), errors="coerce")
    imd_df = imd_df[["Date", "Past_24_hrs_Rainfall"]].rename(columns={"Date": "Datetime", "Past_24_hrs_Rainfall": "IMD"})
    return imd_df

def load_wrf():
    """Load WRF Excel file."""
    wrf_df = pd.read_excel(wrf_file)
    wrf_df.columns = ['Datetime', 'WRF_Lead Day_1', 'WRF_Lead Day_2', 'WRF_Lead Day_3']
    wrf_df['Datetime'] = pd.to_datetime(wrf_df['Datetime'], errors='coerce')
    return wrf_df

def build_combined_dataframe():
    """Final merged dataframe with Statistical, AWS, IMD, and WRF."""
    combined_df = load_statistical_and_aws()
    imd_df = load_imd()
    wrf_df = load_wrf()

    combined_df = pd.merge(combined_df, imd_df, on="Datetime", how="left")
    combined_df = pd.merge(combined_df, wrf_df, on="Datetime", how="left")

    return combined_df

