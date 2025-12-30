# Contact Management System
# Week 3 Project - Functions & Dictionaries

import json
import re
from datetime import datetime
import csv
import os

# Global contacts dictionary
contacts = {}

def validate_phone(phone):
    """Validate phone number format"""
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)

    # Check if we have 10-15 digits (international format)
    if 10 <= len(digits) <= 15:
        return True, digits
    return False, None

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def load_from_file():
    """Load contacts from JSON file"""
    global contacts
    if os.path.exists('contacts.json'):
        try:
            with open('contacts.json', 'r') as f:
                contacts = json.load(f)
            print(f"✅ Loaded {len(contacts)} contacts from file.")
        except json.JSONDecodeError:
            print("❌ Error loading contacts file. Starting with empty contacts.")
            contacts = {}
    else:
        print("No contacts file found. Starting fresh.")

def save_to_file():
    """Save contacts to JSON file"""
    try:
        with open('contacts.json', 'w') as f:
            json.dump(contacts, f, indent=4)
        print("✅ Contacts saved to file.")
    except Exception as e:
        print(f"❌ Error saving contacts: {e}")

def add_contact():
    """Add a new contact to the dictionary"""
    print("\n--- ADD NEW CONTACT ---")

    # Get contact name
    while True:
        name = input("Enter contact name: ").strip()
        if name:
            if name in contacts:
                print(f"Contact '{name}' already exists!")
                choice = input("Do you want to update instead? (y/n): ").lower()
                if choice == 'y':
                    update_contact(name)
                    return
                else:
                    continue
            break
        print("Name cannot be empty!")

    # Get phone number with validation
    while True:
        phone = input("Enter phone number: ").strip()
        is_valid, cleaned_phone = validate_phone(phone)
        if is_valid:
            break
        print("Invalid phone number! Please enter 10-15 digits.")

    # Get email with validation
    while True:
        email = input("Enter email (optional, press Enter to skip): ").strip()
        if not email or validate_email(email):
            break
        print("Invalid email format!")

    # Get additional info
    address = input("Enter address (optional): ").strip()
    group = input("Enter group (Friends/Work/Family/Other): ").strip() or "Other"

    # Store in dictionary
    contacts[name] = {
        'phone': cleaned_phone,
        'email': email if email else None,
        'address': address if address else None,
        'group': group,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }

    print(f"✅ Contact '{name}' added successfully!")
    save_to_file()

def search_contacts():
    """Search contacts by name or phone (partial match)"""
    print("\n--- SEARCH CONTACTS ---")
    search_term = input("Enter name or phone to search: ").strip().lower()
    if not search_term:
        print("Search term cannot be empty.")
        return

    results = {}

    for name, info in contacts.items():
        if (search_term in name.lower() or
            search_term in info['phone'] or
            (info['email'] and search_term in info['email'].lower())):
            results[name] = info

    display_search_results(results)

def display_search_results(results):
    """Display search results in formatted way"""
    if not results:
        print("No contacts found.")
        return

    print(f"\nFound {len(results)} contact(s):")
    print("-" * 50)

    for i, (name, info) in enumerate(results.items(), 1):
        print(f"{i}. {name}")
        print(f"   📞 Phone: {info['phone']}")
        if info['email']:
            print(f"   📧 Email: {info['email']}")
        if info['address']:
            print(f"   📍 Address: {info['address']}")
        print(f"   👥 Group: {info['group']}")
        print()

