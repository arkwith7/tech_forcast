# 논문·특허 데이터 수집 방법 분석 요약

## 📋 현황 요약

### ✅ 현재 구현된 것
1. **특허 데이터 (HBM 관련)**
   - 8개의 CSV 파일로 저장됨 (총 2.1MB)
   - 출원인, 발명자, 분류코드, 초록 등 포함
   - 출처: Gemini Patent Database (추정)
   - ⚠️ 수집 스크립트 없음 (수동 다운로드로 추정)

2. **뉴스 데이터**
   - SK하이닉스, 삼성전자 뉴스 스크래핑 완성
   - Selenium 기반 자동화
   - CSV 형식으로 저장

3. **주식 데이터**
   - yfinance를 통한 자동 수집
   - 2016-2024년 데이터

### ❌ 구현되지 않은 것
1. **논문 데이터 수집**
   - 코드 없음 (README에 계획만 존재)
   - 특허-논문 교차 분석 불가

2. **특허 데이터 자동 업데이트**
   - API 연동 없음
   - 증분 업데이트 불가

3. **자동화 파이프라인**
   - 스케줄링 없음
   - 수동 실행 필요

---

## 🔍 특허 데이터 상세

### 파일 구성
```
data/raw/HBM/
├── HBM_Gemini.csv (264KB) - 종합 데이터
├── HBM_Gemini_Applicant.csv (4.4KB) - 출원인별 통계
├── HBM_Gemini_Code.csv (1.7KB) - 기술분류 코드
├── HBM_Gemini_Inventor_Rank.csv (696B) - 발명자 순위
├── HBM_Gemini_Metric_Impact.csv (576B) - 영향력 지표
├── HBM_Gemini_With_Abstract.csv (1.7MB) - 초록 포함
├── HBM_Gemini_With_NO Abstract.csv (13KB) - 초록 없음
└── HBM_Gemini_Export_Pub_Numbers.csv (53KB) - 공개번호
```

### 주요 출원인
1. Micron Technology - 61건
2. Samsung Electronics - 25건
3. SanDisk Technologies - 18건
4. IBM - 18건

### 데이터 분석 (04_patent_analysis.ipynb)
- 출원인 분석 (기술 점유율)
- 발명자 분석 (핵심 인재)
- 기술 분류 분석 (IPC/CPC)
- 영향력 분석 (인용수 등)
- 텍스트 마이닝 (WordCloud)

---

## 📚 논문 데이터 현황

### 계획은 있으나 미구현
`data/raw/README.md`에 다음 형식이 언급됨:
```
papers_YYYY.jsonl: 학술 논문 메타데이터 및 초록
```

### 예상 소스 (미구현)
- arXiv
- Semantic Scholar
- PubMed
- IEEE Xplore
- Google Scholar

---

## 🛠️ 핵심 개선 제안

### 1순위: 특허 수집 자동화 (즉시)
```python
# 구현 필요
src/data/patent_collector.py
- PatentView API 연동
- 증분 업데이트 로직
- 데이터 검증 기능
```

**API 옵션:**
- USPTO PatentView (무료, 제한 있음)
- Google Patents (스크래핑, 저작권 주의)
- EPO Open Patent Services

### 2순위: 논문 수집 구현 (1개월)
```python
# 구현 필요
src/data/paper_collector.py
- arXiv API 연동
- Semantic Scholar API 연동
- JSONL 저장 형식
```

**권장 API:**
```python
# arXiv
import arxiv
search = arxiv.Search(query="HBM memory", max_results=100)

# Semantic Scholar
import requests
url = "https://api.semanticscholar.org/graph/v1/paper/search"
params = {"query": "HBM", "fields": "title,abstract,year"}
```

### 3순위: 자동화 파이프라인 (2개월)
```yaml
# .github/workflows/data_collection.yml
name: Weekly Data Collection
on:
  schedule:
    - cron: '0 0 * * 0'  # 매주 일요일
jobs:
  collect:
    - 특허 수집
    - 논문 수집
    - 데이터 검증
    - Git commit & push
```

---

## 📊 현재 분석 방법론

### AI 기반 하이브리드 프레임워크 (3단계)

| 단계 | 기법 | 목적 | 도구 |
|-----|------|------|------|
| 1단계 | BERTopic | 기술 진화 추적 | 동적 토픽 모델링 |
| 2단계 | SNA | 개념 간 관계 | 네트워크 분석 |
| 3단계 | LLM | 맥락 해석 | GPT 기반 분석 |

