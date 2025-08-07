import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
from models import Base, User, Category, Product
from crud import create_user, create_category, create_product
from schemas import UserCreate, CategoryCreate, ProductCreate
from auth import get_password_hash
from datetime import datetime

def seed_database():
    """Seed the database with initial data"""
    db = SessionLocal()
    
    try:
        # Create admin user
        admin_user_data = UserCreate(
            email="admin@toysmarketplace.com",
            username="admin",
            full_name="Admin User",
            password="admin123"
        )
        admin_user = create_user(db=db, user=admin_user_data)
        # Set admin role
        admin_user.is_admin = True
        db.commit()
        print(f"✅ Created admin user: {admin_user.email}")
        
        # Create regular user
        regular_user_data = UserCreate(
            email="user@toysmarketplace.com",
            username="user",
            full_name="Regular User",
            password="user123"
        )
        regular_user = create_user(db=db, user=regular_user_data)
        print(f"✅ Created regular user: {regular_user.email}")
        
        # Create categories
        categories_data = [
            {
                "name": "Action Figures",
                "description": "Collectible action figures and superhero toys",
                "image_url": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=400&h=300&fit=crop"
            },
            {
                "name": "Building Blocks",
                "description": "LEGO sets, building blocks, and construction toys",
                "image_url": "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=300&fit=crop"
            },
            {
                "name": "Educational Toys",
                "description": "Learning toys, puzzles, and educational games",
                "image_url": "https://images.unsplash.com/photo-1596464716127-f2a82984de30?w=400&h=300&fit=crop"
            },
            {
                "name": "Board Games",
                "description": "Family board games and strategy games",
                "image_url": "https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?w=400&h=300&fit=crop"
            },
            {
                "name": "Plush Toys",
                "description": "Soft plush toys and stuffed animals",
                "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop"
            },
            {
                "name": "Remote Control",
                "description": "RC cars, drones, and remote control toys",
                "image_url": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=400&h=300&fit=crop"
            }
        ]
        
        created_categories = []
        for cat_data in categories_data:
            category_data = CategoryCreate(**cat_data)
            category = create_category(db=db, category=category_data)
            created_categories.append(category)
            print(f"✅ Created category: {category.name}")
        
        # Create products
        products_data = [
            {
                "name": "Marvel Avengers Action Figure Set",
                "description": "Complete set of Marvel Avengers action figures including Iron Man, Captain America, Thor, and Hulk. High-quality collectible figures with detailed sculpting and articulation.",
                "price": 89.99,
                "stock_quantity": 25,
                "category_id": 1,  # Action Figures
                "image_url": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=400&h=300&fit=crop",
                "is_featured": True
            },
            {
                "name": "LEGO Star Wars Millennium Falcon",
                "description": "Iconic LEGO Star Wars Millennium Falcon building set with 1,329 pieces. Includes detailed interior and minifigures. Perfect for Star Wars fans and LEGO enthusiasts.",
                "price": 159.99,
                "stock_quantity": 15,
                "category_id": 2,  # Building Blocks
                "image_url": "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=300&fit=crop",
                "is_featured": True
            },
            {
                "name": "Educational Science Kit",
                "description": "Complete science experiment kit for kids aged 8-12. Includes 50+ experiments covering chemistry, physics, and biology. Safe and educational fun for young scientists.",
                "price": 49.99,
                "stock_quantity": 30,
                "category_id": 3,  # Educational Toys
                "image_url": "https://images.unsplash.com/photo-1596464716127-f2a82984de30?w=400&h=300&fit=crop",
                "is_featured": False
            },
            {
                "name": "Monopoly Classic Board Game",
                "description": "Classic Monopoly board game with updated properties and modern design. Perfect for family game nights. Includes all original components and rules.",
                "price": 29.99,
                "stock_quantity": 40,
                "category_id": 4,  # Board Games
                "image_url": "https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?w=400&h=300&fit=crop",
                "is_featured": False
            },
            {
                "name": "Giant Teddy Bear",
                "description": "Large plush teddy bear measuring 24 inches tall. Made from premium soft fabric with embroidered details. Perfect gift for children and teddy bear collectors.",
                "price": 39.99,
                "stock_quantity": 20,
                "category_id": 5,  # Plush Toys
                "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop",
                "is_featured": False
            },
            {
                "name": "RC Racing Car",
                "description": "High-speed remote control racing car with 4WD and 2.4GHz control. Reaches speeds up to 25 mph. Includes rechargeable battery and charger. Ages 8+.",
                "price": 79.99,
                "stock_quantity": 18,
                "category_id": 6,  # Remote Control
                "image_url": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=400&h=300&fit=crop",
                "is_featured": True
            },
            {
                "name": "Disney Princess Collection",
                "description": "Beautiful Disney Princess action figure collection including Cinderella, Belle, Ariel, and Snow White. Each figure comes with accessories and detailed costumes.",
                "price": 69.99,
                "stock_quantity": 22,
                "category_id": 1,  # Action Figures
                "image_url": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=400&h=300&fit=crop",
                "is_featured": False
            },
            {
                "name": "LEGO City Police Station",
                "description": "LEGO City Police Station building set with 743 pieces. Includes police car, motorcycle, and 6 minifigures. Perfect for imaginative play and building skills.",
                "price": 89.99,
                "stock_quantity": 12,
                "category_id": 2,  # Building Blocks
                "image_url": "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=300&fit=crop",
                "is_featured": False
            },
            {
                "name": "Math Learning Puzzle Set",
                "description": "Educational math puzzle set with 100+ problems covering addition, subtraction, multiplication, and division. Includes colorful pieces and answer key.",
                "price": 24.99,
                "stock_quantity": 35,
                "category_id": 3,  # Educational Toys
                "image_url": "https://images.unsplash.com/photo-1596464716127-f2a82984de30?w=400&h=300&fit=crop",
                "is_featured": False
            },
            {
                "name": "Chess Master Set",
                "description": "Professional chess set with wooden pieces and tournament-size board. Includes storage case and extra pieces. Perfect for learning and competitive play.",
                "price": 44.99,
                "stock_quantity": 16,
                "category_id": 4,  # Board Games
                "image_url": "https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?w=400&h=300&fit=crop",
                "is_featured": False
            },
            {
                "name": "Unicorn Plush Collection",
                "description": "Magical unicorn plush collection with rainbow mane and tail. Soft, huggable design perfect for unicorn lovers. Available in multiple sizes.",
                "price": 34.99,
                "stock_quantity": 28,
                "category_id": 5,  # Plush Toys
                "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop",
                "is_featured": False
            },
            {
                "name": "RC Drone with Camera",
                "description": "4K HD camera drone with 2.4GHz control and 15-minute flight time. Includes altitude hold, headless mode, and one-key return. Perfect for aerial photography.",
                "price": 129.99,
                "stock_quantity": 10,
                "category_id": 6,  # Remote Control
                "image_url": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=400&h=300&fit=crop",
                "is_featured": True
            }
        ]
        
        for prod_data in products_data:
            product_data = ProductCreate(**prod_data)
            product = create_product(db=db, product=product_data, seller_id=admin_user.id)
            print(f"✅ Created product: {product.name} - ${product.price}")
        
        print("\n🎉 Database seeding completed successfully!")
        print(f"📊 Created {len(categories_data)} categories and {len(products_data)} products")
        print("\n👤 Test Accounts:")
        print("   Admin: admin@toysmarketplace.com / admin123")
        print("   User: user@toysmarketplace.com / user123")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🌱 Starting database seeding...")
    seed_database() 