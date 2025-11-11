"""텍스트 전처리 관련 함수 모음."""

import re
from dataclasses import dataclass
from typing import Iterable, List

import nltk
from nltk.corpus import stopwords

# 필요한 리소스가 없는 경우 자동 다운로드
try:  # pragma: no cover - 런타임에서만 실행
    stopwords.words("english")
except LookupError:  # pragma: no cover
    nltk.download("stopwords", quiet=True)


@dataclass
class TextPreprocessor:
    languages: Iterable[str]
    lowercase: bool = True
    remove_numbers: bool = True
    min_token_length: int = 2

    def __post_init__(self):
        self._stopwords = set()
        for lang in self.languages:
            try:
                self._stopwords.update(stopwords.words(lang))
            except OSError:
                nltk.download("stopwords", quiet=True)
                self._stopwords.update(stopwords.words(lang))

    def clean(self, text: str) -> str:
        if self.lowercase:
            text = text.lower()
        if self.remove_numbers:
            text = re.sub(r"\d+", " ", text)
        tokens = [
            token
            for token in re.findall(r"\b\w+\b", text)
            if len(token) >= self.min_token_length and token not in self._stopwords
        ]
        return " ".join(tokens)


def batch_clean(texts: Iterable[str], preprocessor: TextPreprocessor) -> List[str]:
    """주어진 문자열 반복자에 대해 전처리를 수행합니다."""
    return [preprocessor.clean(text) for text in texts]
