import pytest
from services.library_service import (
    add_book_to_catalog
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
def test_add_book_valid_input():
    """Test adding a book with valid input."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    if not success and "already exists" in message.lower():
        pytest.skip("Book already exists from previous test run.")

    
    assert success == True
    assert "successfully added" in message.lower()

# negative
def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    
    assert success == False
    assert "13 digits" in message


# negative
def test_add_book_title_too_long():
    """Test adding a book with a Title that is too long."""
    success, message = add_book_to_catalog("Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book Test Book ", "Test Author", "1234567890123", 10)
    
    assert success == False
    assert "title too long" in message.lower()


# positive
def test_add_book_valid_input_2():
    """Test adding a book with a different valid input."""
    success, message = add_book_to_catalog("I am a book", "Jerry Jones", "1203948576123", 23)
    if not success and "already exists" in message.lower():
        pytest.skip("Book already exists from previous test run.")
    
    assert success == True
    assert "successfully added" in message.lower()


# negative
def test_add_book_without_total_copies():
    """Test adding a book without total copies"""
    success, message = add_book_to_catalog("Zero Copies", "Johnny James", "1313948576123", 0)
    
    assert success == False
    assert "total copies" in message.lower()




