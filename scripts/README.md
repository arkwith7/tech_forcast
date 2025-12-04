# 데이터 수집 스크립트

이 디렉토리는 논문 및 특허 데이터를 자동으로 수집하는 스크립트를 포함합니다.

## 스크립트 목록

### 1. collect_patents.py
USPTO PatentView API를 사용하여 특허 데이터를 수집합니다.

**사용법:**
```bash
python scripts/collect_patents.py
```

**기능:**
- HBM 관련 특허 자동 검색
- 페이지네이션 지원 (대량 데이터 수집)
- 중복 제거
- 출원인별, 연도별 통계 자동 생성
- CSV 형식으로 저장

**출력 파일:**
- `data/raw/HBM/HBM_PatentView_YYYYMMDD.csv` - 전체 특허 데이터
- `data/raw/HBM/HBM_Assignee_Stats_YYYYMMDD.csv` - 출원인별 통계
- `data/raw/HBM/HBM_Yearly_Stats_YYYYMMDD.csv` - 연도별 통계

### 2. collect_papers.py
arXiv API를 사용하여 학술 논문 데이터를 수집합니다.

**사용법:**
```bash
python scripts/collect_papers.py
```

**기능:**
- HBM 관련 논문 자동 검색
- 컴퓨터 아키텍처, 분산 컴퓨팅 등 관련 카테고리 필터링
- 중복 제거
- CSV 및 JSONL 형식 지원
- 메타데이터 포함 (저자, 초록, 카테고리 등)

**출력 파일:**
- `data/raw/papers_HBM_arxiv_YYYYMMDD.csv` - CSV 형식
- `data/raw/papers_HBM_arxiv_YYYYMMDD.jsonl` - JSONL 형식 (README 권장 형식)

## 필요 라이브러리

스크립트 실행 전 필요한 라이브러리를 설치하세요:

```bash
pip install arxiv requests pandas
```

또는 requirements.txt에 추가:
```
arxiv>=2.0.0
```

## API 정보

### PatentView API
- **URL:** https://api.patentsview.org/
- **문서:** https://patentsview.org/apis/api-endpoints
- **API 키:** 현재 불필요 (무료, rate limit 있음)
- **Rate Limit:** 요청당 1초 대기 권장

### arXiv API
- **URL:** https://arxiv.org/help/api/
- **문서:** https://info.arxiv.org/help/api/index.html
- **API 키:** 불필요
- **Rate Limit:** 요청당 3초 대기 권장 (스크립트는 0.5초 설정)

## 커스터마이징

### 검색 키워드 변경
각 스크립트의 `keywords` 또는 `queries` 리스트를 수정:

```python
# collect_patents.py
keywords = [
    "HBM",
    "High Bandwidth Memory",
    "YOUR_KEYWORD_HERE"
]

# collect_papers.py
queries = [
    "HBM",
    "YOUR_QUERY_HERE"
]
```

### 날짜 범위 변경
```python
# collect_patents.py
df = collector.search_patents(
    keyword=keyword,
    start_date="2020-01-01",  # 시작 날짜
    end_date="2024-12-31",     # 종료 날짜
    max_results=500
)
```

### 결과 수 변경
```python
max_results=1000  # 더 많은 결과 수집
```

## 자동화 예제

### Makefile 사용
```makefile
collect-all:
	python scripts/collect_patents.py
	python scripts/collect_papers.py
```

실행:
```bash
make collect-all
```

### Cron 작업 (Linux/Mac)
매주 일요일 자동 실행:
```bash
0 0 * * 0 cd /path/to/tech_forcast && python scripts/collect_patents.py
0 1 * * 0 cd /path/to/tech_forcast && python scripts/collect_papers.py
```

### GitHub Actions
`.github/workflows/data_collection.yml` 파일 참조 (별도 생성 필요)

## 문제 해결

### 1. API 타임아웃
```python
# timeout 값 증가
response = self.session.post(self.BASE_URL, json=query, timeout=60)
```

### 2. Rate Limit 오류
```python
# 대기 시간 증가
time.sleep(3)  # 1초 -> 3초
```

### 3. 네트워크 오류
재시도 로직 추가 (향후 구현 예정)

## 향후 개선 계획

- [ ] 증분 업데이트 기능 (마지막 수집 이후 데이터만)
- [ ] 설정 파일 기반 실행 (YAML)
- [ ] 오류 재시도 로직
- [ ] Semantic Scholar API 추가
- [ ] PubMed API 추가
- [ ] 진행률 표시
- [ ] 이메일 알림 기능

## 참고 자료

- [USPTO PatentView Documentation](https://patentsview.org/apis/api-endpoints)
- [arXiv API User Manual](https://info.arxiv.org/help/api/user-manual.html)
- [Python arxiv Package](https://pypi.org/project/arxiv/)
