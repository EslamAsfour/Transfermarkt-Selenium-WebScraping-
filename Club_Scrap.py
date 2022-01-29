from lib2to3.pgen2.driver import Driver
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

import pandas as pd 

#! Step 1
# Load Dataset 
df = pd.read_csv('clubs.csv')

#! Step 2
# Driver Path
Path = "C:\Program Files (x86)\chromedriver.exe"
# Start Chrome driver
driver = webdriver.Chrome(Path)

# Flags 
count =0
total = len(df)

with open('E:\BI Dev ITI\Scraping\Club_Logo_Country.csv', mode='a') as file_:
    for index, row in df.iterrows():
        count += 1
        # Replace '-' with '+' so we can add it to the url
        CName = row["name"].replace("-","+")
        # Enter and go to the url
        path = f'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={CName}'
        driver.get(path)
        #! Find the Club Logo
        try:
            # Wait max 10 seconds to get the url
            img = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="yw0"]/table/tbody/tr[1]/td[1]/img')) )
            # Get the src attribute from the tag
            # Change img size from small to big
            C_LOGO=  img.get_attribute("src").replace('small','big')
        except:
            # Couldn't get the img url so we add the default img
            C_LOGO = 'https://tmssl.akamaized.net/images/wappen/big/default.png?lm=1539765803'
        #! Find the Competition Country
        try:
            # Wait max 10 seconds to get the url
            img = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="yw0"]/table/tbody/tr[1]/td[3]/img')) )
            # Get the src attribute from the tag
            # Change img size from small to big
            C_country=  img.get_attribute("src").replace('verysmall','medium')
            print('{}/{} Success --  Name : {}'.format(count,total,CName.replace('+',' ')))
        except:
            # Couldn't get the img url so we add the default img
            C_country = 'https://tmssl.akamaized.net/images/flagge/medium/default.png?lm=1520611569'  
            print('{}/{} Failed --  Name : {}'.format(count,total,CName.replace('+',' ')))
            
        # Add row in csv
        file_.write("{},{},{}".format(CName.replace('+',' '), C_LOGO,C_country))
        file_.write("\n")  # Next line.  

# Close the Driver when done
driver.quit()