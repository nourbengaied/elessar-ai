import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';

const AuthTest: React.FC = () => {
    const { user, isAuthenticated, loading } = useAuth();
    const [testResult, setTestResult] = useState<string>('');

    const testAuth = async () => {
        try {
            console.log('Testing auth endpoint...');
            const response = await api.get('/api/v1/auth/me');
            setTestResult(`✅ Auth test successful: ${JSON.stringify(response.data)}`);
        } catch (error: any) {
            setTestResult(`❌ Auth test failed: ${error.response?.status} - ${error.message}`);
        }
    };

    const testHealth = async () => {
        try {
            console.log('Testing health endpoint...');
            const response = await api.get('/health');
            setTestResult(`✅ Health test successful: ${JSON.stringify(response.data)}`);
        } catch (error: any) {
            setTestResult(`❌ Health test failed: ${error.response?.status} - ${error.message}`);
        }
    };

    if (process.env.NODE_ENV !== 'development') {
        return null;
    }

    return (
        <div className="fixed top-4 right-4 bg-gray-800 text-white p-4 rounded-lg text-xs max-w-sm z-50">
            <h3 className="font-bold mb-2">Auth Test Panel</h3>
            <div className="space-y-2">
                <div>User: {user?.email || 'None'}</div>
                <div>Authenticated: {isAuthenticated ? 'Yes' : 'No'}</div>
                <div>Loading: {loading ? 'Yes' : 'No'}</div>
                <div>Token: {localStorage.getItem('token') ? 'Present' : 'Missing'}</div>
            </div>
            <div className="mt-4 space-y-2">
                <button
                    onClick={testAuth}
                    className="w-full bg-blue-600 hover:bg-blue-700 px-2 py-1 rounded text-xs"
                >
                    Test Auth
                </button>
                <button
                    onClick={testHealth}
                    className="w-full bg-green-600 hover:bg-green-700 px-2 py-1 rounded text-xs"
                >
                    Test Health
                </button>
            </div>
            {testResult && (
                <div className="mt-2 p-2 bg-gray-700 rounded text-xs">
                    {testResult}
                </div>
            )}
        </div>
    );
};

export default AuthTest; 