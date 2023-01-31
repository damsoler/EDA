from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd
import requests


####################################################
#             ENMASCARAR DIRECCION MAC             #
#          para evitar bloqueo de idealista        #
#                  a la consulta                   #              
####################################################


url = "https://www.idealista.com/sala-de-prensa/informes-precio-vivienda/alquiler/comunitat-valenciana/historico/"
response = requests.get(url)
print(response) 

driver = webdriver.Chrome(ChromeDriverManager().install())
url = "https://www.idealista.com/sala-de-prensa/informes-precio-vivienda/alquiler/comunitat-valenciana/report/"
driver.get(url)
time.sleep(10)
Cookies = driver.find_element(by= By.XPATH,value="/html/body/div[1]/div/div/div/div/div[2]/button[2]")
Cookies.click()
time.sleep(5)

soup = bs(driver.page_source,"lxml")



####################################################
#   el soup avanza en intervalos de 7, por lo que  #
#      los slicings deben hacerse en bucles de     #
#             (i*7-"elemento a acceder")           #              
####################################################
soup2 = soup.select("td.table__cell")
def extraer_porcentaje(df,columna):
    if columna == "Variacion_trimestral(%)":
        r = 4
    elif columna == "Variacion_anual(%)":
        r = 3
    elif columna == "Variacion_Maximo(%)":
        r = 1

    if df[i*7-r].get_text().split()[0] == "n.d.":
        d.setdefault(columna, []).append(0)
    elif df[i*7-r].get_text().split()[0] == "0,0":
        d.setdefault(columna, []).append(0)
    else:
        d.setdefault(columna, []).append(eval(df[i*7-r].get_text().split()[0] + df[i*7-r].get_text().split()[1].replace(",", ".")))



d = {}
#for i in range(int(len(soup2)/7)):
for i in range(1,134): 
    d.setdefault("Localidad",  []).append(soup2[i*7-7].get_text())
    d.setdefault("Precio_(€/m2)" , []).append(soup2[i*7-6].get_text().split()[0])
    extraer_porcentaje(soup2,"Variacion_trimestral(%)")
    extraer_porcentaje(soup2,"Variacion_anual(%)") 
    d.setdefault("Maximo_historico(€/m2)",  []).append(soup2[i*7-2].get_text().split()[0])
    extraer_porcentaje(soup2,"Variacion_Maximo(%)")
    


TABLA_PROP_INTERANUAL = pd.DataFrame(d)
TABLA_PROP_INTERANUAL.to_csv ('tabla_idealista.csv')