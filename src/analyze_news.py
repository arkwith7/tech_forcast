import pandas as pd
import re
import os
from collections import Counter
from datetime import datetime

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
    
    # Combine title and content for analysis
    df['text'] = df['title'].fillna('') + " " + df['content'].fillna('')
    return df

def extract_keywords(text):
    # 기술 용어(영어+숫자 등) 보존을 위한 정규식
    # 예: HBM, DDR5, 3D NAND, GAA, 10nm
    
    # 1. 영어/숫자 혼합 키워드 추출 (예: HBM3E, DDR5, i7)
    tech_terms = re.findall(r'\b[A-Za-z]+[0-9]+[A-Za-z]*\b|\b[A-Za-z]{2,}\b', text)
    
    # 2. 한글 명사 추출 (간이) - 조사가 붙는 패턴 제외 노력
    # 실제로는 형태소 분석기가 좋지만, 복합명사 처리를 위해 N-gram이나 명사 패턴을 정규식으로 근사
    # 여기서는 간단하게 2글자 이상 한글만 추출
    korean_nouns = re.findall(r'[가-힣]{2,}', text)
    
    # 불용어 제거 (분석에 방해되는 일반 명사들)
    stop_words = set(['삼성', '삼성전자', '하이닉스', 'SK하이닉스', '전자', '반도체', '발표', '개최', '참석', '진행', '예정', '이번', '통해', '위해', '관련', '제공', '사용', '적용', '기준', '부문', '기록', '대비', '증가', '감소', '설명', '포함', '시작', '계획', '목표'])
    
    keywords = [w for w in tech_terms + korean_nouns if w not in stop_words and len(w) > 1]
    return keywords

def analyze_trends(df):
    # 주요 기술 키워드 정의
    target_techs = ['HBM', 'DDR', 'NAND', 'DRAM', 'EUV', 'GAA', 'CIS', 'Foundry', '파운드리', 'OLED', 'AI', 'LPDDR', 'GDDR', 'HBM3', 'HBM3E']
    
    results = []
    
    df['year_month'] = df['date'].dt.to_period('M')
    
    for period, group in df.groupby(['year_month', 'company']):
        text_blob = " ".join(group['text'].tolist())
        # 대소문자 통일하여 검색
        text_lower = text_blob.lower()
        
        counts = {}
        for tech in target_techs:
            # 단순 포함 여부가 아니라 빈도수 체크
            counts[tech] = text_lower.count(tech.lower())
            
        row = {
            'date': str(period[0]),
            'company': period[1],
            **counts
        }
        results.append(row)
        
    return pd.DataFrame(results)

def extract_milestones(df):
    # 마일스톤: (기술) + (행위) 패턴 문장 추출
    milestones = []
    
    tech_pattern = r'(HBM|DDR|NAND|DRAM|파운드리|EUV|GAA|CXL|PIM)'
    action_pattern = r'(개발|양산|공급|공개|출시|성공|최초)'
    
    for idx, row in df.iterrows():
        sentences = re.split(r'[.!?]\s+', str(row['text']))
        for sent in sentences:
            if re.search(tech_pattern, sent, re.IGNORECASE) and re.search(action_pattern, sent):
                # 날짜, 회사, 관련 기술, 내용
                tech_match = re.search(tech_pattern, sent, re.IGNORECASE)
                tech_name = tech_match.group(0).upper() if tech_match else "ETC"
                
                milestones.append({
                    'date': row['date'],
                    'company': row['company'],
                    'tech': tech_name,
                    'content': sent[:200].strip() # 너무 길면 자름
                })
    
    return pd.DataFrame(milestones)

def main():
    print("Loading data...")
    df = load_data()
    print(f"Data loaded. Total records (2016-2024): {len(df)}")
    
    # 1. 기술 트렌드 시계열 데이터 생성
    print("Analyzing trends...")
    trend_df = analyze_trends(df)
    trend_save_path = os.path.join(OUTPUT_DIR, "tech_trends_timeseries.csv")
    trend_df.to_csv(trend_save_path, index=False)
    print(f"Trend data saved to {trend_save_path}")
    
    # 2. 마일스톤 데이터 생성
    print("Extracting milestones...")
    milestone_df = extract_milestones(df)
    milestone_save_path = os.path.join(OUTPUT_DIR, "tech_milestones.csv")
    milestone_df = milestone_df.sort_values('date')
    milestone_df.to_csv(milestone_save_path, index=False)
    print(f"Milestone data saved to {milestone_save_path}")
    
    # 3. 요약 통계 출력 (보고서 작성용)
    print("\n=== Summary Statistics ===")
    print(trend_df.groupby('company').sum())
    
    print("\n=== Recent Milestones (2024) ===")
    recent = milestone_df[milestone_df['date'] >= '2024-01-01'].head(5)
    for _, row in recent.iterrows():
        print(f"[{row['date'].date()}] {row['company']} - {row['tech']}: {row['content'][:100]}...")

if __name__ == "__main__":
    main()

