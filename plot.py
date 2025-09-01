#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os

plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 16,
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 12,
})

# ------------------------------------------------------------
# 1️⃣ Time-series comparison plot
# ------------------------------------------------------------
def plot_combined_timeseries(
    df,
    pred_cols,
    wrf_cols,
    col_aws="AWS",
    col_imd="IMD",
    save_folder=".",
    save_prefix="Predicted"
):
    """Plot statistical, WRF, AWS, and IMD timeseries + errors."""

    global_min, global_max = df["Datetime"].min(), df["Datetime"].max()

    for pred_col, wrf_col in zip(pred_cols, wrf_cols):

        # Restrict subset where prediction exists
        df_sub = df.loc[df[pred_col].notna(), ["Datetime", pred_col, col_aws, col_imd, wrf_col]].copy()
        start_date = df_sub["Datetime"].min()

        # Filter AWS/IMD from start_date
        df_aws = df.loc[df["Datetime"] >= start_date, ["Datetime", col_aws, col_imd]]

        fig, axs = plt.subplots(3, 1, figsize=(16, 15), sharex=True)

        # --- (1) Rainfall Timeseries
        axs[0].plot(df_sub["Datetime"], df_sub[pred_col], color="blue", marker="o",
                    label=f"{pred_col} (Statistical Model)(00–23:59 hrs)")
        axs[0].plot(df_sub["Datetime"], df_sub[col_aws], color="black", linestyle="--",
                    label=f"{col_aws} (Zomato)(00–23:59 hrs)")
        axs[0].scatter(df_sub["Datetime"], df_sub[col_imd], color="deeppink", marker="*",
                       s=120, label="IMD_AWS (08:30–08:30 hrs)")
        axs[0].plot(df_sub["Datetime"], df_sub[wrf_col], color="seagreen", marker="o",
                    label=f"{wrf_col} (WRF Hydro)(00–23:59 hrs)")

        axs[0].set_ylabel("Rainfall (mm)")
        axs[0].set_title(f"{pred_col} vs Zomato vs IMD vs WRF (Ahmedabad)")
        axs[0].legend(loc="upper left")
        axs[0].grid(True)

        max_val = df_sub[[pred_col, wrf_col, col_aws, col_imd]].max().max()
        axs[0].set_ylim(0, max_val + 10)

        # --- (2) Error (model - AWS)
        error_model = df_sub[pred_col] - df_sub[col_aws]
        error_wrf = df_sub[wrf_col] - df_sub[col_aws]

        axs[1].bar(df_sub["Datetime"] - pd.Timedelta(days=0.15), error_model, width=0.3,
                   color="red", label=f"Error {pred_col}")
        axs[1].bar(df_sub["Datetime"] + pd.Timedelta(days=0.15), error_wrf, width=0.3,
                   color="seagreen", label=f"Error {wrf_col}")

        axs[1].axhline(0, color="black", linewidth=1.2)
        axs[1].set_ylabel("Error (mm)")
        axs[1].set_title(f"Error: {pred_col} vs Zomato_{col_aws}")
        axs[1].legend(loc="upper left")
        axs[1].grid(True)

        # --- (3) % Error
        pct_error_model = np.where(df_sub[col_aws] != 0, error_model / df_sub[col_aws], 0)
        pct_error_wrf = np.where(df_sub[col_aws] != 0, error_wrf / df_sub[col_aws], 0)

        axs[2].bar(df_sub["Datetime"] - pd.Timedelta(days=0.15), pct_error_model, width=0.3,
                   color="orange", label=f"% Error {pred_col}")
        axs[2].bar(df_sub["Datetime"] + pd.Timedelta(days=0.15), pct_error_wrf, width=0.3,
                   color="seagreen", label=f"% Error {wrf_col}")

        axs[2].axhline(0, color="black", linewidth=1.2)
        axs[2].set_ylabel("Error Fraction")
        axs[2].set_title(f"% Error: ({pred_col} - AWS) / AWS")
        axs[2].legend(loc="upper left")
        axs[2].grid(True)

        # --- Shared X-axis formatting
        for ax in axs:
            ax.set_xlim(global_min, global_max)
            locator = mdates.DayLocator(interval=3)
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            ax.tick_params(axis="x", rotation=90)

        fig.supxlabel("Datetime", fontsize=14)
        plt.tight_layout(rect=[0, 0, 1, 0.97])

        save_name = os.path.join(save_folder, f"{save_prefix}_{pred_col}_comparison.png")
        plt.savefig(save_name, dpi=300)
        plt.close(fig)

        print(f"✅ Saved timeseries plot: {save_name}")


# ------------------------------------------------------------
# 2️⃣ Metrics bar plot
# ------------------------------------------------------------
def plot_metrics_combined(metrics_df, threshold, save_folder):
    """Plot Recall, Precision, F1 for Statistical vs WRF in one plot."""

    labels = ["Day 1", "Day 2", "Day 3"]
    metrics = ["Recall", "Precision", "F1"]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]  # one color per metric

    x = np.arange(len(labels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(12, 6))

    # --- Extract values
    stat_vals = metrics_df[metrics_df["Model"] == "Statistical"].set_index("Lead").loc[labels][metrics].values
    wrf_vals = metrics_df[metrics_df["Model"] == "WRF"].set_index("Lead").loc[labels][metrics].values

    # --- Bars (Statistical model)
    for i, metric in enumerate(metrics):
        positions = x + (i - 1) * width
        ax.bar(positions, stat_vals[:, i], width, color=colors[i], label=f"{metric} (Statistical)" if i == 0 else "")

        # Annotate bars
        for j, xpos in enumerate(positions):
            val = stat_vals[j, i]
            ax.annotate(f"{val:.2f}", xy=(xpos, val), xytext=(0, 3),
                        textcoords="offset points", ha="center", fontsize=10)

        # WRF markers
        for j, xpos in enumerate(positions):
            wrf_val = wrf_vals[j, i]
            ax.plot(xpos, wrf_val, marker="*", color="red", markersize=9,
                    label="WRF metrics" if (i == 0 and j == 0) else "")

    ax.set_ylabel("Performance Score")
    ax.set_title(f"Event-based Metrics (Threshold ≥ {threshold} mm)", fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, max(stat_vals.max(), wrf_vals.max()) + 0.3)
    ax.legend()

    plt.tight_layout()
    save_path = os.path.join(save_folder, f"Performance_Metrics_{threshold}mm.png")
    plt.savefig(save_path, dpi=300)
    plt.close(fig)

    print(f"✅ Saved metrics plot: {save_path}")

