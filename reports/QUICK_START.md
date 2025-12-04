# 빠른 시작 가이드 (Quick Start)

## 📖 문서 읽는 순서

### 1️⃣ 먼저 읽어야 할 문서
**`ANALYSIS_SUMMARY.md`** ⭐ (본 문서부터 시작)
- 전체 분석 결과 요약
- 핵심 발견사항
- 즉시 실행 가능한 코드

### 2️⃣ 상세 내용이 궁금하다면
**`data_collection_analysis.md`** 📊
- 20KB 상세 분석 보고서
- 문제점 및 해결책
- 구현 로드맵
- 참고 자료

### 3️⃣ 간단한 요약이 필요하다면
**`data_collection_summary_ko.md`** 📝
- 핵심 내용만 간추림
- SWOT 분석
- 즉시 실행 코드

### 4️⃣ 시각적 이해가 필요하다면
**`data_pipeline_diagram.md`** 🎨
- 데이터 흐름도
- 시스템 아키텍처
- 시간선 다이어그램

---

## 🚀 즉시 실행하기

### 특허 데이터 수집
```bash
# 1. 저장소 루트로 이동
cd /path/to/tech_forcast

# 2. 특허 수집 실행
python scripts/collect_patents.py

# 3. 결과 확인
ls -lh data/raw/HBM/HBM_PatentView_*.csv
```

### 논문 데이터 수집
```bash
# 1. arxiv 라이브러리 설치
pip install arxiv

# 2. 논문 수집 실행
python scripts/collect_papers.py

# 3. 결과 확인
ls -lh data/raw/papers_HBM_arxiv_*.csv
ls -lh data/raw/papers_HBM_arxiv_*.jsonl
```

---

## 📋 체크리스트

### 현재 상태 확인
- [ ] 특허 데이터가 있는가? (`data/raw/HBM/*.csv`)
- [ ] 논문 데이터가 있는가? (`data/raw/papers_*.jsonl`)
- [ ] 뉴스 데이터가 있는가? (`data/raw/*_news.csv`)

### 개선 사항 구현
- [ ] 특허 수집 스크립트 실행 (`scripts/collect_patents.py`)
- [ ] 논문 수집 스크립트 실행 (`scripts/collect_papers.py`)
- [ ] 자동화 파이프라인 설정 (GitHub Actions)
- [ ] 데이터 품질 검증 구현

---

## 🎯 핵심 포인트

### 문제점
1. ⚠️ 특허 데이터: 수집 스크립트 없음 (수동 다운로드)
2. ❌ 논문 데이터: 미구현
3. ⚠️ 자동화: 없음

### 해결책
1. ✅ PatentView API 연동 스크립트 제공
2. ✅ arXiv API 연동 스크립트 제공
3. ✅ GitHub Actions 예제 제공 (문서)

### 다음 단계
1. 스크립트 실행 테스트
2. GitHub Actions 설정
3. 데이터 품질 관리 구현

---

## 📞 도움말

### 에러 발생 시
1. `scripts/README.md` 의 "문제 해결" 섹션 확인
2. API 타임아웃: `timeout` 값 증가
3. Rate Limit: `time.sleep()` 값 증가

### 더 알고 싶다면
- 상세 분석: `data_collection_analysis.md`
- 스크립트 가이드: `scripts/README.md`
- 시각화: `data_pipeline_diagram.md`

---

**작성일:** 2025-12-04  
**버전:** 1.0
