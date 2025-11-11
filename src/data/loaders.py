"""데이터 로딩 관련 유틸리티 모듈."""

from pathlib import Path
from typing import Union

import pandas as pd


def load_csv(path: Union[str, Path], **read_kwargs) -> pd.DataFrame:
    """CSV 파일을 DataFrame으로 로드합니다."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"CSV 파일을 찾을 수 없습니다: {path}")
    return pd.read_csv(path, **read_kwargs)


def list_patent_files(directory: Union[str, Path], suffix: str = ".xml"):
    """특허 XML/JSON 파일 목록을 반환합니다."""
    directory = Path(directory)
    if not directory.exists():
        return []
    return sorted(directory.glob(f"*{suffix}"))
