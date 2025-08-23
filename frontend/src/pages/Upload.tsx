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
            await api.post('/transactions/cancel-processing');
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

            console.log(`[${uploadId}] Making API request to /transactions/upload`);
            const startTime = Date.now();

            const response = await api.post<UploadResult>('/transactions/upload', formData, {
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
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 pb-8">
            <div className="space-y-6">
                {/* Header */}
                <div>
                    <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Upload Statement</h1>
                    <p className="mt-1 text-base text-zinc-500 tracking-tight">
                        Upload your CSV or PDF bank statement for AI-powered transaction classification
                    </p>
                </div>

                {/* Upload Area */}
                <div className="bg-white rounded-lg shadow p-8">
                    {!uploading && !uploadResult && (
                        <div className="text-center">
                            <div className="mx-auto w-24 h-24 bg-brand-100 rounded-full flex items-center justify-center mb-6">
                                <CloudArrowUpIcon className="h-12 w-12 text-brand-600" />
                            </div>
                            <h2 className="text-xl font-semibold text-gray-900 mb-2">Upload your statement</h2>
                            <p className="text-base text-gray-600 mb-6">
                                Drag and drop your CSV or PDF file here, or click to browse
                            </p>
                            <div
                                {...getRootProps()}
                                className="border-2 border-dashed border-gray-300 rounded-lg p-8 hover:border-brand-400 transition-colors cursor-pointer"
                            >
                                <input {...getInputProps()} />
                                <div className="text-center">
                                    <CloudArrowUpIcon className="mx-auto h-12 w-12 text-gray-400" />
                                    <p className="mt-2 text-sm text-gray-600">
                                        <span className="font-medium text-brand-600 hover:text-brand-500">
                                            Click to upload
                                        </span>{' '}
                                        or drag and drop
                                    </p>
                                    <p className="text-xs text-gray-500 mt-1">CSV or PDF files only</p>
                                </div>
                            </div>
                        </div>
                    )}

                    {uploading && (
                        <div className="text-center">
                            <div className="mx-auto w-24 h-24 bg-brand-100 rounded-full flex items-center justify-center mb-6">
                                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-600"></div>
                            </div>
                            <h2 className="text-xl font-semibold text-gray-900 mb-2">Processing your statement</h2>
                            <p className="text-base text-gray-600 mb-6">
                                Our AI is analyzing and classifying your transactions. This may take a few moments.
                            </p>
                            <button
                                onClick={handleCancelProcessing}
                                disabled={cancelling}
                                className="inline-flex items-center px-4 py-2 border border-red-300 rounded-md shadow-sm text-sm font-medium text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
                            >
                                <StopIcon className="h-4 w-4 mr-2" />
                                {cancelling ? 'Cancelling...' : 'Cancel Processing'}
                            </button>
                        </div>
                    )}

                    {uploadResult && (
                        <div className="text-center">
                            <div className="mx-auto w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mb-6">
                                <CheckCircleIcon className="h-12 w-12 text-green-600" />
                            </div>
                            <h2 className="text-xl font-semibold text-gray-900 mb-2">Upload successful!</h2>
                            <div className="bg-gray-50 rounded-lg p-6 mb-6">
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                                    <div>
                                        <p className="text-2xl font-bold text-brand-600">{uploadResult.processed_count}</p>
                                        <p className="text-sm text-gray-600">Transactions processed</p>
                                    </div>
                                    <div>
                                        <p className="text-2xl font-bold text-brand-600">
                                            {uploadResult.transactions.filter(t => t.is_business_expense).length}
                                        </p>
                                        <p className="text-sm text-gray-600">Business transactions</p>
                                    </div>
                                    <div>
                                        <p className="text-2xl font-bold text-brand-600">
                                            {uploadResult.transactions.filter(t => !t.is_business_expense).length}
                                        </p>
                                        <p className="text-sm text-gray-600">Personal transactions</p>
                                    </div>
                                </div>
                            </div>
                            <div className="flex flex-col sm:flex-row gap-4 justify-center">
                                <button
                                    onClick={() => window.location.href = '/transactions'}
                                    className="inline-flex items-center px-6 py-3 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-brand-600 hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500"
                                >
                                    View Transactions
                                </button>
                                <button
                                    onClick={() => {
                                        setUploadResult(null);
                                        setUploading(false);
                                    }}
                                    className="inline-flex items-center px-6 py-3 border border-gray-300 rounded-md shadow-sm text-base font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500"
                                >
                                    Upload Another File
                                </button>
                            </div>
                        </div>
                    )}
                </div>

                {/* Instructions */}
                <div className="bg-gray-50 rounded-lg p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Supported Formats</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <h4 className="font-medium text-gray-900 mb-2">CSV Files</h4>
                            <ul className="text-sm text-gray-600 space-y-1">
                                <li>• Export from your bank's online portal</li>
                                <li>• Should include date, description, and amount columns</li>
                                <li>• Common formats: QIF, OFX, or custom CSV</li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-medium text-gray-900 mb-2">PDF Statements</h4>
                            <ul className="text-sm text-gray-600 space-y-1">
                                <li>• Monthly or quarterly bank statements</li>
                                <li>• Our AI will extract transaction data</li>
                                <li>• Supports most standard bank statement formats</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Upload; 