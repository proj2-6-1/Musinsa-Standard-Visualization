# 무신사 스탠다드 판매 분석 대시보드

<div align=center>
    <img src="https://autumn-windscreen-3f2.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2F4ed342a9-8224-49ba-bbad-655f8be13df1%2Fa472ffc2-14c2-4010-93c9-414b5e86030f%2Fmusinsastandard.png?table=block&id=e306676d-1ba0-4aed-a45c-d54e3624d22a&spaceId=4ed342a9-8224-49ba-bbad-655f8be13df1&width=260&userId=&cache=v2" width="150">
</div>

## **프로젝트 목적**

- 무신사 스탠다드 브랜드의 전체 상품 목록을 크롤링하고 데이터 웨어하우스에 적재
  - 파이썬과 SQL, AWS 클라우드 서비스를 사용해 봄으로써 ETL을 실습해 봄
- 상품 관련 정보를 분석하고 시각화
  - 무신사 스탠다드 브랜드에 대한 인사이트를 얻어 매출 증대에 기여할 수 있는 데이터 제공
    - 무신사 스탠다드의 판매 추이와 카테고리별 매출 분석
    - 카테고리 별 통계를 통한 구매자의 성향 파악
    - 구매 고객들의 사이즈 추천 자료를 통한 신체 사이즈로 사이즈 가이드 제공

## **활용 언어 및 활용 기술**

- 활용한 프로그래밍 언어
  - Python
  - SQL
- 활용한 기술 및 프레임워크
  - AWS S3, IAM, Redshift
  - Docker, Superset
  - Colab, Jupyter Notebook

## **프로젝트 진행 개요**

- ETL
  - Extract
    - 파이썬으로 무신사 스탠다드 상품 관련 정보 크롤링
    - CSV 파일 생성
  - Transform
    - 파이썬 Colab으로 시각화를 위한 테이블 변형
    - CSV 파일 생성
  - Load
    - AWS S3에 데이터 업로드
    - AWS Redshift에 테이블을 만들고 S3로부터 COPY하여 데이터 적재
- 시각화
  - Docker를 이용하여 Superset 실행
  - 각 차트 생성
  - 대시보드 구성

## **시각화에 사용한 데이터**

집계 상품 수, 연간 총 매출액 (가격대 별)

- 상품 수, 상품 당 매출

카테고리별 (대분류)

- 월간 조회수, 연간 판매 수, 연간 총 매출, 구매자 성별 비율

카테고리별 (중분류)

- 사이즈 구매 추이

## **프로젝트 실행 과정**

### 무신사 스탠다드에서 상품 정보 크롤링

