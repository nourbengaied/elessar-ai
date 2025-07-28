import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

const BackendStatus: React.FC = () => {
    const [status, setStatus] = useState<'checking' | 'online' | 'offline'>('checking');

    useEffect(() => {
        checkBackendStatus();
    }, []);

    const checkBackendStatus = async () => {
        try {
            await api.get('/health');
            setStatus('online');
        } catch (error) {
            console.error('Backend status check failed:', error);
            setStatus('offline');
        }
    };

    if (process.env.NODE_ENV !== 'development') {
        return null;
    }

    const getStatusColor = () => {
        switch (status) {
            case 'online':
                return 'bg-green-500';
            case 'offline':
                return 'bg-red-500';
            default:
                return 'bg-yellow-500';
        }
    };

    const getStatusText = () => {
        switch (status) {
            case 'online':
                return 'Backend Online';
            case 'offline':
                return 'Backend Offline';
            default:
                return 'Checking...';
        }
    };

    return (
        <div className="fixed bottom-4 left-4 bg-gray-800 text-white p-4 rounded-lg text-xs z-50">
            <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${getStatusColor()}`}></div>
                <span>{getStatusText()}</span>
            </div>
            <button
                onClick={checkBackendStatus}
                className="mt-2 text-blue-300 hover:text-blue-100 text-xs"
            >
                Retry
            </button>
        </div>
    );
};

export default BackendStatus; 