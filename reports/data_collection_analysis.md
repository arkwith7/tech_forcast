# 논문 및 특허 데이터 수집 방법 분석 보고서

## 1. 개요

본 문서는 `tech_forcast` 저장소의 논문 및 특허 데이터 수집 방법과 관련 코드를 분석한 결과를 정리한 것입니다.

**분석 일시:** 2025-12-04  
**저장소:** arkwith7/tech_forcast  
**주요 초점:** 특허 및 논문 데이터의 수집, 저장, 분석 방법론

---

## 2. 현재 데이터 수집 현황

### 2.1 특허 데이터

#### 2.1.1 데이터 소스
- **주요 출처:** Gemini Patent Database (추정)
- **분석 대상 기술:** HBM (High Bandwidth Memory)
- **데이터 위치:** `data/raw/HBM/`

#### 2.1.2 수집된 특허 데이터 파일
저장소에는 다음과 같은 특허 관련 CSV 파일들이 존재합니다:

1. **HBM_Gemini.csv** (264KB)
   - HBM 관련 특허의 종합 데이터
   - 특허 전반의 메타데이터 포함

2. **HBM_Gemini_Applicant.csv** (4.4KB)
   - 출원인별 특허 수 집계
   - 컬럼: `applicant_name`, `country`, `patent_count`, `last_filing_year`
   - 주요 출원인: Micron Technology (61건), Samsung Electronics (25건), SanDisk Technologies (18건) 등

3. **HBM_Gemini_Code.csv** (1.7KB)
   - IPC/CPC 기술 분류 코드 정보
   - 특허의 기술 분야 카테고리화

4. **HBM_Gemini_Inventor_Rank.csv** (696B)
   - 핵심 발명자 랭킹 데이터
   - 발명자별 특허 출원 건수

5. **HBM_Gemini_Metric_Impact.csv** (576B)
   - 특허의 기술적 영향력 지표
   - 인용 수, 패밀리 국가 수 등 질적 평가 지표

6. **HBM_Gemini_With_Abstract.csv** (1.7MB)
   - 특허 초록(Abstract)을 포함한 상세 데이터
   - 텍스트 마이닝 및 키워드 분석용

7. **HBM_Gemini_With_NO Abstract.csv** (13KB)
   - 초록이 없는 특허 데이터

8. **HBM_Gemini_Export_Pub_Numbers.csv** (53KB)
   - 특허 공개번호 목록

#### 2.1.3 특허 데이터 수집 방법

**현재 확인된 사항:**
- 파일명에 "Gemini"가 포함되어 있어 **Gemini Patent Database** 또는 유사한 특허 검색 플랫폼을 통해 수집된 것으로 추정
- 데이터는 이미 구조화된 CSV 형식으로 저장되어 있음
- 자동화된 API 또는 데이터 다운로드 스크립트는 저장소에서 발견되지 않음

**데이터 특성:**
- 수집 기간: 최소 2024년까지 (최신 출원년도 기준)
- 검색 쿼리: "HBM" 키워드 기반 검색으로 추정
- 데이터 품질: 출원인, 발명자, 분류 코드, 초록 등 포괄적인 메타데이터 포함

### 2.2 논문 데이터

#### 2.2.1 현재 상태
저장소 분석 결과, **학술 논문 데이터의 실제 수집 코드나 데이터 파일은 발견되지 않았습니다.**

다만, 다음과 같은 참조가 확인되었습니다:

1. **data/raw/README.md**
   ```markdown
   원본 특허 및 논문 데이터를 저장하는 디렉토리입니다. 파일 예시:
   - patents_YYYY.csv: 특허 메타데이터 및 본문
   - papers_YYYY.jsonl: 학술 논문 메타데이터 및 초록
   ```
   - 논문 데이터 저장 형식 가이드는 있으나 실제 데이터는 없음

2. **src/data/loaders.py**
   ```python
   def list_patent_files(directory: Union[str, Path], suffix: str = ".xml"):
       """특허 XML/JSON 파일 목록을 반환합니다."""
   ```
   - 특허 파일 로딩 함수는 있으나 논문 관련 함수는 없음

3. **연구 보고서 (reports/research_paper_v2.md)**
   - 향후 연구 방향으로 "특허 데이터와의 교차 분석"을 언급
   - 현재는 뉴스 데이터 위주의 분석

#### 2.2.2 논문 데이터 수집 계획 (추정)
`data/raw/README.md`의 내용을 바탕으로 다음과 같은 형식의 논문 데이터 수집이 계획된 것으로 보입니다:

