import axios from 'axios';
import config from '../config';

// Create axios instance
const api = axios.create({
  baseURL: config.api.baseUrl,
  timeout: config.api.timeout,
  headers: config.api.headers,
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 400) {
      // Extract error messages from response
      const errorData = error.response.data;
      if (typeof errorData === 'object' && errorData !== null) {
        // Convert field errors to simple list
        const errorMessages = [];
        Object.keys(errorData).forEach(field => {
          const errors = errorData[field];
          if (Array.isArray(errors)) {
            errors.forEach(msg => errorMessages.push(msg));
          } else if (typeof errors === 'string') {
            errorMessages.push(errors);
          }
        });
        error.errorMessages = errorMessages;
      }
    }
    return Promise.reject(error);
  }
);

export default api; 