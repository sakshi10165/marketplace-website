from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from database import get_db, engine
from models import Base
from schemas import (
    User, UserCreate, UserLogin, Token,
    Category, CategoryCreate, CategoryUpdate,
    Product, ProductCreate, ProductUpdate,
    CartItem, CartItemCreate, CartItemUpdate
)
from crud import (
    create_user, get_user_by_email, get_user_by_username, authenticate_user,
    get_categories, create_category, update_category, delete_category,
    get_products, create_product, update_product, delete_product,
    get_user_cart, create_cart_item, update_cart_item, delete_cart_item, clear_user_cart
)
from auth import create_access_token, get_current_active_user, get_current_admin_user
from config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Toys Marketplace API",
    description="A comprehensive API for the Toys Marketplace e-commerce platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://marketplace-website-six.vercel.app",
        "https://marketplace-website-paav.onrender.com"
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication endpoints
@app.post("/auth/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    return create_user(db=db, user=user)

@app.post("/auth/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me", response_model=User)
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    return current_user

# Category endpoints
@app.get("/categories", response_model=List[Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = get_categories(db, skip=skip, limit=limit)
    return categories

@app.post("/categories", response_model=Category)
def create_new_category(
    category: CategoryCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    return create_category(db=db, category=category)

@app.put("/categories/{category_id}", response_model=Category)
def update_existing_category(
    category_id: int,
    category_update: CategoryUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    db_category = update_category(db, category_id, category_update)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@app.delete("/categories/{category_id}")
def delete_existing_category(
    category_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    db_category = delete_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}

# Product endpoints
@app.get("/products", response_model=List[Product])
def read_products(
    skip: int = 0,
    limit: int = 100,
    category_id: int = None,
    db: Session = Depends(get_db)
):
    products = get_products(db, skip=skip, limit=limit, category_id=category_id)
    return products

@app.post("/products", response_model=Product)
def create_new_product(
    product: ProductCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return create_product(db=db, product=product, seller_id=current_user.id)

@app.put("/products/{product_id}", response_model=Product)
def update_existing_product(
    product_id: int,
    product_update: ProductUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_product = update_product(db, product_id, product_update)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.delete("/products/{product_id}")
def delete_existing_product(
    product_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_product = delete_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# Cart endpoints
@app.get("/cart", response_model=List[CartItem])
def read_user_cart(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_user_cart(db, current_user.id)

@app.post("/cart", response_model=CartItem)
def add_to_cart(
    cart_item: CartItemCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return create_cart_item(db=db, cart_item=cart_item, user_id=current_user.id)

@app.put("/cart/{cart_item_id}", response_model=CartItem)
def update_cart_item_quantity(
    cart_item_id: int,
    cart_item_update: CartItemUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_cart_item = update_cart_item(db, cart_item_id, cart_item_update.quantity)
    if db_cart_item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return db_cart_item

@app.delete("/cart/{cart_item_id}")
def remove_from_cart(
    cart_item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_cart_item = delete_cart_item(db, cart_item_id)
    if db_cart_item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Item removed from cart"}

@app.delete("/cart")
def clear_cart(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    clear_user_cart(db, current_user.id)
    return {"message": "Cart cleared successfully"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Toys Marketplace API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, "https://marketplace-website-paav.onrender.com") 