#This extracts Cancer deaths by department, gender, age, year, body location of cancer
#As it done manually at http://cepidc-data.inserm.fr/inserm/html/index2.htm

import codecs
import pandas as pd 
import numpy as np
from bs4 import BeautifulSoup

# Colonnes pour la df
colnames = ['Code CIM', 'Libellé',  'M_Total', 'M_inf_1', 'M_1_4', 'M_5_14', 'M_15_24', 'M_25_34', 'M_35_44', 'M_45_54', 'M_55_64', 'M_65_74', 'M_75_84', 'M_85_94', 'M_95_et_plus', 'F_Total', 'F_inf_1', 'F_1_4', 'F_5_14', 'F_15_24', 'F_25_34', 'F_35_44', 'F_45_54', 'F_55_64', 'F_65_74', 'F_75_84', 'F_85_94', 'F_95_et_plus', 'T_Total', 'T_inf_1', 'T_1_4', 'T_5_14', 'T_15_24', 'T_25_34', 'T_35_44', 'T_45_54', 'T_55_64', 'T_65_74', 'T_75_84', 'T_85_94', 'T_95_et_plus']
# Création de la df finale
retrieved_data = pd.DataFrame(columns=colnames)

# Génération de la liste des CODE_GEO pour la boucle sur les départements
dep = list(map(str, range(1, 96)))
dep.append('971')
dep.append('972')
dep.append('973')
dep.append('974')
list_departement = []
for i in dep:
    if len(i)==1:
        i = '0'+str(i)
    list_departement.append(i)
# Génération de la liste des AN_DEB pour la boucle sur les années
list_annee = list(map(str, range(2010, 2017)))
# Génération de la liste des SEC_CAUSE pour la boucle sur les pathologies
cause = list(map(str, range(18)))
list_cause = []
for i in cause:
    if len(i)==1:
        i = '0'+i
    list_cause.append(i)

# Génération des urls
list_url = []
for stat in ['E', 'T']:
    for geo in ['D', 'F']:
        if geo=='D':
            for d in list_departement:
                print(stat, '-', d)
                for a in list_annee: 
                    for c in list_cause:
                        list_url.append('http://cepidc-data.inserm.fr/cgi-bin/broker.exe?TYPE=%s&AXEGEO=D&CODE_GEO=%s&AN_DEB=%s&AN_FIN=&TCAUSE=S&SEC_CAUSE=%s&CAUSE=0703&NOMEN=910&TYPE_SORTIE=T&PREV_AXEGEO=D&_SERVICE=inserm&_PROGRAM=INTLIB.GENERAL.ET_OUTPUT_GEN.SCL&_DEBUG=0' % (stat, d, a, c))
        else:
            print(stat, '-', 'France entière')
            for a in list_annee: ### Voir ce qu'on doit change dans l'URL (pas de sélection de département)
                    for c in list_cause:
                        list_url.append('http://cepidc-data.inserm.fr/cgi-bin/broker.exe?TYPE=%s&AXEGEO=F&CODE_GEO=%s&AN_DEB=%s&AN_FIN=&TCAUSE=S&SEC_CAUSE=%s&CAUSE=0703&NOMEN=910&TYPE_SORTIE=T&PREV_AXEGEO=D&_SERVICE=inserm&_PROGRAM=INTLIB.GENERAL.ET_OUTPUT_GEN.SCL&_DEBUG=0' % (stat, d, a, c))

# Remplissage de la df finale pour avoir toutes les données dans une seule df 
for url in list_url:
    value_concat = pd.DataFrame # une url = une df 
    file = codecs.open(url, "r") # lecture du code
    soup = BeautifulSoup(file)
    annee = soup.find_all('table')[0].find_all('td')[1].get_text # récupération de l'année
    departement = soup.find_all('table')[0].find_all('td')[5].get_text.replace(" ", "") # récupération de la localisation
    
    # calculer la valeur pour remplacer le 5 dans la ligne suivante (première ligne avec [])
    for i in range(5):
        value = [] # nouvelle value à chaque ligne
        for j in range(len(soup.find_all('table')[2].find_all('td')[(16+44*i):(60+44*i)])):
            if soup.find_all('table')[2].find_all('td')[(16+44*i):(60+44*i)][j]: 
                value.append(soup.find_all('table')[2].find_all('td')[(16+44*i):(60+44*i)][j].get_text.replace('\n',''))
        value_concat = pd.concat([value_concat, pd.DataFrame(value).transpose]) # concaténation avec la df créée pour cette url
        value_concat = value_concat.reset_index(drop=True) 
        value_concat.columns = ['Code CIM', 'Libellé',  'M', 'M_Total', 'M_inf_1', 'M_1_4', 'M_5_14', 'M_15_24', 'M_25_34', 'M_35_44', 'M_45_54', 'M_55_64', 'M_65_74', 'M_75_84', 'M_85_94', 'M_95_et_plus', 'F', 'F_Total', 'F_inf_1', 'F_1_4', 'F_5_14', 'F_15_24', 'F_25_34', 'F_35_44', 'F_45_54', 'F_55_64', 'F_65_74', 'F_75_84', 'F_85_94', 'F_95_et_plus', 'T', 'T_Total', 'T_inf_1', 'T_1_4', 'T_5_14', 'T_15_24', 'T_25_34', 'T_35_44', 'T_45_54', 'T_55_64', 'T_65_74', 'T_75_84', 'T_85_94', 'T_95_et_plus']
        value_concat = value_concat.drop(columns=["M", "F", "T"])
        value_concat['Année'] = annee
        value_concat['Département'] = departement
    retrieved_data = pd.concat([retrieved_data, value_concat]) # concaténation avec la df qui regroupe toutes les données 

value_concat.to_csv('cepidc_retrieve_data.csv', index=False)