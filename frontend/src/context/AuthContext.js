import React, { createContext, useState, useCallback } from 'react';
import { authAPI, setAuthToken, clearAuthToken, getAuthToken } from '../services/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem('user');
    return stored ? JSON.parse(stored) : null;
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const register = useCallback(async (email, password) => {
    setLoading(true);
    setError(null);
    try {
      const response = await authAPI.register(email, password);
      const userData = response.data;
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      return userData;
    } catch (err) {
      const message = err.response?.data?.detail || 'Registration failed';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const login = useCallback(async (email, password) => {
    setLoading(true);
    setError(null);
    try {
      const response = await authAPI.login(email, password);
      const { access_token, token_type } = response.data;
      const token = access_token;
      
      setAuthToken(token);
      
      // Store user info
      const userData = { email, id: 'user' };
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      
      return { token, user: userData };
    } catch (err) {
      const message = err.response?.data?.detail || 'Login failed';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    clearAuthToken();
  }, []);

  const value = {
    user,
    loading,
    error,
    register,
    login,
    logout,
    isAuthenticated: !!user,
    token: getAuthToken()
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = React.useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
