import json
import os

# 노트북 내용 정의 (JSON 구조)
notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 04. Comprehensive HBM Patent Data EDA\n",
    "## HBM 관련 특허 데이터 종합 탐색적 분석\n",
    "\n",
    "이 노트북은 `data/raw/HBM` 디렉토리 내의 다양한 특허 분석 데이터를 로드하고 시각화합니다.\n",
    "뉴스 데이터가 '시장 담론'을 보여준다면, 이 특허 데이터는 **'기술적 실체'와 'R&D 경쟁 구도'**를 명확히 보여줍니다.\n",
    "\n",
    "**분석 대상 파일 및 내용:**\n",
    "1. **Applicant:** 출원인별 특허 수 (기술 점유율)\n",
    "2. **Inventor:** 핵심 발명자 랭킹 (Key Talent)\n",
    "3. **Metric Impact:** 기술 영향력 지표 (Citations 등 - 질적 평가)\n",
    "4. **Code:** IPC/CPC 기술 분류 코드 (기술 세부 분야)\n",
    "5. **Abstract:** 특허 초록 텍스트 마이닝 (핵심 키워드)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import os\n",
    "from wordcloud import WordCloud\n",
    "import glob\n",
    "\n",
    "# 시각화 설정\n",
    "sns.set(style=\"whitegrid\")\n",
    "font_name = \"NanumGothic\"\n",
    "plt.rcParams[\"font.family\"] = font_name\n",
    "plt.rcParams[\"axes.unicode_minus\"] = False\n",
    "\n",
    "# 데이터 경로\n",
    "DATA_DIR = \"../data/raw/HBM\"\n",
    "print(f\"Data Directory: {DATA_DIR}\")\n",
    "\n",
    "# 파일 목록 확인\n",
    "files = glob.glob(os.path.join(DATA_DIR, \"*.csv\"))\n",
    "print(\"Found Files:\")\n",
    "for f in files:\n",
    "    print(f\" - {os.path.basename(f)}\")\n",
    "\n",
    "# ------------------------------------------\n",
    "# 안전한 CSV 로드 함수 (인코딩 에러 방지)\n",
    "# ------------------------------------------\n",
    "def load_csv_safe(filepath):\n",
    "    encodings = ['utf-8', 'cp949', 'euc-kr', 'latin1']\n",
    "    for enc in encodings:\n",
    "        try:\n",
    "            df = pd.read_csv(filepath, encoding=enc)\n",
    "            print(f\"Successfully loaded {os.path.basename(filepath)} with encoding='{enc}'\")\n",
    "            return df\n",
    "        except UnicodeDecodeError:\n",
    "            continue\n",
    "        except Exception as e:\n",
    "            print(f\"Error reading {filepath}: {e}\")\n",
    "            return None\n",
    "    print(f\"Failed to load {filepath} with tested encodings.\")\n",
    "    return None"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "### 1. Top Applicants Analysis (출원인 랭킹)\n",
    "어떤 기업이 HBM 기술을 주도하고 있는지 파악합니다."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "app_df = load_csv_safe(os.path.join(DATA_DIR, \"HBM_Gemini_Applicant.csv\"))\n",
    "\n",
    "if app_df is not None:\n",
    "    # 상위 15개 기업 시각화\n",
    "    top_15 = app_df.head(15)\n",
    "    \n",
    "    plt.figure(figsize=(14, 8))\n",
    "    sns.barplot(data=top_15, x='patent_count', y='applicant_name', palette='viridis')\n",
    "    plt.title(\"Top 15 Applicants for HBM Patents\", fontsize=15)\n",
    "    plt.xlabel(\"Number of Patents\")\n",
    "    plt.ylabel(\"\")\n",
    "    plt.tight_layout()\n",
    "    plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "### 2. Key Inventor Analysis (핵심 발명자)\n",
    "어떤 연구자가 핵심적인 기여를 했는지 분석합니다. 특정 기업에 핵심 인재가 쏠려 있는지 확인할 수 있습니다."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "inv_df = load_csv_safe(os.path.join(DATA_DIR, \"HBM_Gemini_Inventor_Rank.csv\"))\n",
    "\n",
    "if inv_df is not None:\n",
    "    top_inv = inv_df.head(15)\n",
    "    \n",
    "    plt.figure(figsize=(14, 8))\n",
    "    sns.barplot(data=top_inv, x='patent_count', y='inventor_name', palette='magma')\n",
    "    plt.title(\"Top 15 Inventors in HBM Field\", fontsize=15)\n",
    "    plt.xlabel(\"Patent Count\")\n",
    "    plt.ylabel(\"Inventor\")\n",
    "    plt.tight_layout()\n",
    "    plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "### 3. Tech Classification (IPC/CPC Code Analysis)\n",
    "특허 분류 코드를 통해 HBM 기술이 구체적으로 어떤 세부 기술(메모리 소자 vs 패키징 vs 회로 등)에 집중되어 있는지 파악합니다."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "code_df = load_csv_safe(os.path.join(DATA_DIR, \"HBM_Gemini_Code.csv\"))\n",
    "\n",
    "if code_df is not None:\n",
    "    # 데이터 구조 확인 (컬럼명)\n",
    "    print(\"Columns:\", code_df.columns.tolist())\n",
    "    \n",
    "    # 'code'나 'ipc', 'cpc' 등의 컬럼을 찾아 빈도수 시각화\n",
    "    # (CSV 구조에 따라 수정 필요 가능성 있음, 여기선 첫 번째 컬럼을 코드로 가정)\n",
    "    target_col = code_df.columns[0] # 가령 'Code' or 'IPC'\n",
    "    count_col = code_df.columns[1] if len(code_df.columns) > 1 else None\n",
    "    \n",
    "    if count_col:\n",
    "        top_codes = code_df.sort_values(count_col, ascending=False).head(10)\n",
    "        plt.figure(figsize=(12, 6))\n",
    "        sns.barplot(data=top_codes, x=count_col, y=target_col, palette='Blues_r')\n",
    "        plt.title(f\"Top 10 Technology Codes ({target_col})\", fontsize=15)\n",
    "        plt.show()\n",
    "    else:\n",
    "        # 카운트 컬럼이 없으면 직접 카운트\n",
    "        top_codes = code_df[target_col].value_counts().head(10)\n",
    "        plt.figure(figsize=(12, 6))\n",
    "        sns.barplot(x=top_codes.values, y=top_codes.index, palette='Blues_r')\n",
    "        plt.title(f\"Top 10 Technology Codes ({target_col})\", fontsize=15)\n",
    "        plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "### 4. Technology Impact (질적 평가)\n",
    "단순 특허 수가 아닌, 기술적 영향력(Metric)을 살펴봅니다. (예: 인용 수, 패밀리 국가 수 등)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "metric_df = load_csv_safe(os.path.join(DATA_DIR, \"HBM_Gemini_Metric_Impact.csv\"))\n",
    "\n",
    "if metric_df is not None:\n",
    "    print(metric_df.head(3))\n",
    "    \n",
    "    numeric_cols = metric_df.select_dtypes(include=['float64', 'int64']).columns\n",
    "    if len(numeric_cols) > 1:\n",
    "        plt.figure(figsize=(10, 8))\n",
    "        sns.heatmap(metric_df[numeric_cols].corr(), annot=True, cmap='coolwarm', center=0)\n",
    "        plt.title(\"Correlation Matrix of Impact Metrics\", fontsize=15)\n",
    "        plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "### 5. Abstract Keyword Analysis (텍스트 마이닝)\n",
    "특허 초록에서 빈출되는 기술 용어를 시각화합니다."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "abstract_df = load_csv_safe(os.path.join(DATA_DIR, \"HBM_Gemini_With_Abstract.csv\"))\n",
    "\n",
    "if abstract_df is not None:\n",
    "    # 'Abstract' 컬럼이 있는지 확인, 없으면 비슷한 이름 찾기\n",
    "    abs_col = None\n",
    "    for col in abstract_df.columns:\n",
    "        if 'abstract' in col.lower():\n",
    "            abs_col = col\n",
    "            break\n",
    "            \n",
    "    if abs_col:\n",
    "        text = \" \".join(abstract_df[abs_col].fillna('').astype(str))\n",
    "        try:\n",
    "            wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='magma').generate(text)\n",
    "            plt.figure(figsize=(12, 6))\n",
    "            plt.imshow(wordcloud, interpolation='bilinear')\n",
    "            plt.axis('off')\n",
    "            plt.title(\"HBM Patent Abstract Word Cloud\", fontsize=15)\n",
    "            plt.show()\n",
    "        except ImportError:\n",
    "            print(\"WordCloud library not installed.\")\n",
    "    else:\n",
    "        print(\"Abstract column not found.\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

# 파일 생성
output_path = "/home/arkwith/SKKU/tech_forcast/notebooks/04_patent_analysis.ipynb"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(notebook_content, f, indent=1, ensure_ascii=False)

print(f"Notebook created at {output_path}")
