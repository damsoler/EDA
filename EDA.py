import numpy as np
import pandas as pd
import os
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 20)

# RENTAL
alq_alicante = pd.read_excel("raw/ALQ_COM_VALENCIANA.xlsx", sheet_name="ALQ_ALICANTE")
alq_castellon = pd.read_excel("raw/ALQ_COM_VALENCIANA.xlsx", sheet_name="ALQ_CASTELLON")
alq_valencia = pd.read_excel("raw/ALQ_COM_VALENCIANA.xlsx", sheet_name="ALQ_VALENCIA")
idealista_table = pd.read_csv("idealista_localidades_cv.csv")

### VALENCIA
alq_valencia = alq_valencia.drop('unidad',axis=1)
alq_valencia["date"]= pd.to_datetime(alq_valencia.Mes)
alq_valencia = alq_valencia.drop('Mes',axis=1)
alq_valencia.set_index("date", inplace=True)
alq_valencia = alq_valencia.sort_index(ascending=True)
alq_valencia = alq_valencia.rename(str.lower, axis='columns')
first_price = alq_valencia.precio_alq_valencia[0]
alq_valencia["precio_alq_valencia_normalizado"]= alq_valencia.precio_alq_valencia.div(first_price).mul(100)

### ALICANTE
alq_alicante = alq_alicante.drop('unidad',axis=1)
alq_alicante["date"]= pd.to_datetime(alq_alicante.Mes)
alq_alicante = alq_alicante.drop('Mes',axis=1)
alq_alicante.set_index("date", inplace=True)
alq_alicante = alq_alicante.sort_index(ascending=True)
alq_alicante = alq_alicante.rename(str.lower, axis='columns')
first_price = alq_alicante.precio_alq_alicante[0]
alq_alicante["precio_alq_alicante_normalizado"]= alq_alicante.precio_alq_alicante.div(first_price).mul(100)

### CASTELLON
alq_castellon = alq_castellon.drop('unidad',axis=1)
alq_castellon["date"]= pd.to_datetime(alq_castellon.Mes)
alq_castellon = alq_castellon.drop('Mes',axis=1)
alq_castellon.set_index("date", inplace=True)
alq_castellon = alq_castellon.sort_index(ascending=True)
alq_castellon = alq_castellon.rename(str.lower, axis='columns')
first_price = alq_castellon.precio_alq_castellon[0]
alq_castellon["precio_alq_castellon_normalizado"]= alq_castellon.precio_alq_castellon.div(first_price).mul(100)

# SALES 
vta_valencia = pd.read_excel("raw/VTA_COM_VALENCIANA.xlsx", sheet_name="VALENCIA")
vta_alicante = pd.read_excel("raw/VTA_COM_VALENCIANA.xlsx", sheet_name="ALICANTE")
vta_castellon = pd.read_excel("raw/VTA_COM_VALENCIANA.xlsx", sheet_name="CASTELLON")

### VALENCIA
vta_valencia["date"]=[x.replace("-"," 20") for x in vta_valencia["fecha"]]
vta_valencia["date"]=pd.to_datetime(vta_valencia["date"])
vta_valencia.set_index("date", inplace=True)
vta_valencia = vta_valencia.sort_index(ascending=True)
vta_valencia = vta_valencia.rename(str.lower, axis='columns')
first_price = vta_valencia.precio_vta_valencia[0]
vta_valencia["precio_vta_valencia_normalizado"]= vta_valencia.precio_vta_valencia.div(first_price).mul(100)
vta_valencia = vta_valencia.drop("fecha", axis=1)

### ALICANTE
vta_alicante = vta_alicante.rename(columns={'fecha':'date'})
vta_alicante["date"] = pd.to_datetime(vta_alicante.date)
vta_alicante.set_index("date", inplace=True)
vta_alicante = vta_alicante.sort_index(ascending=True)
vta_alicante = vta_alicante.rename(str.lower, axis='columns')
first_price = vta_alicante.precio_vta_alicante[0]
vta_alicante["precio_vta_alicante_normalizado"]= vta_alicante.precio_vta_alicante.div(first_price).mul(100)

