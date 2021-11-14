library(readr)
library(dplyr)

dbp = readRDS('../data/AllCauseMortality/individual_deaths_Fr_2018-2020.rds')
#summary(dbp)

#count deaths by gender and age in 2018
a = dbp %>% filter(deces_annee == 2018
) %>% mutate(age = deces_annee - naissance_annee
) %>% count(sexe, age)
#same but long writing
#a = dbp %>% filter(deces_annee == 2018 
#) %>% mutate(age = deces_annee - naissance_annee) %>% select(age, sexe
#) %>% group_by(sexe, age) %>% summarize(ndeaths = n()) %>% arrange(sexe, age)

#plot
H = filter(a, sexe==1)
F = filter(a, sexe==2)
plot(H$age,H$ndeaths,col="blue")
lines(F$age,F$ndeaths,col="red")

invisible(readline(prompt="Press [enter] to continue"))

#Count deaths by department
deaths_byDpt = dbp %>% filter(deces_annee == 2018) %>% count(deces_dep)
plot(deaths_byDpt)

dbp %>% filter(deces_annee < 2021
) %>% count(deces_annee, sexe, deces_dep
) %>% write_csv("deaths_byDpt.csv")

dbp %>% filter(deces_annee < 2021
) %>% mutate(age = deces_annee - naissance_annee
) %>% count(deces_annee, sexe, age, deces_dep
) %>% write_csv("deaths_byAgeDpt.csv")
