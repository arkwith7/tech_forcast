import json
import os


def main():
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# 03. 시계열 기반 반도체 기술 트렌드 예측\n",
                    "## Tech Trend Forecasting using Linear Regression\n",
                    "\n",
                    "이 노트북은 `data/processed/tech_trends_quarterly.csv`를 활용하여\n",
                    "HBM, DDR, NAND 등 주요 기술 키워드의 **분기별 언급량 시계열**을 분석하고,\n",
                    "간단한 선형 회귀 모델을 이용해 **향후 분기별 트렌드 예측 곡선**을 생성합니다.\n",
                    "\n",
                    "생성되는 그래프는 연구 보고서의 도식(예: *그림 3. 기술별 트렌드 예측 곡선*)에 해당합니다.\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "from sklearn.linear_model import LinearRegression\n",
                    "import os\n",
                    "\n",
                    "sns.set(style=\"whitegrid\")\n",
                    "plt.rcParams['font.family'] = 'sans-serif'\n",
                    "plt.rcParams['axes.unicode_minus'] = False\n",
                    "\n",
                    "DATA_PATH = \"../data/processed/tech_trends_quarterly.csv\"\n",
                    "print(f\"Loading: {DATA_PATH}\")\n",
                    "trends = pd.read_csv(DATA_PATH)\n",
                    "print(trends.head())\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 분기(date)를 시계열 인덱스로 변환\n",
                    "trends['date'] = trends['date'].astype(str)\n",
                    "# 정렬 보장\n",
                    "trends = trends.sort_values(['company', 'date'])\n",
                    "\n",
                    "tech_cols = [c for c in trends.columns if c not in ['date', 'company']]\n",
                    "print(\"기술 컬럼:\", tech_cols)\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "def forecast_tech(trends_df, company, tech, horizon=8):\n",
                    "    \"\"\"단순 선형 회귀를 사용해 향후 horizon 개 분기 예측\"\"\"\n",
                    "    df = trends_df[trends_df['company'] == company].copy()\n",
                    "    if tech not in df.columns:\n",
                    "        raise ValueError(f\"컬럼 {tech} 이(가) 데이터에 없습니다.\")\n",
                    "\n",
                    "    # 시간 인덱스 t = 0..T-1\n",
                    "    df = df.reset_index(drop=True)\n",
                    "    df['t'] = np.arange(len(df))\n",
                    "\n",
                    "    X = df[['t']].values\n",
                    "    y = df[tech].values\n",
                    "\n",
                    "    model = LinearRegression()\n",
                    "    model.fit(X, y)\n",
                    "\n",
                    "    # 미래 t 값 생성\n",
                    "    last_t = df['t'].iloc[-1]\n",
                    "    future_t = np.arange(last_t + 1, last_t + 1 + horizon)\n",
                    "    future_X = future_t.reshape(-1, 1)\n",
                    "    future_pred = model.predict(future_X)\n",
                    "\n",
                    "    # 결과 DataFrame 구성\n",
                    "    hist_df = df[['date', tech]].copy()\n",
                    "    hist_df['type'] = 'actual'\n",
                    "\n",
                    "    # 미래 date 라벨은 단순히 t 인덱스로 표기 (혹은 별도 매핑 가능)\n",
                    "    future_df = pd.DataFrame({\n",
                    "        'date': [f\"t+{i}\" for i in range(1, horizon + 1)],\n",
                    "        tech: future_pred,\n",
                    "        'type': 'forecast'\n",
                    "    })\n",
                    "\n",
                    "    return hist_df, future_df, model\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "def plot_forecast(trends_df, company, tech, horizon=8):\n",
                    "    hist_df, future_df, model = forecast_tech(trends_df, company, tech, horizon=horizon)\n",
                    "    combined = pd.concat([hist_df, future_df], ignore_index=True)\n",
                    "\n",
                    "    plt.figure(figsize=(12, 5))\n",
                    "    sns.lineplot(data=combined, x='date', y=tech, hue='type', marker='o')\n",
                    "    plt.title(f\"{company} - {tech} 분기별 언급량 및 예측\")\n",
                    "    plt.xticks(rotation=45)\n",
                    "    plt.ylabel(\"Mention Frequency\")\n",
                    "    plt.tight_layout()\n",
                    "    plt.show()\n",
                    "\n",
                    "    coef = float(model.coef_[0])\n",
                    "    print(f\"선형 회귀 계수 (추세 기울기): {coef:.3f}\")\n",
                    "    return coef\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 예시: HBM, DDR, NAND에 대해 삼성/하이닉스 각각 예측 수행\n",
                    "target_techs = [t for t in ['HBM', 'DDR', 'NAND'] if t in tech_cols]\n",
                    "companies = trends['company'].unique()\n",
                    "\n",
                    "results = []\n",
                    "for company in companies:\n",
                    "    for tech in target_techs:\n",
                    "        print(\"=\"*60)\n",
                    "        print(f\"{company} - {tech} 예측\")\n",
                    "        coef = plot_forecast(trends, company, tech, horizon=8)\n",
                    "        results.append({\n",
                    "            'company': company,\n",
                    "            'tech': tech,\n",
                    "            'trend_coef': coef\n",
                    "        })\n",
                    "\n",
                    "trend_summary = pd.DataFrame(results)\n",
                    "trend_summary\n",
                ],
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.11",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 4,
    }

    output_path = "/home/arkwith/SKKU/tech_forcast/notebooks/03_forecasting.ipynb"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(notebook_content, f, indent=1, ensure_ascii=False)

    print(f"Notebook created at {output_path}")


if __name__ == "__main__":
    main()


