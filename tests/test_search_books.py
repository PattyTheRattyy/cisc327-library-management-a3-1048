
import pytest
from services.library_service import (
    search_books_in_catalog
)
import os
from database import init_database, add_sample_data, seed_test_patrons

@pytest.fixture(autouse=True)
def reset_db():
    """Reset the database before each test."""
    if os.path.exists('library.db'):
        os.remove('library.db')
    init_database()
    add_sample_data()
    seed_test_patrons()
    yield

# positive
def test_search_exact_ISBN():
    """Test searching with exact ISBN"""
    results = search_books_in_catalog("1234567890123", "isbn")
    
    assert len(results) > 0
    assert results[0]["isbn"] == "1234567890123"

# negative
def test_search_for_book_that_does_not_exist():
    """Test searching when book does not exist"""
    results = search_books_in_catalog("the pink flamingo flocks to the sea", "title")
    
    assert results == []

# negative
def test_search_invalid_format():
    """Test searching when the format is invalid"""
    results = search_books_in_catalog("1432167890123", "author")
    
    assert results == []

# positive
def test_search_partial_title():
    """Test searching with partial title"""
    results = search_books_in_catalog("Scorch", "title")
    
    assert len(results) > 0
    assert all("scorch" in book["title"].lower() for book in results)

# positive
def test_search_partial_author():
    """Test searching with partial author"""
    results = search_books_in_catalog("patty", "author")
    
    assert len(results) > 0
    assert all("patty" in book["author"].lower() for book in results)







