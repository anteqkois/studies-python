import pandas as pd
import numpy as np
import random

print("Zadanie 1\n")
bankruptcy = pd.read_csv("./bankruptcy.csv")

# print(bankruptcy.dtypes)

# Losuję 2 kolumny z zakresu 1-6 zawierające dane numeryczne
numeric_cols = bankruptcy.select_dtypes(include=[np.number]).columns.tolist()
selected_cols = random.sample(numeric_cols, 2)

# Dodaje braki danych
for col in selected_cols:
    bankruptcy.loc[random.sample(range(len(bankruptcy)), 2), col] = np.nan

print("Statystyki opisowe:")
print(bankruptcy.describe())

# Uzupełniam braki danych średnią
for col in selected_cols:
    bankruptcy[col] = bankruptcy[col].fillna(bankruptcy[col].mean())

# Zapisuję finalny plik
bankruptcy.to_csv("bankruptcy_uzupelnione.csv", index=False)

print("\nZadanie 2\n")
from scipy.spatial.distance import cdist

# Losuję 2 kolumny z zakresu 1-6 zawierające dane numeryczne
numeric_cols = bankruptcy.select_dtypes(include=[np.number]).columns.tolist()
selected_cols = random.sample(numeric_cols, 2)

# Dodaje braki danych
for col in selected_cols:
    bankruptcy.loc[random.sample(range(len(bankruptcy)), 2), col] = np.nan
    
# Unitaryzacja kolumny z zakresu 1:5, które NIE mają braków danych
# Zbieram kolumny, które nie mają braków danych
unitary_cols = []
for col in bankruptcy.columns[0:5]:
    if bankruptcy[col].isna().sum() == 0 and pd.api.types.is_numeric_dtype(bankruptcy[col]):
        unitary_cols.append(col)

# Unitaryzuję tylko wybrane kolumny
bankruptcy_uni = bankruptcy.copy()
for col in unitary_cols:
    min_val = bankruptcy[col].min()
    max_val = bankruptcy[col].max()
    bankruptcy_uni[col] = (bankruptcy[col] - min_val) / (max_val - min_val)

# Funkcja która wypisuje trzy wiersze najbliższe szukanemu
def find_min_dist_row_idx(df, row_idx, k=3):
    row = df.iloc[row_idx]
    ignored_col_names = row[row.isna()].index
    
    # pomiń kolumny z nan
    df = df.drop(ignored_col_names, axis=1)
    row = df.iloc[row_idx]
    
    # policz odległości - ignoruj unnamed (błąd przy wczytaniu oraz nazwę)
    dists = cdist([row[1:]], df.iloc[:, 1:])[0]
    min_dist_idx = dists.argsort()[:k + 1]
    return np.delete(min_dist_idx, np.where(min_dist_idx == row_idx))

# Dla każdego wiersza z brakami wypełniam je średnią z 3 najbliższych (po unitaryzacji)
filled_bankruptcy = bankruptcy.copy()

rows_with_na = bankruptcy[selected_cols].isna().any(axis=1)

print(bankruptcy_uni.dtypes)
numeric_cols = bankruptcy_uni.select_dtypes(include=[np.number]).columns.tolist()

for row_idx in bankruptcy[rows_with_na].index:
    neighbors_idx = find_min_dist_row_idx(bankruptcy_uni[numeric_cols], row_idx, k=3)

    for col in selected_cols:
        if pd.isna(bankruptcy.loc[row_idx, col]):
            filled_bankruptcy.loc[row_idx, col] = bankruptcy.loc[neighbors_idx, col].mean(skipna=True)

# Przedstawiam statystyki opisowe PRZED i PO uzupełnieniu danych
print("Statystyki PRZED:")
print(bankruptcy.describe())

print("\nStatystyki PO:")
print(filled_bankruptcy.describe())
    
