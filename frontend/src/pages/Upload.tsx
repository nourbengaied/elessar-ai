import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { api } from '../services/api';
import { UploadResult } from '../types/api';
import toast from 'react-hot-toast';
import {
    CloudArrowUpIcon,
    DocumentTextIcon,
    CheckCircleIcon,
    ExclamationTriangleIcon,
} from '@heroicons/react/24/outline';

const Upload: React.FC = () => {
    const [uploading, setUploading] = useState(false);
    const [uploadResult, setUploadResult] = useState<UploadResult | null>(null);

    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        if (acceptedFiles.length === 0) return;

        const file = acceptedFiles[0];

        // Validate file type
        if (!file.name.toLowerCase().endsWith('.csv')) {
            toast.error('Please upload a CSV file');
            return;
        }

        setUploading(true);
        setUploadResult(null);

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await api.post<UploadResult>('/api/v1/transactions/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setUploadResult(response.data);
            toast.success(`Successfully processed ${response.data.processed_count} transactions`);
        } catch (error: any) {
            toast.error(error.response?.data?.detail || 'Upload failed');
        } finally {
            setUploading(false);
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'text/csv': ['.csv'],
        },
        multiple: false,
    });

    return (
        <div className="space-y-6">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-bold text-gray-900">Upload Transactions</h1>
                <p className="mt-1 text-sm text-gray-500">
                    Upload a CSV file with your transaction data for AI-powered classification
                </p>
            </div>

            {/* Upload Area */}
            <div className="bg-white shadow rounded-lg p-6">
                <div
                    {...getRootProps()}
                    className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${isDragActive
                            ? 'border-primary-400 bg-primary-50'
                            : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
                        }`}
                >
                    <input {...getInputProps()} />
                    <CloudArrowUpIcon className="mx-auto h-12 w-12 text-gray-400" />
                    <div className="mt-4">
                        <p className="text-lg font-medium text-gray-900">
                            {isDragActive ? 'Drop the CSV file here' : 'Drag and drop a CSV file here'}
                        </p>
                        <p className="mt-2 text-sm text-gray-500">
                            or click to browse files
                        </p>
                    </div>
                    <p className="mt-4 text-xs text-gray-400">
                        Supported format: CSV files only
                    </p>
                </div>
            </div>

            {/* Upload Progress */}
            {uploading && (
                <div className="bg-white shadow rounded-lg p-6">
                    <div className="flex items-center">
                        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600 mr-3"></div>
                        <p className="text-sm font-medium text-gray-900">
                            Processing your transactions...
                        </p>
                    </div>
                </div>
            )}

            {/* Upload Results */}
            {uploadResult && (
                <div className="bg-white shadow rounded-lg p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Upload Results</h3>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                        <div className="bg-success-50 border border-success-200 rounded-lg p-4">
                            <div className="flex items-center">
                                <CheckCircleIcon className="h-5 w-5 text-success-600 mr-2" />
                                <span className="text-sm font-medium text-success-900">
                                    Processed: {uploadResult.processed_count}
                                </span>
                            </div>
                        </div>

                        {uploadResult.errors.length > 0 && (
                            <div className="bg-warning-50 border border-warning-200 rounded-lg p-4">
                                <div className="flex items-center">
                                    <ExclamationTriangleIcon className="h-5 w-5 text-warning-600 mr-2" />
                                    <span className="text-sm font-medium text-warning-900">
                                        Errors: {uploadResult.errors.length}
                                    </span>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Error Details */}
                    {uploadResult.errors.length > 0 && (
                        <div className="mb-6">
                            <h4 className="text-sm font-medium text-gray-900 mb-2">Errors:</h4>
                            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                                <ul className="text-sm text-red-700 space-y-1">
                                    {uploadResult.errors.map((error, index) => (
                                        <li key={index}>• {error}</li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    )}

                    {/* Sample Transactions */}
                    {uploadResult.transactions.length > 0 && (
                        <div>
                            <h4 className="text-sm font-medium text-gray-900 mb-2">
                                Sample Processed Transactions:
                            </h4>
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
                                                Classification
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody className="bg-white divide-y divide-gray-200">
                                        {uploadResult.transactions.slice(0, 5).map((transaction, index) => (
                                            <tr key={index}>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                                    {transaction.date}
                                                </td>
                                                <td className="px-6 py-4 text-sm text-gray-900">
                                                    {transaction.description}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                                    ${transaction.amount}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap">
                                                    <span
                                                        className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${transaction.is_business
                                                                ? 'bg-success-100 text-success-800'
                                                                : 'bg-gray-100 text-gray-800'
                                                            }`}
                                                    >
                                                        {transaction.is_business ? 'Business' : 'Personal'}
                                                    </span>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* Instructions */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                <h3 className="text-lg font-medium text-blue-900 mb-4">CSV Format Requirements</h3>
                <div className="text-sm text-blue-800 space-y-2">
                    <p>Your CSV file should contain the following columns:</p>
                    <ul className="list-disc list-inside space-y-1 ml-4">
                        <li><strong>date</strong> - Transaction date (YYYY-MM-DD format)</li>
                        <li><strong>description</strong> - Transaction description</li>
                        <li><strong>amount</strong> - Transaction amount (positive for income, negative for expenses)</li>
                        <li><strong>category</strong> - Optional category field</li>
                    </ul>
                    <p className="mt-4">
                        <strong>Example:</strong><br />
                        date,description,amount,category<br />
                        2024-01-15,Client Payment,1500.00,Income<br />
                        2024-01-16,Office Supplies,-45.50,Expenses
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Upload; 