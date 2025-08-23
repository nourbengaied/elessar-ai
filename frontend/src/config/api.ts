/**
 * API Configuration
 * Handles different environments and deployment scenarios
 */

interface ApiConfig {
    baseURL: string;
    timeout: number;
}

const getApiConfig = (): ApiConfig => {
    // Environment-specific configurations
    const configs = {
        development: {
            baseURL: process.env.REACT_APP_API_URL || 'https://nv9zp49sye.execute-api.eu-west-2.amazonaws.com/prod/',
            timeout: 10000,
        },
        production: {
            baseURL: process.env.REACT_APP_API_URL || 'https://nv9zp49sye.execute-api.eu-west-2.amazonaws.com/prod/',
            timeout: 30000,
        },
        test: {
            baseURL: 'http://localhost:8000',
            timeout: 5000,
        }
    };

    const env = process.env.NODE_ENV as keyof typeof configs || 'development';
    return configs[env] || configs.development;
};

export const apiConfig = getApiConfig();

// Log the configuration in development
if (process.env.NODE_ENV === 'development') {
    console.log('🔧 API Configuration:', apiConfig);
}
