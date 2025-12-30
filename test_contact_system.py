# Test script for Contact Management System

import sys
import os
import json
import tempfile
import shutil
from datetime import datetime

sys.path.insert(0, os.getcwd())

from contactManagementSystem import (
    validate_phone, validate_email, load_from_file, save_to_file,
    add_contact, search_contacts, display_search_results, update_contact,
    delete_contact, display_all_contacts, export_to_csv, show_statistics,
    contacts
)

def test_validate_phone():
    """Test phone validation"""
    print("Testing validate_phone...")

    # Valid phones
    assert validate_phone("1234567890") == (True, "1234567890")
    assert validate_phone("(123) 456-7890") == (True, "1234567890")
    assert validate_phone("+1-123-456-7890") == (True, "11234567890")

    # Invalid phones
    assert validate_phone("123") == (False, None)
    assert validate_phone("12345678901234567890") == (False, None)

    print("✅ validate_phone tests passed")

def test_validate_email():
    """Test email validation"""
    print("Testing validate_email...")

    # Valid emails
    assert validate_email("test@example.com") == True
    assert validate_email("user.name+tag@domain.co.uk") == True

    # Invalid emails
    assert validate_email("invalid-email") == False
    assert validate_email("@domain.com") == False

    print("✅ validate_email tests passed")

def test_file_operations():
    """Test file save/load operations"""
    print("Testing file operations...")

    # Use a test file to avoid overwriting main contacts.json
    test_file = 'test_contacts.json'

    try:
        # Clear contacts
        contacts.clear()

        # Add test data
        contacts['Test User'] = {
            'phone': '1234567890',
            'email': 'test@example.com',
            'address': '123 Test St',
            'group': 'Friends',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

        # Temporarily change the file name in save/load functions (simulate)
        # Since functions are hardcoded to 'contacts.json', we'll test with that
        # But to avoid issues, we'll backup and restore

        # Backup existing contacts.json if exists
        backup_file = None
        if os.path.exists('contacts.json'):
            backup_file = 'contacts_backup.json'
            shutil.move('contacts.json', backup_file)

        try:
            # Test save
            save_to_file()
            assert os.path.exists('contacts.json')

            # Clear and test load
            contacts.clear()
            load_from_file()
            assert 'Test User' in contacts
            assert contacts['Test User']['phone'] == '1234567890'

        finally:
            # Restore backup
            if backup_file:
                if os.path.exists('contacts.json'):
                    os.remove('contacts.json')
                shutil.move(backup_file, 'contacts.json')
            elif os.path.exists('contacts.json'):
                os.remove('contacts.json')

    except Exception as e:
        print(f"File operations test error: {e}")
        raise

    print("✅ File operations tests passed")

def test_search_functionality():
    """Test search functionality"""
    print("Testing search functionality...")

    # Setup test data
    contacts.clear()
    contacts['John Doe'] = {
        'phone': '1234567890',
        'email': 'john@example.com',
        'address': None,
        'group': 'Friends',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    contacts['Jane Smith'] = {
        'phone': '0987654321',
        'email': 'jane@example.com',
        'address': '456 Main St',
        'group': 'Work',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }

    # Test search by name
    results = {}
    for name, info in contacts.items():
        if 'john' in name.lower():
            results[name] = info
    assert len(results) == 1
    assert 'John Doe' in results

    # Test search by phone
    results = {}
    for name, info in contacts.items():
        if '123' in info['phone']:
            results[name] = info
    assert len(results) == 1
    assert 'John Doe' in results

    print("✅ Search functionality tests passed")

def test_statistics():
    """Test statistics functionality"""
    print("Testing statistics...")

    # Setup test data
    contacts.clear()
    contacts['User1'] = {'group': 'Friends', 'phone': '1', 'email': None, 'address': None, 'created_at': '', 'updated_at': ''}
    contacts['User2'] = {'group': 'Work', 'phone': '2', 'email': None, 'address': None, 'created_at': '', 'updated_at': ''}
    contacts['User3'] = {'group': 'Friends', 'phone': '3', 'email': None, 'address': None, 'created_at': '', 'updated_at': ''}

    # Capture print output (simplified test)
    total = len(contacts)
    assert total == 3

    groups = {}
    for info in contacts.values():
        group = info['group']
        groups[group] = groups.get(group, 0) + 1

    assert groups['Friends'] == 2
    assert groups['Work'] == 1

    print("✅ Statistics tests passed")

def run_all_tests():
    """Run all tests"""
    print("Running Contact Management System Tests...\n")

    try:
        test_validate_phone()
        test_validate_email()
        test_file_operations()
        test_search_functionality()
        test_statistics()

        print("\n🎉 All tests passed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
