import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const DebugAuth: React.FC = () => {
    const { user, isAuthenticated, loading } = useAuth();
    const token = localStorage.getItem('token');

    if (process.env.NODE_ENV !== 'development') {
        return null;
    }

    return (
        <div className="fixed bottom-4 right-4 bg-gray-800 text-white p-4 rounded-lg text-xs max-w-sm z-50">
            <h3 className="font-bold mb-2">Auth Debug Info</h3>
            <div className="space-y-1">
                <div>Loading: {loading ? 'Yes' : 'No'}</div>
                <div>Authenticated: {isAuthenticated ? 'Yes' : 'No'}</div>
                <div>Token: {token ? 'Present' : 'Missing'}</div>
                <div>User: {user ? user.email : 'None'}</div>
                <div>User ID: {user?.id || 'None'}</div>
            </div>
        </div>
    );
};

export default DebugAuth; 