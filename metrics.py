#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np

def calculate_metrics(pred, obs, threshold):
    event_obs = obs >= threshold
    event_pred = pred >= threshold
    hits = (event_pred & event_obs).sum()
    misses = (~event_pred & event_obs).sum()
    false_alarms = (event_pred & ~event_obs).sum()

    recall = hits / (hits + misses) if (hits + misses) else 0
    precision = hits / (hits + false_alarms) if (hits + false_alarms) else 0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0
    return recall, precision, f1

def compute_metrics_table(df, stat_cols, wrf_cols, obs_col, threshold):
    results = []
    for lead, stat_col, wrf_col in zip(['Day 1', 'Day 2', 'Day 3'], stat_cols, wrf_cols):
        r1, p1, f1_1 = calculate_metrics(df[stat_col], df[obs_col], threshold)
        r2, p2, f1_2 = calculate_metrics(df[wrf_col], df[obs_col], threshold)
        results.append(['Statistical', lead, r1, p1, f1_1])
        results.append(['WRF', lead, r2, p2, f1_2])
    return pd.DataFrame(results, columns=['Model', 'Lead', 'Recall', 'Precision', 'F1'])

