# Tech Forecast NLP 프로젝트

이 저장소는 특허 및 논문 텍스트를 활용해 자연어처리 기반 기술 예측을 수행하기 위한 초기 환경을 제공합니다.

## 주요 디렉토리 구조

- `data/raw`: 원본 데이터 (특허, 논문 등)
- `data/interim`: 전처리 중간 산출물
- `data/processed`: 모델 및 분석에 사용 가능한 정제된 데이터
- `notebooks`: 탐색적 데이터 분석 및 실험용 주피터 노트북
- `src/`: 재사용 가능한 파이썬 모듈
  - `src/data`: 데이터 로딩 및 전처리 모듈
  - `src/features`: 특징 공학 관련 코드
  - `src/models`: 모델 학습 및 예측 코드
  - `src/visualization`: 시각화 관련 코드
- `configs`: 설정 파일 (예: 실험 설정, API 키 템플릿 등)
- `reports`: 리포트, 발표 자료 등 산출물

## 시작하기

1. 가상환경 생성 및 활성화

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
   ```

2. 패키지 설치

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. 주피터 커널 등록 (선택)

   ```bash
   python -m ipykernel install --user --name tech_forecast --display-name "Tech Forecast"
   ```

## 참고 사항

- `.env` 파일을 사용해 민감 정보(API 키 등)를 관리할 수 있습니다. 템플릿은 차후 `configs/` 디렉토리에 추가할 수 있습니다.
- 데이터 용량이 큰 경우, Git LFS 또는 별도의 데이터 저장소 활용을 고려하세요.

