import os
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd

os.environ['PATH'] += r"C:/SeleniumDrivers"
driver=webdriver.Chrome()
driver.get("https://www.nationalprecision.com/")
#driver.maximize_window()
driver.implicitly_wait(5)

def extract():
    driver.execute_script("window.scrollBy(0, 680);")
    header = driver.find_elements(By.CSS_SELECTOR, "th[ng-style='$parent.plc.headerHeight']")
    #for head in header:
        #print(head.text)


    header2=driver.find_elements(By.CSS_SELECTOR,'th[class="group-label ng-binding ng-scope has-group"]')
    #for ead in header2:
    #    print(ead.text)


    subheader=driver.find_elements(By.XPATH, '//th[@class="column-label ng-scope no-group"]//span[@class="ng-binding"]')
    #for sub in subheader:
    #    print(sub.text)


    time.sleep(2)
    bearings_name=driver.find_elements(By.XPATH,'//a[starts-with(@ng-href, "/products/p/ball-bearings/")]')
    s=[]

    for bearing in bearings_name:
        if "Check Inventory" not in bearing.text: 
            if bearing.text not in s:
                s.append(bearing.text)

    #print(s)
    #for bearing_text in s:
    #    print(bearing_text)


    details=driver.find_elements(By.XPATH,'//td[@ng-repeat="filter in $parent.$parent.plc.metricsData.filters"]')
    #for det in details:
    #    print(det.text)

    #print('-'*50)

    no_of_row = driver.find_elements(By.XPATH, "//div[@class='fixed-columns']/table/tbody/tr")

    k=0
    m=0
    #print(k)
    while k<len(no_of_row):

        for h in header:
            print(h.text,end="=\t")
            print(s[k])

        for i in subheader:
            print(f"{i.text}=",end="\t")
            print(f"{details[m].text}")
            m+=1

        print()
        print("-"*50)
        print()
        k+=1
    k=0

    headers_text = [h.text for h in header]
    subheaders_text = [i.text for i in subheader]
    rows = []

    k = 0
    m = 0

    while k < len(no_of_row):
        row_data = {}
        # Add header and bearing name to the row data
        for h in header:
            row_data[h.text] = s[k]
        
        # Add subheader and corresponding details to the row data
        for i in subheader:
            row_data[i.text] = details[m].text
            m += 1
        
        rows.append(row_data)
        k += 1

    # Create a pandas DataFrame
    df = pd.DataFrame(rows)

    # Generate a dynamic file name
    counter = 1
    while True:
        filename = f"data_output_{counter}.csv"
        if not os.path.exists(filename):
            break
        counter += 1

    # Save to a dynamically named CSV file
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


cookie_accpt=driver.find_element('id','CybotCookiebotDialogBodyButtonAccept')
cookie_accpt.click()

products=driver.find_element(By.CSS_SELECTOR, "a[href='/products/']")
# Create an instance of ActionChains
actions = ActionChains(driver)

# Hover over the "Products" link
actions.move_to_element(products).perform()

ball_bearings = driver.find_element(By.CSS_SELECTOR, "a[href='/products/c/ball-bearings/']")
ball_bearings.click()

driver.execute_script("window.scrollBy(0, 900);")

driver.maximize_window()
series_selector = driver.find_elements(By.CSS_SELECTOR, "ul.grid-accordion > li > a[href]")



for i in series_selector:
    print(i.text)
    if i.text=="Steel":
        #continue
        i.click()
        time.sleep(1)
        sub_series = driver.find_elements(By.CSS_SELECTOR, "a[href*='/products/c/ball-bearings/steel/']")
        for j in sub_series:
            print(j.text)
            j.click()
            time.sleep(1)
            extract()
            driver.back()
            print('-'*100)
            print("Steel")

    elif i.text=="Stainless Steel": 
        #continue
        i.click()
        time.sleep(1)
        sub_series = driver.find_elements(By.CSS_SELECTOR, f"a[href*='/products/c/ball-bearings/stainless-steel/']")
        for j in sub_series:
            print(j.text)
            j.click()
            time.sleep(1)
            extract()
            driver.back()
            print('-'*100)
            print("Stainless Steel")


    elif i.text=="Thrust Bearings": 
        #continue
        i.click()
        time.sleep(1)
        sub_series = driver.find_elements(By.CSS_SELECTOR, f"a[href*='/products/c/ball-bearings/thrust-bearings/']")
        for j in sub_series:
            print(j.text)
            j.click()
            time.sleep(1)
            extract()
            driver.back()
            print('-'*100)
            print("Thrust Bearing")

    elif i.text=="Angular Contact Ball Bearing": 
        #continue
        i.click()
        time.sleep(1)
        sub_series = driver.find_elements(By.CSS_SELECTOR, f"a[href*='/products/c/ball-bearings/angular-contact-ball-bearing/']")
        for j in sub_series:
            print(j.text)
            j.click()
            time.sleep(1)
            extract()  
            driver.back()  
            print('-'*100)
            print("Angular Contact Ball Bearing")

    else:    
        #continue
        i.click()
        time.sleep(1)
        extract()
        driver.back()

    print('-'*200)

input()