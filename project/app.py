import pandas as pd
import streamlit as st
from data_loader import fetch_covid_data, process_covid_data
from data_processing import merge_and_clean, calculate_statistics
from plotting import plot_global_trend, plot_mortality_rate

st.set_page_config(page_title="COVID-19 Analysis", layout="wide")
st.title("Analiza danych COVID-19")

# Pobieranie i przetwarzanie danych
cases_data, vaccines_data = fetch_covid_data()
cases_df, vaccines_df = process_covid_data(cases_data, vaccines_data)
merged_df = merge_and_clean(cases_df, vaccines_df)
stats_df = calculate_statistics(merged_df)

# Kontrolki w sidebarze
st.sidebar.header("Filtry")
start_date = st.sidebar.date_input("Data początkowa", merged_df["date"].min())
end_date = st.sidebar.date_input("Data końcowa", merged_df["date"].max())

# Filtrowanie danych
filtered_df = stats_df[
    (stats_df["date"] >= pd.to_datetime(start_date)) &
    (stats_df["date"] <= pd.to_datetime(end_date))
]

# Prezentacja wyników
col1, col2 = st.columns(2)
with col1:
    st.subheader("Statystyki globalne")
    st.dataframe(filtered_df.style.background_gradient(cmap="YlOrRd"))

with col2:
    st.subheader("Wskaźniki")
    st.metric("Łączna liczba przypadków", f"{int(filtered_df['cases'].sum()):,}")
    st.metric("Łączna liczba zgonów", f"{int(filtered_df['deaths'].sum()):,}")
    st.metric("Łączna liczba szczepień", f"{int(filtered_df['vaccines'].sum()):,}")

# Wykresy
st.subheader("Wizualizacje")
st.pyplot(plot_global_trend(filtered_df))
st.pyplot(plot_mortality_rate(filtered_df))