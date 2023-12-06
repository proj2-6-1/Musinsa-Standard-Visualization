# 필요한 라이브러리 불러오기
from time import sleep
import pickle

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

# 상품 페이지 url 리스트
urls = []
for i in range(1, 58):   
    # 상품 리스트 페이지 url 요청
    page_url = f"https://www.musinsa.com/brands/musinsastandard?category3DepthCodes=&category2DepthCodes=&category1DepthCode=&colorCodes=&startPrice=&endPrice=&exclusiveYn=&includeSoldOut=&saleGoods=&timeSale=&includeKeywords=&sortCode=POPULAR_BRAND&tags=&page={i}&size=90&listViewType=small&campaignCode=&groupSale=&outletGoods=&plusDelivery="
    page_res = requests.get(page_url)
    page_soup = BeautifulSoup(page_res.text, "html.parser")
    
    # 상품 페이지 url 리스트 수집
    product_list = page_soup.find("ul", id="searchList").find_all("li", "li_box")
    for product in product_list:
        urls.append("https:" + product.find("a", attrs={"name": "goods_link"})["href"])

print(f"There are {len(urls)} - products")       

# 데이터 리스트
data = []
with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    # 브라우저 창 최대화
    driver.maximize_window()
    
    for url in tqdm(urls):
        try:
            # 각 상품 페이지 url 접속
            driver.get(url)
            
            # 요청 간 텀을 주기 위함
            sleep(0.5)        
            
            # 상품 품번, 상품 명, 카테고리, 가격 수집
            product_id = driver.find_element(By.CLASS_NAME, "product_info_section").find_element(By.CLASS_NAME, "product_article_contents").text.split(" / ")[1]
            product_name = driver.find_element(By.CLASS_NAME, "product_title").find_element(By.TAG_NAME, "em").text
            category = list()
            for elem in driver.find_element(By.CLASS_NAME, "item_categories").find_elements(By.TAG_NAME, "a")[:2]:
                category.append(elem.text)
            price = driver.find_element(By.ID, "goods_price").text
            
            # 최종 데이터 dictionary 및 데이터 리스트에 추가
            elem = {
                    "id" : product_id,
                    "product_name" : product_name,
                    "category" : category,
                    "price" : price,
                    "url" : url
                }
            data.append(elem)
        except:
            print(url)    
            
# 수집된 데이터 파일 저장 
with open("../data/product_info.pkl", "wb") as f:
    pickle.dump(data, f)