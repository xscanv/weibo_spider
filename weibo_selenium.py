from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

def get_driver():
    return webdriver.Chrome()

def prepare_csv(keyword):
    colname = ["author_list", "text_list"]
    csvFile = open(f"{keyword}.csv", "w", encoding="utf-8-sig", newline="")
    writer = csv.writer(csvFile)
    writer.writerow(colname)
    return csvFile, writer

def get_page_information(driver, writer):
    for i in range(20):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    nodes = driver.find_elements(By.XPATH, "//h3[@class='m-text-cut']")
    articles = driver.find_elements(By.XPATH, "//div[@class='weibo-text']")
    print(len(articles))
    author_list = []
    text_list = []
    for node in nodes:
        if "#" in node.text:
            continue
        else:
            author_list.append(node.text)
    for article in articles:
        text_list.append(article.text)
    for i in range(min(len(author_list), len(text_list))):
        write_row = [author_list[i], text_list[i]]
        print(write_row)
        writer.writerow(write_row)

def enter_AND_search(driver, keyword):
    search_box = driver.find_element(By.XPATH, "//div[@class='m-text-cut']")
    print('find it')
    search_box.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='search']")))
    input_box = driver.find_element(By.XPATH, "//input[@type='search']")  
    input_box.click()  
    input_box.send_keys(keyword)
    input_box.send_keys(Keys.RETURN)
    time.sleep(5)
    return driver

if __name__ == "__main__":
    driver = get_driver()
    keyword_list = ['中国','阿根廷','澳大利亚','巴西','加拿大','法国','德国','印度','印度尼西亚','意大利','日本','韩国','墨西哥','俄罗斯','沙特阿拉伯','南非共和国','土耳其','英国','美国'] 
    try:
        for keyword in keyword_list:
            csvFile, writer = prepare_csv(keyword)
            url = "https://m.weibo.cn/"
            driver.get(url)
            driver = enter_AND_search(driver, keyword)
            get_page_information(driver, writer)
            csvFile.close()  
    finally:
        driver.quit()  
    print("done")
