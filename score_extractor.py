import pandas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

path = "chromedriver_win32\\chromedriver"
url = "https://www.espncricinfo.com/series/8048/scorecard/1237181/delhi-capitals-vs-mumbai-indians-final-indian-premier-league-2020-21"

score_table = None
headers = []

tbl_xpath_str1 = "//*[@id='main-container']/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div/table[1]/tbody/tr["
tbl_xpath_str2 = "]/td["
tbl_xpath_str3 = "]"

driver = webdriver.Chrome(path)
driver.get(url)

while score_table is None:
    try:
        score_table = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='main-container']/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div/table[1]/tbody/tr"))
            )
    except:
        pass
    if score_table:
        break

if score_table:
    row_count = len(driver.find_elements_by_xpath("//*[@id='main-container']/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div/table[1]/tbody/tr"))
    col_count = len(driver.find_elements_by_xpath("//*[@id='main-container']/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div/table[1]/tbody/tr[1]/td"))

header_count = len(driver.find_elements_by_xpath("//*[@id='main-container']/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div/table[1]/thead/tr/th"))

for col in range(1, header_count+1):
    col_name = driver.find_elements_by_xpath("//*[@id='main-container']/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div/table[1]/thead/tr/th[" + str(col) + "]")[0].text
    headers.append(col_name)

df = pandas.DataFrame(columns = headers)

for row in range(1, row_count+1):
    table_row_list = []
    for col in range(1, col_count+1):
        try:
            tbl_xpath_fullstr = tbl_xpath_str1 + str(row) + tbl_xpath_str2 + str(col) + tbl_xpath_str3
            table_data = driver.find_element_by_xpath(tbl_xpath_fullstr).text
            table_row_list.append(table_data)
        except:
            pass
    
    if table_row_list != ['']:
        if len(table_row_list)==len(df.columns):
            df1 = pandas.DataFrame([table_row_list], columns = headers)
            df = df.append(df1, ignore_index=True)
        else:
            if len(table_row_list) < len(df.columns):
                for i in range(len(table_row_list), len(df.columns)):
                    table_row_list.append(None)
                df1 = pandas.DataFrame([table_row_list], columns = headers)
                df = df.append(df1, ignore_index=True)

print(df)
