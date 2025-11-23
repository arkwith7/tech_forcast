import json
import os

# 노트북 내용 정의 (JSON 구조)
notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# EDA & Visualization for Semiconductor Tech Trends\n",
    "## 뉴스 데이터를 활용한 반도체 기술 트렌드 및 사회적 영향 분석\n",
    "\n",
    "이 노트북은 `src/analyze_news_v2.py`를 통해 전처리된 데이터를 시각화하여 분석 결과를 도출합니다.\n",
    "\n",
    "**주요 분석 내용:**\n",
    "1. **기술 트렌드:** 분기별 주요 기술(HBM, GAA 등) 언급 빈도 변화\n",
    "2. **기술-사회 영향:** 기술 키워드와 사회적 키워드(AI, 친환경 등)의 동시 출현 분석 (Heatmap)\n",
    "3. **시장 감성:** 뉴스 톤앤매너를 통한 시장 반응(Sentiment) 시계열 분석"
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
    "import matplotlib.font_manager as fm\n",
    "\n",
    "# 1. 시각화 환경 설정\n",
    "sns.set(style=\"whitegrid\")\n",
    "\n",
    "# 한글 폰트 설정 (시스템 환경에 따라 적절한 폰트로 변경 필요)\n",
    "# 예: 윈도우='Malgun Gothic', 맥='AppleGothic', 리눅스='NanumGothic' 등\n",
    "plt.rcParams['font.family'] = 'sans-serif' \n",
    "plt.rcParams['axes.unicode_minus'] = False\n",
    "\n",
    "# 데이터 경로 설정\n",
    "DATA_DIR = \"../data/processed\"\n",
    "\n",
    "print(\"Environment Setup Complete.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 2. 데이터 로드\n",
    "try:\n",
    "    trends_df = pd.read_csv(os.path.join(DATA_DIR, \"tech_trends_quarterly.csv\"))\n",
    "    impact_df = pd.read_csv(os.path.join(DATA_DIR, \"tech_social_impact.csv\"))\n",
    "    sentiment_df = pd.read_csv(os.path.join(DATA_DIR, \"market_sentiment.csv\"))\n",
    "    \n",
    "    print(\"Data loaded successfully.\")\n",
    "    print(f\"- Trends Data: {trends_df.shape}\")\n",
    "    print(f\"- Impact Data: {impact_df.shape}\")\n",
    "    print(f\"- Sentiment Data: {sentiment_df.shape}\")\n",
    "except FileNotFoundError:\n",
    "    print(\"Error: Data files not found. Please run 'src/analyze_news_v2.py' first.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 3. Technology Trend Analysis (Quarterly Line Plot)\n",
    "def plot_tech_trends(company_name):\n",
    "    subset = trends_df[trends_df['company'] == company_name].copy()\n",
    "    subset['date'] = subset['date'].astype(str)\n",
    "    \n",
    "    # 주요 기술 선택 (데이터에 존재하는 것만)\n",
    "    techs = ['HBM', 'DDR', 'NAND', 'GAA', '파운드리', 'EUV']\n",
    "    available_techs = [t for t in techs if t in subset.columns]\n",
    "    \n",
    "    plt.figure(figsize=(14, 6))\n",
    "    for tech in available_techs:\n",
    "        plt.plot(subset['date'], subset[tech], label=tech, marker='o')\n",
    "            \n",
    "    plt.title(f\"{company_name} Technology Trends (Quarterly Frequency)\", fontsize=15)\n",
    "    plt.xticks(rotation=45)\n",
    "    plt.xlabel(\"Quarter\")\n",
    "    plt.ylabel(\"Mention Frequency\")\n",
    "    plt.legend()\n",
    "    plt.tight_layout()\n",
    "    plt.show()\n",
    "\n",
    "print(\"Trend Function Defined.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 4. Tech-Social Impact Analysis (Heatmap)\n",
    "def plot_impact_heatmap(year):\n",
    "    subset = impact_df[impact_df['year'] == year]\n",
    "    if subset.empty:\n",
    "        print(f\"No data for year {year}\")\n",
    "        return\n",
    "        \n",
    "    # Pivot table: Tech vs Social Category\n",
    "    # Columns should match those defined in analyze_news_v2.py\n",
    "    target_cols = ['AI_Computing', 'Mobility', 'Consumer', 'Environment', 'Economy']\n",
    "    available_cols = [c for c in target_cols if c in subset.columns]\n",
    "    \n",
    "    pivot_data = subset.set_index('tech')[available_cols]\n",
    "    \n",
    "    plt.figure(figsize=(10, 8))\n",
    "    sns.heatmap(pivot_data, annot=True, fmt=\"d\", cmap=\"YlGnBu\")\n",
    "    plt.title(f\"Technology - Social Impact Co-occurrence ({year})\", fontsize=15)\n",
    "    plt.ylabel(\"Semiconductor Tech\")\n",
    "    plt.xlabel(\"Social/Application Area\")\n",
    "    plt.tight_layout()\n",
    "    plt.show()\n",
    "\n",
    "print(\"Heatmap Function Defined.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 5. Sentiment Analysis (Market Atmosphere)\n",
    "def plot_sentiment():\n",
    "    plt.figure(figsize=(14, 6))\n",
    "    sns.lineplot(data=sentiment_df, x='date', y='sentiment_index', hue='company', marker='o')\n",
    "    plt.axhline(0, color='red', linestyle='--', alpha=0.5)\n",
    "    plt.title(\"Market Sentiment Trend (News Tone)\", fontsize=15)\n",
    "    plt.xticks(rotation=45)\n",
    "    plt.ylabel(\"Sentiment Index (Positive - Negative)\")\n",
    "    plt.tight_layout()\n",
    "    plt.show()\n",
    "\n",
    "print(\"Sentiment Function Defined.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 6. 실행 및 시각화\n",
    "print(\"=== Samsung Tech Trends ===\")\n",
    "plot_tech_trends('Samsung')\n",
    "\n",
    "print(\"=== SK Hynix Tech Trends ===\")\n",
    "plot_tech_trends('SKHynix')\n",
    "\n",
    "print(\"=== 2023 Tech-Social Impact Heatmap ===\")\n",
    "plot_impact_heatmap(2023)\n",
    "\n",
    "print(\"=== 2024 Tech-Social Impact Heatmap ===\")\n",
    "plot_impact_heatmap(2024)\n",
    "\n",
    "print(\"=== Market Sentiment Analysis ===\")\n",
    "plot_sentiment()"
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
output_path = "/home/arkwith/SKKU/tech_forcast/notebooks/01_exploration.ipynb"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(notebook_content, f, indent=1, ensure_ascii=False)

print(f"Notebook created at {output_path}")

