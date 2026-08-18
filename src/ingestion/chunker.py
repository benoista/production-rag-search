"""Semantic chunking of documents.

The chunker splits a Document into Chunks by detecting drops in semantic
similarity between consecutive sentences, while respecting a hard token limit.
"""

import re

import numpy as np
from sentence_transformers import SentenceTransformer

# Split after a sentence-ending punctuation (. ! ?) that is followed by
# whitespace and an uppercase letter. This over-splits on abbreviations
# (e.g. "Dr. Smith"), which is acceptable here: fragments of the same
# sentence have high cosine similarity and get merged back into one chunk.
_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def split_into_sentences(text: str) -> list[str]:
    """Split raw text into a list of sentences.

    Args:
        text: The document text to split.

    Returns:
        A list of non-empty, stripped sentences. Returns an empty list
        if the text is empty or contains only whitespace.
    """
    sentences = _SENTENCE_BOUNDARY.split(text.strip())
    return [s.strip() for s in sentences if s.strip()]

def embed_sentences(sentences: list[str], model: SentenceTransformer) -> np.ndarray:
    """Embed a list of sentences into a list of embeddings.

    Args:
        sentences: A list of sentences to embed.
        model: A SentenceTransformer model to use for embedding.

    Returns:
        A array of embeddings corresponding to the input sentences.
    """
    if len(sentences) == 0:
        return np.zeros((0, model.get_embedding_dimension()))
    
    return model.encode(sentences, convert_to_numpy=True)
