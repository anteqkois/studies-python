import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

url = "https://www.polskawliczbach.pl/najszybciej_wyludniajace_sie_miasta_w_polsce"

# Uruchamimam przeglądarkę
driver = webdriver.Chrome(ChromeDriverManager().install())

# Wchodzę na stronę
driver.get(url)

# Sprawdzam tytuł strony
print("Tytuł strony:", driver.title)

# Odnajduję tabelę
tabela_element = driver.find_element(By.XPATH, "//*[@id='lstTab']")

# Przewinjam do elementu tabeli, wówczas JS może załadować dane
driver.execute_script("arguments[0].scrollIntoView(true);", tabela_element)

# Czekam (max 10 sekund) aż pojawią się wiersze w tabeli
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lstTab"]/tbody/tr')))

# Pobieram kontent html
dfs = pd.read_html(tabela_element.get_attribute('outerHTML'))
table = pd.DataFrame(dfs[0])

print(table)
print("Tabela ma kształt:", table.shape)

# Zapisuję do pliku CSV
table.to_csv("wyludnienie.csv", index=False, encoding='utf-8')

driver.close()