def update_contact(name=None):
    """Update an existing contact"""
    if not name:
        print("\n--- UPDATE CONTACT ---")
        name = input("Enter contact name to update: ").strip()
        if name not in contacts:
            print(f"Contact '{name}' not found.")
            return

    info = contacts[name]
    print(f"\nUpdating contact: {name}")
    print(f"Current info: Phone: {info['phone']}, Email: {info.get('email', 'N/A')}, Address: {info.get('address', 'N/A')}, Group: {info['group']}")

    # Update phone
    phone_choice = input("Update phone? (y/n): ").lower()
    if phone_choice == 'y':
        while True:
            phone = input("Enter new phone number: ").strip()
            is_valid, cleaned_phone = validate_phone(phone)
            if is_valid:
                info['phone'] = cleaned_phone
                break
            print("Invalid phone number!")

    # Update email
    email_choice = input("Update email? (y/n): ").lower()
    if email_choice == 'y':
        while True:
            email = input("Enter new email (optional, press Enter to skip): ").strip()
            if not email or validate_email(email):
                info['email'] = email if email else None
                break
            print("Invalid email format!")

    # Update address
    address_choice = input("Update address? (y/n): ").lower()
    if address_choice == 'y':
        info['address'] = input("Enter new address (optional): ").strip() or None

    # Update group
    group_choice = input("Update group? (y/n): ").lower()
    if group_choice == 'y':
        info['group'] = input("Enter new group (Friends/Work/Family/Other): ").strip() or "Other"

    info['updated_at'] = datetime.now().isoformat()
    print(f"✅ Contact '{name}' updated successfully!")
    save_to_file()

def delete_contact():
    """Delete a contact with confirmation"""
    print("\n--- DELETE CONTACT ---")
    name = input("Enter contact name to delete: ").strip()
    if name not in contacts:
        print(f"Contact '{name}' not found.")
        return

    confirm = input(f"Are you sure you want to delete '{name}'? (yes/no): ").lower()
    if confirm == 'yes':
        del contacts[name]
        print(f"✅ Contact '{name}' deleted successfully!")
        save_to_file()
    else:
        print("Deletion cancelled.")

def display_all_contacts():
    """Display all contacts"""
    if not contacts:
        print("\nNo contacts to display.")
        return

    print(f"\n--- ALL CONTACTS ({len(contacts)}) ---")
    print("-" * 50)

    for name, info in sorted(contacts.items()):
        print(f"Name: {name}")
        print(f"   📞 Phone: {info['phone']}")
        if info['email']:
            print(f"   📧 Email: {info['email']}")
        if info['address']:
            print(f"   📍 Address: {info['address']}")
        print(f"   👥 Group: {info['group']}")
        print()

def export_to_csv():
    """Export contacts to CSV file"""
    if not contacts:
        print("No contacts to export.")
        return

    filename = input("Enter CSV filename (default: contacts.csv): ").strip() or "contacts.csv"

    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['name', 'phone', 'email', 'address', 'group', 'created_at', 'updated_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for name, info in contacts.items():
                row = {
                    'name': name,
                    'phone': info['phone'],
                    'email': info.get('email', ''),
                    'address': info.get('address', ''),
                    'group': info['group'],
                    'created_at': info['created_at'],
                    'updated_at': info['updated_at']
                }
                writer.writerow(row)

        print(f"✅ Contacts exported to {filename}")
    except Exception as e:
        print(f"❌ Error exporting to CSV: {e}")

def show_statistics():
    """Show contact statistics"""
    total = len(contacts)
    if total == 0:
        print("\nNo contacts in the system.")
        return

    groups = {}
    for info in contacts.values():
        group = info['group']
        groups[group] = groups.get(group, 0) + 1

    print(f"\n--- CONTACT STATISTICS ---")
    print(f"Total Contacts: {total}")
    print("Contacts by Group:")
    for group, count in groups.items():
        print(f"  {group}: {count}")

def main_menu():
    """Main menu function"""
    load_from_file()

    while True:
        print("\n" + "="*40)
        print("📱 CONTACT MANAGEMENT SYSTEM")
        print("="*40)
        print("1. Add Contact")
        print("2. Search Contacts")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Display All Contacts")
        print("6. Export to CSV")
        print("7. Show Statistics")
        print("8. Save & Exit")
        print("="*40)

        choice = input("Enter your choice (1-8): ").strip()

        if choice == '1':
            add_contact()
        elif choice == '2':
            search_contacts()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            delete_contact()
        elif choice == '5':
            display_all_contacts()
        elif choice == '6':
            export_to_csv()
        elif choice == '7':
            show_statistics()
        elif choice == '8':
            save_to_file()
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()
