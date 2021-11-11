#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver

from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("download.default_directory=goodies")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import time
import datetime

import numpy as np


# In[ ]:


#Get URL
url='https://www.geodair.fr/donnees/consultation'

driver.get(url)
#time.sleep(1)


# In[ ]:


years=np.arange(2013,2022,1)
months=['JANV','FÉVR','MARS','AVR','MAI','JUIN','JUIL','AOÛT','SEPT','OCT','NOV','DÉC']
days=np.arange(1,31,1)
#select dayly mean
ddelement= driver.find_element_by_id('mat-select-2').click()
driver.find_element_by_xpath("//div[@id='mat-select-2-panel']/mat-option[2]").click()
time.sleep(1)
for year in years:
    time.sleep(1)
    styear=str(year)
    for month in months:
        for day in days:
                ddelement= driver.find_element_by_id('mat-select-2').click()
                driver.find_element_by_xpath("//div[@id='mat-select-2-panel']/mat-option[2]").click()
                driver.execute_script('el = document.elementFromPoint(1, 1); el.click();')

                #print('step 1')
                
                try:
                    driver.find_element_by_xpath("//button[@class='mat-focus-indicator mat-icon-button mat-button-base']").click()
                except:
                    driver.find_element_by_xpath("//button[@class='mat-focus-indicator.mat-icon-button-base.cdk-focused.cdk-program-focused']").click()
                time.sleep(0.5)
                #print('step 2')
                driver.find_element_by_xpath("//span[@id='mat-calendar-button-0']").click()
                #print('step 3')
                time.sleep(2)
                #year
                ytext=('//*[contains(text(), \''+styear+'\')]')
                #print('step 4')
                driver.find_element_by_xpath(ytext).click()
                time.sleep(1)
                #month
                ymonth='//*[contains(text(), \''+month+'\')]'
                driver.find_element_by_xpath(ymonth).click()
                time.sleep(1)
                #day
                stday=str(day)
                yday='//td[contains(.,  \''+stday+'\')]'
                
                try:
                    dbut=driver.find_element_by_xpath(yday)
                    dbut.click()
                    time.sleep(2)
                
                    driver.find_element_by_xpath("//div[@class='download-container col-xs-12 col-sm-4 col-lg-3 ng-star-inserted']/button/span").click()
                    time.sleep(10)
                    print(url,styear,month,stday)
                    driver.refresh()
                    time.sleep(2)
                except:
                    driver.refresh()
                    time.sleep(2)