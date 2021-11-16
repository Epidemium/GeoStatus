#
# WARNING: it takes many hours to run this and is an unnecessary work load for the CépiDC website
# Wouldn't you instead open the Excel file that is in this directory ?
#

cat("# WARNING: it takes many hours to run this and is an unnecessary work load for the CépiDC website\n")
cat("# WARNING: Shouldn't you instead open the Excel file that is in this directory ?\n")
cat("# Please click on the STOP red button at the top\n")
invisible(readline(prompt="Press [enter] to continue"))
a=1
cat("\n\n# WARNING: are you sure to continue?\n")
cat("# Please click on the STOP red button at the top\n\n\n")
invisible(readline(prompt="Press [enter] to continue"))


library(stringr)
library(writexl)
#warning: the code below was created for a one-shot scrapping.
#Significant adjustments would be needed to robustly scrap other causes-of-death
matable = data.frame(Annee=rep(NA,3*10^5), Dep=NA, CodeCIM=NA, Libelle=NA, Sexe=NA, Total=NA, Age0=NA, Age1_4=NA, Age5_14=NA,
Age15_24=NA, Age25_34=NA, Age35_44=NA, Age45_54=NA, Age55_64=NA, Age65_74=NA, Age75_84=NA, Age85_94=NA, Age95plus=NA)

ligne=1
for(annee in 1981:2017) #year
for(dpt_i in c(paste0("0",1:9),10:95,971:974)) #departments
 {
 cat(annee, dpt_i, ligne, "\n")
 matable[ligne+(0:62),1] = annee
 matable[ligne+(0:62),2] = dpt_i
 content = readChar(paste0("http://cepidc-data.inserm.fr/cgi-bin/broker.exe?TYPE=E&AXEGEO=D&CODE_GEO=", dpt_i, "&AN_DEB=", annee, "&AN_FIN=", annee, "&TCAUSE=S&SEC_CAUSE=02&CAUSE=02&NOMEN=910&TYPE_SORTIE=T&PREV_AXEGEO=D&_SERVICE=inserm&_PROGRAM=INTLIB.GENERAL.ET_OUTPUT_GEN.SCL&_DEBUG=0"),nchars=1e6)
 for(groupeDe3lignes in 1:21)
  {
  cursor = str_locate(content,"<TD rowspan=3 align=left>")[2]; if(is.na(cursor)) next; content = substring(content, cursor)
  cursor = str_locate(content,"<B>")[2]; if(is.na(cursor)) next;
  if(cursor < 30) content = substring(content, cursor) #this skips the effect of the previous ligne if <B> if far: if not bold 
  cursor = str_locate(content,"\n</")[1]; if(is.na(cursor)) next
  matable[ligne+(0:2),3] = CodeCIM = substr(content, 3, cursor-1)
  cursor = str_locate(content,"<TD rowspan=3 align=left>")[2]; if(is.na(cursor)) next; content = substring(content, cursor)
  cursor = str_locate(content,"<B>")[2]; if(is.na(cursor)) next;
  if(cursor < 30) content = substring(content, cursor) #this skips the effect of the previous ligne if <B> if far: if not bold 
  cursor = str_locate(content,"\n</")[1]; if(is.na(cursor)) next
  matable[ligne+(0:2),4] = Libelle = substr(content, 3, cursor-1)
  for(row_i in 0:2)
   {
   cursor = str_locate(content,"<TD align=center>\n")[2]; if(is.na(cursor)) next; content = substring(content, cursor)
   cursor = str_locate(content,"\n</TD>")[1]; if(is.na(cursor)) next
   matable[ligne+row_i,5] = Sexe = substr(content, 2, cursor-1)
   for(col_i in 6:18)
    {
    cursor = str_locate(content,"<TD align=right>\n")[2]; if(is.na(cursor)) next; content = substring(content, cursor)
    cursor = str_locate(content,"\n</TD>")[1]; if(is.na(cursor)) next
    matable[ligne+row_i,col_i] = substr(content, 2, cursor-1)
    }
   }
  ligne=ligne+3
  }
 }
write_xlsx(matable[1:(ligne-1),],"CepiDC_cancer_deaths.xlsx")
