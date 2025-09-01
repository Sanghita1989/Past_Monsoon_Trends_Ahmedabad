#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from parsers.imd_parser import process_imd_data
from parsers.zomato_parser import process_zomato_data
from parsers.file_loader import build_combined_dataframe
from analysis.metrics import compute_metrics_table
from analysis.plotting import plot_combined_timeseries, plot_metrics_combined
from config import plot_dir


def main():
    print("🔄 Starting rainfall prediction workflow...")

    # Step 1: Parse & update raw IMD and Zomato data
    print("📥 Processing IMD data...")
    imd_df = process_imd_data()

    print("📥 Processing Zomato AWS data...")
    zomato_df = process_zomato_data()

    # Step 2: Build combined dataframe (Statistical + AWS + IMD + WRF)
    print("📊 Building combined dataset...")
    combined_df = build_combined_dataframe()
    print(f"✅ Combined dataset shape: {combined_df.shape}")

    # Step 3: Compute event-based metrics
    print("📈 Computing performance metrics...")
    threshold = 25  # mm rainfall event threshold
    prediction_columns = ["Predicted_Lead Day_1", "Predicted_Lead Day_2", "Predicted_Lead Day_3"]
    wrf_columns = ["WRF_Lead Day_1", "WRF_Lead Day_2", "WRF_Lead Day_3"]

    metrics_df = compute_metrics_table(
        combined_df,
        prediction_columns,
        wrf_columns,
        obs_col="AWS",
        threshold=threshold
    )
    print(metrics_df)

    # Step 4: Generate plots
    print("🖼️ Generating metrics plot...")
    plot_metrics_combined(metrics_df, threshold, plot_dir)

    print("🖼️ Generating timeseries plots...")
    plot_combined_timeseries(combined_df, prediction_columns, wrf_columns, save_folder=plot_dir)

    print("🎉 Workflow complete! All outputs saved in:", plot_dir)


if __name__ == "__main__":
    main()