### CASTELLON
vta_castellon = vta_castellon.rename(columns={'fecha':'date'})
vta_castellon["date"] = pd.to_datetime(vta_castellon.date)
vta_castellon.set_index("date", inplace=True)
vta_castellon = vta_castellon.sort_index(ascending=True)
vta_castellon = vta_castellon.rename(str.lower, axis='columns')
vta_castellon = vta_castellon[vta_castellon["precio_vta_castellon"]>0]
first_price = vta_castellon.precio_vta_castellon[0]
vta_castellon["precio_vta_castellon_normalizado"]= vta_castellon.precio_vta_castellon.div(first_price).mul(100)


##################
##################
os.chdir("c:\\Users\\soler\\OneDrive\\THE_BRIDGE\\GITHUB\\DEREPO_ds_ft_sep_22\\Entregas\\EDA\\")

vta_valencia.to_csv("N_vta_valencia.csv")
vta_alicante.to_csv("N_vta_alicante.csv")
vta_castellon.to_csv("N_vta_castellon.csv")

alq_alicante.to_csv("N_alq_alicante.csv")
alq_valencia.to_csv("N_alq_valencia.csv")
alq_castellon.to_csv("N_alq_castellon.csv")

####################
####################

# COVID CASES 
covid_cases = pd.read_csv("raw/COVID_nuevos_casos_notificados_CVAL.csv", sep=";", encoding='latin-1' )
covid_cases= covid_cases.drop("Unnamed: 4",axis=1) # drop de unnamed
covid_cases.drop(covid_cases.columns[[0,1]],axis=1, inplace=True) #drop columnas 1 y 2 

covid_cases["Fecha"] = [x.replace("de","") for x in covid_cases["Fecha"]] # removes "de" in Fecha

dic_meses={ "enero":"01",
            "febrero":"02",
            "marzo":"03", 
            "abril":"04",
            "mayo":"05", 
            "junio":"06" , 
            "julio": "07" ,
            "agosto":"08", 
            "septiembre": "09",
            "setiembre":"09", 
            "octubre" : "10", 
            "noviembre" : "11", 
            "diciembre": "12" } # set dictionary of months days 

covid_cases["Fecha"] = [x.replace(x.split()[1], dic_meses[x.split()[1]]) for x in covid_cases["Fecha"]] # changes month name by number
covid_cases["date"] = covid_cases["Fecha"].str.split().str[2]+"-"+ covid_cases["Fecha"].str.split().str[1]+"-"+covid_cases["Fecha"].str.split().str[0] 
covid_cases.set_index("date", inplace=True)
covid_cases= covid_cases.drop("Fecha",axis=1)
covid_cases.to_csv("covid_cases.csv")

# TABLA IDEALISTA 
idealista = pd.read_csv("tabla_idealista.csv")
idealista = idealista.drop("Unnamed: 0", axis=1)
idealista["precio"] = [x.split()[0].replace(",",".") for x in idealista["Precio_(€/m2)"]]
idealista["maximo"] = [x.split()[0].replace(",",".") for x in idealista["Maximo_historico(€/m2)"]]
idealista.drop(idealista.columns[[1,4]],axis=1, inplace=True)
idealista = idealista[["Localidad","precio", "maximo","Variacion_trimestral(%)","Variacion_anual(%)","Variacion_Maximo(%)"]]
idealista.to_csv("idealista_localidades_cv.csv")

# EURIBOR EVOLUTION 
euribor = pd.read_csv("raw/FIN_evolucion_del_euribor_mensual.csv")
dic_inicio_mes={ "enero":"01-01", 
            "febrero":"02-01", 
            "marzo":"03-01", 
            "abril":"04-01",
            "mayo":"05-01", 
            "junio":"06-01" , 
            "julio": "07-01" ,
            "agosto":"08-01", 
            "septiembre": "09-01",
            "setiembre":"09-01", 
            "octubre" : "10-01", 
            "noviembre" : "11-01", 
            "diciembre": "12-01" }

euribor["Periodo"] = euribor["Periodo"].str.lower()
euribor["mes"] = [x.replace(x.split()[0],dic_inicio_mes[x.split()[0]])for x in euribor["Periodo"]]
euribor["Año"] = euribor["Año"].apply(str)
euribor["date"] = euribor["Año"]+"-"+euribor["mes"]

