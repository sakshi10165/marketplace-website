import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Package, Star, ShoppingCart, ArrowRight } from 'lucide-react';
import axios from 'axios';
import { useCart } from '../contexts/CartContext';
import { useAuth } from '../contexts/AuthContext';

const Home = () => {
  const [categories, setCategories] = useState([]);
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const { addToCart } = useCart();
  const { isAuthenticated } = useAuth();

  const API_BASE_URL = 'https://marketplace-website-paav.onrender.com';

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [categoriesRes, productsRes] = await Promise.all([
          axios.get(`${API_BASE_URL}/categories`),
          axios.get(`${API_BASE_URL}/products?limit=6`)
        ]);

        setCategories(Array.isArray(categoriesRes.data) ? categoriesRes.data : []);
        setFeaturedProducts(Array.isArray(productsRes.data) ? productsRes.data : []);
      } catch (error) {
        console.error('Failed to fetch data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleAddToCart = async (productId) => {
    if (!isAuthenticated) {
      // Redirect to login or show login modal
      return;
    }
    await addToCart(productId);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-primary-500 to-primary-600 rounded-2xl overflow-hidden">
        <div className="absolute inset-0 bg-black opacity-10"></div>
        <div className="relative px-6 py-16 sm:px-12 sm:py-24">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl sm:text-6xl font-bold text-white mb-6">
              Welcome to Toys Marketplace
            </h1>
            <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
              Discover amazing toys for all ages. From educational games to action figures, 
              we have everything to spark imagination and create lasting memories.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/products"
                className="inline-flex items-center px-6 py-3 bg-white text-primary-600 font-semibold rounded-lg hover:bg-gray-50 transition-colors duration-200"
              >
                Browse Products
                <ArrowRight className="ml-2" size={20} />
              </Link>
              {!isAuthenticated && (
                <Link
                  to="/register"
                  className="inline-flex items-center px-6 py-3 border-2 border-white text-white font-semibold rounded-lg hover:bg-white hover:text-primary-600 transition-colors duration-200"
                >
                  Join Now
                </Link>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section>
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-3xl font-bold text-gray-900">Shop by Category</h2>
          <Link to="/products" className="text-primary-600 hover:text-primary-700 font-medium">
            View all
          </Link>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {Array.isArray(categories) && categories.length > 0 ? (
            categories.slice(0, 4).map((category) => (
              <Link
                key={category.id}
                to={`/products?category=${category.id}`}
                className="card p-6 text-center hover:scale-105 transition-transform duration-200"
              >
                <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Package className="w-8 h-8 text-primary-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">{category.name}</h3>
                <p className="text-sm text-gray-600">{category.description}</p>
              </Link>
            ))
          ) : (
            <p>No categories available</p>
          )}
        </div>
      </section>

      {/* Featured Products */}
      <section>
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-3xl font-bold text-gray-900">Featured Products</h2>
          <Link to="/products" className="text-primary-600 hover:text-primary-700 font-medium">
            View all
          </Link>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.isArray(featuredProducts) && featuredProducts.length > 0 ? (
            featuredProducts.map((product) => (
              <div key={product.id} className="card p-6">
                <div className="aspect-square bg-gray-100 rounded-lg mb-4 flex items-center justify-center">
                  {product.image_url ? (
                    <img
                      src={product.image_url}
                      alt={product.name}
                      className="w-full h-full object-cover rounded-lg"
                    />
                  ) : (
                    <Package className="w-16 h-16 text-gray-400" />
                  )}
                </div>
                <div className="space-y-3">
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-1">{product.name}</h3>
                    <p className="text-sm text-gray-600 line-clamp-2">{product.description}</p>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-1">
                      <Star className="w-4 h-4 text-yellow-400 fill-current" />
                      <span className="text-sm text-gray-600">4.5</span>
                    </div>
                    <span className="font-bold text-lg text-primary-600">
                      ${product.price}
                    </span>
                  </div>
                  <button
                    onClick={() => handleAddToCart(product.id)}
                    className="w-full btn-primary flex items-center justify-center"
                  >
                    <ShoppingCart className="w-4 h-4 mr-2" />
                    Add to Cart
                  </button>
                </div>
              </div>
            ))
          ) : (
            <p>No featured products available</p>
          )}
        </div>
      </section>

      {/* Call to Action */}
      <section className="bg-gray-900 rounded-2xl p-8 text-center">
        <h2 className="text-3xl font-bold text-white mb-4">
          Ready to Start Shopping?
        </h2>
        <p className="text-gray-300 mb-6 max-w-2xl mx-auto">
          Join thousands of happy customers who trust Toys Marketplace for quality toys and excellent service.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/products"
            className="btn-primary"
          >
            Browse All Products
          </Link>
          {!isAuthenticated && (
            <Link
              to="/register"
              className="btn-secondary"
            >
              Create Account
            </Link>
          )}
        </div>
      </section>
    </div>
  );
};

export default Home;