- **파일 형식:** JSONL (JSON Lines)
- **포함 정보:** 메타데이터 및 초록
- **예상 소스:** 
  - arXiv
  - PubMed
  - Semantic Scholar
  - Google Scholar API
  - IEEE Xplore

### 2.3 뉴스 데이터 (보완 정보)

논문/특허 데이터와 함께 분석에 활용되는 뉴스 데이터는 활발히 수집되고 있습니다.

#### 2.3.1 뉴스 스크래핑 노트북
1. **00_1_sk_hynix_news_scraping.ipynb**
   - SK하이닉스 뉴스룸 스크래핑
   - Selenium WebDriver 사용
   - 결과 파일: `data/raw/skhynix_news.csv`

2. **00_2_samsung_semiconductor_news_scraping.ipynb**
   - 삼성전자 반도체 뉴스룸 스크래핑
   - Selenium WebDriver 사용
   - 결과 파일: `data/raw/samsung_news.csv`

#### 2.3.2 뉴스 스크래핑 기술 스택
```python
# 주요 라이브러리
- selenium: 동적 웹페이지 스크래핑
- webdriver-manager: ChromeDriver 자동 관리
- pandas: 데이터 저장 및 처리
- BeautifulSoup4: HTML 파싱 (requirements.txt에 포함)
```

#### 2.3.3 뉴스 스크래퍼 구조
```python
class SKHynixNewsScraper / SamsungSemiconNewsScraper:
    - ChromeDriverWrapper: 싱글톤 패턴으로 WebDriver 관리
    - 헤드리스 모드 실행 (--headless)
    - 로깅 시스템 구축
    - URL 인코딩 처리
    - 예외 처리 및 재시도 로직
```

### 2.4 주식 데이터 (참고)

`src/collect_stock_data.py`를 통해 보조 데이터로 주식 정보도 수집합니다:

```python
# yfinance를 사용한 주식 데이터 수집
- 삼성전자: 005930.KS
- SK하이닉스: 000660.KS
- 기간: 2016-01-01 ~ 2024-12-31
- 결과: data/raw/samsung_stock.csv, skhynix_stock.csv
```

---

## 3. 데이터 처리 및 분석 파이프라인

### 3.1 데이터 로딩 모듈 (src/data/loaders.py)

```python
def load_csv(path: Union[str, Path], **read_kwargs) -> pd.DataFrame:
    """CSV 파일을 DataFrame으로 로드"""
    # 파일 존재 여부 확인
    # 인코딩 문제 자동 처리

def list_patent_files(directory: Union[str, Path], suffix: str = ".xml"):
    """특허 XML/JSON 파일 목록을 반환"""
    # .xml 또는 .json 확장자 파일 검색
```

### 3.2 특허 데이터 분석 노트북

**04_patent_analysis.ipynb** 에서 수행하는 분석:

1. **출원인(Applicant) 분석**
   - Top 15 기업의 특허 수 시각화
   - 기술 점유율 파악

2. **발명자(Inventor) 분석**
   - 핵심 인재 파악
   - 기업별 인재 쏠림 현상 분석

3. **기술 분류(IPC/CPC Code) 분석**
   - HBM 기술의 세부 기술 분야 분포
   - 메모리 소자 vs 패키징 vs 회로 비중

4. **기술 영향력(Impact Metric) 분석**
   - 인용 수, 패밀리 국가 수 등
   - 양적/질적 평가 결합

5. **초록 텍스트 마이닝**
   - WordCloud 시각화
   - 핵심 키워드 추출

### 3.3 안전한 데이터 로딩

```python
def load_csv_safe(filepath):
    """인코딩 에러를 방지하는 안전한 CSV 로딩"""
    encodings = ['utf-8', 'cp949', 'euc-kr', 'latin1']
    for enc in encodings:
        try:
            df = pd.read_csv(filepath, encoding=enc)
            return df
        except UnicodeDecodeError:
            continue
    return None
```

---

## 4. 분석 방법론: AI 기반 하이브리드 프레임워크

저장소의 연구 보고서(research_paper_v2.md)에 따르면, 다음과 같은 3단계 분석을 수행합니다:

### 4.1 1단계: BERTopic (동적 토픽 모델링)
- **목적:** 기술의 시계열적 진화 추적
- **적용:** 2016-2024년 DRAM → HBM → AI 메모리 분화 과정 분석
- **도구:** BERTopic, BERT 기반 임베딩

