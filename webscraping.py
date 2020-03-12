# -*- coding: utf-8 -*-

import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

# 1. Pegar conteúdo HTML a partir da URL
url = "https://stats.nba.com/players/traditional/?sort=STL&dir=-1&Season=2019-20&SeasonType=Regular%20Season&PerMode=Totals"

option = Options()
option.headless = True
driver = webdriver.Firefox()

driver.get(url)
time.sleep(10)

driver.find_element_by_xpath("//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='PTS']").click()

element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
html_content = element.get_attribute('outerHTML')

# 2. Parsear o conteúdo HTML - BeaultifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')

# 3. Estruturar conteúdo em um Data Frame - Pandas
df_full = pd.read_html( str(table) )[0].head(10)
df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', 'PTS']]
df.columns = ['pos', 'player', 'team', 'total']

print(df)
# 4. Transformar os Dados em um Dicionário de dados próprio
driver.quit()
# 5. Converter e salvar em um arquivo JSON