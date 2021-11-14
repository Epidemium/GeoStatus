import pandas as pd
import matplotlib.pyplot as plt

#get Y
#Y=pd.read_csv('mort-prostate-M-2007-2014.csv', sep=';', header=1)
#Y=pd.read_csv('mort-poumon-M-2007-2014.csv', sep=';', header=1)
Y=pd.read_csv('mort-sein-F-2007-2014.csv', sep=';', header=1)
Y = Y[['Numéro du département', 'Taux d\'incidence standardisé monde']]

#get X
X=pd.read_excel('radioactivite-naturelle.xls')
#X = X[X['Série']=='RA01Maximum de radon enregistrée']
X = X[X['Série']=='RA01Concentration moyenne de radon dans les unités d\'habitation']
X = X[['N° région, département','1999']]

#merge
M = pd.merge(Y,X, left_on='Numéro du département', right_on='N° région, département')

#plot
plt.scatter(M['1999'], M['Taux d\'incidence standardisé monde'], alpha=0.5)
plt.title("Spurious correlation!")
plt.xlabel("RADON LEVELS")
plt.ylabel("BREAST CANCER MORTALITY")
plt.text(-50,11,'Annual 2007-2014 rate, by French department\nPer 100k persons, World- age-standardized\nlesdonnees.e-cancer.fr/Themes/epidemiologie',
         alpha=0.5,rotation='vertical',horizontalalignment ='center')
plt.text(130,8.5,"Average concentration in homes in Bq/m³, by French departement\nhttp://www.stats.environnement.developpement-durable.gouv.fr/Eider/series.do",
         alpha=0.5,horizontalalignment ='center')

#for i in range(M.shape[0]):
#    plt.text(M['1999'][i],M['Taux d\'incidence standardisé monde'][i],s=M['Numéro du département'][i], alpha=0.5)
plt.show()