### 4.2 2단계: SNA (의미 연결망 분석)
- **목적:** 기술 개념 간 구조적 관계 규명
- **방법:** Co-occurrence Network, Centrality Analysis
- **결과:** 기업별 기술 전략 차이 식별 (SK하이닉스: 집중형 vs 삼성전자: 분산형)

### 4.3 3단계: LLM (생성형 AI 증강 분석)
- **목적:** 맥락 해석 및 예측
- **적용:**
  - Weak Signal Detection (하이브리드 본딩, CXL 등)
  - 속성 기반 감성 분석
  - 기술-사업성 분리 평가

---

## 5. 문제점 및 개선 방향

### 5.1 현재 문제점

#### A. 특허 데이터 수집의 재현성 부족
**문제:**
- 특허 데이터가 이미 CSV 파일로만 제공됨
- 데이터 수집 스크립트가 없어 업데이트 불가
- 수집 날짜, 검색 쿼리, 필터 조건 등 메타정보 부재

**영향:**
- 최신 데이터 업데이트 어려움
- 다른 기술 키워드로 확장 불가
- 연구 재현성 저하

#### B. 논문 데이터 수집 기능 부재
**문제:**
- 논문 데이터 수집 코드 전무
- README에 계획만 있고 실제 구현 없음
- 특허 데이터와 논문 데이터의 교차 분석 불가

**영향:**
- 기술 발전의 학술적 배경 분석 불가
- 산업(특허)과 학계(논문)의 시차 분석 불가
- 연구의 완성도 저하

#### C. 데이터 수집 자동화 부재
**문제:**
- 뉴스 스크래핑은 수동으로 노트북 실행 필요
- 스케줄링 기능 없음
- 증분(incremental) 업데이트 로직 없음

**영향:**
- 데이터 신선도 유지 어려움
- 수동 작업에 따른 오류 가능성

#### D. 데이터 품질 관리 부족
**문제:**
- 중복 데이터 제거 로직 부재
- 데이터 검증(validation) 과정 없음
- 결측치 처리 전략 불명확

### 5.2 개선 제안

#### A. 특허 데이터 수집 자동화 구축

**제안 1: PatentView API 활용**
```python
# src/data/patent_collector.py (신규 생성)

import requests
import pandas as pd
from typing import List, Dict

class PatentViewCollector:
    """USPTO PatentView API를 사용한 특허 데이터 수집"""
    
    BASE_URL = "https://api.patentsview.org/patents/query"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        
    def search_patents(
        self, 
        keyword: str, 
        start_date: str = "2020-01-01",
        end_date: str = "2024-12-31",
        fields: List[str] = None
    ) -> pd.DataFrame:
        """키워드 기반 특허 검색"""
        
        if fields is None:
            fields = [
                "patent_number", "patent_title", "patent_abstract",
                "patent_date", "assignee_organization", "inventor_last_name",
                "cpc_subgroup_id", "patent_num_cited_by_us_patents"
            ]
        
        query = {
            "q": {"_text_any": {"patent_abstract": keyword}},
            "f": fields,
            "o": {"per_page": 100}
        }
        
        response = requests.post(self.BASE_URL, json=query)
        data = response.json()
        
        return pd.DataFrame(data.get("patents", []))
    
    def get_patent_details(self, patent_number: str) -> Dict:
        """특정 특허의 상세 정보 조회"""
        # 구현 예정
        pass
```

**제안 2: Google Patents 스크래퍼 구축**
```python
# src/data/google_patents_scraper.py (신규 생성)

from selenium import webdriver
import pandas as pd

class GooglePatentsScraper:
    """Google Patents 검색 결과 스크래핑"""
    
    def __init__(self):
        self.base_url = "https://patents.google.com/"
        
    def search_patents(self, query: str, num_results: int = 100):
        """Google Patents 검색"""
        # Selenium 기반 스크래핑 로직
        pass
    
    def get_patent_metadata(self, patent_id: str):
        """특허 메타데이터 추출"""
        pass
```

**제안 3: 데이터 수집 설정 파일**
```yaml
# configs/patent_collection.yaml (신규 생성)

patent_sources:
  - name: "PatentView"
    enabled: true
    api_key: "${PATENTVIEW_API_KEY}"
    
  - name: "Google Patents"
    enabled: false  # 저작권 이슈 주의
    
search_queries:
  - keyword: "HBM"
    aliases: ["High Bandwidth Memory", "HBM2", "HBM3"]
    date_range:
      start: "2020-01-01"
      end: "2024-12-31"
      
  - keyword: "3D NAND"
    aliases: ["V-NAND", "3D Flash Memory"]
    date_range:
      start: "2020-01-01"
      end: "2024-12-31"

fields_to_collect:
  - patent_number
  - title
  - abstract
  - filing_date
  - publication_date
  - assignee
  - inventor
  - cpc_codes
  - ipc_codes
  - citations_count
  - family_size
```

