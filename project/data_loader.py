import pandas as pd
import requests
from datetime import datetime


def fetch_covid_data():
    # Pobieranie danych o przypadkach
    cases_url = "https://disease.sh/v3/covid-19/historical/all?lastdays=all"
    cases_data = requests.get(cases_url).json()

    # Pobieranie danych o szczepieniach
    vaccines_url = "https://disease.sh/v3/covid-19/vaccine/coverage/countries?lastdays=all"
    vaccines_data = requests.get(vaccines_url).json()

    return cases_data, vaccines_data


def process_covid_data(cases_data, vaccines_data):
    # Przetwarzanie danych o przypadkach
    # print(list(cases_data["cases"].keys())[:5])
    cases_df = pd.DataFrame({
        "date": pd.to_datetime(list(cases_data["cases"].keys()), format="%m/%d/%y"),
        "cases": list(cases_data["cases"].values()),
        "deaths": list(cases_data["deaths"].values())
    })

    # Przetwarzanie danych o szczepieniach
    vaccines_df = pd.DataFrame()
    for country in vaccines_data:
        country_df = pd.DataFrame({
            "date": pd.to_datetime(list(country["timeline"].keys()), format="%m/%d/%y"),
            "country": country["country"],
            "vaccines": list(country["timeline"].values())
        })
        vaccines_df = pd.concat([vaccines_df, country_df])

    return cases_df, vaccines_df