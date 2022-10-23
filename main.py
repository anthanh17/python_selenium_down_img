"""
    Win platform
    Chrome version: 106
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup
import requests

from time import sleep
from typing import Optional

def init_driver(filePath: str):
    chromeOption = webdriver.ChromeOptions()
    # Config open Chrome specific path
    # Chrome profile
    chromeOption.add_argument(
        "user-data-dir=" + filePath
    )

    #config don't load pictures
    """ 
    prefs = {
        "profile.managed_default_content_settings.images" : 2
    }
    chromeOption.add_experimental_option("prefs", prefs)
    """
    
    driver = webdriver.Chrome('./chromedriver', chrome_options=chromeOption)
    return driver

def download_page(url: str) -> Optional[str]: # url can None => Optional
    res = requests.get(url)
    if res.status_code != requests.codes.ok:
        print(f'Cannot get page, eror: {res.status_code}')
        return
    return res.text

def get_url_image(html: str) -> str:
    bs_obj = BeautifulSoup(html, 'html.parser')
    elements = bs_obj.select('#comic > img')
    image_url = elements[0].attrs['src']
    if len(image_url) < 2:
        return image_url
 
    if image_url[:2] == '//':
        return 'http:' + image_url
 
    return 'http://' + image_url

def download_image(url: str):
    res = requests.get(url)
    if res.status_code != requests.codes.ok:
            print(f'Cannot get page, error: {res.status_code}')
            return
 
    img_name = url.split('/')[-1]
    f = open(img_name, "wb")
    for chunk in res.iter_content(100000):
        f.write(chunk)
 
    f.close()

def generate_image(driver):
    actionChains = ActionChains(driver)
    elemet = driver.find_element(By.XPATH, '//*[@id="middleContainer"]/ul[1]/li[3]/a')
    actionChains.click(elemet).perform()

    pageHtml = download_page(driver.current_url)
    imgUrl = get_url_image(pageHtml)
    download_image(imgUrl)

if __name__ == '__main__':
    #driver = init_driver("C:\\Users\\anthanh\\Desktop\\python_selenium_down_img\\profile")
    driver = webdriver.Chrome('./chromedriver')
    url = "https://xkcd.com/"
    driver.get(url)

    for i in range(10):
        generate_image(driver)
    """sleep(2)
    try:
        a = driver.find_element()
        a.send_keys()
        sleep(2)
    except:
        print('Was not able to find an element with that name.')
    

    try:
        b = driver.find_element_by_xpath()
        b.click()
        sleep(2)
    except:
        print('Was not able to find an element with that name.')"""
    