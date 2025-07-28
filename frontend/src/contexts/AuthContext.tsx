import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { api } from '../services/api';
import { User, LoginResponse, RegisterResponse } from '../types/api';

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    login: (email: string, password: string) => Promise<void>;
    register: (email: string, password: string, business_name?: string, tax_id?: string) => Promise<void>;
    logout: () => void;
    loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

interface AuthProviderProps {
    children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        console.log('AuthProvider: Initializing...');
        const token = localStorage.getItem('token');
        console.log('AuthProvider: Token found:', !!token);
        
        if (token) {
            api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            fetchUser();
        } else {
            console.log('AuthProvider: No token found, setting loading to false');
            setLoading(false);
        }
    }, []);

    const fetchUser = async () => {
        try {
            console.log('AuthProvider: Fetching user data...');
            const response = await api.get('/api/v1/auth/me');
            console.log('AuthProvider: User data received:', response.data);
            setUser(response.data as User);
        } catch (error: any) {
            console.error('AuthProvider: Failed to fetch user:', error);
            // Only clear token if it's an authentication error
            if (error.response?.status === 401) {
                console.log('AuthProvider: 401 error, clearing token');
                localStorage.removeItem('token');
                delete api.defaults.headers.common['Authorization'];
            }
        } finally {
            setLoading(false);
        }
    };

    const login = async (email: string, password: string) => {
        try {
            console.log('AuthProvider: Logging in...');
            const response = await api.post<LoginResponse>('/api/v1/auth/login', { email, password });
            const { access_token } = response.data;
            console.log('AuthProvider: Login successful, token received');

            localStorage.setItem('token', access_token);
            api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

            // Fetch user details
            const userResponse = await api.get('/api/v1/auth/me');
            setUser(userResponse.data as User);
            console.log('AuthProvider: User data set after login');
        } catch (error: any) {
            console.error('AuthProvider: Login failed:', error);
            throw error;
        }
    };

    const register = async (email: string, password: string, business_name?: string, tax_id?: string) => {
        try {
            console.log('AuthProvider: Registering...');
            const response = await api.post<RegisterResponse>('/api/v1/auth/register', {
                email,
                password,
                business_name,
                tax_id
            });
            const { access_token } = response.data;
            console.log('AuthProvider: Registration successful, token received');

            localStorage.setItem('token', access_token);
            api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

            // Fetch user details
            const userResponse = await api.get('/api/v1/auth/me');
            setUser(userResponse.data as User);
            console.log('AuthProvider: User data set after registration');
        } catch (error: any) {
            console.error('AuthProvider: Registration failed:', error);
            throw error;
        }
    };

    const logout = () => {
        console.log('AuthProvider: Logging out...');
        localStorage.removeItem('token');
        delete api.defaults.headers.common['Authorization'];
        setUser(null);
    };

    const value: AuthContextType = {
        user,
        isAuthenticated: !!user,
        login,
        register,
        logout,
        loading
    };

    console.log('AuthProvider: Current state - user:', !!user, 'loading:', loading, 'isAuthenticated:', !!user);

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}; 