- [무신사 스탠다드 브랜드 페이지](https://www.musinsa.com/brands/musinsastandard)
- [크롤링, 테이블 변형 코드](https://github.com/proj2-6-1/scraping)
- 파이썬 BeautifulSoup, Selenium 사용

### AWS 환경 설정

- AWS S3 버킷 생성

- AWS IAM에서 Redshift와 S3에 FullAccess 권한을 포함하는 역할 생성

- AWS Redshift에 해당 IAM을 연결하여 클러스터 생성

### AWS S3에 데이터 업로드

- AWS S3 버킷에 크롤링한 데이터 업로드

- raw_data 테이블로부터 원하는 형태로 테이블 재구성 후 CSV 파일로 저장

  - Colab 사용

- AWS S3 버킷의 analytics 폴더에 업로드

### AWS Redshift에 데이터 COPY

- Redshift schema 정하기

  - raw_data - ETL 결과가 들어감
  - analytics - ELT 결과가 들어감

- Redshift schema 아래 분석 테이블의 구조 정하기

  ```SQL
  CREATE TABLE analytics.main_category (
      category VARCHAR(100),                 -- 대분류, 문자열
      average_price DECIMAL(10, 3),          -- 평균가격, 소수점 포함 숫자
      total_annual_sales BIGINT,             -- 연간총매출, 큰 숫자
      monthly_average_views DECIMAL(10, 3),  -- 월간평균조회수, 소수점 포함 숫자
      annual_average_sales DECIMAL(10, 3),   -- 연간평균판매수, 소수점 포함 숫자
      sales_per_view DECIMAL(10, 3),         -- 조회수대비판매수, 소수점 포함 숫자
      male_buyer_ratio DECIMAL(10, 3),        -- 남성구매자비율평균, 소수점 포함 숫자
      female_buyer_ratio DECIMAL(10, 3)       -- 여성구매자비율평균, 소수점 포함 숫자
  );

  CREATE TABLE analytics.sub_category (
      subcategory VARCHAR(100),             -- 중분류, 문자열
      maincategory VARCHAR(100),            -- 대분류, 문자열
      average_likes DECIMAL(10, 3),         -- 평균좋아요, 소수점 포함 숫자
      average_rating DECIMAL(10, 3),        -- 평균평점, 소수점 포함 숫자
      average_price DECIMAL(10, 3),         -- 평균가격, 소수점 포함 숫자
      total_annual_sales BIGINT,            -- 연간총매출, 큰 숫자
      monthly_average_views DECIMAL(20, 3), -- 월간평균조회수, 소수점 포함 숫자
      annual_average_sales DECIMAL(20, 3),  -- 연간평균판매수, 소수점 포함 숫자
      male_buyer_ratio DECIMAL(10, 3),      -- 남성구매자비율평균, 소수점 포함 숫자
      female_buyer_ratio DECIMAL(10, 3)     -- 여성구매자비율평균, 소수점 포함 숫자
  );

  CREATE TABLE analytics.overall_information (
      product_count INT,                            -- 건수, 정수
      total_annual_sales BIGINT,            -- 연간총매출, 큰 숫자
      monthly_total_views BIGINT,           -- 월간전체조회수, 큰 숫자
      annual_cumulative_sales BIGINT,       -- 연간누적판매수, 큰 숫자
      sales_per_view_ratio DECIMAL(10, 3),  -- 조회수대비실판매비율, 소수점 포함 숫자
      male_buyer_ratio DECIMAL(10, 3),      -- 남성구매자비율평균, 소수점 포함 숫자
      female_buyer_ratio DECIMAL(10, 3)     -- 여성구매자비율평균, 소수점 포함 숫자
  );

  CREATE TABLE analytics.price_sales_data (
      price_range VARCHAR(100),              -- 가격 범위, 문자열
      product_count INT,                    -- 상품 개수, 정수
      annual_units_sold INT,                -- 연간 판매된 단위, 정수
      annual_sales BIGINT,                  -- 연간 매출, 큰 숫자
      sales_per_product BIGINT              -- 상품당 매출, 큰 숫자
  );

  CREATE TABLE analytics.size_recommendations (
      recom_id INT,                        -- 추천 ID, 정수
      product_id VARCHAR(50),              -- 제품 ID, 문자열
      category1 VARCHAR(50),               -- 카테고리1, 문자열
      category2 VARCHAR(50),               -- 카테고리2, 문자열
      gender VARCHAR(10),                 -- 성별, 문자열
      height INT,                          -- 키, 정수
      weight INT,                          -- 몸무게, 정수
      keyword VARCHAR(50),                -- 키워드, 문자열
      size VARCHAR(10)                     -- 사이즈, 문자열
  );
  ```

- Redshift 쿼리 편집기에서 schema, 테이블 생성

  - 클러스터(작업 그룹)에서 퍼블릭 액세스 허용으로 설정 변경
  - VPC security group의 인바운드 룰 설정 확인

- S3 버킷으로부터 Redshift에 COPY

### Superset 대시보드 구성

- Docker로 Superset 실행 후 admin으로 로그인
- 데이터베이스 연결 후 데이터 셋 만들기
- 차트 생성
  - 브랜드의 총 상품수
    - 데이터 레코드 수 합산
    - SUM(product_count)
  - 연간 총 매출 시각화
    - 1년 동안의 매출 합산
    - SUM(total_annual_sales)
  - 카테고리별 전체 통계
    - 월간 조회수: monthly_average_views (bar)
    - 연간 판매 수: annual_average_sales (bar)
    - 연간 총 매출: total_annual_sales (line)
  - 구매자 성별 비율
    - 제품별 타켓팅 방향성 분석
    - 남성 비율: male_buyer_ratio
    - 여성 비율: female_buyer_ratio
  - 가격대별 상품 및 매출 통계
    - 상품 수 Pie Chart
    - 상품 별 매출 Line Chart
    - 조회수 대비 실제 구매자 비율 Line Chart
  - 대/중분류별 몸무게,키를 통한 사이즈 선택 통계
    - 고객: 사이즈 선택 용이 / 브랜드: 생산량 파악 및 조정
    - 남성/ 여성 별 사이즈 선택 현황 파악
    - 카테고리 필터링 → 대분류/중분류 필터 박스 이용
    - 필요한 카테고리를 선택하여 필요한 정보 획득
- 대시 보드에 차트 배치

## **대시보드 결과물**

<img src="https://autumn-windscreen-3f2.notion.site/image/https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FboyJy8%2FbtsBGop4hsG%2Fcvsfn7jq4s7gYeIcj6dIGk%2Fimg.jpg?table=block&id=ea04222a-4c5a-4d9a-8129-ecfe1e84701a&spaceId=4ed342a9-8224-49ba-bbad-655f8be13df1&width=1400&userId=&cache=v2" width="700">

- 인사이트

  - 조회수 대비 실제 구매 비율은 대략 2.3%
  - 사이즈
    - 남성 기준 L > XL > M 선호
    - 여성 기준 M > S > L 선호
  - 매출
    - 전체 매출 비율은 5만원 이하 가격대의 가장 높음
    - 상품 하나 당 매출 비율은 15만원 이상~20만원 미만 구간이 가장 높음
    - 전체 구매자 성별 비율 - 남성(62.5%), 여성(37.5%)

- [결과물 소개 문서](https://file.notion.so/f/f/e937a7f9-dece-4540-8e1e-3c5966896424/73d646f6-ad12-4581-a021-cf6ba8031363/2%E1%84%8E%E1%85%A1%E1%84%91%E1%85%B3%E1%84%85%E1%85%A9%E1%84%8C%E1%85%A6%E1%86%A8%E1%84%90%E1%85%B3_6%E1%84%90%E1%85%B5%E1%86%B71%E1%84%8C%E1%85%A9.pdf?id=124a1313-6de8-43f2-9c95-3f9479347a41&table=block&spaceId=e937a7f9-dece-4540-8e1e-3c5966896424&expirationTimestamp=1707062400000&signature=tMK5dArlVL8ALMoplr9YrDlzujKxjpDySey_anjAnmU&downloadName=2%E1%84%8E%E1%85%A1%E1%84%91%E1%85%B3%E1%84%85%E1%85%A9%E1%84%8C%E1%85%A6%E1%86%A8%E1%84%90%E1%85%B3_6%E1%84%90%E1%85%B5%E1%86%B71%E1%84%8C%E1%85%A9.pdf)

## **검토 / 개선점**

- ETL 과정에서 크롤링한 데이터를 활용 가능한 데이터로 재구성하는 과정
  - 시각화를 포함해 직접적인 데이터 활용을 위한 데이터 처리, 가공의 중요성을 알게 됨
- 데이터 copy를 위한 테이블 설계 오류로 테이블을 여러 번 삭제, 재 생성
  - 각 column에 들어갈 데이터의 형식을 정확히 파악하고 테이블을 만드는 것의 중요성을 배움
- 마지막에 Redshift 프리티어가 종료되어 준비한 데이터를 모두 활용하여 대시보드를 만들지 못하는 문제점이 있었음
  - 다른 데이터 웨어하우스 서비스와 Redshift를 선택하는 것 사이의 고민이 부족했음
  - 적절한 옵션을 선택하는 것의 중요성을 알게 됨
