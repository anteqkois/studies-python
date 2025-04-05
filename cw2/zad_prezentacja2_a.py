import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import re

# zad 1
url = "https://pl.wikipedia.org/wiki/Lista_najwi%C4%99kszych_przedsi%C4%99biorstw"

# Pobieram treść ze strony
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Szukam tabel
tables = soup.find_all('table', class_='wikitable')

# Sprawdzam ile tabel zostało znaleźionych
print(len(tables))
# Mamy tylko jedną tabelę

table = tables[0]

# Wyodrębniam wiersze i komórki
rows = table.find_all('tr')
data = []
for row in rows[1:]:  # pomijam pierwszy wiersz nagłówka
    cells = row.find_all('td')

    # Nazwa przedsiębiorstwa
    enterprise = cells[1].get_text(strip=True)

    # Komórka z miastem i krajem
    # Kraj jest zazwyczaj w ostatnim linku (<a>) w tej komórce:
    links_in_cell = cells[6].find_all('a')
    if links_in_cell:
        country = links_in_cell[-1].get_text(strip=True)
    else:
        # gdyby z jakiegoś powodu linków nie było
        country = cells[6].get_text(strip=True)

    # Przychód jest w komórce nr. 4
    revenue_text = cells[3].get_text(strip=True)
    # print(cells)


    # Usuwamy zbędne znaki (np. spacje, znak miliarda itd.) – w zależności od tego, jak kolumna jest sformatowana:
    # Na potrzeby przykładu – wyciągnijmy tylko liczby z tekstu:
    match = re.search(r'(\d+(?:[.,]\d+)*)', revenue_text)
    if match:
        # Zamieniamy ewentualny przecinek na kropkę, by poprawnie konwertować na float
        numeric_value_str = match.group(1).replace(',', '.')
        try:
            revenue = float(numeric_value_str)
        except ValueError:
            revenue = 0.0
    else:
        revenue = 0.0

    data.append((country, revenue))

# Tworzę data frame i grupuję przychody według kraju
df = pd.DataFrame(data, columns=['Country', 'Revenue'])
grouped = df.groupby('Country', as_index=False)['Revenue'].sum()

# Rysuję wykres
plt.figure(figsize=(10, 6))
plt.bar(grouped['Country'], grouped['Revenue'])
plt.xticks(rotation=90)
plt.title("Suma wartości (np. przychodów) największych przedsiębiorstw wg kraju")
plt.xlabel("Kraj")
plt.ylabel("Suma przychodów (wartość przykładowa)")
plt.tight_layout()
plt.show()