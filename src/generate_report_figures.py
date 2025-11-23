import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import seaborn as sns
import networkx as nx
import os
import re
from itertools import combinations
from collections import Counter
from sklearn.linear_model import LinearRegression

# 설정
OUTPUT_DIR = "/home/arkwith/SKKU/tech_forcast/reports/Figure"
DATA_RAW_DIR = "/home/arkwith/SKKU/tech_forcast/data/raw"
DATA_PROC_DIR = "/home/arkwith/SKKU/tech_forcast/data/processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 폰트 설정
font_name = "NanumGothic"
plt.rcParams["font.family"] = font_name
plt.rcParams["axes.unicode_minus"] = False

def save_fig(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=300, bbox_inches='tight')
    print(f"Saved: {path}")
    plt.close(fig)

# ==========================================
# 1. 연구 프레임워크 도식화 (Research Framework)
# ==========================================
def draw_framework():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # 스타일 정의
    box_style = dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#333333', linewidth=2)
    arrow_props = dict(facecolor='#333333', arrowstyle='->', linewidth=1.5)

    # 1. Data Collection
    ax.text(2, 7, "Data Collection\n(News 2016-2024)", ha='center', va='center', size=11, bbox=dict(boxstyle='round,pad=0.5', facecolor='#E6F3FF', edgecolor='blue'))
    
    # 2. Preprocessing
    ax.text(6, 7, "Preprocessing\n(Keyword Extraction)", ha='center', va='center', size=11, bbox=dict(boxstyle='round,pad=0.5', facecolor='#E6F3FF', edgecolor='blue'))
    
    # 화살표 (Data -> Preprocessing)
    ax.annotate('', xy=(4.5, 7), xytext=(3.5, 7), arrowprops=arrow_props)

    # 3. Hybrid Analysis Framework (Main Box)
    rect = patches.Rectangle((1, 1.5), 10, 4.5, linewidth=2, edgecolor='#444444', facecolor='#F9F9F9', linestyle='--')
    ax.add_patch(rect)
    ax.text(6, 6.3, "AI-Based Hybrid Analysis Framework", ha='center', size=13, weight='bold', color='#333333')

    # 3-1. BERTopic
    ax.text(3, 4.5, "1. BERTopic\n(Dynamic Trend)", ha='center', va='center', size=10, bbox=box_style)
    ax.text(3, 3.8, "Output:\nTopic Evolution", ha='center', va='center', size=8, color='gray')

    # 3-2. SNA
    ax.text(6, 4.5, "2. SNA\n(Network Analysis)", ha='center', va='center', size=10, bbox=box_style)
    ax.text(6, 3.8, "Output:\nTech Ecosystem", ha='center', va='center', size=8, color='gray')

    # 3-3. LLM
    ax.text(9, 4.5, "3. LLM Analysis\n(Reasoning)", ha='center', va='center', size=10, bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF0E0', edgecolor='#FF8800', linewidth=2))
    ax.text(9, 3.8, "Output:\nContext & Weak Signal", ha='center', va='center', size=8, color='gray')

    # 화살표 (Preprocessing -> Analysis)
    ax.annotate('', xy=(6, 5.5), xytext=(6, 6.5), arrowprops=arrow_props)

    # 내부 화살표 (BERTopic/SNA -> LLM)
    ax.annotate('', xy=(8, 4.5), xytext=(4, 4.5), arrowprops=dict(arrowstyle='->', linestyle='dashed', color='gray'))
    
    # 4. Insight & Report
    ax.text(6, 0.5, "Final Report & Strategy Insight\n(Forecasting / Comparison / Suggestion)", ha='center', va='center', size=11, bbox=dict(boxstyle='round,pad=0.5', facecolor='#E6FFEA', edgecolor='green'))
    
    # 화살표 (Analysis -> Insight)
    ax.annotate('', xy=(6, 1.0), xytext=(6, 1.5), arrowprops=arrow_props)

    save_fig(fig, "fig_01_research_framework.png")

# ==========================================
# 2. 기술 트렌드 그래프 (EDA)
# ==========================================
def draw_tech_trends():
    try:
        df = pd.read_csv(os.path.join(DATA_PROC_DIR, "tech_trends_quarterly.csv"))
    except:
        print("Tech trend data not found.")
        return

    df['date'] = df['date'].astype(str)
    
    techs = ['HBM', 'DDR', 'NAND', 'GAA', '파운드리']
    companies = df['company'].unique()

    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    
    for idx, comp in enumerate(companies):
        subset = df[df['company'] == comp]
        for tech in techs:
            if tech in subset.columns:
                axes[idx].plot(subset['date'], subset[tech], marker='o', label=tech)
        
        axes[idx].set_title(f"{comp} Tech Keyword Trends (Quarterly)", fontsize=14)
        axes[idx].legend()
        axes[idx].set_ylabel("Frequency")
        # X축 레이블 간소화 (4개 간격)
        ticks = subset['date'].unique()
        axes[idx].set_xticks(ticks[::4])
        axes[idx].set_xticklabels(ticks[::4], rotation=45)
        axes[idx].grid(True, alpha=0.3)

    plt.tight_layout()
    save_fig(fig, "fig_02_tech_trends.png")

# ==========================================
# 3. 기술-사회 히트맵 (Heatmap)
# ==========================================
def draw_heatmap():
    try:
        df = pd.read_csv(os.path.join(DATA_PROC_DIR, "tech_social_impact.csv"))
    except:
        return

    # 2023년, 2024년 비교
    years = [2023, 2024]
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    target_cols = ['AI_Computing', 'Mobility', 'Consumer', 'Environment', 'Economy']

    for idx, year in enumerate(years):
        subset = df[df['year'] == year]
        if subset.empty: continue
        
        pivot = subset.set_index('tech')[target_cols]
        sns.heatmap(pivot, ax=axes[idx], annot=True, fmt="d", cmap="Blues", cbar=False)
        axes[idx].set_title(f"Tech-Social Co-occurrence ({year})", fontsize=14)
        axes[idx].set_ylabel("Technology")
    
    plt.tight_layout()
    save_fig(fig, "fig_03_tech_social_heatmap.png")

# ==========================================
# 4. 시계열 예측 그래프 (Forecasting)
# ==========================================
def draw_forecast():
    try:
        df = pd.read_csv(os.path.join(DATA_PROC_DIR, "tech_trends_quarterly.csv"))
    except:
        return

    target_tech = "HBM" # 대표적으로 HBM만 시각화
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    companies = df['company'].unique()
    colors = {'Samsung': 'blue', 'SKHynix': 'red'}

    for comp in companies:
        subset = df[df['company'] == comp].copy().reset_index(drop=True)
        if target_tech not in subset.columns: continue

        subset['t'] = np.arange(len(subset))
        
        # Regression
        X = subset[['t']].values
        y = subset[target_tech].values
        model = LinearRegression()
        model.fit(X, y)
        
        # Forecast (Next 8 quarters)
        last_t = subset['t'].iloc[-1]
        future_t = np.arange(last_t + 1, last_t + 9).reshape(-1, 1)
        future_pred = model.predict(future_t)
        
        # Plot Historical
        ax.plot(subset['date'], y, marker='o', label=f"{comp} (Actual)", color=colors.get(comp), alpha=0.6)
        
        # Plot Forecast (X축 라벨 처리는 생략하고 점선으로 이음)
        # 마지막 실제값과 연결
        connect_x = [len(subset)-1] + list(future_t.flatten())
        connect_y = [y[-1]] + list(future_pred)
        
        # X축 좌표 매핑 (단순화)
        x_indices = np.arange(len(subset) + 8)
        ax.plot(x_indices[len(subset)-1:], connect_y, linestyle='--', color=colors.get(comp), linewidth=2, label=f"{comp} (Forecast)")

    ax.set_title(f"Forecasting: {target_tech} Mention Trend (Linear Regression)", fontsize=15)
    ax.set_ylabel("Frequency")
    ax.set_xlabel("Time (Quarter Index)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_fig(fig, "fig_04_forecast_hbm.png")

# ==========================================
# 5. 네트워크 그래프 (SNA) - 약식 구현
# ==========================================
def draw_network():
    # 간단한 네트워크 생성을 위해 최근 데이터만 로드하여 그리기 (시간 절약)
    try:
        sam_df = pd.read_csv(os.path.join(DATA_RAW_DIR, "samsung_news.csv"))
        sk_df = pd.read_csv(os.path.join(DATA_RAW_DIR, "skhynix_news.csv"))
    except:
        return

    # 전처리 함수
    def extract_keywords(text):
        text = str(text)
        techs = re.findall(r'\b[A-Za-z][A-Za-z0-9]+\b', text)
        korean = re.findall(r'[가-힣]{2,}', text)
        targets = set(['HBM', 'DDR', 'AI', '파운드리', '수율', '엔비디아', 'GPU', 'TSMC', 'GAA', '패키징', 'SK하이닉스', '삼성전자'])
        found = []
        for w in techs + korean:
            for t in targets:
                if t in w.upper() or w.upper() in t:
                    found.append(t)
                    break
        return list(set(found))

    def create_graph(df, title, filename):
        # 최근 500개만 사용
        subset = df.tail(500).copy()
        subset['text'] = subset['title'].fillna('') + " " + subset['content'].fillna('')
        subset['keywords'] = subset['text'].apply(extract_keywords)
        
        edge_list = []
        for k in subset['keywords']:
            if len(k) > 1:
                edge_list.extend(combinations(sorted(k), 2))
        
        edge_counts = Counter(edge_list)
        G = nx.Graph()
        for (u, v), c in edge_counts.items():
            if c >= 10: # Threshold
                G.add_edge(u, v, weight=c)
        
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G, k=0.6, seed=42)
        d = dict(G.degree(weight='weight'))
        sizes = [v * 10 for v in d.values()]
        
        nx.draw_networkx_nodes(G, pos, node_size=sizes, node_color='skyblue', alpha=0.9)
        nx.draw_networkx_edges(G, pos, width=1, alpha=0.3)
        nx.draw_networkx_labels(G, pos, font_family=font_name, font_size=10, font_weight='bold')
        
        plt.title(title, fontsize=15)
        plt.axis('off')
        save_fig(plt.gcf(), filename)

    create_graph(sk_df, "SK Hynix Semantic Network (Recent)", "fig_05_network_skhynix.png")
    create_graph(sam_df, "Samsung Semantic Network (Recent)", "fig_06_network_samsung.png")


def main():
    print("Generating Figures...")
    draw_framework()
    draw_tech_trends()
    draw_heatmap()
    draw_forecast()
    draw_network()
    print("All figures generated in reports/Figure/")

if __name__ == "__main__":
    main()

