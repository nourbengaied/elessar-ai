import React from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Dashboard from '../pages/Dashboard';
import Transactions from '../pages/Transactions';
import Upload from '../pages/Upload';
import Reports from '../pages/Reports';
import Logo from './Logo';
import {
    HomeIcon,
    DocumentTextIcon,
    CloudArrowUpIcon,
    ChartBarIcon,
    UserCircleIcon,
    ArrowRightOnRectangleIcon,
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

const Layout: React.FC = () => {
    const { user, logout } = useAuth();
    const location = useLocation();
    const navigate = useNavigate();

    const navigation = [
        { name: 'Dashboard', href: '/', icon: HomeIcon },
        { name: 'Transactions', href: '/transactions', icon: DocumentTextIcon },
        { name: 'Upload', href: '/upload', icon: CloudArrowUpIcon },
        { name: 'Reports', href: '/reports', icon: ChartBarIcon },
    ];

    const handleLogout = () => {
        logout();
        toast.success('Logged out successfully');
        navigate('/login');
    };

    const renderContent = () => {
        switch (location.pathname) {
            case '/':
                return <Dashboard />;
            case '/transactions':
                return <Transactions />;
            case '/upload':
                return <Upload />;
            case '/reports':
                return <Reports />;
            default:
                return <Dashboard />;
        }
    };

    return (
        <div className="min-h-screen bg-sand-400">
            {/* Floating Top Navigation */}
            <div className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50">
                <div className="bg-white/90 backdrop-blur-sm shadow-lg rounded-full px-6 py-3 border border-sand-200">
                    <div className="flex items-center space-x-8">
                        {/* Logo */}
                        <Logo size={36} />

                        {/* Navigation */}
                        <nav className="flex items-center space-x-1">
                            {navigation.map((item) => {
                                const isActive = location.pathname === item.href;
                                return (
                                    <Link
                                        key={item.name}
                                        to={item.href}
                                        className={`group flex items-center rounded-full px-4 py-2 text-sm font-medium transition-colors tracking-tight font-neo ${isActive
                                                ? 'bg-brand-100 text-brand-700'
                                                : 'text-gray-600 hover:bg-sand-50 hover:text-gray-900'
                                            }`}
                                    >
                                        <item.icon
                                            className={`mr-2 h-4 w-4 flex-shrink-0 ${isActive ? 'text-brand-500' : 'text-gray-400 group-hover:text-gray-500'
                                                }`}
                                        />
                                        {item.name}
                                    </Link>
                                );
                            })}
                        </nav>

                        {/* User section */}
                        <div className="flex items-center space-x-3">
                            <div className="flex items-center">
                                <UserCircleIcon className="h-6 w-6 text-gray-400" />
                                <div className="ml-2">
                                    <p className="text-sm font-medium text-gray-900 tracking-tight font-neo">{user?.email}</p>
                                    <p className="text-xs text-zinc-500 tracking-tight font-neo">
                                        {user?.business_name || 'Freelancer'}
                                    </p>
                                </div>
                            </div>
                            <button
                                onClick={handleLogout}
                                className="flex items-center rounded-full px-3 py-2 text-sm font-medium text-gray-600 hover:bg-sand-50 hover:text-gray-900 tracking-tight font-neo"
                            >
                                <ArrowRightOnRectangleIcon className="mr-2 h-4 w-4" />
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* Main content */}
            <div className="pt-20">
                <main className="py-6">
                    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                        {renderContent()}
                    </div>
                </main>
            </div>
        </div>
    );
};

export default Layout; 