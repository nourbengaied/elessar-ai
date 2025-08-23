import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';
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
    XMarkIcon,
    PencilIcon,
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

const Layout: React.FC = () => {
    const { user, logout, updateUser } = useAuth();
    const location = useLocation();
    const navigate = useNavigate();
    const [scrollY, setScrollY] = useState(0);
    const [showProfileModal, setShowProfileModal] = useState(false);
    const [hoveredNav, setHoveredNav] = useState<string | null>(null);
    const [backgroundPosition, setBackgroundPosition] = useState({ left: 0, width: 0 });
    const navRefs = useRef<{ [key: string]: HTMLAnchorElement | null }>({});
    const [profileForm, setProfileForm] = useState({
        firstName: user?.first_name || '',
        lastName: user?.last_name || '',
        email: user?.email || '',
        businessName: user?.business_name || '',
        taxId: user?.tax_id || '',
    });

    const navigation = [
        { name: 'Dashboard', href: '/', icon: HomeIcon },
        { name: 'Transactions', href: '/transactions', icon: DocumentTextIcon },
        { name: 'Upload', href: '/upload', icon: CloudArrowUpIcon },
        { name: 'Reports', href: '/reports', icon: ChartBarIcon },
    ];

    useEffect(() => {
        const handleScroll = () => {
            setScrollY(window.scrollY);
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    // Update profile form when user data changes
    useEffect(() => {
        if (user) {
            setProfileForm({
                firstName: user.first_name || '',
                lastName: user.last_name || '',
                email: user.email || '',
                businessName: user.business_name || '',
                taxId: user.tax_id || '',
            });
        }
    }, [user]);

    const handleLogout = () => {
        logout();
        toast.success('Logged out successfully');
        navigate('/login');
    };

    const handleProfileUpdate = async () => {
        try {
            // Convert empty strings to null for proper backend handling
            const updateData = {
                first_name: profileForm.firstName.trim() || null,
                last_name: profileForm.lastName.trim() || null,
                email: profileForm.email.trim() || null,
                business_name: profileForm.businessName.trim() || null,
                tax_id: profileForm.taxId.trim() || null,
            };
            
            console.log('Sending profile update data:', updateData);
            
            await api.put('/auth/profile', updateData);
            toast.success('Profile updated successfully');
            setShowProfileModal(false);
            updateUser(); // Refresh user data after successful update
        } catch (error) {
            console.error('Profile update error:', error);
            toast.error('Failed to update profile');
        }
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

    // Calculate opacity based on scroll position
    const logoOpacity = Math.max(0, 1 - scrollY / 200); // Fade out over 200px of scroll

    return (
        <div className="min-h-screen bg-sand-400">
            {/* Logo - positioned at same level as menu */}
            <div 
                className="fixed top-5 left-4 z-50 transition-opacity duration-300"
                style={{ opacity: logoOpacity }}
            >
                <Logo size={64} variant="minimal" />
            </div>

            {/* Floating Top Navigation */}
            <div className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50">
                <div className="bg-white/95 shadow-lg rounded-full px-3 py-1.5 border border-sand-200">
                    <div className="flex items-center space-x-4">
                        {/* Parsea Brand */}
                        <div className="flex items-center">
                            <span className="font-inter font-semibold tracking-tight text-2xl leading-none text-[#0C1D16]">
                                Par<span className="bg-gradient-to-r from-[#EC4899] to-[#3B82F6] bg-clip-text text-transparent">sea</span>
                            </span>
                        </div>

                        {/* Navigation */}
                        <nav className="flex items-center space-x-1 relative">
                            {navigation.map((item) => {
                                const isActive = location.pathname === item.href;
                                return (
                                    <Link
                                        key={item.name}
                                        to={item.href}
                                        ref={(el) => navRefs.current[item.href] = el}
                                        onMouseEnter={() => {
                                            setHoveredNav(item.href);
                                            const element = navRefs.current[item.href];
                                            if (element) {
                                                const rect = element.getBoundingClientRect();
                                                const navRect = element.parentElement?.getBoundingClientRect();
                                                if (navRect) {
                                                    setBackgroundPosition({
                                                        left: rect.left - navRect.left,
                                                        width: rect.width
                                                    });
                                                }
                                            }
                                        }}
                                        onMouseLeave={() => setHoveredNav(null)}
                                        className={`group flex items-center rounded-full px-2.5 py-1 text-lg font-medium transition-all duration-300 tracking-tight font-neo relative z-10 ${
                                            isActive
                                                ? 'text-black'
                                                : 'text-gray-700 hover:text-gray-900'
                                        }`}
                                    >
                                        <item.icon
                                            className={`mr-1.5 h-4 w-4 flex-shrink-0 transition-colors duration-300 ${
                                                isActive ? 'text-black' : 'text-gray-600 group-hover:text-gray-700'
                                            }`}
                                        />
                                        {item.name}
                                    </Link>
                                );
                            })}
                            {/* Moving background pill */}
                            <div className={`absolute bg-brand-100 rounded-full pointer-events-none z-0 ${
                                hoveredNav ? 'opacity-100' : 'opacity-0'
                            } transition-opacity duration-200`}
                                 style={{
                                     left: `${backgroundPosition.left}px`,
                                     width: `${backgroundPosition.width}px`,
                                     height: '40px'
                                 }}>
                            </div>
                        </nav>

                        {/* User section */}
                        <div className="flex items-center space-x-2">
                            <button
                                onClick={() => setShowProfileModal(true)}
                                className="flex items-center hover:bg-sand-50 rounded-full px-2 py-1 transition-colors cursor-pointer"
                            >
                                <UserCircleIcon className="h-6 w-6 text-gray-400" />
                                <div className="ml-2 text-left">
                                    <p className="text-lg font-medium text-gray-900 tracking-tight font-neo">
                                        {user?.first_name || user?.email}
                                    </p>
                                </div>
                            </button>
                            <button
                                onClick={handleLogout}
                                className="flex items-center rounded-full px-2.5 py-1 text-lg font-medium text-gray-600 hover:bg-sand-50 hover:text-gray-900 tracking-tight font-neo"
                            >
                                <ArrowRightOnRectangleIcon className="mr-1.5 h-4 w-4" />
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* Profile Modal */}
            {showProfileModal && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
                        <div className="flex items-center justify-between p-6 border-b border-gray-200">
                            <h2 className="text-xl font-semibold text-gray-900">Edit Profile</h2>
                            <button
                                onClick={() => setShowProfileModal(false)}
                                className="text-gray-400 hover:text-gray-600 transition-colors"
                            >
                                <XMarkIcon className="h-6 w-6" />
                            </button>
                        </div>
                        
                        <div className="p-6 space-y-4">
                            <div>
                                <label htmlFor="firstName" className="block text-sm font-medium text-gray-700 mb-1">
                                    First Name
                                </label>
                                <input
                                    type="text"
                                    id="firstName"
                                    value={profileForm.firstName}
                                    onChange={(e) => setProfileForm(prev => ({ ...prev, firstName: e.target.value }))}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                                />
                            </div>
                            
                            <div>
                                <label htmlFor="lastName" className="block text-sm font-medium text-gray-700 mb-1">
                                    Last Name
                                </label>
                                <input
                                    type="text"
                                    id="lastName"
                                    value={profileForm.lastName}
                                    onChange={(e) => setProfileForm(prev => ({ ...prev, lastName: e.target.value }))}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                                />
                            </div>
                            
                            <div>
                                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                                    Email
                                </label>
                                <input
                                    type="email"
                                    id="email"
                                    value={profileForm.email}
                                    onChange={(e) => setProfileForm(prev => ({ ...prev, email: e.target.value }))}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                                />
                            </div>
                            
                            <div>
                                <label htmlFor="businessName" className="block text-sm font-medium text-gray-700 mb-1">
                                    Business Name
                                </label>
                                <input
                                    type="text"
                                    id="businessName"
                                    value={profileForm.businessName}
                                    onChange={(e) => setProfileForm(prev => ({ ...prev, businessName: e.target.value }))}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                                />
                            </div>
                            
                            <div>
                                <label htmlFor="taxId" className="block text-sm font-medium text-gray-700 mb-1">
                                    Tax ID (Optional)
                                </label>
                                <input
                                    type="text"
                                    id="taxId"
                                    value={profileForm.taxId}
                                    onChange={(e) => setProfileForm(prev => ({ ...prev, taxId: e.target.value }))}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                                    placeholder="EIN or SSN"
                                />
                            </div>
                        </div>
                        
                        <div className="flex items-center justify-end space-x-3 p-6 border-t border-gray-200">
                            <button
                                onClick={() => setShowProfileModal(false)}
                                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleProfileUpdate}
                                className="px-4 py-2 text-sm font-medium text-white bg-brand-600 hover:bg-brand-700 rounded-md transition-colors"
                            >
                                Save Changes
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Main content */}
            <div className="pt-20">
                <main>
                    {renderContent()}
                </main>
            </div>
        </div>
    );
};

export default Layout; 