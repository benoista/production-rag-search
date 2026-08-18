import datetime

import pytest
from pydantic import ValidationError

from src.models.schema import Chunk, Document

"""Test if the document is created successfully"""
def test_document_creation():
    document = Document(
        id="1",
        content="Hello, world!",
        filepath="test.txt",
        created_at=datetime.datetime.now(),
        metadata={"author": "John Doe"},
    )
    assert document.content_hash != ""

"""Test if the document raise a exception if create with missing args"""
def test_document_creating_missing_args():
    with pytest.raises(ValidationError):
        document = Document(
            id="1",
            content="Hello, world!",
            created_at=datetime.datetime.now(),
            metadata={"author": "John Doe"},
        )

"""Test if the metadata (str, str) type is not respected then throw an error"""
def test_document_creation_metadata_types_error():
    with pytest.raises(ValidationError):
        document = Document(
            id="1",
            content="Hello, world!",
            filepath="test.txt",
            created_at=datetime.datetime.now(),
            metadata={123: "John Doe"},
        )

# Test if the created_at type is not respected then throw an error
def test_document_creation_created_types_error():
    with pytest.raises(ValidationError):
        document = Document(
            id="1",
            content="Hello, world!",
            filepath="test.txt",
            created_at=datetime.datetime.year,
            metadata={123: "John Doe"},
        )

"""Test if the content hash is the same for two documents with the same content"""
def test_same_hash_content():
    document = Document(
        id="1",
        content="Hello, world!",
        filepath="test.txt",
        created_at=datetime.datetime.now(),
        metadata={"author": "John Doe"},
    )
    document2 = Document(
        id="2",
        content="Hello, world!",
        filepath="test.txt",
        created_at=datetime.datetime.now(),
        metadata={"author": "John Doe"},
    )
    assert document.content_hash == document2.content_hash


"""Test if the content hash is the same for two documents with the same content"""
def test_different_hash_content():
    document = Document(
        id="1",
        content="Hello, world!",
        filepath="test.txt",
        created_at=datetime.datetime.now(),
        metadata={"author": "John Doe"},
    )
    document2 = Document(
        id="2",
        content="Goodbye, world!",
        filepath="test.txt",
        created_at=datetime.datetime.now(),
        metadata={"author": "John Doe"},
    )
    assert document.content_hash != document2.content_hash

"""Test if the Chunk id is created"""
def test_chunk_creation():
    chunk = Chunk(
        id="1",
        content="Hello, world!",
        document_id="1",
        index = 1,
        token_nbr=300,
    )
    assert chunk.id == "1::1"