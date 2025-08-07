#!/usr/bin/env python3
"""
Script to run the database seeder for the Toys Marketplace application.
This script will populate the database with initial categories, products, and test users.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main function to run the seeder"""
    try:
        print("🚀 Starting Toys Marketplace Database Seeder...")
        print("=" * 50)
        
        # Import and run the seeder
        from seeder import seed_database
        
        print("📊 Seeding database with initial data...")
        seed_database()
        
        print("\n✅ Seeding completed successfully!")
        print("\n🎯 Next steps:")
        print("   1. Start the backend server: python main.py")
        print("   2. Start the frontend: npm start")
        print("   3. Login with admin account: admin@toysmarketplace.com / admin123")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this script from the backend directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running seeder: {e}")
        print("Please check your database connection and try again")
        sys.exit(1)

if __name__ == "__main__":
    main() 