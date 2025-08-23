import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';
import { Statistics, Transaction, TransactionsResponse } from '../types/api';
import Logo from '../components/Logo';
import {
    BanknotesIcon,
    ChartBarIcon,
    DocumentTextIcon,
    CloudArrowUpIcon,
    CheckCircleIcon,
    ArrowRightIcon,
    DocumentArrowUpIcon,
    CpuChipIcon,
    EyeIcon,
    CurrencyDollarIcon,
    BuildingOfficeIcon,
    ShoppingBagIcon,
    SparklesIcon,
    ChartPieIcon,
} from '@heroicons/react/24/outline';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

const Dashboard: React.FC = () => {
    const { user } = useAuth();
    const [statistics, setStatistics] = useState<Statistics | null>(null);
    const [topTransactions, setTopTransactions] = useState<Transaction[]>([]);
    const [loading, setLoading] = useState(true);
    const [hoveredCard, setHoveredCard] = useState<string | null>(null);
    const [activeStep, setActiveStep] = useState(0);

    useEffect(() => {
        fetchStatistics();
        fetchTopTransactions();
    }, []);

    // Auto-progress through steps
    useEffect(() => {
        const interval = setInterval(() => {
            setActiveStep((prev) => (prev + 1) % 4);
        }, 2000); // Change step every 2 seconds

        return () => clearInterval(interval);
    }, []);

    const fetchStatistics = async () => {
        try {
            const response = await api.get<Statistics>('/transactions/statistics/summary');
            setStatistics(response.data);
        } catch (error) {
            console.error('Failed to fetch statistics:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchTopTransactions = async () => {
        try {
            const response = await api.get<TransactionsResponse>('/transactions?limit=5&sort_by=amount&sort_order=desc');
            setTopTransactions(response.data.transactions || []);
        } catch (error) {
            console.error('Failed to fetch top transactions:', error);
        }
    };

    const pieData = statistics ? [
        { name: 'Business', value: statistics.business_transactions, color: '#3b82f6' },
        { name: 'Personal', value: statistics.personal_transactions, color: '#ef4444' },
    ] : [];

    const COLORS = ['#3b82f6', '#ef4444'];

    const howItWorksSteps = [
        {
            id: 1,
            title: "Upload Statement",
            description: "Upload your CSV file or PDF bank statement",
            icon: DocumentArrowUpIcon,
            color: "text-brand-600",
            bgColor: "bg-brand-50",
        },
        {
            id: 2,
            title: "AI Processing",
            description: "Our AI analyzes and classifies transactions",
            icon: CpuChipIcon,
            color: "text-mint-600",
            bgColor: "bg-mint-50",
        },
        {
            id: 3,
            title: "Review Results",
            description: "Review and adjust classifications as needed",
            icon: EyeIcon,
            color: "text-coral-600",
            bgColor: "bg-coral-50",
        },
        {
            id: 4,
            title: "Export & Report",
            description: "Generate reports and export your data",
            icon: ChartBarIcon,
            color: "text-brand-700",
            bgColor: "bg-brand-50",
        },
    ];

    const sampleTransactions = [
        { id: 1, description: "Office Supplies Co", amount: -45.99, category: "Business", icon: BuildingOfficeIcon },
        { id: 2, description: "Grocery Store", amount: -23.50, category: "Personal", icon: ShoppingBagIcon },
        { id: 3, description: "Client Payment", amount: 500.00, category: "Business", icon: CurrencyDollarIcon },
        { id: 4, description: "Coffee Shop", amount: -4.75, category: "Personal", icon: ShoppingBagIcon },
    ];

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
        );
    }

    return (
        <div className="animate-fade-in">
            {/* Header */}
            <div className="py-8 px-8 animate-slide-down">
                <div className="flex items-start">
            <div>
                        <p className="text-lg text-zinc-500 tracking-tight">
                    Welcome back, {user?.business_name || user?.email}
                </p>
                    </div>
                </div>
            </div>

            {/* Subtle Divider */}
            <div className="border-t border-gray-200/10"></div>

            {/* Upload Section */}
            <div className="py-12 px-8 animate-slide-up">
                <div className="text-center">
                <div className="max-w-md mx-auto">
                        <div className="relative mb-6">
                            <div className="absolute inset-0 bg-gradient-to-r from-brand-400 to-mint-400 rounded-full blur-xl opacity-20 animate-pulse"></div>
                            <CloudArrowUpIcon className="relative mx-auto h-16 w-16 text-brand-500 animate-bounce-slow" />
                        </div>
                        <h2 className="text-2xl font-semibold text-gray-900 mb-2 tracking-tight">
                            Upload Statement
                    </h2>
                        <p className="text-lg text-zinc-500 mb-6 tracking-tight">
                        Get started by uploading your CSV file or PDF bank statement for AI-powered classification
                    </p>
                    <Link
                        to="/upload"
                            className="group inline-flex items-center px-6 py-3 border border-transparent rounded-xl shadow-lg text-lg font-medium text-white bg-gradient-to-r from-brand-600 to-brand-700 hover:from-brand-700 hover:to-brand-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500 transition-all duration-300 tracking-tight transform hover:scale-105 hover:shadow-xl"
                    >
                            <CloudArrowUpIcon className="h-5 w-5 mr-2 transition-transform duration-300 group-hover:translate-y-[-2px]" />
                            Upload Statement
                    </Link>
                    </div>
                </div>
            </div>

            {/* Subtle Divider */}
            <div className="border-t border-gray-200/12"></div>

            {/* Statistics Section */}
            <div className="py-12 px-8 animate-slide-up-delay">
                <div className="mb-8">
                    <h2 className="text-2xl font-semibold text-gray-800 tracking-tight mb-2">Overview</h2>
                    <p className="text-lg text-zinc-500 tracking-tight">Your transaction statistics at a glance</p>
                </div>
                <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 animate-slide-up-delay">
                    <div 
                        className={`bg-white/80 backdrop-blur-sm shadow-lg rounded-xl border border-white/20 transition-all duration-500 transform hover:scale-105 hover:shadow-xl cursor-pointer ${
                            hoveredCard === 'total' ? 'ring-2 ring-brand-200 shadow-xl' : ''
                        }`}
                        onMouseEnter={() => setHoveredCard('total')}
                        onMouseLeave={() => setHoveredCard(null)}
                    >
                        <div className="p-6">
                        <div className="flex items-center">
                            <div className="flex-shrink-0">
                                    <div className="p-2 bg-brand-50 rounded-lg">
                                        <DocumentTextIcon className={`h-6 w-6 text-brand-500 transition-all duration-300 ${
                                            hoveredCard === 'total' ? 'scale-110' : ''
                                        }`} />
                                    </div>
                            </div>
                                <div className="ml-4 w-0 flex-1">
                                <dl>
                                    <dt className="text-base font-medium text-zinc-500 truncate tracking-tight">
                                        Total Transactions
                                    </dt>
                                        <dd className="text-3xl font-bold text-gray-900 tracking-tight">
                                        {statistics?.total_transactions || 0}
                                    </dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>

                    <div 
                        className={`bg-white/80 backdrop-blur-sm shadow-lg rounded-xl border border-white/20 transition-all duration-500 transform hover:scale-105 hover:shadow-xl cursor-pointer ${
                            hoveredCard === 'business' ? 'ring-2 ring-brand-200 shadow-xl' : ''
                        }`}
                        onMouseEnter={() => setHoveredCard('business')}
                        onMouseLeave={() => setHoveredCard(null)}
                    >
                        <div className="p-6">
                        <div className="flex items-center">
                            <div className="flex-shrink-0">
                                    <div className="p-2 bg-brand-50 rounded-lg">
                                        <BanknotesIcon className={`h-6 w-6 text-brand-600 transition-all duration-300 ${
                                            hoveredCard === 'business' ? 'scale-110' : ''
                                        }`} />
                                    </div>
                            </div>
                                <div className="ml-4 w-0 flex-1">
                                <dl>
                                    <dt className="text-base font-medium text-zinc-500 truncate tracking-tight">
                                        Business Transactions
                                    </dt>
                                        <dd className="text-3xl font-bold text-gray-900 tracking-tight">
                                        {statistics?.business_transactions || 0}
                                    </dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>

                    <div 
                        className={`bg-white/80 backdrop-blur-sm shadow-lg rounded-xl border border-white/20 transition-all duration-500 transform hover:scale-105 hover:shadow-xl cursor-pointer ${
                            hoveredCard === 'amount' ? 'ring-2 ring-brand-200 shadow-xl' : ''
                        }`}
                        onMouseEnter={() => setHoveredCard('amount')}
                        onMouseLeave={() => setHoveredCard(null)}
                    >
                        <div className="p-6">
                        <div className="flex items-center">
                            <div className="flex-shrink-0">
                                    <div className="p-2 bg-mint-50 rounded-lg">
                                        <ChartBarIcon className={`h-6 w-6 text-mint-600 transition-all duration-300 ${
                                            hoveredCard === 'amount' ? 'scale-110' : ''
                                        }`} />
                                    </div>
                            </div>
                                <div className="ml-4 w-0 flex-1">
                                <dl>
                                    <dt className="text-base font-medium text-zinc-500 truncate tracking-tight">
                                        Total Amount
                                    </dt>
                                        <dd className="text-3xl font-bold text-gray-900 tracking-tight">
                                        ${statistics?.total_amount?.toLocaleString() || '0'}
                                    </dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>

                    <div 
                        className={`bg-white/80 backdrop-blur-sm shadow-lg rounded-xl border border-white/20 transition-all duration-500 transform hover:scale-105 hover:shadow-xl cursor-pointer ${
                            hoveredCard === 'business-amount' ? 'ring-2 ring-brand-200 shadow-xl' : ''
                        }`}
                        onMouseEnter={() => setHoveredCard('business-amount')}
                        onMouseLeave={() => setHoveredCard(null)}
                    >
                        <div className="p-6">
                        <div className="flex items-center">
                            <div className="flex-shrink-0">
                                    <div className="p-2 bg-coral-50 rounded-lg">
                                        <CloudArrowUpIcon className={`h-6 w-6 text-coral-600 transition-all duration-300 ${
                                            hoveredCard === 'business-amount' ? 'scale-110' : ''
                                        }`} />
                                    </div>
                            </div>
                                <div className="ml-4 w-0 flex-1">
                                <dl>
                                    <dt className="text-base font-medium text-zinc-500 truncate tracking-tight">
                                        Business Amount
                                    </dt>
                                        <dd className="text-3xl font-bold text-gray-900 tracking-tight">
                                        ${statistics?.business_amount?.toLocaleString() || '0'}
                                    </dd>
                                </dl>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Subtle Divider */}
            <div className="border-t border-gray-200/15"></div>

            {/* How It Works Section */}
            <div className="py-12 px-8 animate-slide-up-delay-2">
                <div className="mb-8">
                    <h2 className="text-2xl font-semibold text-gray-800 tracking-tight mb-2">How It Works</h2>
                    <p className="text-lg text-zinc-500 tracking-tight">See how our AI processes your transactions</p>
                </div>
                <div className="transition-all duration-500 animate-slide-up-delay-2">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                        {howItWorksSteps.map((step, index) => {
                            const IconComponent = step.icon;
                            const isActive = activeStep === index;
                            const isCompleted = activeStep > index;
                            
                            return (
                                <div
                                    key={step.id}
                                    className={`relative p-6 rounded-xl border-2 transition-all duration-500 cursor-pointer transform hover:scale-105 hover:shadow-lg ${
                                        isActive 
                                            ? 'border-brand-600 bg-brand-50/80 shadow-lg' 
                                            : isCompleted 
                                            ? 'border-green-600 bg-green-50/80' 
                                            : 'border-gray-200 bg-gray-50/80 hover:border-brand-400'
                                    }`}
                                    onClick={() => setActiveStep(index)}
                                >
                                    <div className="flex items-center space-x-4">
                                        <div className={`flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-500 ${
                                            isActive ? 'bg-brand-600 text-white shadow-lg' : isCompleted ? 'bg-green-600 text-white shadow-lg' : step.bgColor
                                        }`}>
                                            {isCompleted ? (
                                                <CheckCircleIcon className="h-7 w-7" />
                                            ) : (
                                                <IconComponent className={`h-7 w-7 ${step.color}`} />
                                            )}
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <p className={`text-base font-medium transition-colors duration-300 ${
                                                isActive ? 'text-brand-800' : isCompleted ? 'text-green-800' : 'text-gray-700'
                                            }`}>
                                                {step.title}
                                            </p>
                                            <p className={`text-sm transition-colors duration-300 ${
                                                isActive ? 'text-brand-700' : isCompleted ? 'text-green-700' : 'text-gray-500'
                                            }`}>
                                                {step.description}
                                            </p>
                                        </div>
                                    </div>
                                    
                                    {/* Step number */}
                                    <div className={`absolute -top-3 -right-3 w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition-all duration-300 ${
                                        isActive ? 'bg-brand-600 text-white shadow-lg' : isCompleted ? 'bg-green-600 text-white shadow-lg' : 'bg-gray-300 text-gray-600'
                                    }`}>
                                        {step.id}
                                    </div>
                                    
                                    {/* Arrow connector */}
                                    {index < howItWorksSteps.length - 1 && (
                                        <div className="hidden lg:block absolute top-1/2 -right-3 transform -translate-y-1/2">
                                            <ArrowRightIcon className={`h-7 w-7 transition-colors duration-300 ${
                                                isCompleted ? 'text-green-500' : 'text-gray-300'
                                            }`} />
                                        </div>
                                    )}
                                </div>
                            );
                        })}
                    </div>
                    
                    {/* Transaction Extraction Visual */}
                    <div className="bg-gradient-to-r from-sand-50 to-sand-100 rounded-xl border border-sand-200 p-8">
                        <h4 className="text-xl font-semibold text-gray-800 mb-6">
                            Transaction Extraction Process
                        </h4>
                        
                        {/* Table Header */}
                        <div className="bg-white/90 backdrop-blur-sm rounded-xl border border-sand-200 overflow-hidden mb-6 shadow-lg">
                            <div className="grid grid-cols-12 bg-sand-50/80 border-b border-sand-200 px-6 py-4">
                                <div className="col-span-1">
                                    <span className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Status</span>
                                </div>
                                <div className="col-span-4">
                                    <span className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Description</span>
                                </div>
                                <div className="col-span-2">
                                    <span className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Amount</span>
                                </div>
                                <div className="col-span-2">
                                    <span className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Category</span>
                                </div>
                                <div className="col-span-2">
                                    <span className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Confidence</span>
                                </div>
                                <div className="col-span-1">
                                    <span className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Action</span>
                                </div>
                            </div>
                            
                            {/* Table Rows */}
                            {sampleTransactions.map((transaction, index) => {
                                const IconComponent = transaction.icon;
                                const isProcessing = activeStep === 1 && index < 2;
                                const isClassified = activeStep >= 2;
                                const isBusiness = transaction.category === "Business";
                                const confidence = isClassified ? (isBusiness ? 95 : 87) : (isProcessing ? 0 : null);
                                
                                return (
                                    <div
                                        key={transaction.id}
                                        className={`grid grid-cols-12 px-6 py-4 border-b border-sand-100 transition-all duration-500 ${
                                            isProcessing 
                                                ? 'bg-mint-50/80 border-l-4 border-l-mint-600' 
                                                : isClassified 
                                                ? `bg-${isBusiness ? 'brand' : 'coral'}-50/80 border-l-4 border-l-${isBusiness ? 'brand' : 'coral'}-600` 
                                                : 'bg-white/80'
                                        } ${isProcessing ? 'animate-pulse' : ''}`}
                                    >
                                        {/* Status */}
                                        <div className="col-span-1 flex items-center">
                                            {isProcessing ? (
                                                <div className="w-3 h-3 bg-mint-600 rounded-full animate-ping"></div>
                                            ) : isClassified ? (
                                                <div className={`w-3 h-3 rounded-full ${isBusiness ? 'bg-brand-600' : 'bg-coral-600'}`}></div>
                                            ) : (
                                                <div className="w-3 h-3 bg-gray-300 rounded-full"></div>
                                            )}
                                        </div>
                                        
                                        {/* Description */}
                                        <div className="col-span-4 flex items-center space-x-3">
                                            <IconComponent className={`h-4 w-4 ${
                                                isProcessing 
                                                    ? 'text-mint-600' 
                                                    : isClassified 
                                                    ? `text-${isBusiness ? 'brand' : 'coral'}-600` 
                                                    : 'text-gray-400'
                                            }`} />
                                            <span className={`text-base font-medium transition-colors duration-300 ${
                                                isProcessing 
                                                    ? 'text-mint-800' 
                                                    : isClassified 
                                                    ? `text-${isBusiness ? 'brand' : 'coral'}-800` 
                                                    : 'text-gray-700'
                                            }`}>
                                                {transaction.description}
                                            </span>
                                        </div>
                                        
                                        {/* Amount */}
                                        <div className="col-span-2 flex items-center">
                                            <span className={`text-base font-semibold transition-colors duration-300 ${
                                                transaction.amount > 0 ? 'text-green-600' : 'text-red-600'
                                            }`}>
                                                {transaction.amount > 0 ? '+' : ''}${Math.abs(transaction.amount).toFixed(2)}
                                            </span>
                                        </div>
                                        
                                        {/* Category */}
                                        <div className="col-span-2 flex items-center">
                                            {isClassified ? (
                                                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                                                    isBusiness 
                                                        ? 'bg-brand-100 text-brand-800' 
                                                        : 'bg-coral-100 text-coral-800'
                                                }`}>
                                                    {transaction.category}
                                                </span>
                                            ) : (
                                                <span className="text-base text-gray-400">—</span>
                                            )}
                                        </div>
                                        
                                        {/* Confidence */}
                                        <div className="col-span-2 flex items-center">
                                            {confidence !== null ? (
                                                <div className="flex items-center space-x-3">
                                                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                                                        <div 
                                                            className={`h-2 rounded-full transition-all duration-500 ${
                                                                isBusiness ? 'bg-brand-600' : 'bg-coral-600'
                                                            }`}
                                                            style={{ width: `${confidence}%` }}
                                                        ></div>
                                                    </div>
                                                    <span className="text-sm font-medium text-gray-600">{confidence}%</span>
                                                </div>
                                            ) : (
                                                <span className="text-base text-gray-400">—</span>
                                            )}
                                        </div>
                                        
                                        {/* Action */}
                                        <div className="col-span-1 flex items-center">
                                            {isClassified ? (
                                                <button className="text-sm text-brand-600 hover:text-brand-800 transition-colors duration-200 underline-offset-2 hover:underline">
                                                    Edit
                                                </button>
                                            ) : (
                                                <span className="text-base text-gray-400">—</span>
                                            )}
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                        
                        {/* Process status */}
                        <div className="text-center">
                            <p className={`text-base font-medium transition-colors duration-300 ${
                                activeStep === 0 ? 'text-brand-700' : 
                                activeStep === 1 ? 'text-mint-700' : 
                                activeStep === 2 ? 'text-coral-700' : 
                                'text-brand-700'
                            }`}>
                                {activeStep === 0 && "📄 Uploading statement..."}
                                {activeStep === 1 && "🤖 AI processing transactions..."}
                                {activeStep === 2 && "👁️ Reviewing classifications..."}
                                {activeStep === 3 && "📊 Generating reports..."}
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Subtle Divider */}
            <div className="border-t border-gray-200/12"></div>

            {/* Analytics Section */}
            <div className="py-12 px-8 animate-slide-up-delay-3">
                <div className="mb-8">
                    <h2 className="text-2xl font-semibold text-gray-800 tracking-tight mb-2">Analytics</h2>
                    <p className="text-lg text-zinc-500 tracking-tight">Visual insights into your transaction data</p>
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-slide-up-delay-3">
                    {/* Pie Chart - Smaller */}
                    <div className="bg-white/80 backdrop-blur-sm shadow-lg rounded-xl border border-white/20 p-8 transition-all duration-500 hover:shadow-xl">
                        <div className="flex items-center mb-6">
                            <div className="p-2 bg-brand-50 rounded-lg mr-3">
                                <ChartPieIcon className="h-6 w-6 text-brand-600" />
                            </div>
                            <h3 className="text-xl font-semibold text-gray-900 tracking-tight">
                        Transaction Distribution
                    </h3>
                        </div>
                        <div className="h-48">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={pieData}
                                    cx="50%"
                                    cy="50%"
                                    labelLine={false}
                                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                                        outerRadius={60}
                                    fill="#8884d8"
                                    dataKey="value"
                                >
                                    {pieData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={index === 0 ? '#4A7C59' : '#EF4444'} />
                                    ))}
                                </Pie>
                                <Tooltip />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                    {/* Tax-Deductible Business Transactions */}
                    <div className="bg-white/80 backdrop-blur-sm shadow-lg rounded-xl border border-white/20 p-8 transition-all duration-500 hover:shadow-xl">
                        <div className="flex items-center mb-6">
                            <div className="p-2 bg-green-50 rounded-lg mr-3">
                                <CurrencyDollarIcon className="h-6 w-6 text-green-600" />
                            </div>
                            <h3 className="text-xl font-semibold text-gray-900 tracking-tight">
                                Tax-Deductible Business
                            </h3>
                        </div>
                        <div className="text-center">
                            <div className="text-4xl font-bold text-green-600 mb-2">
                                {statistics?.business_transactions ? Math.round((statistics.business_transactions / statistics.total_transactions) * 100) : 0}%
                            </div>
                            <p className="text-lg text-gray-600 tracking-tight">
                                of business transactions are tax-deductible
                            </p>
                            <div className="mt-4 bg-green-50 rounded-lg p-4">
                                <p className="text-sm text-green-700">
                                    Based on AI classification and business expense patterns
                                </p>
                            </div>
                        </div>
                    </div>

                    {/* Top 5 Largest Transactions */}
                    <div className="bg-white/80 backdrop-blur-sm shadow-lg rounded-xl border border-white/20 p-8 transition-all duration-500 hover:shadow-xl">
                        <div className="flex items-center mb-6">
                            <div className="p-2 bg-red-50 rounded-lg mr-3">
                                <ChartBarIcon className="h-6 w-6 text-red-600" />
                            </div>
                            <h3 className="text-xl font-semibold text-gray-900 tracking-tight">
                                Top 5 Largest Transactions
                            </h3>
                        </div>
                        <div className="space-y-3">
                            {topTransactions.map((transaction, index) => (
                                <div key={transaction.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                    <div className="flex-1 min-w-0">
                                        <div className="flex items-center space-x-3 mb-1">
                                            <span className="text-sm font-medium text-gray-500">
                                                {new Date(transaction.date).toLocaleDateString()}
                                            </span>
                                            <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                                                transaction.is_business_expense 
                                                    ? 'bg-green-100 text-green-800' 
                                                    : 'bg-red-100 text-red-800'
                                            }`}>
                                                {transaction.is_business_expense ? 'Business' : 'Personal'}
                                            </span>
                                        </div>
                                        <p className="text-sm font-medium text-gray-900 truncate">
                                            {transaction.description}
                                        </p>
                                    </div>
                                    <span className="text-lg font-semibold text-gray-900 ml-4">
                                        ${Math.abs(transaction.amount).toLocaleString()}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* Subtle Divider */}
            <div className="border-t border-gray-200/10"></div>

            {/* Quick Actions Section */}
            <div className="py-12 px-8 animate-slide-up-delay-3">
                <div className="mb-8">
                    <h2 className="text-2xl font-semibold text-gray-800 tracking-tight mb-2">Quick Actions</h2>
                    <p className="text-lg text-zinc-500 tracking-tight">Common tasks to help you get things done</p>
                </div>
                <div className="transition-all duration-500 animate-slide-up-delay-3">
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    <Link
                        to="/transactions"
                            className="group relative rounded-xl border border-sand-200 bg-white/60 px-8 py-6 shadow-lg flex items-center space-x-4 hover:border-brand-200 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-brand-500 transition-all duration-500 transform hover:scale-105 hover:shadow-xl"
                    >
                        <div className="flex-shrink-0">
                                <div className="p-2 bg-brand-50 rounded-lg">
                                    <DocumentTextIcon className="h-7 w-7 text-brand-600 transition-transform duration-300 group-hover:scale-110" />
                                </div>
                        </div>
                        <div className="flex-1 min-w-0">
                            <span className="absolute inset-0" aria-hidden="true" />
                                <p className="text-lg font-medium text-gray-900 tracking-tight group-hover:text-brand-700 transition-colors duration-300">View Transactions</p>
                                <p className="text-lg text-zinc-500 tracking-tight">Browse all transactions</p>
                        </div>
                    </Link>

                    <Link
                        to="/reports"
                            className="group relative rounded-xl border border-sand-200 bg-white/60 px-8 py-6 shadow-lg flex items-center space-x-4 hover:border-brand-200 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-brand-500 transition-all duration-500 transform hover:scale-105 hover:shadow-xl"
                    >
                        <div className="flex-shrink-0">
                                <div className="p-2 bg-brand-50 rounded-lg">
                                    <ChartBarIcon className="h-7 w-7 text-brand-600 transition-transform duration-300 group-hover:scale-110" />
                                </div>
                        </div>
                        <div className="flex-1 min-w-0">
                            <span className="absolute inset-0" aria-hidden="true" />
                                <p className="text-lg font-medium text-gray-900 tracking-tight group-hover:text-brand-700 transition-colors duration-300">Generate Reports</p>
                                <p className="text-lg text-zinc-500 tracking-tight">Export data</p>
                        </div>
                    </Link>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard; 