import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';
import { Statistics } from '../types/api';
import {
    BanknotesIcon,
    ChartBarIcon,
    DocumentTextIcon,
    CloudArrowUpIcon,
} from '@heroicons/react/24/outline';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const Dashboard: React.FC = () => {
    const { user } = useAuth();
    const [statistics, setStatistics] = useState<Statistics | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchStatistics();
    }, []);

    const fetchStatistics = async () => {
        try {
            const response = await api.get<Statistics>('/api/v1/transactions/statistics/summary');
            setStatistics(response.data);
        } catch (error) {
            console.error('Failed to fetch statistics:', error);
        } finally {
            setLoading(false);
        }
    };

    const pieData = statistics ? [
        { name: 'Business', value: statistics.business_transactions, color: '#3b82f6' },
        { name: 'Personal', value: statistics.personal_transactions, color: '#ef4444' },
    ] : [];

    const COLORS = ['#3b82f6', '#ef4444'];

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
                <p className="mt-1 text-sm text-gray-500">
                    Welcome back, {user?.business_name || user?.email}
                </p>
            </div>

            {/* Statistics Cards */}
            <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
                <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="p-5">
                        <div className="flex items-center">
                            <div className="flex-shrink-0">
                                <DocumentTextIcon className="h-6 w-6 text-gray-400" />
                            </div>
                            <div className="ml-5 w-0 flex-1">
                                <dl>
                                    <dt className="text-sm font-medium text-gray-500 truncate">
                                        Total Transactions
                                    </dt>
                                    <dd className="text-lg font-medium text-gray-900">
                                        {statistics?.total_transactions || 0}
                                    </dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="p-5">
                        <div className="flex items-center">
                            <div className="flex-shrink-0">
                                <BanknotesIcon className="h-6 w-6 text-primary-400" />
                            </div>
                            <div className="ml-5 w-0 flex-1">
                                <dl>
                                    <dt className="text-sm font-medium text-gray-500 truncate">
                                        Business Transactions
                                    </dt>
                                    <dd className="text-lg font-medium text-gray-900">
                                        {statistics?.business_transactions || 0}
                                    </dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="p-5">
                        <div className="flex items-center">
                            <div className="flex-shrink-0">
                                <ChartBarIcon className="h-6 w-6 text-success-400" />
                            </div>
                            <div className="ml-5 w-0 flex-1">
                                <dl>
                                    <dt className="text-sm font-medium text-gray-500 truncate">
                                        Total Amount
                                    </dt>
                                    <dd className="text-lg font-medium text-gray-900">
                                        ${statistics?.total_amount?.toFixed(2) || '0.00'}
                                    </dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="p-5">
                        <div className="flex items-center">
                            <div className="flex-shrink-0">
                                <CloudArrowUpIcon className="h-6 w-6 text-warning-400" />
                            </div>
                            <div className="ml-5 w-0 flex-1">
                                <dl>
                                    <dt className="text-sm font-medium text-gray-500 truncate">
                                        Business Amount
                                    </dt>
                                    <dd className="text-lg font-medium text-gray-900">
                                        ${statistics?.business_amount?.toFixed(2) || '0.00'}
                                    </dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Pie Chart */}
                <div className="bg-white shadow rounded-lg p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">
                        Transaction Distribution
                    </h3>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={pieData}
                                    cx="50%"
                                    cy="50%"
                                    labelLine={false}
                                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                                    outerRadius={80}
                                    fill="#8884d8"
                                    dataKey="value"
                                >
                                    {pieData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Bar Chart */}
                <div className="bg-white shadow rounded-lg p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">
                        Monthly Breakdown
                    </h3>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={statistics?.monthly_breakdown || []}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="month" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="business" fill="#3b82f6" />
                                <Bar dataKey="personal" fill="#ef4444" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white shadow rounded-lg p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <a
                        href="/upload"
                        className="relative rounded-lg border border-gray-300 bg-white px-6 py-5 shadow-sm flex items-center space-x-3 hover:border-gray-400 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500"
                    >
                        <div className="flex-shrink-0">
                            <CloudArrowUpIcon className="h-6 w-6 text-primary-600" />
                        </div>
                        <div className="flex-1 min-w-0">
                            <span className="absolute inset-0" aria-hidden="true" />
                            <p className="text-sm font-medium text-gray-900">Upload Transactions</p>
                            <p className="text-sm text-gray-500">Import CSV file</p>
                        </div>
                    </a>

                    <a
                        href="/transactions"
                        className="relative rounded-lg border border-gray-300 bg-white px-6 py-5 shadow-sm flex items-center space-x-3 hover:border-gray-400 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500"
                    >
                        <div className="flex-shrink-0">
                            <DocumentTextIcon className="h-6 w-6 text-primary-600" />
                        </div>
                        <div className="flex-1 min-w-0">
                            <span className="absolute inset-0" aria-hidden="true" />
                            <p className="text-sm font-medium text-gray-900">View Transactions</p>
                            <p className="text-sm text-gray-500">Browse all transactions</p>
                        </div>
                    </a>

                    <a
                        href="/reports"
                        className="relative rounded-lg border border-gray-300 bg-white px-6 py-5 shadow-sm flex items-center space-x-3 hover:border-gray-400 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500"
                    >
                        <div className="flex-shrink-0">
                            <ChartBarIcon className="h-6 w-6 text-primary-600" />
                        </div>
                        <div className="flex-1 min-w-0">
                            <span className="absolute inset-0" aria-hidden="true" />
                            <p className="text-sm font-medium text-gray-900">Generate Reports</p>
                            <p className="text-sm text-gray-500">Export data</p>
                        </div>
                    </a>
                </div>
            </div>
        </div>
    );
};

export default Dashboard; 