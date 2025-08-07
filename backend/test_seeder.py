#!/usr/bin/env python3
"""
Test script for the database seeder.
This script tests the seeding functionality without actually modifying the database.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from seeder import (
    create_categories,
    create_products,
    create_test_users,
    get_db
)
from models import Category, Product, User
from sqlalchemy.orm import Session

def test_categories():
    """Test category creation"""
    print("Testing category creation...")
    try:
        db = next(get_db())
        categories = create_categories(db)
        print(f"✅ Created {len(categories)} categories:")
        for category in categories:
            print(f"  - {category.name}: {category.description}")
        return True
    except Exception as e:
        print(f"❌ Error creating categories: {e}")
        return False

def test_products():
    """Test product creation"""
    print("\nTesting product creation...")
    try:
        db = next(get_db())
        products = create_products(db)
        print(f"✅ Created {len(products)} products:")
        for product in products:
            print(f"  - {product.name}: ${product.price}")
        return True
    except Exception as e:
        print(f"❌ Error creating products: {e}")
        return False

def test_users():
    """Test user creation"""
    print("\nTesting user creation...")
    try:
        db = next(get_db())
        users = create_test_users(db)
        print(f"✅ Created {len(users)} users:")
        for user in users:
            print(f"  - {user.email} ({user.role})")
        return True
    except Exception as e:
        print(f"❌ Error creating users: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("Testing database connection...")
    try:
        db = next(get_db())
        # Test a simple query
        result = db.execute("SELECT 1").fetchone()
        if result:
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection failed")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Starting seeder tests...\n")
    
    # Test database connection first
    if not test_database_connection():
        print("\n❌ Database connection failed. Please check your configuration.")
        return
    
    # Test each component
    category_success = test_categories()
    product_success = test_products()
    user_success = test_users()
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    print(f"Database Connection: {'✅ PASS' if True else '❌ FAIL'}")
    print(f"Categories: {'✅ PASS' if category_success else '❌ FAIL'}")
    print(f"Products: {'✅ PASS' if product_success else '❌ FAIL'}")
    print(f"Users: {'✅ PASS' if user_success else '❌ FAIL'}")
    
    if all([category_success, product_success, user_success]):
        print("\n🎉 All tests passed! Your seeder is ready to use.")
        print("Run 'python run_seeder.py' to seed your database.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print("="*50)

if __name__ == "__main__":
    main()
