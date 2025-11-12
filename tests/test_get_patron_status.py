
import pytest
from services.library_service import (
    get_patron_status_report
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
def test_patron_status_no_borrowing():
    """Test patron status that has never borrowed"""
    status = get_patron_status_report("567899")
    
    assert status['borrowed_books'] == []
    assert status['late_fees'] == 0.0
    assert status['borrowed_books_count'] == 0
    assert status['borrow_history'] == []

# positive
def test_patron_status_no_fees():
    """Test patron status with no fees"""
    status = get_patron_status_report("654321")
    
    assert [book['book_id'] for book in status['borrowed_books']] == [1, 2]
    assert status['late_fees'] == 1.0
    assert status['borrowed_books_count'] == 2
    assert status['borrow_history'] == []

# negative
def test_patron_that_does_not_exist():
    """Test with a patron that does not exist"""
    status = get_patron_status_report("209049")
    
    assert status['borrowed_books'] == []
    assert status['late_fees'] == 0.0
    assert status['borrowed_books_count'] == 0
    assert status['borrow_history'] == []

# negative
def test_patron_invalid_ID():
    """Test with an invalid patron ID"""
    status = get_patron_status_report("abcdef")
    
    assert status['borrowed_books'] == []
    assert status['late_fees'] == 0.0
    assert status['borrowed_books_count'] == 0
    assert status['borrow_history'] == []

# positive
def test_patron_with_fees():
    """Test patron with late fees"""
    status = get_patron_status_report("123456")
    
    assert [book['book_id'] for book in status['borrowed_books']] == [5,1,4,2,3]
    assert status['late_fees'] == 8.5
    assert status['borrowed_books_count'] == 5
    assert status['borrow_history'] == []




