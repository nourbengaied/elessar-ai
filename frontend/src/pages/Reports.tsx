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
                    url = `/api/v1/export/transactions/csv`;
                    filename = `transactions_${startDate || 'all'}_${endDate || 'all'}.csv`;
                    break;
                case 'business-expenses':
                    url = `/api/v1/export/business-expenses/csv`;
                    filename = `business_expenses_${startDate || 'all'}_${endDate || 'all'}.csv`;
                    break;
                case 'tax-report':
                    url = `/api/v1/export/tax-report/csv?tax_year=${taxYear}`;
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
            color: 'bg-blue-500',
            action: () => handleExport('transactions'),
        },
        {
            id: 'business-expenses',
            title: 'Business Expenses',
            description: 'Export only business-related transactions',
            icon: BanknotesIcon,
            color: 'bg-green-500',
            action: () => handleExport('business-expenses'),
        },
        {
            id: 'tax-report',
            title: 'Tax Report',
            description: 'Generate tax-ready report for a specific year',
            icon: ChartBarIcon,
            color: 'bg-purple-500',
            action: () => handleExport('tax-report'),
        },
    ];

    return (
        <div className="space-y-6">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-bold text-gray-900">Reports & Exports</h1>
                <p className="mt-1 text-sm text-gray-500">
                    Generate and download reports for your transaction data
                </p>
            </div>

            {/* Date Range Filter */}
            <div className="bg-white shadow rounded-lg p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Date Range</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                        <label htmlFor="start-date" className="block text-sm font-medium text-gray-700 mb-1">
                            Start Date
                        </label>
                        <input
                            type="date"
                            id="start-date"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                            value={startDate}
                            onChange={(e) => setStartDate(e.target.value)}
                        />
                    </div>

                    <div>
                        <label htmlFor="end-date" className="block text-sm font-medium text-gray-700 mb-1">
                            End Date
                        </label>
                        <input
                            type="date"
                            id="end-date"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                            value={endDate}
                            onChange={(e) => setEndDate(e.target.value)}
                        />
                    </div>

                    <div>
                        <label htmlFor="tax-year" className="block text-sm font-medium text-gray-700 mb-1">
                            Tax Year
                        </label>
                        <input
                            type="number"
                            id="tax-year"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                            value={taxYear}
                            onChange={(e) => setTaxYear(e.target.value)}
                            min="2020"
                            max="2030"
                        />
                    </div>
                </div>
            </div>

            {/* Report Types */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {reportTypes.map((report) => (
                    <div key={report.id} className="bg-white shadow rounded-lg p-6">
                        <div className="flex items-center">
                            <div className={`flex-shrink-0 w-12 h-12 rounded-lg flex items-center justify-center ${report.color}`}>
                                <report.icon className="h-6 w-6 text-white" />
                            </div>
                            <div className="ml-4 flex-1">
                                <h3 className="text-lg font-medium text-gray-900">{report.title}</h3>
                                <p className="text-sm text-gray-500">{report.description}</p>
                            </div>
                        </div>

                        <div className="mt-6">
                            <button
                                onClick={report.action}
                                disabled={loading}
                                className="w-full flex justify-center items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {loading ? (
                                    <>
                                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                                        Generating...
                                    </>
                                ) : (
                                    <>
                                        <DocumentArrowDownIcon className="h-4 w-4 mr-2" />
                                        Export Report
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            {/* Instructions */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                <h3 className="text-lg font-medium text-blue-900 mb-4">Report Types</h3>
                <div className="text-sm text-blue-800 space-y-3">
                    <div>
                        <h4 className="font-medium">All Transactions</h4>
                        <p>Complete export of all transactions with their AI classifications, confidence scores, and manual overrides.</p>
                    </div>
                    <div>
                        <h4 className="font-medium">Business Expenses</h4>
                        <p>Filtered export containing only transactions classified as business-related. Perfect for expense tracking and tax preparation.</p>
                    </div>
                    <div>
                        <h4 className="font-medium">Tax Report</h4>
                        <p>Tax-ready report for a specific year with proper formatting for tax filing. Includes business income and deductible expenses.</p>
                    </div>
                </div>
            </div>

            {/* Tips */}
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
                <h3 className="text-lg font-medium text-yellow-900 mb-4">Tips for Better Reports</h3>
                <ul className="text-sm text-yellow-800 space-y-2">
                    <li>• Use date ranges to focus on specific periods (e.g., quarterly reports)</li>
                    <li>• Review and correct classifications before generating tax reports</li>
                    <li>• Export business expenses regularly for expense tracking</li>
                    <li>• Keep your transaction descriptions clear for better AI classification</li>
                </ul>
            </div>
        </div>
    );
};

export default Reports; 