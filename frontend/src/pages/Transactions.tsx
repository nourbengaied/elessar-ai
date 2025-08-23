import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Transaction, TransactionsResponse } from '../types/api';
import toast from 'react-hot-toast';
import {
    TrashIcon,
    FunnelIcon,
    ChevronDownIcon,
    PencilIcon,
    XMarkIcon,
    CheckIcon,
} from '@heroicons/react/24/outline';

const Transactions: React.FC = () => {
    const [transactions, setTransactions] = useState<Transaction[]>([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState<'all' | 'business' | 'personal'>('all');
    const [searchTerm, setSearchTerm] = useState('');
    const [openDropdown, setOpenDropdown] = useState<string | null>(null);
    const [editingTransaction, setEditingTransaction] = useState<string | null>(null);
    const [editForm, setEditForm] = useState({
        description: '',
        amount: '',
        category: '',
        date: '',
    });

    useEffect(() => {
        fetchTransactions();
    }, []);

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = () => {
            setOpenDropdown(null);
        };

        document.addEventListener('click', handleClickOutside);
        return () => document.removeEventListener('click', handleClickOutside);
    }, []);

    const fetchTransactions = async () => {
        try {
            const response = await api.get<TransactionsResponse>('/transactions/');
            setTransactions(response.data.transactions);
        } catch (error) {
            toast.error('Failed to fetch transactions');
        } finally {
            setLoading(false);
        }
    };

    const handleClassificationChange = async (transactionId: string, isBusiness: boolean) => {
        try {
            await api.put(`/transactions/${transactionId}`, {
                is_business: isBusiness,
            });

            setTransactions(prev =>
                prev.map(t =>
                    t.id === transactionId ? { ...t, is_business_expense: isBusiness } : t
                )
            );

            toast.success('Classification updated successfully');
            setOpenDropdown(null);
        } catch (error) {
            toast.error('Failed to update classification');
        }
    };

    const handleDeleteTransaction = async (transactionId: string) => {
        if (!window.confirm('Are you sure you want to delete this transaction?')) {
            return;
        }

        try {
            await api.delete(`/transactions/${transactionId}`);
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
            const response = await api.delete<{message: string; deleted_count: number}>('/transactions/');
            setTransactions([]);
            toast.success(`Successfully cleared ${response.data.deleted_count} transactions`);
        } catch (error) {
            toast.error('Failed to clear transactions');
        }
    };

    const toggleDropdown = (transactionId: string, event: React.MouseEvent) => {
        event.stopPropagation();
        setOpenDropdown(openDropdown === transactionId ? null : transactionId);
    };

    const startEditing = (transaction: Transaction) => {
        setEditingTransaction(transaction.id);
        setEditForm({
            description: transaction.description,
            amount: Math.abs(transaction.amount).toString(),
            category: transaction.category || '',
            date: transaction.date.split('T')[0], // Convert ISO date to YYYY-MM-DD
        });
    };

    const cancelEditing = () => {
        setEditingTransaction(null);
        setEditForm({
            description: '',
            amount: '',
            category: '',
            date: '',
        });
    };

    const saveEdit = async (transactionId: string) => {
        const transaction = transactions.find(t => t.id === transactionId);
        if (!transaction) return;

        try {
            const updatedData = {
                description: editForm.description,
                amount: transaction.amount >= 0 ? parseFloat(editForm.amount) : -parseFloat(editForm.amount),
                category: editForm.category || undefined,
                date: editForm.date,
            };

            await api.put(`/transactions/${transactionId}/details`, updatedData);

            setTransactions(prev =>
                prev.map(t =>
                    t.id === transactionId ? { ...t, ...updatedData } : t
                )
            );

            toast.success('Transaction updated successfully');
            setEditingTransaction(null);
            setEditForm({
                description: '',
                amount: '',
                category: '',
                date: '',
            });
        } catch (error) {
            toast.error('Failed to update transaction');
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
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 pb-8">
            <div className="space-y-6">
                {/* Header */}
                <div className="flex justify-between items-start">
                    <div>
                        <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Transactions</h1>
                        <p className="mt-1 text-base text-zinc-500 tracking-tight">
                            View and manage your transaction data
                        </p>
                    </div>
                </div>

                {/* Filters and Search */}
                <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
                    <div className="flex flex-wrap gap-2">
                        <button
                            onClick={() => setFilter('all')}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                                filter === 'all'
                                    ? 'bg-brand-100 text-brand-700'
                                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                            }`}
                        >
                            All ({transactions.length})
                        </button>
                        <button
                            onClick={() => setFilter('business')}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                                filter === 'business'
                                    ? 'bg-brand-100 text-brand-700'
                                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                            }`}
                        >
                            Business ({transactions.filter(t => t.is_business_expense).length})
                        </button>
                        <button
                            onClick={() => setFilter('personal')}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                                filter === 'personal'
                                    ? 'bg-brand-100 text-brand-700'
                                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                            }`}
                        >
                            Personal ({transactions.filter(t => !t.is_business_expense).length})
                        </button>
                    </div>

                    <div className="flex gap-2">
                        <input
                            type="text"
                            placeholder="Search transactions..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                        />
                        <button
                            onClick={handleClearAllTransactions}
                            className="px-4 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors flex items-center gap-2"
                        >
                            <TrashIcon className="h-4 w-4" />
                            Clear All
                        </button>
                    </div>
                </div>

                {/* Transactions List */}
                <div className="bg-white rounded-lg shadow">
                    {filteredTransactions.length === 0 ? (
                        <div className="p-8 text-center">
                            <p className="text-gray-500">No transactions found.</p>
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="min-w-full divide-y divide-gray-200">
                                <thead className="bg-gray-50">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Description
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Amount
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Date
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Category
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Type
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {filteredTransactions.map((transaction) => (
                                        <tr key={transaction.id} className="hover:bg-gray-50">
                                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                                <div className="flex items-center justify-between">
                                                    <span>{editingTransaction === transaction.id ? (
                                                        <input
                                                            type="text"
                                                            value={editForm.description}
                                                            onChange={(e) => setEditForm(prev => ({ ...prev, description: e.target.value }))}
                                                            className="w-full px-2 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-brand-500 focus:border-transparent text-sm"
                                                        />
                                                    ) : (
                                                        transaction.description
                                                    )}</span>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                                {editingTransaction === transaction.id ? (
                                                    <input
                                                        type="number"
                                                        step="0.01"
                                                        value={editForm.amount}
                                                        onChange={(e) => setEditForm(prev => ({ ...prev, amount: e.target.value }))}
                                                        className="w-24 px-2 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-brand-500 focus:border-transparent text-sm"
                                                    />
                                                ) : (
                                                    <span className={transaction.amount >= 0 ? 'text-green-600' : 'text-red-600'}>
                                                        {transaction.amount >= 0 ? '+' : ''}${Math.abs(transaction.amount).toFixed(2)}
                                                    </span>
                                                )}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {editingTransaction === transaction.id ? (
                                                    <input
                                                        type="date"
                                                        value={editForm.date}
                                                        onChange={(e) => setEditForm(prev => ({ ...prev, date: e.target.value }))}
                                                        className="px-2 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-brand-500 focus:border-transparent text-sm"
                                                    />
                                                ) : (
                                                    new Date(transaction.date).toLocaleDateString()
                                                )}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {editingTransaction === transaction.id ? (
                                                    <input
                                                        type="text"
                                                        value={editForm.category}
                                                        onChange={(e) => setEditForm(prev => ({ ...prev, category: e.target.value }))}
                                                        className="w-full px-2 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-brand-500 focus:border-transparent text-sm"
                                                    />
                                                ) : (
                                                    transaction.category || 'Uncategorized'
                                                )}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <div className="flex items-center justify-between">
                                                    <div className="relative">
                                                        <button
                                                            onClick={(e) => toggleDropdown(transaction.id, e)}
                                                            className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                                                                transaction.is_business_expense
                                                                    ? 'bg-brand-100 text-brand-800 hover:bg-brand-200'
                                                                    : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                                                            }`}
                                                        >
                                                            {transaction.is_business_expense ? 'Business' : 'Personal'}
                                                            <ChevronDownIcon className="ml-1 h-3 w-3" />
                                                        </button>
                                                        
                                                        {openDropdown === transaction.id && (
                                                            <div className="absolute right-0 mt-1 w-32 bg-white rounded-md shadow-lg border border-gray-200 z-10">
                                                                <div className="py-1">
                                                                    <button
                                                                        onClick={() => handleClassificationChange(transaction.id, true)}
                                                                        className={`block w-full text-left px-4 py-2 text-sm ${
                                                                            transaction.is_business_expense
                                                                                ? 'bg-brand-50 text-brand-700'
                                                                                : 'text-gray-700 hover:bg-gray-50'
                                                                        }`}
                                                                    >
                                                                        Business
                                                                    </button>
                                                                    <button
                                                                        onClick={() => handleClassificationChange(transaction.id, false)}
                                                                        className={`block w-full text-left px-4 py-2 text-sm ${
                                                                            !transaction.is_business_expense
                                                                                ? 'bg-gray-50 text-gray-700'
                                                                                : 'text-gray-700 hover:bg-gray-50'
                                                                        }`}
                                                                    >
                                                                        Personal
                                                                    </button>
                                                                </div>
                                                            </div>
                                                        )}
                                                    </div>
                                                    {editingTransaction === transaction.id ? (
                                                        <div className="flex gap-2 ml-2">
                                                            <button
                                                                onClick={() => saveEdit(transaction.id)}
                                                                className="text-green-600 hover:text-green-900 p-2 rounded-lg hover:bg-green-100 transition-all duration-200 hover:scale-125 hover:shadow-sm"
                                                                title="Save changes"
                                                            >
                                                                <CheckIcon className="h-4 w-4" />
                                                            </button>
                                                            <button
                                                                onClick={cancelEditing}
                                                                className="text-gray-600 hover:text-gray-900 p-2 rounded-lg hover:bg-gray-100 transition-all duration-200 hover:scale-125 hover:shadow-sm"
                                                                title="Cancel editing"
                                                            >
                                                                <XMarkIcon className="h-4 w-4" />
                                                            </button>
                                                            <button
                                                                onClick={() => handleDeleteTransaction(transaction.id)}
                                                                className="text-red-600 hover:text-red-900 p-2 rounded-lg hover:bg-red-100 transition-all duration-200 hover:scale-125 hover:shadow-sm"
                                                                title="Delete transaction"
                                                            >
                                                                <TrashIcon className="h-4 w-4" />
                                                            </button>
                                                        </div>
                                                    ) : (
                                                        <button
                                                            onClick={() => startEditing(transaction)}
                                                            className="text-brand-600 hover:text-brand-900 p-2 rounded-lg hover:bg-brand-100 transition-all duration-200 hover:scale-125 hover:shadow-sm ml-2"
                                                            title="Edit transaction"
                                                        >
                                                            <PencilIcon className="h-4 w-4" />
                                                        </button>
                                                    )}
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Transactions; 