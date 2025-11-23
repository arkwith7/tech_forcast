import pandas as pd
import re
import os
from collections import Counter
from datetime import datetime
import itertools

# 설정
DATA_DIR = "/home/arkwith/SKKU/tech_forcast/data/raw"
OUTPUT_DIR = "/home/arkwith/SKKU/tech_forcast/data/processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data():
    # Samsung Data
    sam_df = pd.read_csv(os.path.join(DATA_DIR, "samsung_news.csv"))
    sam_df['date'] = pd.to_datetime(sam_df['date'], format='%Y.%m.%d', errors='coerce')
    sam_df['company'] = 'Samsung'
    
    # SK Hynix Data
    sk_df = pd.read_csv(os.path.join(DATA_DIR, "skhynix_news.csv"))
    sk_df['date'] = pd.to_datetime(sk_df['date'], format='%Y-%m-%d', errors='coerce')
    sk_df['company'] = 'SKHynix'
    
    # Merge and Filter (2016-2024)
    df = pd.concat([sam_df, sk_df], ignore_index=True)
    df = df[(df['date'] >= '2016-01-01') & (df['date'] <= '2024-12-31')]
    
    # Combine title and content
    df['text'] = df['title'].fillna('') + " " + df['content'].fillna('')
    return df

def get_tech_keywords():
    return ['HBM', 'DDR', 'NAND', 'DRAM', 'EUV', 'GAA', '파운드리', 'CIS', 'SSD', 'AP', '패키징']

def get_social_keywords():
    # 기술의 사회적 영향/응용 분야 키워드
    return {
        'AI_Computing': ['AI', '인공지능', '서버', '데이터센터', '클라우드', '딥러닝', 'GPT'],
        'Mobility': ['자율주행', '전기차', '차량용', '오토모티브'],
        'Consumer': ['스마트폰', '게이밍', 'PC', '메타버스', 'VR', 'AR'],
        'Environment': ['탄소중립', '친환경', 'ESG', '저전력', '에너지'],
        'Economy': ['수출', '경제', '고용', '투자', '경기', '공급망']
    }

def analyze_tech_social_impact(df):
    techs = get_tech_keywords()
    social_cats = get_social_keywords()
    
    results = []
    
    # 연도별 기술-사회 키워드 동시 출현 빈도 분석
    df['year'] = df['date'].dt.year
    
    for year, group in df.groupby('year'):
        text_blob = " ".join(group['text'].tolist()).lower()
        
        for tech in techs:
            tech_count = text_blob.count(tech.lower())
            if tech_count == 0: continue
                
            row = {'year': year, 'tech': tech}
            
            for cat_name, keywords in social_cats.items():
                # 해당 기술이 언급된 문맥 근처에 사회적 키워드가 있는지 확인하는 것이 가장 좋으나,
                # 여기서는 전체 텍스트 내 공기(co-occurrence) 빈도로 근사합니다.
                # 정교함을 위해 '기술' 키워드가 포함된 기사들만 필터링하여 사회 키워드 카운트
                tech_articles = group[group['text'].str.contains(tech, case=False, na=False)]
                tech_article_blob = " ".join(tech_articles['text'].tolist()).lower()
                
                cat_count = 0
                for kw in keywords:
                    cat_count += tech_article_blob.count(kw.lower())
                
                row[cat_name] = cat_count
            
            results.append(row)
            
    return pd.DataFrame(results)

def analyze_sentiment(df):
    # 간단한 감성 사전
    pos_words = ['최대', '성장', '호조', '달성', '성공', '최초', '개선', '확대', '혁신', '수상', '흑자']
    neg_words = ['감소', '적자', '하락', '둔화', '위기', '우려', '불확실', '부진', '축소', '손실']
    
    results = []
    df['year_month'] = df['date'].dt.to_period('M')
    
    for (period, company), group in df.groupby(['year_month', 'company']):
        text_blob = " ".join(group['text'].tolist())
        
        pos_score = sum(text_blob.count(w) for w in pos_words)
        neg_score = sum(text_blob.count(w) for w in neg_words)
        total_words = len(text_blob.split())
        
        # 정규화된 점수
        sentiment_index = (pos_score - neg_score) / (pos_score + neg_score + 1) # -1 ~ 1 사이
        
        results.append({
            'date': str(period),
            'company': company,
            'positive_freq': pos_score,
            'negative_freq': neg_score,
            'sentiment_index': sentiment_index,
            'article_count': len(group)
        })
        
    return pd.DataFrame(results)

def main():
    print("Loading data...")
    df = load_data()
    print(f"Loaded {len(df)} records.")
    
    # 1. 기술-사회 상호작용 데이터 (논문 'Discussion' 파트용)
    print("Analyzing Tech-Social Impact...")
    impact_df = analyze_tech_social_impact(df)
    impact_df.to_csv(os.path.join(OUTPUT_DIR, "tech_social_impact.csv"), index=False)
    
    # 2. 감성 분석 데이터 (시장 반응 대리 지표)
    print("Analyzing Sentiment...")
    sentiment_df = analyze_sentiment(df)
    sentiment_df.to_csv(os.path.join(OUTPUT_DIR, "market_sentiment.csv"), index=False)
    
    # 3. 기존 시계열 트렌드 (재확인)
    print("Analyzing Tech Trends...")
    techs = get_tech_keywords()
    trend_results = []
    df['year_quarter'] = df['date'].dt.to_period('Q')
    
    for (period, company), group in df.groupby(['year_quarter', 'company']):
        text_blob = " ".join(group['text'].tolist()).lower()
        row = {'date': str(period), 'company': company}
        for tech in techs:
            row[tech] = text_blob.count(tech.lower())
        trend_results.append(row)
        
    pd.DataFrame(trend_results).to_csv(os.path.join(OUTPUT_DIR, "tech_trends_quarterly.csv"), index=False)
    
    print("Analysis Complete. Data saved to processed/ directory.")

if __name__ == "__main__":
    main()