euribor = euribor.drop(euribor.columns[[0,1,3]], axis=1)
euribor = euribor[euribor.date > "2006-01-01"]
euribor["date"]= pd.to_datetime(euribor["date"])
euribor.set_index("date", inplace=True)
first_price = euribor.Euribor[0]
euribor["euribor_normalizado"]= euribor.Euribor.div(first_price).mul(100)
euribor.to_csv("N_euribor_mes.csv")

# MORTGAGE EXECUTIONS
mortgages = pd.read_csv("raw/FIN_ejecuciones_hipotecarias_comunidad_valenciana.csv")
print(mortgages)
mortgages["Periodo"] = pd.to_datetime(mortgages["Periodo"])
mortgages["Comunidad"] = mortgages["Comunidad"].str[3:]
mortgages = mortgages.drop("Total Nacional", axis=1)
mortgages.rename(columns= {"Periodo":"date"}, inplace=True)
mortgages.set_index("date", inplace=True)
mortgages = mortgages.sort_index(ascending=True)
mortgages = mortgages.rename(str.lower, axis="columns")
first_value = mortgages.total[0]
mortgages["executions_normalized"]= mortgages.total.div(first_value).mul(100) 
mortgages.to_csv("N_Ejecuciones_hipotecarias_cv.csv")

# MORTGAGE TYPE 
mort_type = pd.read_csv("raw/FIN_interes _fijo_vs_variable.csv")
mort_type = mort_type.rename(str.lower, axis="columns")
mort_type["date"] = pd.to_datetime(mort_type["periodo"])
mort_type = mort_type.drop(mort_type.columns[[1,2]],axis=1)
mort_type.set_index(mort_type["date"],inplace=True)
mort_type = mort_type.drop(mort_type.columns[[2]],axis=1)
mort_type.to_csv("emisiones_hipotecas_tipo.csv")

# RATES

### IPC 
ipc_type = pd.read_csv("raw/IND_ipc_CV_evolucion.csv")
ipc_type = ipc_type.rename(str.lower, axis="columns")

ipc_type = ipc_type.drop("tipo de dato", axis=1)
ipc_type["date"] = pd.to_datetime(ipc_type["periodo"])
ipc_type = ipc_type.drop(ipc_type.columns[[0,2]], axis=1)
ipc_type["grupos_ipc_type"] = ipc_type["grupos ecoicop"].str[3:].str.lower()
ipc_type = ipc_type.drop("grupos ecoicop", axis=1)
ipc_type.set_index("date", inplace=True)

ipc_type.to_csv("ipc_type_cv_tipos.csv")

### IPC GENERAL 
ipc = pd.read_csv("raw/IND_IPC_GENERAL.csv", sep=";", encoding="latin-1")
ipc = ipc.rename(str.lower, axis="columns")
ipc["date"] = ipc.periodo.apply(lambda x: x.replace("M","-"))
ipc["date"] = pd.to_datetime(ipc.date)
ipc = ipc.set_index("date")
ipc = ipc.sort_index(ascending=True)
ipc = ipc["2006-01-01":] # set time according to others DF 
ipc = ipc.drop("periodo", axis=1)
ipc.total = ipc.total.apply((lambda x : x.replace(",",".")))
ipc.total = ipc.total.astype(float)
#### NORMALIZE
ipc = ipc.assign(ipc_normalizado = 'NAN')
ipc = ipc.reset_index()
ipc.loc[0,"ipc_normalizado"] = 100
pd.set_option('display.float_format', lambda x: '%.5f' % x)
for i in range(1,len(ipc)):
    ipc.loc[i,"ipc_normalizado"] = ipc.loc[i-1,"ipc_normalizado"]+ipc.loc[i-1,"ipc_normalizado"]*ipc.loc[i-1,"total"]/100
ipc = ipc.set_index("date")
ipc.to_csv("N_ipc_general.csv")

### SMI
smia = pd.read_csv("raw/IND_SMI_ANUAL.csv", sep=",")
smia = smia.sort_index(ascending=False)
smia["date"] = pd.to_datetime(smia["date"])
smia.set_index("date", inplace=True)
first_smia = smia["smi"].iloc[0]
first_smia
smia["smi_normalizado"] = smia.smi.div(first_smia).mul(100)
smia.to_csv("N_smi_anual.csv")
dates = pd.date_range('2006-09-01','2022-09-01', freq='MS').to_frame()
prueba = pd.merge(smia,dates, left_index=True, right_index=True, how="outer")
prueba = pd.merge(smia,dates, left_index=True, right_index=True, how="outer")
smi = prueba.interpolate(method="linear")
smi.index.name = "date"
smi.rename(columns= {"variacion_anual_smi":"variacion_mensual_smi",
                    "var_anual_smi_b100":"CONTROL var_mensual_smi_b100"}, inplace=True)
