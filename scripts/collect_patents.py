"""
특허 데이터 수집 스크립트

USPTO PatentView API를 사용하여 HBM 관련 특허 데이터를 수집합니다.
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
import logging
from typing import List, Dict, Optional
import time

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PatentViewCollector:
    """USPTO PatentView API를 사용한 특허 데이터 수집"""
    
    BASE_URL = "https://api.patentsview.org/patents/query"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Args:
            api_key: API 키 (현재 PatentView는 키 불필요, 향후 대비)
        """
        self.api_key = api_key
        self.session = requests.Session()
        
    def search_patents(
        self, 
        keyword: str, 
        start_date: str = "2020-01-01",
        end_date: str = "2024-12-31",
        max_results: int = 1000,
        fields: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        키워드 기반 특허 검색
        
        Args:
            keyword: 검색 키워드
            start_date: 시작 날짜 (YYYY-MM-DD)
            end_date: 종료 날짜 (YYYY-MM-DD)
            max_results: 최대 결과 수
            fields: 조회할 필드 목록
            
        Returns:
            특허 데이터 DataFrame
        """
        if fields is None:
            fields = [
                "patent_number",
                "patent_title", 
                "patent_abstract",
                "patent_date",
                "assignee_organization",
                "assignee_country",
                "inventor_last_name",
                "inventor_first_name",
                "cpc_subgroup_id",
                "patent_num_cited_by_us_patents"
            ]
        
        # 페이지네이션을 고려한 데이터 수집
        all_patents = []
        page = 1
        per_page = min(100, max_results)  # API 제한
        
        while len(all_patents) < max_results:
            logger.info(f"Fetching page {page} for keyword '{keyword}'...")
            
            query = {
                "q": {
                    "_and": [
                        {"_text_any": {"patent_abstract": keyword}},
                        {"_gte": {"patent_date": start_date}},
                        {"_lte": {"patent_date": end_date}}
                    ]
                },
                "f": fields,
                "o": {
                    "page": page,
                    "per_page": per_page
                }
            }
            
            try:
                response = self.session.post(self.BASE_URL, json=query, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                patents = data.get("patents", [])
                if not patents:
                    logger.info("No more patents found")
                    break
                
                all_patents.extend(patents)
                logger.info(f"Collected {len(all_patents)} patents so far")
                
                # API rate limiting 대응
                time.sleep(1)
                page += 1
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching patents: {e}")
                break
        
        if not all_patents:
            logger.warning(f"No patents found for keyword '{keyword}'")
            return pd.DataFrame()
        
        df = pd.DataFrame(all_patents)
        logger.info(f"Total patents collected: {len(df)}")
        return df
    
    def save_to_csv(
        self, 
        df: pd.DataFrame, 
        output_path: str,
        append: bool = False
    ):
        """
        DataFrame을 CSV 파일로 저장
        
        Args:
            df: 저장할 DataFrame
            output_path: 출력 파일 경로
            append: 기존 파일에 추가할지 여부
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if append and output_path.exists():
            existing_df = pd.read_csv(output_path)
            df = pd.concat([existing_df, df], ignore_index=True)
            # 중복 제거 (patent_number 기준)
            df = df.drop_duplicates(subset=['patent_number'], keep='last')
            logger.info(f"Appended to existing file, total rows: {len(df)}")
        
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        logger.info(f"Saved {len(df)} patents to {output_path}")


def collect_hbm_patents():
    """HBM 관련 특허 수집 메인 함수"""
    collector = PatentViewCollector()
    
    # HBM 및 관련 키워드로 검색
    keywords = [
        "HBM",
        "High Bandwidth Memory",
        "HBM2",
        "HBM3"
    ]
    
    all_patents = []
    
    for keyword in keywords:
        logger.info(f"Searching for keyword: {keyword}")
        df = collector.search_patents(
            keyword=keyword,
            start_date="2020-01-01",
            end_date="2024-12-31",
            max_results=500
        )
        
        if not df.empty:
            df['search_keyword'] = keyword
            all_patents.append(df)
    
    if not all_patents:
        logger.error("No patents collected")
        return
    
    # 모든 결과 병합
    combined_df = pd.concat(all_patents, ignore_index=True)
    
    # 중복 제거
    combined_df = combined_df.drop_duplicates(subset=['patent_number'], keep='first')
    
    logger.info(f"Total unique patents: {len(combined_df)}")
    
    # 저장
    output_dir = Path(__file__).parent.parent / "data" / "raw" / "HBM"
    timestamp = datetime.now().strftime("%Y%m%d")
    output_file = output_dir / f"HBM_PatentView_{timestamp}.csv"
    
    collector.save_to_csv(combined_df, output_file)
    
    # 통계 정보 생성
    generate_statistics(combined_df, output_dir)


def generate_statistics(df: pd.DataFrame, output_dir: Path):
    """특허 데이터 통계 생성"""
    
    # 출원인별 통계
    if 'assignee_organization' in df.columns:
        assignee_stats = df.groupby('assignee_organization').agg({
            'patent_number': 'count',
            'patent_date': 'max'
        }).reset_index()
        assignee_stats.columns = ['assignee_name', 'patent_count', 'last_filing_date']
        assignee_stats = assignee_stats.sort_values('patent_count', ascending=False)
        
        output_file = output_dir / f"HBM_Assignee_Stats_{datetime.now().strftime('%Y%m%d')}.csv"
        assignee_stats.to_csv(output_file, index=False, encoding='utf-8-sig')
        logger.info(f"Saved assignee statistics to {output_file}")
    
    # 연도별 통계
    if 'patent_date' in df.columns:
        df['year'] = pd.to_datetime(df['patent_date']).dt.year
        yearly_stats = df.groupby('year')['patent_number'].count().reset_index()
        yearly_stats.columns = ['year', 'patent_count']
        
        output_file = output_dir / f"HBM_Yearly_Stats_{datetime.now().strftime('%Y%m%d')}.csv"
        yearly_stats.to_csv(output_file, index=False, encoding='utf-8-sig')
        logger.info(f"Saved yearly statistics to {output_file}")


if __name__ == "__main__":
    logger.info("Starting patent collection...")
    collect_hbm_patents()
    logger.info("Patent collection completed")
