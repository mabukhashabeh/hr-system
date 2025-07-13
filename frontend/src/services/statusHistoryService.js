import api from './api';

/**
 * Status History Service
 * Handles all status history-related API operations (admin only)
 */

export const statusHistoryService = {
  /**
   * Get all status history with filtering and pagination
   * @param {Object} params - Query parameters for filtering and pagination
   * @returns {Promise<Object>} - Paginated status history data
   */
  getStatusHistory: async (params = {}) => {
    const response = await api.get('/status-history/', { params });
    return response.data;
  },

  /**
   * Get status history for a specific candidate
   * @param {string|number} candidateId - Candidate ID
   * @returns {Promise<Object>} - Status history data for the candidate
   */
  getCandidateStatusHistory: async (candidateId) => {
    const response = await api.get(`/candidates/${candidateId}/status-history/`);
    return response.data;
  },

  /**
   * Update candidate status by email (admin only)
   * @param {string} email - Candidate email
   * @param {Object} statusData - Status update data
   * @returns {Promise<Object>} - Updated status data
   */
  updateStatusByEmail: async (email, statusData) => {
    const response = await api.patch('/status-history/', {
      email,
      ...statusData,
    });
    return response.data;
  },

  /**
   * Get status by email
   * @param {string} email - Candidate email
   * @returns {Promise<Object>} - Status data
   */
  getStatusByEmail: async (email) => {
    const response = await api.get('/status-history/', { 
      params: { email } 
    });
    return response.data;
  },
}; 