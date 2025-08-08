import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import { useAuth } from './AuthContext';

const CartContext = createContext();
const API_BASE_URL = 'https://marketplace-website-paav.onrender.com';
export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const { isAuthenticated } = useAuth();

  // Load cart items when user is authenticated
  useEffect(() => {
    if (isAuthenticated) {
      loadCart();
    } else {
      setCartItems([]);
    }
  }, [isAuthenticated]);

  const loadCart = async () => {
    if (!isAuthenticated) return;
    
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/cart`);
      console.log('Cart API response data:', response.data);
      if (Array.isArray(response.data)) {
        setCartItems(response.data);
      } else {
        console.warn('Cart data is not an array, resetting to empty array');
        setCartItems([]);
      }
    } catch (error) {
      console.error('Failed to load cart:', error);
      toast.error('Failed to load cart items');
    } finally {
      setLoading(false);
    }
  };

  const addToCart = async (productId, quantity = 1) => {
    if (!isAuthenticated) {
      toast.error('Please log in to add items to cart');
      return false;
    }

    try {
      const response = await axios.post(`${API_BASE_URL}/cart`, {
        product_id: productId,
        quantity: quantity
      });
      
      // Update cart items
      await loadCart();
      toast.success('Added to cart!');
      return true;
    } catch (error) {
      const message = error.response?.data?.detail || 'Failed to add to cart';
      toast.error(message);
      return false;
    }
  };

  const updateCartItem = async (cartItemId, quantity) => {
    if (!isAuthenticated) return false;

    try {
      await axios.put(`${API_BASE_URL}/cart/${cartItemId}`, { quantity });
      await loadCart();
      toast.success('Cart updated!');
      return true;
    } catch (error) {
      const message = error.response?.data?.detail || 'Failed to update cart';
      toast.error(message);
      return false;
    }
  };

  const removeFromCart = async (cartItemId) => {
    if (!isAuthenticated) return false;

    try {
      await axios.delete(`${API_BASE_URL}/cart/${cartItemId}`);
      await loadCart();
      toast.success('Item removed from cart');
      return true;
    } catch (error) {
      const message = error.response?.data?.detail || 'Failed to remove item';
      toast.error(message);
      return false;
    }
  };

  const clearCart = async () => {
    if (!isAuthenticated) return false;

    try {
      await axios.delete(`${API_BASE_URL}/cart`);
      setCartItems([]);
      toast.success('Cart cleared');
      return true;
    } catch (error) {
      const message = error.response?.data?.detail || 'Failed to clear cart';
      toast.error(message);
      return false;
    }
  };

  const getCartTotal = () => {
    if (!Array.isArray(cartItems)) return 0;
    return cartItems.reduce((total, item) => total + (item.product.price * item.quantity), 0);
  };

  const getCartItemCount = () => {
    if (!Array.isArray(cartItems)) return 0;
    return cartItems.reduce((count, item) => count + item.quantity, 0);
  };

  const value = {
    cartItems,
    loading,
    addToCart,
    updateCartItem,
    removeFromCart,
    clearCart,
    loadCart,
    getCartTotal,
    getCartItemCount,
  };

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  );
}; 