smi.drop(0, axis=1, inplace=True)
smi = smi.sort_index(axis=0, ascending=True)

# TURISM

### TURISTS INCOMING EVOLUTION
nturi = pd.read_csv("raw/TUR_evolucion_del_numero_de_turistas_extranjeros_en_comunidad_valenciana__en_lo_que_va_de_año.csv",sep=",")
first_nturi = nturi["Nº acumulado de los turistas extranjeros"][0]
nturi["turists_normalized"] = nturi["Nº acumulado de los turistas extranjeros"].div(first_nturi).mul(100)
nturi["date"] = nturi["Año"].astype(str)+"-08-01"
nturi.date = pd.to_datetime(nturi.date)
nturi.set_index("date", inplace=True)
nturi = nturi.drop(nturi.columns[[0,1]], axis=1)
nturi.to_csv("N_numero_turistas_ingresados.csv")

# MIGRATION

### TO COMUNIDAD VALENCIANA MIGRATION EVOLUTION
migration = pd.read_csv("raw/migraciones interiores hacia valencia.csv")
migration["date"] = migration.Periodo.astype(str) + "-08-01"
migration = migration.drop("Comunidades y ciudades autonomas de destino", axis=1)
migration = migration.drop("Periodo", axis=1)
migration = migration.drop("Sexo", axis=1)
migration["Comunidades y ciudades autonomas de origen"] = migration["Comunidades y ciudades autonomas de origen"].str[3:]
migration.set_index("date", inplace=True)
migration.index = pd.to_datetime(migration.index)
migration = migration.sort_index(ascending=True)
groupby_migration =  migration.groupby(["date","Comunidades y ciudades autonomas de origen"]).sum()
first_values = groupby_migration.loc[("2008"),"Total"].values
len(list(first_values) * 14)
groupby_migration["el_bicho_a_dividir"] = list(first_values) * 14
groupby_migration["normalized_migration"] = groupby_migration["Total"] / groupby_migration["el_bicho_a_dividir"] * 100
clean_migration = groupby_migration.reset_index(level=-1)
clean_migration.to_csv("Nsaldo_migratorio_interno_acomval.csv")

#*lista de DATAFRAMES*
#---
#---
# alq_valencia # rent prices for Valencia
# alq_alicante # rent prices for Alicante
# alq_castellon # rent prices for Castellon
# vta_valencia # sell prices for Valencia
# vta_alicante # sell prices for Alicante
# vta_castellon # sell prices for Castellon
# euribor # EURIBOR evolution
# mortgages # mortgages excecutions 
# mort_type # mortgages emission types 
# ipc # IPC evolution
# smia # minimum interpersonal salary anual evolution
# covid_cases # covid cases dettected by day
# nturi # number of turists entered CV by year 
# clean_migration # internal migration to CV 
# idealista_table # idealista scapping with selenium by city




##### PLOTS ######
comparation = pd.concat(
        [alq_valencia["precio_alq_valencia_normalizado"],
        alq_alicante["precio_alq_alicante_normalizado"],
        alq_castellon["precio_alq_castellon_normalizado"],
        vta_valencia["precio_vta_valencia_normalizado"],
        vta_alicante["precio_vta_alicante_normalizado"],
        vta_castellon["precio_vta_castellon_normalizado"],
        euribor["euribor_normalizado"],
        mortgages["executions_normalized"],
        ipc["ipc_normalizado"],
        smia["smi_normalizado"],
        nturi["turists_normalized"],
        ], axis=1)


