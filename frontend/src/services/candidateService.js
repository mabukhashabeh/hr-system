import api from './api';

/**
 * Candidate Service
 * Handles all candidate-related API operations
 */

const adminHeaders = { 'X-ADMIN': '1' };

export const candidateService = {
  /**
   * Get all candidates with filtering and pagination
   * @param {Object} params - Query parameters for filtering and pagination
   * @returns {Promise<Object>} - Paginated candidates data
   */
  getCandidates: async (params = {}) => {
    const response = await api.get('/candidates/', { params, headers: adminHeaders });
    return response.data;
  },

  /**
   * Get a single candidate by ID
   * @param {string|number} id - Candidate ID
   * @returns {Promise<Object>} - Candidate data
   */
  getCandidate: async (id) => {
    const response = await api.get(`/candidates/${id}/`, { headers: adminHeaders });
    return response.data;
  },

  /**
   * Create a new candidate
   * @param {Object} candidateData - Candidate data including resume file
   * @returns {Promise<Object>} - Created candidate data
   */
  createCandidate: async (candidateData) => {
    const formData = new FormData();
    
    // Add candidate data to form
    Object.keys(candidateData).forEach(key => {
      if (key === 'resume' && candidateData[key]) {
        formData.append('resume', candidateData[key]);
      } else if (candidateData[key] !== null && candidateData[key] !== undefined) {
        formData.append(key, candidateData[key]);
      }
    });

    const response = await api.post('/candidates/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Update a candidate
   * @param {string|number} id - Candidate ID
   * @param {Object} candidateData - Updated candidate data
   * @returns {Promise<Object>} - Updated candidate data
   */
  updateCandidate: async (id, candidateData) => {
    const formData = new FormData();
    
    // Add candidate data to form
    Object.keys(candidateData).forEach(key => {
      if (key === 'resume' && candidateData[key]) {
        formData.append('resume', candidateData[key]);
      } else if (candidateData[key] !== null && candidateData[key] !== undefined) {
        formData.append(key, candidateData[key]);
      }
    });

    const response = await api.patch(`/candidates/${id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data', ...adminHeaders
      },
    });
    return response.data;
  },

  /**
   * Delete a candidate
   * @param {string|number} id - Candidate ID
   * @returns {Promise<Object>} - Deletion response
   */
  deleteCandidate: async (id) => {
    const response = await api.delete(`/candidates/${id}/`, { headers: adminHeaders });
    return response.data;
  },

  /**
   * Get candidate status by email
   * @param {string} email - Candidate email
   * @returns {Promise<Object>} - Candidate status data
   */
  getCandidateStatus: async (email) => {
    const response = await api.get(`/candidates/status/`, { 
      params: { email } 
    });
    return response.data;
  },

  /**
   * Download candidate resume
   * @param {string|number} id - Candidate ID
   * @returns {Promise<string>} - Resume file url
   */
  downloadResume: async (id) => {
    const response = await api.get(`/candidates/${id}/resume/`, { headers: adminHeaders });
    return response.data;
  },

  /**
   * Update candidate status (admin only)
   * @param {string|number} id - Candidate ID
   * @param {Object} statusData - Status update data
   * @returns {Promise<Object>} - Updated candidate data
   */
  updateCandidateStatus: async (id, statusData) => {
    const response = await api.patch(`/candidates/${id}/`, statusData, { headers: adminHeaders });
    return response.data;
  },
};