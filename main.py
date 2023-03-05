import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

city = str(input('type the destination city: '))
pagg = int(input('how many page do you scrap: '))
cep = str(input('type the destination cep: '))

s = Service(r'D:\download\chromedriver')
driver = webdriver.Chrome(service=s)

driver.maximize_window()
driver.get(f'https://www.google.com/search?q=supermarket+in+{cep}+{city}')
time.sleep(6)
driver.find_element(by=By.XPATH, value='//*[@id="Odp5De"]/div/div/div[2]/div[1]/div[2]/g-more-link/a/div/span[1]').click()

data = []
# scraping time!!
for a in range(0, pagg):
    time.sleep(6)
    mainpage = driver.find_elements(by=By.XPATH, value='//div[@jsname="jXK9ad"]')

    for start in mainpage:
        start.find_element(by=By.CLASS_NAME, value='rllt__details').click()

        # waiting for opened js
        time.sleep(7)

        # start scrap
        title = driver.find_element(by=By.CLASS_NAME, value='SPZz6b').find_element(by=By.TAG_NAME, value='h2').find_element(by=By.TAG_NAME, value='span').text

        #try cat rating 
        try:
            rating = driver.find_element(by=By.CLASS_NAME, value='Aq14fc').text
        except Exception:
            rating = 'no rating'


        #review = driver.find_element(by=By.CLASS_NAME, value='RDApEe YrbPuc').text
        location = driver.find_element(by=By.CLASS_NAME, value='LrzXr').text

        # scrap phone number
        try:
            numm = driver.find_element(by=By.XPATH, value='//span[(@class="LrzXr zdqRlf kno-fv")]').text
        except Exception:
            numm = 'no phone number'

        # scrap for opening hours
        try:
            driver.find_element(by=By.CLASS_NAME, value='JjSWRd').click()
            opening = driver.find_element(by=By.CLASS_NAME, value='WgFkxc').text
            if opening == '':
                time.sleep(3)
                opening = driver.find_element(by=By.XPATH, value='//table[(@class="WgFkxc CLtZU")]').text
                driver.find_elements(by=By.XPATH, value='//div[@class="Xvesr"]')[3].click()
        except Exception:
            opening = 'no opening hours'

        # storage
        dat = {
            'Name': title,
            'Rating': rating,
            #'Review': review,
            'location': location,
            'Phone Number': numm,
            'Opening Hours': opening
        }
        data.append(dat)

        # test result
        print(f'{title}, rating = {rating}, location: {location}, phone: {numm}, operational hours: {opening}')

    # click next page
    try:
        driver.find_element(by=By.XPATH, value='//*[@id="pnnext"]/span[2]').click()
    except Exception:
        break

# create data excle
df = pd.DataFrame(data)
df.to_excel(f'result from {pagg} page.xlsx', index=False)

driver.close()

