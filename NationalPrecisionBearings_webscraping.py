import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Set path for ChromeDriver
os.environ['PATH'] += r"C:/SeleniumDrivers"
driver = webdriver.Chrome()
driver.get("https://www.nationalprecision.com/")
driver.implicitly_wait(5)

# Accept cookies
try:
    cookie_accept = driver.find_element(By.ID, 'CybotCookiebotDialogBodyButtonAccept')
    cookie_accept.click()
except:
    pass  

#Hover over Products
products = driver.find_element(By.CSS_SELECTOR, "a[href='/products/']")
actions = ActionChains(driver)
actions.move_to_element(products).perform()

#Click Ball Bearings category
ball_bearings = driver.find_element(By.CSS_SELECTOR, "a[href='/products/c/ball-bearings/']")
ball_bearings.click()

driver.execute_script("window.scrollBy(0, 900);")
driver.maximize_window()

#clean headings to store as filename
def sanitize(name):
    return name.strip().replace(" ", "_").replace("/", "-")

#extract table and save as CSV
def extract_and_save(main_heading, sub_heading):
    driver.execute_script("window.scrollBy(0, 680);")
    header = driver.find_elements(By.CSS_SELECTOR, "th[ng-style='$parent.plc.headerHeight']")
    subheader = driver.find_elements(By.XPATH, '//th[@class="column-label ng-scope no-group"]//span[@class="ng-binding"]')
    time.sleep(2)

    bearings_name = driver.find_elements(By.XPATH, '//a[starts-with(@ng-href, "/products/p/ball-bearings/")]')
    s = []
    for bearing in bearings_name:
        if "Check Inventory" not in bearing.text and bearing.text not in s:
            s.append(bearing.text)

    details = driver.find_elements(By.XPATH, '//td[@ng-repeat="filter in $parent.$parent.plc.metricsData.filters"]')
    no_of_row = driver.find_elements(By.XPATH, "//div[@class='fixed-columns']/table/tbody/tr")

    k = 0
    m = 0
    rows = []

    while k < len(no_of_row):
        row_data = {}
        for h in header:
            row_data[h.text] = s[k] if k < len(s) else ""
        for i_ in subheader:
            row_data[i_.text] = details[m].text if m < len(details) else ""
            m += 1
        rows.append(row_data)
        k += 1

    df = pd.DataFrame(rows)

    cleaned_main = sanitize(main_heading)
    cleaned_sub = sanitize(sub_heading)

    filename = f"{cleaned_main}.csv" if cleaned_main == cleaned_sub else f"{cleaned_main}_{cleaned_sub}.csv"
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

#scraping
series_selector = driver.find_elements(By.CSS_SELECTOR, "ul.grid-accordion > li > a[href]")

for i in series_selector:
    main_heading = i.text
    print(main_heading)
    i.click()
    time.sleep(1)

    #Check if heading has subcategories
    if main_heading in ["Steel", "Stainless Steel", "Thrust Bearings", "Angular Contact Ball Bearing"]:
        href_part = main_heading.lower().replace(" ", "-")
        sub_series = driver.find_elements(By.CSS_SELECTOR, f"a[href*='/products/c/ball-bearings/{href_part}/']")
        for j in sub_series:
            sub_heading = j.text
            print(sub_heading)
            j.click()
            time.sleep(1)
            extract_and_save(main_heading, sub_heading)
            driver.back()
            print('-' * 100)
    else:
        extract_and_save(main_heading, main_heading)
        driver.back()

    print('-' * 200)

input("Press Enter to exit...")


