
import pytest
from sentence_transformers import SentenceTransformer

from src.ingestion.chunker import embed_sentences, split_into_sentences


@pytest.fixture(scope="module")
def sentence_transformer():
    """Fixture to provide a SentenceTransformer model for testing."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

def test_chunker_split_into_sentences():
    text = "This is the first sentence. This is the second sentence! Is this the third sentence? Yes, it is."
    expected_sentences = [
        "This is the first sentence.",
        "This is the second sentence!",
        "Is this the third sentence?",
        "Yes, it is."
    ]
    sentences = split_into_sentences(text)
    assert sentences == expected_sentences

def test_chunker_split_empty_string():
    text = ""
    expected_sentences = []

    sentences = split_into_sentences(text)
    assert sentences == expected_sentences

""" Test chunker with limitations 
due to technical choices made: since the split method uses a regex (see src/ingestion/chunker.py).
Which is acceptable here: fragments of the same sentence have high cosine similarity and get merged back into one chunk.
"""

def test_chunker_split_with_limitations():
    text = "Dr. Smith went home."
    expected_sentences = [
        "Dr.",
        "Smith went home."
    ]

    sentences = split_into_sentences(text)
    assert sentences == expected_sentences

"""Test the embed_sentences function with a SentenceTransformer model"""
def test_embed_sentences(sentence_transformer):
    sentences = ["This is the first sentence.", "This is the second sentence."]
    embeddings = embed_sentences(sentences, sentence_transformer)

    assert embeddings.shape == (len(sentences), sentence_transformer.get_embedding_dimension())

"""Test the embed_sentences function with an empty list of sentences"""
def test_embed_sentences_empty_list(sentence_transformer):
    sentences = []
    embeddings = embed_sentences(sentences, sentence_transformer)

    assert embeddings.shape == (0, sentence_transformer.get_embedding_dimension())