from difflib import SequenceMatcher
from .normalizer import normalize_title
def is_duplicate(candidate, existing) -> bool:
    if candidate.url and candidate.url == existing.url: return True
    return SequenceMatcher(None, normalize_title(candidate.title), normalize_title(existing.title)).ratio() >= 0.86
