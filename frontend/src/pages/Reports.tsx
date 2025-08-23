import React, { useState } from 'react';
import { api } from '../services/api';
import toast from 'react-hot-toast';
import {
    DocumentArrowDownIcon,
    ChartBarIcon,
    BanknotesIcon,
} from '@heroicons/react/24/outline';

const Reports: React.FC = () => {
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [taxYear, setTaxYear] = useState(new Date().getFullYear().toString());
    const [loading, setLoading] = useState(false);

    const handleExport = async (type: 'transactions' | 'business-expenses' | 'tax-report') => {
        setLoading(true);

        try {
            let url = '';
            let filename = '';

            switch (type) {
                case 'transactions':
                    url = `/export/transactions/csv`;
                    filename = `transactions_${startDate || 'all'}_${endDate || 'all'}.csv`;
                    break;
                case 'business-expenses':
                    url = `/export/business-expenses/csv`;
                    filename = `business_expenses_${startDate || 'all'}_${endDate || 'all'}.csv`;
                    break;
                case 'tax-report':
                    url = `/export/tax-report/csv?tax_year=${taxYear}`;
                    filename = `tax_report_${taxYear}.csv`;
                    break;
            }

            const response = await api.get(url, {
                params: {
                    start_date: startDate || undefined,
                    end_date: endDate || undefined,
                },
                responseType: 'blob',
            });

            // Create download link
            const blob = new Blob([response.data as BlobPart], { type: 'text/csv' });
            const url2 = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url2;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url2);

            toast.success(`${filename} downloaded successfully`);
        } catch (error) {
            toast.error('Failed to export report');
        } finally {
            setLoading(false);
        }
    };

    const reportTypes = [
        {
            id: 'transactions',
            title: 'All Transactions',
            description: 'Export all transactions with their classifications',
            icon: DocumentArrowDownIcon,
            color: 'bg-brand-500',
            action: () => handleExport('transactions'),
        },
        {
            id: 'business-expenses',
            title: 'Business Expenses',
            description: 'Export only business-related transactions',
            icon: BanknotesIcon,
            color: 'bg-mint-500',
            action: () => handleExport('business-expenses'),
        },
        {
            id: 'tax-report',
            title: 'Tax Report',
            description: 'Generate tax-ready report for a specific year',
            icon: ChartBarIcon,
            color: 'bg-coral-500',
            action: () => handleExport('tax-report'),
        },
    ];

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 pb-8">
            <div className="space-y-6">
                {/* Header */}
                <div>
                    <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Reports & Exports</h1>
                    <p className="mt-1 text-base text-zinc-500 tracking-tight">
                        Generate and download reports for your transaction data
                    </p>
                </div>

                {/* Date Range Selection */}
                <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-lg font-semibold text-gray-900 mb-4">Date Range</h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                            <label htmlFor="startDate" className="block text-sm font-medium text-gray-700 mb-1">
                                Start Date
                            </label>
                            <input
                                type="date"
                                id="startDate"
                                value={startDate}
                                onChange={(e) => setStartDate(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                            />
                        </div>
                        <div>
                            <label htmlFor="endDate" className="block text-sm font-medium text-gray-700 mb-1">
                                End Date
                            </label>
                            <input
                                type="date"
                                id="endDate"
                                value={endDate}
                                onChange={(e) => setEndDate(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                            />
                        </div>
                        <div>
                            <label htmlFor="taxYear" className="block text-sm font-medium text-gray-700 mb-1">
                                Tax Year
                            </label>
                            <input
                                type="number"
                                id="taxYear"
                                value={taxYear}
                                onChange={(e) => setTaxYear(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                            />
                        </div>
                    </div>
                </div>

                {/* Report Types */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {reportTypes.map((report) => {
                        const IconComponent = report.icon;
                        return (
                            <div key={report.id} className="bg-white rounded-lg shadow p-6">
                                <div className="flex items-center mb-4">
                                    <div className={`p-3 rounded-lg ${report.color} bg-opacity-10`}>
                                        <IconComponent className={`h-6 w-6 ${report.color.replace('bg-', 'text-')}`} />
                                    </div>
                                    <h3 className="ml-3 text-lg font-semibold text-gray-900">{report.title}</h3>
                                </div>
                                <p className="text-gray-600 mb-4">{report.description}</p>
                                <button
                                    onClick={report.action}
                                    disabled={loading}
                                    className="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-brand-600 hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500 disabled:opacity-50"
                                >
                                    {loading ? 'Generating...' : 'Generate Report'}
                                </button>
                            </div>
                        );
                    })}
                </div>

                {/* Instructions */}
                <div className="bg-gray-50 rounded-lg p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Report Information</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <h4 className="font-medium text-gray-900 mb-2">All Transactions Report</h4>
                            <ul className="text-sm text-gray-600 space-y-1">
                                <li>• Complete list of all transactions</li>
                                <li>• Includes classifications and categories</li>
                                <li>• Useful for general bookkeeping</li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-medium text-gray-900 mb-2">Business Expenses Report</h4>
                            <ul className="text-sm text-gray-600 space-y-1">
                                <li>• Only business-related transactions</li>
                                <li>• Organized by category and date</li>
                                <li>• Perfect for expense tracking</li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-medium text-gray-900 mb-2">Tax Report</h4>
                            <ul className="text-sm text-gray-600 space-y-1">
                                <li>• Tax-year specific summary</li>
                                <li>• Business expense totals</li>
                                <li>• Ready for tax preparation</li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-medium text-gray-900 mb-2">Export Format</h4>
                            <ul className="text-sm text-gray-600 space-y-1">
                                <li>• All reports export as CSV files</li>
                                <li>• Compatible with Excel and accounting software</li>
                                <li>• UTF-8 encoded for international characters</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Reports; 