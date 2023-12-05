from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"


class Scrape:
    def __init__(self, url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"user-agent={user_agent}")
        self.chrome_options = chrome_options
        self.url = url
    
    # 한 상품 페이지에서 가져올 내용
    def scrape_page(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        self.driver.get(self.url)
        wait = WebDriverWait(self.driver, 10)
        
        data = {}
        data['product_id'] = self.scrape_id(wait)
        data['recommend'] = self.scrape_recommend(wait)

        return data
    
    # 품번 추출
    def scrape_id(self, wait):
        element_id = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product_article_contents')))
        product_id = element_id.text.split(' / ')[-1]
        return product_id

    # 추천 필드 가져오기
    def scrape_recommend(self, wait):
        element_recommend = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'option_size_recom')))
        sample_recommend = element_recommend.text
        recommend_list = sample_recommend.split('[회원추천]')[1:]  # 첫 번째 빈 문자열을 제거합니다.

        recommend = []
        # 필요한 값만 추출
        for item in recommend_list:
            item = item.strip()
            gender = re.search(r'[(](.*?)[ ]', item).group(1)
            height = re.search(r'[ ](.*?)[cm]', item).group(1)
            weight = re.search(r'[\/](.*?)[kg]', item).group(1)
            keyword = re.search(r'[기준\n](.*?)[ ]', item).group(1)
            size = re.search(r'[ ](.*?)[구매]', item).group(1)
            recommend.append({'gender': gender, 'height': height, 'weight': weight, 'keyword': keyword, 'size': size})

        return recommend

    
if __name__ == "__main__":
    collected_data = []
    final_url=[]
    
    # 무신사 페이지 별 각 상품 페이지 주소 추출
    for i in range(1,58):
        res = requests.get(f"https://www.musinsa.com/brands/musinsastandard?category3DepthCodes=&category2DepthCodes=&category1DepthCode=&colorCodes=&startPrice=&endPrice=&exclusiveYn=&includeSoldOut=&saleGoods=&timeSale=&includeKeywords=&sortCode=NEW&tags=&page={i}&size=90&listViewType=small&campaignCode=&groupSale=&outletGoods=&plusDelivery=")
        soup = BeautifulSoup(res.text, "html.parser")
        urls = soup.find_all('p', class_="list_info")

        # 각 상품 페이지 주소 유효한 링크로 변환
        for u in urls:
            result_url = "https://"+u.a["href"].lstrip('//')
            final_url.append(result_url)
    
    
    for url in final_url:
        scrape = Scrape(url)
        data = scrape.scrape_page()
        collected_data.append(data)
                

    # column 명에 따라 정리
    final_data = []
    for item in collected_data:
        for recommend in item['recommend']:
            col = {**{'product_id': item['product_id']}, **recommend}
            final_data.append(col)

    # DataFrame 변환
    df = pd.DataFrame(final_data)

    print(df)
    # csv 파일로 저장
    df.to_csv('data/recommend.csv', encoding='utf-8', index=False)