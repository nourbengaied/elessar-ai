// API Response Types
export interface User {
    id: string;
    email: string;
    first_name?: string;
    last_name?: string;
    business_name?: string;
    tax_id?: string;
    created_at: string;
}

export interface LoginResponse {
    access_token: string;
    token_type: string;
    user_id: string;
    email: string;
}

export interface RegisterResponse {
    access_token: string;
    token_type: string;
    user_id: string;
    email: string;
}

export interface Transaction {
    id: string;
    date: string;
    description: string;
    amount: number;
    currency: string;
    merchant: string;
    category?: string;
    is_business_expense: boolean;
    confidence_score?: number;
    manually_overridden?: boolean;
    llm_reasoning?: string;
    created_at: string;
}

export interface TransactionsResponse {
    transactions: Transaction[];
    limit: number;
    offset: number;
    count: number;
}

export interface Statistics {
    total_transactions: number;
    business_transactions: number;
    personal_transactions: number;
    total_amount: number;
    business_amount: number;
    personal_amount: number;
    monthly_breakdown: Array<{
        month: string;
        business: number;
        personal: number;
    }>;
}

export interface UploadResult {
    processed_count: number;
    errors: string[];
    transactions: Transaction[];
} 