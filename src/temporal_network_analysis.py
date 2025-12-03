"""
시계열 의미 연결망 분석 (Temporal Semantic Network Analysis)
2014-2024년 연도별 토픽 진화 및 네트워크 구조 변화 추적

주요 기능:
1. 연도별 키워드 네트워크 생성
2. 중심성 시계열 분석
3. 토픽 전환 경로 분석 (DRAM → HBM 등)
4. 기업별 전략 진화 비교
5. 신규 등장 키워드 탐지
"""

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
from collections import Counter
from itertools import combinations
import warnings
warnings.filterwarnings('ignore')

# 시각화 설정
sns.set(style="whitegrid")
font_name = "NanumGothic"
plt.rcParams["font.family"] = font_name
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams['figure.figsize'] = (16, 10)

# 경로 설정
DATA_DIR = "data/raw"
OUTPUT_DIR = "reports/Figure"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_and_preprocess():
    """뉴스 데이터 로드 및 연도 정보 추가"""
    sam_df = pd.read_csv(os.path.join(DATA_DIR, "samsung_news.csv"))
    sk_df = pd.read_csv(os.path.join(DATA_DIR, "skhynix_news.csv"))
    
    sam_df['company'] = 'Samsung'
    sk_df['company'] = 'SKHynix'
    
    df = pd.concat([sam_df, sk_df], ignore_index=True)
    df['text'] = df['title'].fillna('') + " " + df['content'].fillna('')
    df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce')
    df = df.dropna(subset=['date']).sort_values('date')
    
    # 연도 추출
    df['year'] = df['date'].dt.year
    
    # 2014-2024년 필터링
    df = df[(df['year'] >= 2014) & (df['year'] <= 2024)]
    
    def clean_text(text):
        text = str(text)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    df['processed_text'] = df['text'].apply(clean_text)
    return df


def extract_keywords_advanced(text):
    """향상된 키워드 추출: 기술, 제품, 응용 분야 모두 포함"""
    if not isinstance(text, str):
        return []
    
    # 확장된 키워드 세트
    target_keywords = [
        # 메모리 기술
        'HBM', 'HBM2', 'HBM3', 'HBM3E',
        'DDR', 'DDR4', 'DDR5', 'LPDDR',
        'DRAM', 'NAND', 'SSD', 'V-NAND',
        
        # 제조 기술
        'EUV', 'GAA', '파운드리', '패키징',
        '10나노', '7나노', '5나노', '3나노', '2나노',
        
        # 응용 분야
        'AI', '인공지능', '머신러닝', 'GPU',
        '서버', '데이터센터', '클라우드',
        '자율주행', '전기차', '차량용',
        '스마트폰', '모바일', '5G',
        
        # 기업/파트너
        '엔비디아', 'NVIDIA', 'AMD', 'Intel',
        'TSMC', '삼성전자', 'SK하이닉스',
        
        # 비즈니스
        '양산', '개발', '출시', '공급',
        '투자', '매출', '수율', '점유율',
        
        # 차세대 기술
        'CXL', 'PIM', 'CIS', 'AP',
        '하이브리드본딩', '3D', 'TSV'
    ]
    
    found = set()
    text_upper = text.upper()
    
    for keyword in target_keywords:
        keyword_upper = keyword.upper()
        if keyword_upper in text_upper or keyword in text:
            found.add(keyword)
    
    return list(found)