#### B. 논문 데이터 수집 구현

**제안 1: arXiv API 활용**
```python
# src/data/paper_collector.py (신규 생성)

import arxiv
import pandas as pd
from typing import List

class ArxivCollector:
    """arXiv API를 사용한 논문 데이터 수집"""
    
    def search_papers(
        self,
        query: str,
        max_results: int = 100,
        categories: List[str] = None
    ) -> pd.DataFrame:
        """논문 검색"""
        
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        papers = []
        for result in search.results():
            papers.append({
                'id': result.entry_id,
                'title': result.title,
                'abstract': result.summary,
                'authors': [author.name for author in result.authors],
                'published': result.published,
                'categories': result.categories,
                'pdf_url': result.pdf_url
            })
        
        return pd.DataFrame(papers)
    
    def save_papers_jsonl(self, df: pd.DataFrame, output_path: str):
        """JSONL 형식으로 저장"""
        df.to_json(output_path, orient='records', lines=True)
```

**제안 2: Semantic Scholar API 활용**
```python
# src/data/semantic_scholar_collector.py (신규 생성)

import requests
import pandas as pd

class SemanticScholarCollector:
    """Semantic Scholar API를 사용한 논문 수집"""
    
    BASE_URL = "https://api.semanticscholar.org/graph/v1"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"x-api-key": api_key}
    
    def search_papers(
        self,
        query: str,
        fields: List[str] = None,
        limit: int = 100
    ) -> pd.DataFrame:
        """논문 검색"""
        
        if fields is None:
            fields = [
                "paperId", "title", "abstract", "year",
                "authors", "citationCount", "referenceCount",
                "fieldsOfStudy", "venue"
            ]
        
        params = {
            "query": query,
            "fields": ",".join(fields),
            "limit": limit
        }
        
        response = requests.get(
            f"{self.BASE_URL}/paper/search",
            params=params,
            headers=self.headers
        )
        
        data = response.json()
        return pd.DataFrame(data.get("data", []))
```

**제안 3: 논문 수집 통합 스크립트**
```python
# scripts/collect_papers.py (신규 생성)

import argparse
from src.data.paper_collector import ArxivCollector
from src.data.semantic_scholar_collector import SemanticScholarCollector
import yaml

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/paper_collection.yaml")
    parser.add_argument("--source", choices=["arxiv", "semantic_scholar", "all"])
    args = parser.parse_args()
    
    with open(args.config) as f:
        config = yaml.safe_load(f)
    
    # 논문 수집 로직
    if args.source in ["arxiv", "all"]:
        collector = ArxivCollector()
        for query_config in config["search_queries"]:
            papers = collector.search_papers(
                query=query_config["keyword"],
                max_results=query_config.get("max_results", 100)
            )
            output_path = f"data/raw/papers_{query_config['keyword']}_arxiv.jsonl"
            collector.save_papers_jsonl(papers, output_path)
            print(f"Collected {len(papers)} papers from arXiv for '{query_config['keyword']}'")
    
    # 추가 소스 처리...

if __name__ == "__main__":
    main()
```

#### C. 데이터 수집 자동화 파이프라인

**제안 1: Makefile 확장**
```makefile
# Makefile에 추가

.PHONY: collect-patents collect-papers collect-news collect-all

collect-patents:
	python scripts/collect_patents.py --config configs/patent_collection.yaml

collect-papers:
	python scripts/collect_papers.py --config configs/paper_collection.yaml

collect-news:
	jupyter nbconvert --to notebook --execute notebooks/00_1_sk_hynix_news_scraping.ipynb
	jupyter nbconvert --to notebook --execute notebooks/00_2_samsung_semiconductor_news_scraping.ipynb

collect-all: collect-patents collect-papers collect-news
	@echo "All data collection completed"

# 데이터 업데이트 (증분)
update-data:
	python scripts/incremental_update.py --days 7
```

