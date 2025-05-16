import pandas as pd
import numpy as np


def merge_and_clean(cases_df, vaccines_df):
    # Scalanie danych
    merged_df = pd.merge(
        cases_df,
        vaccines_df.groupby("date")["vaccines"].sum().reset_index(),
        on="date",
        how="left"
    )

    # Czyszczenie danych
    merged_df["vaccines"] = merged_df["vaccines"].fillna(0)
    merged_df = merged_df[merged_df["cases"] > 0]

    # Obliczanie nowych metryk
    merged_df["mortality_rate"] = np.round(
        (merged_df["deaths"] / merged_df["cases"]) * 100, 2
    )

    # Wykrywanie outlierów
    q = merged_df["cases"].quantile(0.99)
    return merged_df[merged_df["cases"] < q]


def calculate_statistics(df):
    # Zmiana 'M' na 'ME' zgodnie z nową konwencją pandas
    stats = df.groupby(pd.Grouper(key="date", freq="ME")).agg({
        "cases": "sum",
        "deaths": "sum",
        "vaccines": "sum",
        "mortality_rate": "mean"
    })
    return stats.reset_index()