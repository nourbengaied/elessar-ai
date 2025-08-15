import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Transaction, TransactionsResponse } from '../types/api';
import toast from 'react-hot-toast';
import {
    TrashIcon,
    FunnelIcon,
} from '@heroicons/react/24/outline';

const Transactions: React.FC = () => {
    const [transactions, setTransactions] = useState<Transaction[]>([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState<'all' | 'business' | 'personal'>('all');
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        fetchTransactions();
    }, []);

    const fetchTransactions = async () => {
        try {
            const response = await api.get<TransactionsResponse>('/api/v1/transactions/');
            setTransactions(response.data.transactions);
        } catch (error) {
            toast.error('Failed to fetch transactions');
        } finally {
            setLoading(false);
        }
    };

    const handleClassificationChange = async (transactionId: string, isBusiness: boolean) => {
        try {
            await api.put(`/api/v1/transactions/${transactionId}`, {
                is_business: isBusiness,
            });

            setTransactions(prev =>
                prev.map(t =>
                    t.id === transactionId ? { ...t, is_business_expense: isBusiness } : t
                )
            );

            toast.success('Classification updated successfully');
        } catch (error) {
            toast.error('Failed to update classification');
        }
    };

    const handleDeleteTransaction = async (transactionId: string) => {
        if (!window.confirm('Are you sure you want to delete this transaction?')) {
            return;
        }

        try {
            await api.delete(`/api/v1/transactions/${transactionId}`);
            setTransactions(prev => prev.filter(t => t.id !== transactionId));
            toast.success('Transaction deleted successfully');
        } catch (error) {
            toast.error('Failed to delete transaction');
        }
    };

    const handleClearAllTransactions = async () => {
        if (!window.confirm('Are you sure you want to clear ALL transactions? This action cannot be undone.')) {
            return;
        }

        try {
            const response = await api.delete<{message: string; deleted_count: number}>('/api/v1/transactions/');
            setTransactions([]);
            toast.success(`Successfully cleared ${response.data.deleted_count} transactions`);
        } catch (error) {
            toast.error('Failed to clear transactions');
        }
    };

    const filteredTransactions = transactions.filter(transaction => {
        const matchesFilter = filter === 'all' ||
            (filter === 'business' && transaction.is_business_expense) ||
            (filter === 'personal' && !transaction.is_business_expense);

        const matchesSearch = transaction.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
            transaction.category?.toLowerCase().includes(searchTerm.toLowerCase());

        return matchesFilter && matchesSearch;
    });

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
            <div className="flex justify-between items-start">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">Transactions</h1>
                    <p className="mt-1 text-sm text-gray-500">
                        View and manage your transaction classifications
                    </p>
                </div>
                
                {transactions.length > 0 && (
                    <button
                        onClick={handleClearAllTransactions}
                        className="inline-flex items-center px-4 py-2 border border-red-300 rounded-md shadow-sm text-sm font-medium text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors"
                    >
                        <TrashIcon className="h-4 w-4 mr-2" />
                        Clear All
                    </button>
                )}
            </div>

            {/* Filters */}
            <div className="bg-white shadow rounded-lg p-6">
                <div className="flex flex-col sm:flex-row gap-4">
                    <div className="flex-1">
                        <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
                            Search
                        </label>
                        <input
                            type="text"
                            id="search"
                            placeholder="Search transactions..."
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>

                    <div>
                        <label htmlFor="filter" className="block text-sm font-medium text-gray-700 mb-1">
                            Filter
                        </label>
                        <select
                            id="filter"
                            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                            value={filter}
                            onChange={(e) => setFilter(e.target.value as 'all' | 'business' | 'personal')}
                        >
                            <option value="all">All Transactions</option>
                            <option value="business">Business Only</option>
                            <option value="personal">Personal Only</option>
                        </select>
                    </div>
                </div>
            </div>

            {/* Transactions Table */}
            <div className="bg-white shadow rounded-lg overflow-hidden">
                <div className="px-6 py-4 border-b border-gray-200">
                    <h3 className="text-lg font-medium text-gray-900">
                        {filteredTransactions.length} transactions found
                    </h3>
                </div>

                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Date
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Description
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Amount
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Category
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Classification
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Confidence
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Actions
                                </th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {filteredTransactions.map((transaction) => (
                                <tr key={transaction.id} className="hover:bg-gray-50">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                        {new Date(transaction.date).toLocaleDateString()}
                                    </td>
                                    <td className="px-6 py-4 text-sm text-gray-900">
                                        {transaction.description}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                        <span className={transaction.amount >= 0 ? 'text-success-600' : 'text-danger-600'}>
                                            ${Math.abs(transaction.amount).toFixed(2)}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                        {transaction.category || '-'}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <select
                                            className={`text-xs font-semibold rounded-full px-2 py-1 border ${transaction.is_business_expense
                                                    ? 'bg-success-100 text-success-800 border-success-200'
                                                    : 'bg-gray-100 text-gray-800 border-gray-200'
                                                }`}
                                            value={transaction.is_business_expense ? 'business' : 'personal'}
                                            onChange={(e) => handleClassificationChange(transaction.id, e.target.value === 'business')}
                                        >
                                            <option value="business">Business</option>
                                            <option value="personal">Personal</option>
                                        </select>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                        {transaction.confidence_score ? (
                                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${transaction.confidence_score > 0.8
                                                    ? 'bg-success-100 text-success-800'
                                                    : transaction.confidence_score > 0.6
                                                        ? 'bg-warning-100 text-warning-800'
                                                        : 'bg-danger-100 text-danger-800'
                                                }`}>
                                                {(transaction.confidence_score * 100).toFixed(0)}%
                                            </span>
                                        ) : (
                                            '-'
                                        )}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                        <div className="flex space-x-2">
                                            <button
                                                onClick={() => handleDeleteTransaction(transaction.id)}
                                                className="text-danger-600 hover:text-danger-900"
                                                title="Delete transaction"
                                            >
                                                <TrashIcon className="h-4 w-4" />
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {filteredTransactions.length === 0 && (
                    <div className="text-center py-12">
                        <FunnelIcon className="mx-auto h-12 w-12 text-gray-400" />
                        <h3 className="mt-2 text-sm font-medium text-gray-900">No transactions found</h3>
                        <p className="mt-1 text-sm text-gray-500">
                            Try adjusting your search or filter criteria.
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Transactions; 