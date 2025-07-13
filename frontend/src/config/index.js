/**
 * Application Configuration
 * Centralized configuration management for the HR System frontend
 */

const config = {
  // API Configuration
  api: {
    baseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
    timeout: parseInt(import.meta.env.VITE_API_TIMEOUT) || 10000,
    headers: {
      'Content-Type': 'application/json',
    },
  },

  // App Configuration
  app: {
    title: import.meta.env.VITE_APP_TITLE || 'HR Candidate Management System',
    version: import.meta.env.VITE_APP_VERSION || '1.0.0',
    debug: import.meta.env.VITE_DEBUG_MODE === 'true',
    enableLogging: import.meta.env.VITE_ENABLE_LOGGING === 'true',
  },

  // Feature Flags
  features: {
    fileUpload: import.meta.env.VITE_ENABLE_FILE_UPLOAD !== 'false',
    advancedFilters: import.meta.env.VITE_ENABLE_ADVANCED_FILTERS !== 'false',
    exportFeatures: import.meta.env.VITE_ENABLE_EXPORT_FEATURES !== 'false',
  },

  // File Upload Configuration
  upload: {
    maxSize: parseInt(import.meta.env.VITE_MAX_FILE_SIZE) || 5242880, // 5MB
    allowedTypes: (import.meta.env.VITE_ALLOWED_FILE_TYPES || '.pdf,.doc,.docx').split(','),
    maxFiles: 1,
  },

  // Pagination
  pagination: {
    defaultPageSize: 10,
    pageSizeOptions: [5, 10, 20, 50],
  },

  // Validation
  validation: {
    email: {
      pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      message: 'Please enter a valid email address',
    },
    phone: {
      pattern: /^[\+]?[1-9][\d]{0,15}$/,
      message: 'Please enter a valid phone number',
    },
    name: {
      minLength: 2,
      maxLength: 100,
      pattern: /^[a-zA-Z\s]+$/,
      message: 'Name must be 2-100 characters and contain only letters and spaces',
    },
  },

  // Status Options
statusOptions: [
  { value: 'submitted', label: 'Submitted', color: 'blue' },
  { value: 'under_review', label: 'Under Review', color: 'yellow' },
  { value: 'interview_scheduled', label: 'Interview Scheduled', color: 'orange' },
  { value: 'accepted', label: 'Accepted', color: 'green' },
  { value: 'rejected', label: 'Rejected', color: 'red' },
],

  // UI Configuration
  ui: {
    theme: {
      primary: '#3B82F6',
      secondary: '#6B7280',
      success: '#10B981',
      warning: '#F59E0B',
      error: '#EF4444',
      info: '#3B82F6',
    },
    breakpoints: {
      sm: 640,
      md: 768,
      lg: 1024,
      xl: 1280,
    },
  },
};

export default config;

// Helper functions
export const getApiUrl = (endpoint) => {
  const baseUrl = config.api.baseUrl.replace(/\/$/, '');
  const cleanEndpoint = endpoint.replace(/^\//, '');
  return `${baseUrl}/${cleanEndpoint}`;
};

export const getStatusColor = (status) => {
  const statusOption = config.statusOptions.find(option => option.value === status);
  return statusOption ? statusOption.color : 'gray';
};

export const getStatusLabel = (status) => {
  const statusOption = config.statusOptions.find(option => option.value === status);
  return statusOption ? statusOption.label : status;
};

export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

export const validateFile = (file) => {
  const { maxSize, allowedTypes } = config.upload;
  
  if (file.size > maxSize) {
    return { valid: false, message: `File size must be less than ${formatFileSize(maxSize)}` };
  }
  
  const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
  if (!allowedTypes.includes(fileExtension)) {
    return { valid: false, message: `File type not allowed. Allowed types: ${allowedTypes.join(', ')}` };
  }
  
  return { valid: true };
}; 