import React from 'react';
import { Outlet, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
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

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Sidebar */}
            <div className="fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg">
                <div className="flex h-full flex-col">
                    {/* Logo */}
                    <div className="flex h-16 items-center justify-center border-b border-gray-200">
                        <h1 className="text-xl font-bold text-gray-900">
                            Transaction Classifier
                        </h1>
                    </div>

                    {/* Navigation */}
                    <nav className="flex-1 space-y-1 px-4 py-4">
                        {navigation.map((item) => {
                            const isActive = location.pathname === item.href;
                            return (
                                <a
                                    key={item.name}
                                    href={item.href}
                                    className={`group flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors ${isActive
                                            ? 'bg-primary-100 text-primary-700'
                                            : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                                        }`}
                                >
                                    <item.icon
                                        className={`mr-3 h-5 w-5 flex-shrink-0 ${isActive ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500'
                                            }`}
                                    />
                                    {item.name}
                                </a>
                            );
                        })}
                    </nav>

                    {/* User section */}
                    <div className="border-t border-gray-200 p-4">
                        <div className="flex items-center">
                            <UserCircleIcon className="h-8 w-8 text-gray-400" />
                            <div className="ml-3 flex-1">
                                <p className="text-sm font-medium text-gray-900">{user?.email}</p>
                                <p className="text-xs text-gray-500">
                                    {user?.business_name || 'Freelancer'}
                                </p>
                            </div>
                        </div>
                        <button
                            onClick={handleLogout}
                            className="mt-3 flex w-full items-center rounded-md px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                        >
                            <ArrowRightOnRectangleIcon className="mr-3 h-5 w-5" />
                            Logout
                        </button>
                    </div>
                </div>
            </div>

            {/* Main content */}
            <div className="pl-64">
                <main className="py-6">
                    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                        <Outlet />
                    </div>
                </main>
            </div>
        </div>
    );
};

export default Layout; 