def build_yearly_networks(df, company_filter=None, min_edge_weight=3):
    """
    연도별 네트워크 생성
    
    Parameters:
    - df: 전체 데이터프레임
    - company_filter: 'Samsung', 'SKHynix', 또는 None (전체)
    - min_edge_weight: 최소 공출현 횟수
    
    Returns:
    - dict: {year: networkx.Graph}
    """
    if company_filter:
        df = df[df['company'] == company_filter].copy()
    
    yearly_networks = {}
    years = sorted(df['year'].unique())
    
    for year in years:
        year_df = df[df['year'] == year]
        
        # 키워드 공출현 계산
        edge_list = []
        for keywords in year_df['keywords']:
            if len(keywords) > 1:
                edge_list.extend(combinations(sorted(keywords), 2))
        
        edge_counts = Counter(edge_list)
        
        # 네트워크 구축
        G = nx.Graph()
        for (u, v), count in edge_counts.items():
            if count >= min_edge_weight:
                G.add_edge(u, v, weight=count)
        
        yearly_networks[year] = G
        print(f"Year {year}: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    return yearly_networks


def analyze_centrality_evolution(networks_dict):
    """
    연도별 중심성 변화 추적
    
    Returns:
    - DataFrame: 연도별 주요 키워드의 중심성 점수
    """
    centrality_data = []
    
    for year, G in sorted(networks_dict.items()):
        if G.number_of_nodes() == 0:
            continue
        
        # Degree Centrality 계산
        degree_cent = nx.degree_centrality(G)
        
        # 가중치 반영한 Weighted Degree
        weighted_degree = dict(G.degree(weight='weight'))
        
        for node in G.nodes():
            centrality_data.append({
                'year': year,
                'keyword': node,
                'degree_centrality': degree_cent.get(node, 0),
                'weighted_degree': weighted_degree.get(node, 0)
            })
    
    df_cent = pd.DataFrame(centrality_data)
    return df_cent


def plot_keyword_evolution(df_cent, keywords_to_track, title="Keyword Centrality Evolution", 
                          save_path=None):
    """특정 키워드들의 중심성 변화를 시계열 그래프로 표현"""
    plt.figure(figsize=(16, 8))
    
    for keyword in keywords_to_track:
        subset = df_cent[df_cent['keyword'] == keyword].sort_values('year')
        if len(subset) > 0:
            plt.plot(subset['year'], subset['weighted_degree'], 
                    marker='o', linewidth=2.5, markersize=8, label=keyword)
    
    plt.title(title, fontsize=18, fontweight='bold')
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("Weighted Degree (Network Centrality)", fontsize=14)
    plt.legend(loc='best', fontsize=11, ncol=2)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.show()


def create_temporal_heatmap(df_cent, top_n=12, save_path=None):
    """연도별 주요 키워드의 중심성을 히트맵으로 시각화"""
    # 전체 기간에서 가장 중요한 키워드 선택
    top_keywords = (df_cent.groupby('keyword')['weighted_degree']
                    .sum()
                    .sort_values(ascending=False)
                    .head(top_n)
                    .index.tolist())
    
    # 피벗 테이블 생성
    pivot_data = df_cent[df_cent['keyword'].isin(top_keywords)].pivot_table(
        index='keyword',
        columns='year',
        values='weighted_degree',
        fill_value=0
    )
    
    # 키워드를 전체 중심성 합계로 정렬
    pivot_data['total'] = pivot_data.sum(axis=1)
    pivot_data = pivot_data.sort_values('total', ascending=False).drop('total', axis=1)
    
    plt.figure(figsize=(14, 10))
    sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='YlOrRd', 
                linewidths=0.5, cbar_kws={'label': 'Weighted Degree'})
    plt.title('연도별 핵심 키워드 네트워크 중심성 히트맵 (2014-2024)', 
             fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Year', fontsize=13)
    plt.ylabel('Keyword', fontsize=13)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.show()
    
    return pivot_data


def plot_company_comparison(cent_samsung, cent_skhynix, keywords, save_path=None):
    """삼성전자 vs SK하이닉스의 키워드 중심성 비교"""
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    axes = axes.flatten()
    
    for idx, keyword in enumerate(keywords[:4]):
        ax = axes[idx]
        
        # 삼성 데이터
        sam_data = cent_samsung[cent_samsung['keyword'] == keyword].sort_values('year')
        if len(sam_data) > 0:
            ax.plot(sam_data['year'], sam_data['weighted_degree'], 
                   marker='s', linewidth=3, markersize=10, label='Samsung', color='#1f77b4')
        
        # SK하이닉스 데이터
        sk_data = cent_skhynix[cent_skhynix['keyword'] == keyword].sort_values('year')
        if len(sk_data) > 0:
            ax.plot(sk_data['year'], sk_data['weighted_degree'], 
                   marker='o', linewidth=3, markersize=10, label='SK Hynix', color='#ff7f0e')
        
        ax.set_title(f'{keyword} 키워드 중심성 비교', fontsize=14, fontweight='bold')
        ax.set_xlabel('Year', fontsize=11)
        ax.set_ylabel('Weighted Degree', fontsize=11)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
    
    plt.suptitle('삼성전자 vs SK하이닉스: 핵심 키워드 전략 진화 비교', 
                fontsize=18, fontweight='bold', y=1.00)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.show()


def analyze_topic_transition(df_cent, keyword_pairs, save_path=None):
    """
    특정 키워드 쌍의 중심성 역전 시점 분석
    예: DRAM에서 HBM으로의 전환
    """
    fig, axes = plt.subplots(len(keyword_pairs), 1, figsize=(16, 5*len(keyword_pairs)))
    if len(keyword_pairs) == 1:
        axes = [axes]
    
    for idx, (old_topic, new_topic) in enumerate(keyword_pairs):
        ax = axes[idx]
        
        old_data = df_cent[df_cent['keyword'] == old_topic].sort_values('year')
        new_data = df_cent[df_cent['keyword'] == new_topic].sort_values('year')
        
        if len(old_data) > 0:
            ax.plot(old_data['year'], old_data['weighted_degree'], 
                   marker='o', linewidth=3, markersize=10, label=f'{old_topic} (레거시)', 
                   color='#8c564b', linestyle='--')
        
        if len(new_data) > 0:
            ax.plot(new_data['year'], new_data['weighted_degree'], 
                   marker='s', linewidth=3, markersize=10, label=f'{new_topic} (신규)', 
                   color='#e377c2')
        
        # 교차점 찾기
        if len(old_data) > 0 and len(new_data) > 0:
            merged = pd.merge(old_data[['year', 'weighted_degree']], 
                            new_data[['year', 'weighted_degree']], 
                            on='year', suffixes=('_old', '_new'))
            merged['diff'] = merged['weighted_degree_new'] - merged['weighted_degree_old']
            
            crossover = merged[merged['diff'] > 0]
            if len(crossover) > 0:
                crossover_year = crossover.iloc[0]['year']
                ax.axvline(crossover_year, color='red', linestyle=':', linewidth=2, alpha=0.7)
                ax.text(crossover_year, ax.get_ylim()[1]*0.9, 
                       f'전환점: {int(crossover_year)}년', 
                       ha='center', fontsize=12, color='red', fontweight='bold',
                       bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        
        ax.set_title(f'토픽 전환 분석: {old_topic} → {new_topic}', 
                    fontsize=15, fontweight='bold')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Network Centrality', fontsize=12)
        ax.legend(fontsize=11, loc='best')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.show()


def print_summary_report(df, networks_all, centrality_all, centrality_samsung, centrality_skhynix):
    """종합 인사이트 리포트 출력"""
    print("\n" + "="*80)
    print("시계열 네트워크 분석 종합 리포트")
    print("="*80)
    
    # 1. 전체 기간 통계
    print("\n[1] 전체 분석 기간 통계")
    print(f"  - 분석 기간: {df['year'].min()}년 ~ {df['year'].max()}년")
    print(f"  - 총 기사 수: {len(df):,}건")
    print(f"  - 총 추출 키워드 수: {df['keywords'].apply(len).sum():,}개")
    
    # 2. 연도별 네트워크 규모 변화
    print("\n[2] 연도별 네트워크 규모 변화")
    network_stats = []
    for year, G in sorted(networks_all.items()):
        network_stats.append({
            'Year': year,
            'Nodes': G.number_of_nodes(),
            'Edges': G.number_of_edges(),
            'Density': round(nx.density(G), 3) if G.number_of_nodes() > 1 else 0
        })
    df_stats = pd.DataFrame(network_stats)
    print(df_stats.to_string(index=False))
    
    # 3. 시기별 Top 키워드
    print("\n[3] 시기별 Top 3 핵심 키워드")
    periods = [
        (2014, 2017, '초기'),
        (2018, 2020, '중기'),
        (2021, 2024, '최근')
    ]
    
    for start, end, label in periods:
        period_data = centrality_all[
            (centrality_all['year'] >= start) & (centrality_all['year'] <= end)
        ]
        top_keywords = (period_data.groupby('keyword')['weighted_degree']
                       .sum()
                       .sort_values(ascending=False)
                       .head(3))
        print(f"  {label} ({start}-{end}): {', '.join(top_keywords.index.tolist())}")
    
    # 4. 기업별 전략 특징
    print("\n[4] 기업별 전략 특징 (최근 3년 기준)")
    recent_samsung = centrality_samsung[centrality_samsung['year'] >= 2022]
    recent_skhynix = centrality_skhynix[centrality_skhynix['year'] >= 2022]
    
    top_samsung = (recent_samsung.groupby('keyword')['weighted_degree']
                  .sum().sort_values(ascending=False).head(5))
    top_skhynix = (recent_skhynix.groupby('keyword')['weighted_degree']
                  .sum().sort_values(ascending=False).head(5))
    
    print(f"  삼성전자 Top 5: {', '.join(top_samsung.index.tolist())}")
    print(f"  SK하이닉스 Top 5: {', '.join(top_skhynix.index.tolist())}")
    
    print("\n" + "="*80)


def main():
    """메인 실행 함수"""
    print("="*80)
    print("시계열 의미 연결망 분석 (Temporal Semantic Network Analysis)")
    print("="*80)
    
    # 1. 데이터 로딩
    print("\n[Step 1] 데이터 로딩 및 전처리...")
    df = load_and_preprocess()
    print(f"총 {len(df):,}건의 기사 로드 완료")
    
    # 2. 키워드 추출
    print("\n[Step 2] 키워드 추출...")
    df['keywords'] = df['processed_text'].apply(extract_keywords_advanced)
    df['keyword_count'] = df['keywords'].apply(len)
    print(f"키워드 추출 완료: {len(df[df['keyword_count'] > 0])} / {len(df)} 기사")
    
    # 3. 연도별 네트워크 구축
    print("\n[Step 3] 연도별 네트워크 구축...")
    print("\n--- 전체 데이터 ---")
    networks_all = build_yearly_networks(df, company_filter=None, min_edge_weight=5)
    
    print("\n--- 삼성전자 ---")
    networks_samsung = build_yearly_networks(df, company_filter='Samsung', min_edge_weight=3)
    
    print("\n--- SK하이닉스 ---")
    networks_skhynix = build_yearly_networks(df, company_filter='SKHynix', min_edge_weight=3)
    
    # 4. 중심성 분석
    print("\n[Step 4] 중심성 시계열 분석...")
    centrality_all = analyze_centrality_evolution(networks_all)
    centrality_samsung = analyze_centrality_evolution(networks_samsung)
    centrality_skhynix = analyze_centrality_evolution(networks_skhynix)
    print("중심성 분석 완료")
    
    # 5. 시각화
    print("\n[Step 5] 시각화 생성...")
    
    # 5-1. 주요 기술 키워드 진화
    tech_keywords = ['HBM', 'DRAM', 'DDR', 'NAND', 'AI', '파운드리', 'EUV', 'GAA']
    plot_keyword_evolution(
        centrality_all, tech_keywords,
        title="반도체 핵심 기술 키워드의 네트워크 중심성 변화 (2014-2024)",
        save_path=os.path.join(OUTPUT_DIR, 'fig_11_temporal_keyword_evolution.png')
    )
    
    # 5-2. 히트맵
    heatmap_data = create_temporal_heatmap(
        centrality_all, top_n=15,
        save_path=os.path.join(OUTPUT_DIR, 'fig_08_temporal_centrality_heatmap.png')
    )
    
    # 5-3. 기업 비교
    comparison_keywords = ['HBM', 'DRAM', 'AI', '파운드리']
    plot_company_comparison(
        centrality_samsung, centrality_skhynix, comparison_keywords,
        save_path=os.path.join(OUTPUT_DIR, 'fig_07_company_strategy_evolution.png')
    )
    
    # 5-4. 토픽 전환 분석
    transition_pairs = [('DRAM', 'HBM')]
    analyze_topic_transition(
        centrality_all, transition_pairs,
        save_path=os.path.join(OUTPUT_DIR, 'fig_10_topic_transition_analysis.png')
    )
    
    # 6. 종합 리포트
    print_summary_report(df, networks_all, centrality_all, centrality_samsung, centrality_skhynix)
    
    print("\n분석 완료!")
    print(f"생성된 그래프는 {OUTPUT_DIR}/ 디렉토리에 저장되었습니다.")
    print("="*80)


if __name__ == "__main__":
    main()

