#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os

# 📂 Ask user for base folders
imd_raw_folder = input("Enter path to IMD raw JSON folder: ").strip()
project_base   = input("Enter path to project base folder: ").strip()

#imd_raw_folder = "/home/subhojit/IMD_API"
#project_base ="/home/subhojit/Githubs_Code_RUVISION_Final

# 📂 Derived folders
plot_dir    = os.path.join(project_base, "Plot")
data_folder = os.path.join(plot_dir, "U1000_V1000_Prec")

# 📄 File paths
imd_output_excel = os.path.join(data_folder, "IMD_Rainfall_Data.xlsx")
zomato_folder    = os.path.join(project_base, "weatherunion_data")
zomato_output    = os.path.join(data_folder, "DailyRain_Ahmedabad.xlsx")
wrf_file         = os.path.join(data_folder, "file.xlsx")

files = sorted([os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith('.xlsx')])

# ⚙️ Parameters
threshold = 25

# ✅ Auto-create folders if missing
os.makedirs(data_folder, exist_ok=True)
os.makedirs(plot_dir, exist_ok=True)


# In[ ]:




