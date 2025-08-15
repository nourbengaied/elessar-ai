import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { api } from '../services/api';
import { UploadResult } from '../types/api';
import toast from 'react-hot-toast';
import {
    CloudArrowUpIcon,
    CheckCircleIcon,
    ExclamationTriangleIcon,
    StopIcon,
} from '@heroicons/react/24/outline';

const Upload: React.FC = () => {
    const [uploading, setUploading] = useState(false);
    const [uploadResult, setUploadResult] = useState<UploadResult | null>(null);
    const [cancelling, setCancelling] = useState(false);

    const handleCancelProcessing = async () => {
        if (!window.confirm('Are you sure you want to stop the transaction processing? This action cannot be undone.')) {
            return;
        }

        setCancelling(true);
        try {
            await api.post('/api/v1/transactions/cancel-processing');
            toast.success('Processing cancellation requested');
            setUploading(false);
            setUploadResult(null);
        } catch (error: any) {
            toast.error('Failed to cancel processing');
            console.error('Cancel processing error:', error);
        } finally {
            setCancelling(false);
        }
    };

    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        if (acceptedFiles.length === 0) return;

        const file = acceptedFiles[0];
        const fileExtension = file.name.toLowerCase().split('.').pop();
        const uploadId = `upload_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

        console.log(`[${uploadId}] Starting file upload process`);
        console.log(`[${uploadId}] File details:`, {
            name: file.name,
            size: file.size,
            type: file.type,
            extension: fileExtension,
            lastModified: new Date(file.lastModified).toISOString()
        });

        // Validate file type
        if (!['csv', 'pdf'].includes(fileExtension || '')) {
            console.warn(`[${uploadId}] File type validation failed - Extension: ${fileExtension}`);
            toast.error('Please upload a CSV or PDF file');
            return;
        }

        console.log(`[${uploadId}] File type validation passed`);
        setUploading(true);
        setUploadResult(null);

        try {
            console.log(`[${uploadId}] Preparing form data for upload`);
            const formData = new FormData();
            formData.append('file', file);

            console.log(`[${uploadId}] Making API request to /api/v1/transactions/upload`);
            const startTime = Date.now();

            const response = await api.post<UploadResult>('/api/v1/transactions/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            const endTime = Date.now();
            const processingTime = endTime - startTime;

            console.log(`[${uploadId}] API response received successfully:`, {
                status: response.status,
                data: response.data,
                processingTime: `${processingTime}ms`
            });

            setUploadResult(response.data);
            toast.success(`Successfully processed ${response.data.processed_count} transactions`);
            
            console.log(`[${uploadId}] Upload completed successfully - Transactions processed: ${response.data.processed_count}`);
            
        } catch (error: any) {
            const errorDetails = {
                message: error.message,
                status: error.response?.status,
                statusText: error.response?.statusText,
                data: error.response?.data,
                config: {
                    url: error.config?.url,
                    method: error.config?.method,
                    headers: error.config?.headers
                }
            };
            
            console.error(`[${uploadId}] Upload failed:`, errorDetails);
            
            // Handle cancellation specifically
            if (error.response?.status === 499) {
                toast.success('Processing was cancelled successfully');
            } else {
                toast.error(error.response?.data?.detail || 'Upload failed');
            }
        } finally {
            setUploading(false);
            console.log(`[${uploadId}] Upload process completed`);
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'text/csv': ['.csv'],
            'application/pdf': ['.pdf'],
        },
        multiple: false,
        onDropAccepted: (files) => {
            console.log('Files accepted by dropzone:', files.map(f => ({ name: f.name, size: f.size, type: f.type })));
        },
        onDropRejected: (fileRejections) => {
            console.warn('Files rejected by dropzone:', fileRejections.map(fr => ({
                file: fr.file.name,
                errors: fr.errors.map(e => ({ code: e.code, message: e.message }))
            })));
        }
    });

    return (
        <div className="space-y-6">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Upload Transactions</h1>
                <p className="mt-1 text-base text-zinc-500 tracking-tight">
                    Upload a CSV file or PDF bank statement with your transaction data for AI-powered classification
                </p>
            </div>

            {/* Upload Area */}
            <div className="bg-white/80 shadow rounded-lg p-6">
                <div
                    {...getRootProps()}
                    className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${isDragActive
                            ? 'border-brand-400 bg-brand-50'
                            : 'border-sand-300 hover:border-brand-400 hover:bg-sand-50'
                        }`}
                >
                    <input {...getInputProps()} />
                    <CloudArrowUpIcon className="mx-auto h-12 w-12 text-brand-400" />
                    <div className="mt-4">
                        <p className="text-xl font-medium text-gray-900 tracking-tight">
                            {isDragActive ? 'Drop the file here' : 'Drag and drop a CSV or PDF file here'}
                        </p>
                        <p className="mt-2 text-base text-zinc-500 tracking-tight">
                            or click to browse files
                        </p>
                    </div>
                    <p className="mt-4 text-sm text-zinc-400 tracking-tight">
                        Supported formats: CSV files and PDF bank statements
                    </p>
                </div>
            </div>

            {/* Upload Progress */}
            {uploading && (
                <div className="bg-white/80 shadow rounded-lg p-6">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center">
                            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-brand-600 mr-3"></div>
                            <p className="text-base font-medium text-gray-900 tracking-tight">
                                Processing your transactions...
                            </p>
                        </div>
                        <button
                            onClick={handleCancelProcessing}
                            disabled={cancelling}
                            className="inline-flex items-center px-3 py-2 border border-coral-300 rounded-md shadow-sm text-base font-medium text-coral-700 bg-white hover:bg-coral-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-coral-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed tracking-tight"
                        >
                            <StopIcon className="h-4 w-4 mr-2" />
                            {cancelling ? 'Stopping...' : 'Stop Processing'}
                        </button>
                    </div>
                </div>
            )}

            {/* Upload Results */}
            {uploadResult && (
                <div className="bg-white/80 shadow rounded-lg p-6">
                    <h3 className="text-xl font-semibold text-gray-900 mb-4 tracking-tight">Upload Results</h3>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                        <div className="bg-brand-50 border border-brand-200 rounded-lg p-4">
                            <div className="flex items-center">
                                <CheckCircleIcon className="h-5 w-5 text-brand-600 mr-2" />
                                <span className="text-base font-medium text-brand-900 tracking-tight">
                                    Processed: {uploadResult.processed_count}
                                </span>
                            </div>
                        </div>

                        {uploadResult.errors.length > 0 && (
                            <div className="bg-coral-50 border border-coral-200 rounded-lg p-4">
                                <div className="flex items-center">
                                    <ExclamationTriangleIcon className="h-5 w-5 text-coral-600 mr-2" />
                                    <span className="text-base font-medium text-coral-900 tracking-tight">
                                        Errors: {uploadResult.errors.length}
                                    </span>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Error Details */}
                    {uploadResult.errors.length > 0 && (
                        <div className="mb-6">
                            <h4 className="text-base font-medium text-gray-900 mb-2 tracking-tight">Errors:</h4>
                            <div className="bg-coral-50 border border-coral-200 rounded-lg p-4">
                                <ul className="text-base text-coral-700 space-y-1 tracking-tight">
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
                            <h4 className="text-base font-medium text-gray-900 mb-2 tracking-tight">
                                Sample Processed Transactions:
                            </h4>
                            <div className="overflow-x-auto">
                                <table className="min-w-full divide-y divide-sand-200">
                                    <thead className="bg-sand-50">
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
                                    <tbody className="bg-white divide-y divide-sand-200">
                                        {uploadResult.transactions.slice(0, 5).map((transaction, index) => (
                                            <tr key={index}>
                                                <td className="px-6 py-4 whitespace-nowrap text-base text-gray-900 tracking-tight">
                                                    {transaction.date}
                                                </td>
                                                <td className="px-6 py-4 text-base text-gray-900 tracking-tight">
                                                    {transaction.description}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-base text-gray-900 tracking-tight">
                                                    ${transaction.amount}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap">
                                                    <span
                                                        className={`inline-flex px-2 py-1 text-sm font-semibold rounded-full tracking-tight ${transaction.is_business_expense
                                                                ? 'bg-brand-100 text-brand-800'
                                                                : 'bg-sand-100 text-gray-800'
                                                            }`}
                                                    >
                                                        {transaction.is_business_expense ? 'Business' : 'Personal'}
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
            <div className="bg-mint-50 border border-mint-200 rounded-lg p-6">
                <h3 className="text-xl font-semibold text-brand-900 mb-4 tracking-tight">File Format Requirements</h3>
                <div className="text-base text-brand-800 space-y-4 tracking-tight">
                    <div>
                        <h4 className="font-medium">CSV Files:</h4>
                        <p>Your CSV file should contain the following columns:</p>
                        <ul className="list-disc list-inside space-y-1 ml-4 mt-2">
                            <li><strong>date</strong> - Transaction date (YYYY-MM-DD format)</li>
                            <li><strong>description</strong> - Transaction description</li>
                            <li><strong>amount</strong> - Transaction amount (positive for income, negative for expenses)</li>
                            <li><strong>category</strong> - Optional category field</li>
                        </ul>
                        <p className="mt-2">
                            <strong>Example:</strong><br />
                            date,description,amount,category<br />
                            2024-01-15,Client Payment,1500.00,Income<br />
                            2024-01-16,Office Supplies,-45.50,Expenses
                        </p>
                    </div>
                    
                    <div>
                        <h4 className="font-medium">PDF Bank Statements:</h4>
                        <p>Upload your bank statement PDF and our AI will extract and classify the transactions automatically. The system works best with:</p>
                        <ul className="list-disc list-inside space-y-1 ml-4 mt-2">
                            <li>Standard bank statement formats</li>
                            <li>Clear transaction descriptions</li>
                            <li>Well-formatted dates and amounts</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Upload; 