import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Transactions from './pages/Transactions';
import Upload from './pages/Upload';
import Reports from './pages/Reports';
import Layout from './components/Layout';

const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const { isAuthenticated, loading } = useAuth();
    
    console.log('PrivateRoute: isAuthenticated:', isAuthenticated, 'loading:', loading);
    
    // Show loading spinner while checking authentication
    if (loading) {
        return (
            <div className="flex items-center justify-center h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
        );
    }
    
    return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

const App: React.FC = () => {
    return (
        <AuthProvider>
            <Router>
                <div className="min-h-screen bg-gray-50">
                    <Toaster position="top-right" />
                    <Routes>
                        <Route path="/login" element={<Login />} />
                        <Route path="/register" element={<Register />} />
                        <Route
                            path="/"
                            element={
                                <PrivateRoute>
                                    <Layout />
                                </PrivateRoute>
                            }
                        >
                            <Route index element={<Dashboard />} />
                            <Route path="transactions" element={<Transactions />} />
                            <Route path="upload" element={<Upload />} />
                            <Route path="reports" element={<Reports />} />
                        </Route>
                    </Routes>
                </div>
            </Router>
        </AuthProvider>
    );
};

export default App; 