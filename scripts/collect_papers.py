"""
논문 데이터 수집 스크립트

arXiv API를 사용하여 HBM 관련 학술 논문 데이터를 수집합니다.
"""

import arxiv
import pandas as pd
from pathlib import Path
from datetime import datetime
import logging
from typing import List, Optional
import time

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ArxivCollector:
    """arXiv API를 사용한 논문 데이터 수집"""
    
    def __init__(self):
        """arXiv 수집기 초기화"""
        pass
    
    def search_papers(
        self,
        query: str,
        max_results: int = 100,
        categories: Optional[List[str]] = None,
        sort_by: arxiv.SortCriterion = arxiv.SortCriterion.SubmittedDate,
        sort_order: arxiv.SortOrder = arxiv.SortOrder.Descending
    ) -> pd.DataFrame:
        """
        논문 검색
        
        Args:
            query: 검색 쿼리
            max_results: 최대 결과 수
            categories: 카테고리 필터 (예: ['cs.AI', 'cs.LG'])
            sort_by: 정렬 기준
            sort_order: 정렬 순서
            
        Returns:
            논문 데이터 DataFrame
        """
        logger.info(f"Searching arXiv for: {query}")
        
        # 카테고리 필터 추가
        if categories:
            category_query = " OR ".join([f"cat:{cat}" for cat in categories])
            query = f"({query}) AND ({category_query})"
        
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        papers = []
        for result in search.results():
            try:
                papers.append({
                    'id': result.entry_id,
                    'arxiv_id': result.get_short_id(),
                    'title': result.title,
                    'abstract': result.summary,
                    'authors': ', '.join([author.name for author in result.authors]),
                    'published': result.published,
                    'updated': result.updated,
                    'categories': ', '.join(result.categories),
                    'primary_category': result.primary_category,
                    'pdf_url': result.pdf_url,
                    'doi': result.doi,
                    'journal_ref': result.journal_ref,
                    'comment': result.comment
                })
                
                # API rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error processing paper: {e}")
                continue
        
        df = pd.DataFrame(papers)
        logger.info(f"Collected {len(df)} papers")
        return df
    
    def save_to_csv(self, df: pd.DataFrame, output_path: str):
        """CSV 형식으로 저장"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        logger.info(f"Saved {len(df)} papers to {output_path}")
    
    def save_to_jsonl(self, df: pd.DataFrame, output_path: str):
        """JSONL 형식으로 저장"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_json(output_path, orient='records', lines=True, force_ascii=False)
        logger.info(f"Saved {len(df)} papers to {output_path}")


def collect_hbm_papers():
    """HBM 관련 논문 수집 메인 함수"""
    collector = ArxivCollector()
    
    # HBM 및 관련 키워드로 검색
    queries = [
        "HBM",
        "High Bandwidth Memory",
        "HBM2 OR HBM3",
        "3D stacked memory",
        "through-silicon via memory"
    ]
    
    # 관련 카테고리
    categories = ['cs.AR', 'cs.DC', 'eess.SP']  # Computer Architecture, Distributed Computing
    
    all_papers = []
    
    for query in queries:
        logger.info(f"Searching for query: {query}")
        df = collector.search_papers(
            query=query,
            max_results=50,  # 쿼리당 50개
            categories=categories
        )
        
        if not df.empty:
            df['search_query'] = query
            all_papers.append(df)
        
        time.sleep(2)  # API rate limiting
    
    if not all_papers:
        logger.error("No papers collected")
        return
    
    # 모든 결과 병합
    combined_df = pd.concat(all_papers, ignore_index=True)
    
    # 중복 제거 (arxiv_id 기준)
    combined_df = combined_df.drop_duplicates(subset=['arxiv_id'], keep='first')
    
    logger.info(f"Total unique papers: {len(combined_df)}")
    
    # 저장
    output_dir = Path(__file__).parent.parent / "data" / "raw"
    timestamp = datetime.now().strftime("%Y%m%d")
    
    # CSV 저장
    csv_file = output_dir / f"papers_HBM_arxiv_{timestamp}.csv"
    collector.save_to_csv(combined_df, csv_file)
    
    # JSONL 저장 (README에서 제안한 형식)
    jsonl_file = output_dir / f"papers_HBM_arxiv_{timestamp}.jsonl"
    collector.save_to_jsonl(combined_df, jsonl_file)
    
    # 통계 정보 생성
    generate_statistics(combined_df)


def generate_statistics(df: pd.DataFrame):
    """논문 데이터 통계 생성"""
    logger.info("\n=== Paper Collection Statistics ===")
    logger.info(f"Total papers: {len(df)}")
    
    # 연도별 통계
    if 'published' in df.columns:
        df['year'] = pd.to_datetime(df['published']).dt.year
        yearly_counts = df['year'].value_counts().sort_index()
        logger.info("\nPapers by year:")
        for year, count in yearly_counts.items():
            logger.info(f"  {year}: {count}")
    
    # 카테고리별 통계
    if 'primary_category' in df.columns:
        category_counts = df['primary_category'].value_counts().head(10)
        logger.info("\nTop categories:")
        for category, count in category_counts.items():
            logger.info(f"  {category}: {count}")


if __name__ == "__main__":
    logger.info("Starting paper collection...")
    
    try:
        collect_hbm_papers()
        logger.info("Paper collection completed successfully")
    except Exception as e:
        logger.error(f"Paper collection failed: {e}")
        raise
