import axios from 'axios';

export const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        console.log('API Request:', config.method?.toUpperCase(), config.url, 'Token:', !!token);
        if (token && config.headers) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        console.error('API Request Error:', error);
        return Promise.reject(error);
    }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
    (response) => {
        console.log('API Response:', response.status, response.config.url);
        return response;
    },
    (error) => {
        console.error('API Response Error:', error.response?.status, error.config?.url, error.message);
        
        // Only redirect to login if it's a 401 error AND we have a token
        // This prevents redirecting when the backend is not running
        if (error.response?.status === 401 && localStorage.getItem('token')) {
            console.log('API: 401 error with token, clearing token and redirecting');
            localStorage.removeItem('token');
            // Only redirect if we're not already on the login page
            if (window.location.pathname !== '/login') {
                console.log('API: Redirecting to login');
                window.location.href = '/login';
            }
        } else if (error.response?.status === 401) {
            console.log('API: 401 error without token, not redirecting');
        } else {
            console.log('API: Non-401 error, not redirecting');
        }
        return Promise.reject(error);
    }
); 