comparation = pd.concat(
        [alq_valencia.loc['2008-08':'2022-08']["precio_alq_valencia_normalizado"],
        alq_alicante.loc['2008-08':'2022-08']["precio_alq_alicante_normalizado"],
        alq_castellon.loc['2008-08':'2022-08']["precio_alq_castellon_normalizado"],
        vta_valencia.loc['2008-08':'2022-08']["precio_vta_valencia_normalizado"],
        vta_alicante.loc['2008-08':'2022-08']["precio_vta_alicante_normalizado"],
        vta_castellon.loc['2008-08':'2022-08']["precio_vta_castellon_normalizado"],
        euribor.loc['2008-08':'2022-08']["euribor_normalizado"],
        mortgages.loc['2008-08':'2022-08']["executions_normalized"],
        ipc.loc['2008-08':'2022-08']["ipc_normalizado"],
        smia.loc['2008-08':'2022-08']["smi_normalizado"],
        nturi.loc['2008-08':'2022-08']["turists_normalized"],
        ], axis=1)

plt.figure(figsize=(15,15))
sns.heatmap(comparation.corr(),
            vmin=-1,
            vmax=1,
            cmap=sns.diverging_palette(145, 280, s=85, l=25, n=7),
            square=True,
            linewidths=.1,
            annot=True);       


desde = "2015-08"
hasta = "2020-08"

comparation = pd.concat(
        [alq_valencia.loc[desde:hasta]["precio_alq_valencia_normalizado"],
        alq_alicante.loc[desde:hasta]["precio_alq_alicante_normalizado"],
        alq_castellon.loc[desde:hasta]["precio_alq_castellon_normalizado"],
        vta_valencia.loc[desde:hasta]["precio_vta_valencia_normalizado"],
        vta_alicante.loc[desde:hasta]["precio_vta_alicante_normalizado"],
        vta_castellon.loc[desde:hasta]["precio_vta_castellon_normalizado"],
        euribor.loc[desde:hasta]["euribor_normalizado"],
        mortgages.loc[desde:hasta]["executions_normalized"],
        ipc.loc[desde:hasta]["ipc_normalizado"],
        smia.loc[desde:hasta]["smi_normalizado"],
        nturi.loc[desde:hasta]["turists_normalized"],
        ], axis=1)

plt.figure(figsize=(15,15))

sns.heatmap(comparation.corr(),
            vmin=-1,
            vmax=1,
            cmap=sns.diverging_palette(5, 250, s=80, l=25, n=10),
            square=True,
            linewidths=.1,
            annot=True);





#lineplot ###

year = alq_alicante.index[(alq_alicante.index >= '2008-08')&(alq_alicante.index <= '2022-08')]
turistas = nturi.loc['2008-08':'2022-08']["turists_normalized"].resample(rule="m", axis=0).mean().interpolate()
valencia_AL = alq_valencia.resample(rule="m", axis=0).mean().loc['2008-08':'2022-08']["precio_alq_valencia_normalizado"]#.interpolate()
alicante_AL = alq_alicante.resample(rule="m", axis=0).mean().loc['2008-08':'2022-08']["precio_alq_alicante_normalizado"]#.interpolate()
castellon_AL = alq_castellon.loc['2008-08':'2022-08']["precio_alq_castellon_normalizado"]#.interpolate()
plt.plot(year, turistas, 'g', label="TURISTAS")
plt.plot(year, valencia_AL, 'b', label="ALQU VALENCIA")
plt.plot(year, alicante_AL,'r', label="ALQU ALICANTE" )
plt.plot(year, castellon_AL,'c', label="ALQU CASTELLON" )

year = alq_alicante.index[(alq_alicante.index >= '2008-08')&(alq_alicante.index <= '2022-08')]
turistas = nturi.loc['2008-08':'2022-08']["turists_normalized"].resample(rule="m", axis=0).mean().interpolate()
valencia_VTA = vta_valencia.resample(rule="m", axis=0).mean().loc['2008-08':'2022-08']["precio_vta_valencia_normalizado"]#.interpolate()
alicante_VTA = vta_alicante.resample(rule="m", axis=0).mean().loc['2008-08':'2022-08']["precio_vta_alicante_normalizado"]#.interpolate()
castellon_VTA = vta_castellon.loc['2008-08':'2022-08']["precio_vta_castellon_normalizado"]#.interpolate()
plt.plot(year, turistas, 'g', label="TURISTAS")
plt.plot(year, valencia_VTA, 'b', label="VTA VALENCIA")
plt.plot(year, alicante_VTA,'r', label="VTA ALICANTE" )
plt.plot(year, castellon_VTA,'c', label="VTA CASTELLON" )