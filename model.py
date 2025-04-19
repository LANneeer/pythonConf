from functools import lru_cache
from typing import List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE


@lru_cache(maxsize=1)
def _vectorizer() -> TfidfVectorizer:
    """Singleton‑vectorizer, разделяемый всеми дочерними процессами (COW)."""
    return TfidfVectorizer(max_features=10_000, ngram_range=(1, 2))


def embed(texts: List[str]):
    """Преобразует список текстов → список координат (x, y)."""
    if len(texts) < 2:
        raise ValueError("t‑SNE needs at least 2 samples")

    vec = _vectorizer().fit_transform(texts)

    perplexity = max(5, min(30, len(texts) // 3))

    tsne = TSNE(
        n_components=2,
        perplexity=perplexity,
        init="random",
        learning_rate="auto",
        max_iter=600,
        metric="cosine",
        n_jobs=1,
        verbose=0,
    )
    coords = tsne.fit_transform(vec.toarray())
    return [tuple(map(float, xy)) for xy in coords], texts
