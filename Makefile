.PHONY: help setup install install-dev lint format notebooks

PYTHON ?= python3
VENV_DIR ?= .venv
ACTIVATE = source $(VENV_DIR)/bin/activate

help:
	@echo "사용 가능한 명령:"
	@echo "  make setup       - 가상환경 생성 및 기본/개발 패키지 설치"
	@echo "  make install     - requirements.txt 설치"
	@echo "  make install-dev - 개발 도구 설치"
	@echo "  make lint        - ruff를 이용한 린트 검사"
	@echo "  make format      - black을 이용한 코드 포맷팅"
	@echo "  make notebooks   - 주피터 노트북 서버 실행"

setup:
	$(PYTHON) -m venv $(VENV_DIR)
	$(ACTIVATE) && pip install --upgrade pip wheel
	$(ACTIVATE) && pip install -r requirements.txt
	$(ACTIVATE) && pip install -r requirements-dev.txt

install:
	$(ACTIVATE) && pip install -r requirements.txt

install-dev:
	$(ACTIVATE) && pip install -r requirements-dev.txt

lint:
	$(ACTIVATE) && ruff check src

format:
	$(ACTIVATE) && black src

notebooks:
	$(ACTIVATE) && jupyter lab