**제안 2: GitHub Actions 워크플로우**
```yaml
# .github/workflows/data_collection.yml (신규 생성)

name: Weekly Data Collection

on:
  schedule:
    - cron: '0 0 * * 0'  # 매주 일요일 00:00 UTC
  workflow_dispatch:  # 수동 실행 가능

jobs:
  collect-data:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Collect Patents
        env:
          PATENTVIEW_API_KEY: ${{ secrets.PATENTVIEW_API_KEY }}
        run: |
          python scripts/collect_patents.py
      
      - name: Collect Papers
        env:
          SEMANTIC_SCHOLAR_API_KEY: ${{ secrets.SEMANTIC_SCHOLAR_API_KEY }}
        run: |
          python scripts/collect_papers.py
      
      - name: Commit and Push
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add data/raw/
          git commit -m "Auto-update: Weekly data collection $(date)" || exit 0
          git push
```

**제안 3: 증분 업데이트 스크립트**
```python
# scripts/incremental_update.py (신규 생성)

import argparse
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path

def get_last_update_date(data_file: Path) -> datetime:
    """마지막 업데이트 날짜 조회"""
    if not data_file.exists():
        return datetime(2020, 1, 1)  # 기본 시작일
    
    df = pd.read_csv(data_file)
    # 파일의 마지막 날짜 파싱
    last_date = pd.to_datetime(df['date']).max()
    return last_date

def incremental_collect(days: int = 7):
    """최근 N일간의 데이터만 수집"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # 특허 증분 수집
    patent_file = Path("data/raw/HBM_patents.csv")
    last_update = get_last_update_date(patent_file)
    
    if last_update < end_date:
        # 새 데이터 수집
        new_patents = collect_patents_since(last_update)
        
        # 기존 데이터와 병합
        if patent_file.exists():
            existing = pd.read_csv(patent_file)
            combined = pd.concat([existing, new_patents]).drop_duplicates()
        else:
            combined = new_patents
        
        combined.to_csv(patent_file, index=False)
        print(f"Added {len(new_patents)} new patents")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()
    
    incremental_collect(args.days)
```

#### D. 데이터 품질 관리

**제안 1: 데이터 검증 모듈**
```python
# src/data/validator.py (신규 생성)

import pandas as pd
from typing import List, Dict

class DataValidator:
    """데이터 품질 검증"""
    
    def validate_patent_data(self, df: pd.DataFrame) -> Dict:
        """특허 데이터 검증"""
        report = {
            "total_rows": len(df),
            "duplicates": df.duplicated().sum(),
            "missing_values": df.isnull().sum().to_dict(),
            "invalid_dates": 0,
            "issues": []
        }
        
        # 필수 컬럼 확인
        required_cols = ["patent_number", "title", "filing_date"]
        missing_cols = set(required_cols) - set(df.columns)
        if missing_cols:
            report["issues"].append(f"Missing columns: {missing_cols}")
        
        # 날짜 형식 검증
        try:
            pd.to_datetime(df["filing_date"])
        except:
            report["invalid_dates"] = df["filing_date"].isnull().sum()
            report["issues"].append("Invalid date format in filing_date")
        
        return report
    
    def clean_patent_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """데이터 정제"""
        # 중복 제거 (patent_number 기준)
        df = df.drop_duplicates(subset=["patent_number"])
        
        # 결측치 처리
        df["abstract"] = df["abstract"].fillna("No abstract available")
        
        # 날짜 정규화
        df["filing_date"] = pd.to_datetime(df["filing_date"], errors='coerce')
        
        return df
```

**제안 2: 데이터 품질 리포트 생성**
```python
# scripts/generate_data_quality_report.py (신규 생성)

from src.data.validator import DataValidator
import pandas as pd
import json

def generate_report():
    validator = DataValidator()
    
    # 특허 데이터 검증
    patent_df = pd.read_csv("data/raw/HBM_Gemini.csv")
    patent_report = validator.validate_patent_data(patent_df)
    
    # 논문 데이터 검증
    # ...
    
    # 리포트 저장
    with open("reports/data_quality_report.json", "w") as f:
        json.dump({
            "patents": patent_report,
            # "papers": paper_report
        }, f, indent=2)
    
    print("Data quality report generated")

if __name__ == "__main__":
    generate_report()
```

---

## 6. 데이터 수집 우선순위 로드맵

### Phase 1: 즉시 구현 (1-2주)
1. **특허 데이터 수집 자동화**
   - PatentView API 연동
   - 증분 업데이트 로직 구현
   - 데이터 검증 추가

2. **데이터 품질 관리**
   - 중복 제거 로직
   - 결측치 처리 표준화
   - 품질 리포트 자동 생성

