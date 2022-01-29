from lib2to3.pgen2.driver import Driver
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

import pandas as pd 
#! Step 1
# Load Dataset and sort by market value 
df = pd.read_excel('Player Name.xlsx')
df.sort_values('highest_market_value_in_gbp' , inplace=True, ascending=False)
df = df.reset_index()  # make sure indexes pair with number of rows
# -------------------
#! Step 2
# Driver Path
Path = "C:\Program Files (x86)\chromedriver.exe"
# Start Chrome driver
driver = webdriver.Chrome(Path)
# -------------------
# Flags 
count =0
total = len(df)

#! Step 3
# Iterate over each row
with open('E:\BI Dev ITI\Scraping\out.csv', mode='a') as file_:
    for index, row in df.iterrows():
        count += 1
        # Replace '-' with '+' so we can add it to the url
        PName = row["name"].replace("-","+")
        # Enter and go to the url
        path = f'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={PName}'
        driver.get(path)
        #! Find the Player Img element
        try:
            # Wait max 10 seconds to get the url
            img = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.XPATH, '//*[@id="yw0"]/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td[1]/a/img')) )
            # Get the src attribute from the tag
            # Change img size from small to big
            P_Img =  img.get_attribute("src").replace('small','big')
        except:
            # Couldn't get the img url so we add the default img
            P_Img = 'https://img.a.transfermarkt.technology/portrait/big/default.jpg?lm=1'    
                
        #! get country flag img url
        try:
            # Wait max 5 seconds to get the img
            Img_Country = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="yw0"]/table/tbody/tr[1]/td[5]/img[1]')))
            # Get the src attribute from the tag
            # Change img size from verysmall to medium
            C_Img =  Img_Country.get_attribute("src").replace('verysmall','medium')
            print('{}/{} Success --  Name : {}'.format(count,total,PName.replace('+',' ')))
        except:
            # Couldn't get the img url so we add the default
            C_Img = 'https://tmssl.akamaized.net/images/flagge/medium/default.png?lm=1520611569'
            print('{}/{} Failed --  Name : {}'.format(count,total,PName.replace('+',' ')))
        
        # Add row in csv
        file_.write("{},{},{}".format(PName.replace('+',' '), P_Img , C_Img))
        file_.write("\n")  # Next line.  

# Close the Driver when done
driver.quit()
        
    

 
 
    
    
    










