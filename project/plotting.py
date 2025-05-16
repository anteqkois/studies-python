import matplotlib.pyplot as plt
import seaborn as sns

def plot_global_trend(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x="date", y="cases", label="Przypadki", ax=ax)
    sns.lineplot(data=df, x="date", y="vaccines", label="Szczepienia", ax=ax)
    ax.set_title("Globalny trend COVID-19")
    ax.set_ylabel("Liczba")
    plt.xticks(rotation=45)
    return fig


def plot_mortality_rate(df):
    fig, ax = plt.subplots(figsize=(12, 6))

    # Poprawiona składnia barplot z hue i legend=False
    sns.barplot(
        data=df,
        x=df["date"].dt.strftime("%Y-%m"),
        y="mortality_rate",
        hue=df["date"].dt.strftime("%Y-%m"),
        palette="viridis",
        legend=False
    )

    ax.set_title("Śmiertelność miesięczna")
    ax.set_ylabel("Śmiertelność (%)")
    plt.xticks(rotation=90)
    return fig