### Phase 2: 단기 구현 (1개월)
1. **논문 데이터 수집 구축**
   - arXiv API 연동
   - Semantic Scholar API 연동
   - JSONL 저장 형식 구현

2. **자동화 파이프라인**
   - GitHub Actions 워크플로우
   - 스케줄링 설정
   - 오류 알림 시스템

### Phase 3: 중기 개선 (2-3개월)
1. **데이터 소스 확장**
   - PubMed (생명과학 관련)
   - IEEE Xplore (전자공학)
   - WIPO (국제 특허)

2. **고급 분석 기능**
   - 특허-논문 인용 관계 분석
   - 산학 연계 네트워크 분석
   - 기술 확산 시차 분석

### Phase 4: 장기 발전 (6개월+)
1. **AI 기반 데이터 증강**
   - LLM을 활용한 자동 분류
   - 약한 신호 자동 탐지
   - 예측 모델 구축

2. **실시간 모니터링**
   - 스트리밍 데이터 파이프라인
   - 대시보드 구축
   - 알림 시스템

---

## 7. 기술 스택 요약

### 현재 사용 중
- **웹 스크래핑:** Selenium, BeautifulSoup4
- **데이터 처리:** pandas, numpy
- **텍스트 분석:** BERTopic, spaCy, nltk, sentence-transformers
- **네트워크 분석:** networkx
- **시각화:** matplotlib, seaborn, plotly, wordcloud
- **ML/DL:** scikit-learn, torch, transformers
- **노트북:** Jupyter Lab

### 추가 권장
- **특허 API:** `requests`, USPTO PatentView API
- **논문 API:** `arxiv`, Semantic Scholar API
- **스케줄링:** `schedule`, APScheduler
- **데이터 검증:** `pandera`, `great_expectations`
- **워크플로우:** Prefect, Airflow (선택)

---

## 8. 결론

### 8.1 주요 발견사항
1. **특허 데이터는 수집되어 있으나 재현성이 부족**
   - Gemini 데이터베이스에서 수동으로 다운로드한 것으로 추정
   - 업데이트 메커니즘 없음

2. **논문 데이터 수집 기능이 전무**
   - README에 계획만 있고 구현 없음
   - 특허-논문 교차 분석 불가

3. **뉴스 데이터 수집은 잘 구현됨**
   - Selenium 기반 스크래퍼 완성
   - 다만 자동화는 미흡

4. **분석 방법론은 최신 기술 활용**
   - BERTopic, SNA, LLM 결합
   - 학술적 완성도 높음

### 8.2 핵심 권장사항
1. **특허 수집 자동화 최우선 구축**
   - PatentView API 활용
   - 증분 업데이트 구현

2. **논문 수집 기능 신규 개발**
   - arXiv + Semantic Scholar
   - 특허 데이터와 동일 수준으로 구조화

3. **데이터 품질 관리 체계 수립**
   - 검증, 정제, 모니터링
   - 품질 리포트 자동 생성

4. **자동화 파이프라인 구축**
   - GitHub Actions 활용
   - 주간 자동 업데이트

### 8.3 기대 효과
- **재현성 향상:** 누구나 데이터 수집 과정을 재현 가능
- **최신성 유지:** 자동 업데이트로 데이터 신선도 보장
- **분석 확장:** 특허-논문 교차 분석으로 인사이트 심화
- **연구 품질:** 학술 논문 수준의 데이터 파이프라인 완성

---

## 9. 참고 자료

### 특허 데이터 소스
- [USPTO PatentView](https://patentsview.org/apis/api-endpoints)
- [Google Patents](https://patents.google.com/)
- [WIPO Patentscope](https://patentscope.wipo.int/)
- [EPO Open Patent Services](https://www.epo.org/searching-for-patents/data/web-services.html)

### 논문 데이터 소스
- [arXiv API](https://info.arxiv.org/help/api/index.html)
- [Semantic Scholar API](https://www.semanticscholar.org/product/api)
- [PubMed API](https://www.ncbi.nlm.nih.gov/home/develop/api/)
- [IEEE Xplore API](https://developer.ieee.org/)

### 추천 도서 및 논문
- Grootendorst, M. (2022). BERTopic: Neural topic modeling. arXiv:2203.05794
- Newman, M. E. J. (2018). Networks (2nd ed.). Oxford University Press.
- Rogers, E. M. (2003). Diffusion of Innovations (5th ed.). Free Press.

---

**문서 작성:** GitHub Copilot  
**분석 대상 저장소:** arkwith7/tech_forcast  
**작성일:** 2025-12-04  
**버전:** 1.0