### 주요 발견
- **SK하이닉스:** HBM 집중형 전략
- **삼성전자:** 메모리+파운드리 분산형
- **약한 신호:** 하이브리드 본딩, CXL 부상

---

## 🎯 로드맵

### Phase 1: 즉시 (1-2주)
- [ ] PatentView API 연동
- [ ] 증분 업데이트 구현
- [ ] 데이터 검증 추가

### Phase 2: 단기 (1개월)
- [ ] arXiv 수집 구현
- [ ] Semantic Scholar 연동
- [ ] GitHub Actions 설정

### Phase 3: 중기 (2-3개월)
- [ ] PubMed, IEEE 추가
- [ ] 특허-논문 교차분석
- [ ] 대시보드 구축

### Phase 4: 장기 (6개월+)
- [ ] AI 자동 분류
- [ ] 실시간 모니터링
- [ ] 예측 모델 개발

---

## 💡 핵심 인사이트

### 강점
✅ 최신 AI 분석 기법 활용 (BERTopic, LLM)  
✅ 뉴스 데이터 수집 자동화 완성  
✅ 체계적인 디렉토리 구조  

### 약점
⚠️ 특허 수집 재현성 부족  
⚠️ 논문 데이터 수집 미구현  
⚠️ 자동화 파이프라인 부재  

### 기회
🚀 특허-논문 교차분석으로 인사이트 확장  
🚀 자동 업데이트로 실시간 트렌드 파악  
🚀 다양한 API 활용 가능  

### 위험
🔴 데이터 업데이트 불가 (구식 데이터)  
🔴 재현성 부족 (연구 신뢰도 저하)  
🔴 확장성 제한 (새 키워드 추가 어려움)  

---

## 🔧 즉시 실행 가능한 코드

### 1. 특허 수집 (PatentView API)
```python
# scripts/collect_patents.py
import requests
import pandas as pd

def collect_hbm_patents():
    url = "https://api.patentsview.org/patents/query"
    query = {
        "q": {"_text_any": {"patent_abstract": "HBM"}},
        "f": ["patent_number", "patent_title", "patent_abstract", 
              "patent_date", "assignee_organization"],
        "o": {"per_page": 100}
    }
    
    response = requests.post(url, json=query)
    data = response.json()
    
    df = pd.DataFrame(data.get("patents", []))
    df.to_csv("data/raw/HBM_patents_updated.csv", index=False)
    print(f"Collected {len(df)} patents")

if __name__ == "__main__":
    collect_hbm_patents()
```

### 2. 논문 수집 (arXiv)
```python
# scripts/collect_papers.py
import arxiv
import pandas as pd

def collect_hbm_papers():
    search = arxiv.Search(
        query="HBM OR 'High Bandwidth Memory'",
        max_results=100,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    papers = []
    for result in search.results():
        papers.append({
            'title': result.title,
            'abstract': result.summary,
            'published': result.published,
            'authors': ', '.join([a.name for a in result.authors]),
            'pdf_url': result.pdf_url
        })
    
    df = pd.DataFrame(papers)
    df.to_json("data/raw/papers_HBM_arxiv.jsonl", 
               orient='records', lines=True)
    print(f"Collected {len(papers)} papers")

if __name__ == "__main__":
    collect_hbm_papers()
```

### 3. 자동화 (Makefile)
```makefile
# Makefile에 추가
collect-all:
	@echo "Collecting all data..."
	python scripts/collect_patents.py
	python scripts/collect_papers.py
	python src/collect_stock_data.py
	@echo "Data collection complete"

update-weekly:
	@echo "Weekly update..."
	python scripts/incremental_update.py --days 7
```

---

## 📖 참고 자료

### API 문서
- [PatentView API](https://patentsview.org/apis/api-endpoints)
- [arXiv API](https://info.arxiv.org/help/api/index.html)
- [Semantic Scholar](https://www.semanticscholar.org/product/api)

### 필요 라이브러리
```bash
pip install arxiv
pip install semanticscholar  # 또는 requests 사용
```

### 환경 설정
```bash
# .env 파일
PATENTVIEW_API_KEY=your_key_here
SEMANTIC_SCHOLAR_API_KEY=your_key_here
```

---

**작성일:** 2025-12-04  
**상태:** 분석 완료, 개선 제안 포함  
**다음 단계:** 특허 수집 자동화 구현
