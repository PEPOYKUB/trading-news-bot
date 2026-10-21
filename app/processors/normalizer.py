import re
import unicodedata
def normalize_title(title: str) -> str:
    text = unicodedata.normalize("NFKC", title).lower()
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()
