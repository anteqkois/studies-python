from data_loader import fetch_covid_data, process_covid_data
from data_processing import merge_and_clean, calculate_statistics
from plotting import plot_global_trend, plot_mortality_rate
import matplotlib.pyplot as plt


def main():
    print("Rozpoczęcie analizy danych COVID-19...")

    # Pobieranie i przetwarzanie danych
    print("Pobieranie danych z API...")
    cases_data, vaccines_data = fetch_covid_data()
    cases_df, vaccines_df = process_covid_data(cases_data, vaccines_data)

    # Czyszczenie i scalanie
    print("Przetwarzanie danych...")
    merged_df = merge_and_clean(cases_df, vaccines_df)
    stats_df = calculate_statistics(merged_df)

    # Wyświetlanie statystyk
    print("Statystyki miesięczne:\n")
    print(stats_df.describe())

    # Generowanie wykresów
    print("Wykresy\n")
    fig1 = plot_global_trend(stats_df)
    fig2 = plot_mortality_rate(stats_df)

    # Wyświetlanie wykresów
    plt.show()


if __name__ == "__main__":
    main()