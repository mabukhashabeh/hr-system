import { defineStore } from 'pinia';
import { ref, computed, readonly } from 'vue';
import { candidateService } from '../services/candidateService';

/**
 * Candidate Store
 * Manages candidate-related state and operations
 */

export const useCandidateStore = defineStore('candidate', () => {
  // State
  const candidates = ref([]);
  const currentCandidate = ref(null);
  const loading = ref(false);
  const error = ref(null);
  const errorMessages = ref([]);
  const pagination = ref({
    count: 0,
    next: null,
    previous: null,
    page: 1,
    pageSize: 10,
  });

  // Filters - only used when explicitly applied
  const activeFilters = ref({});

  // Computed
  const hasCandidates = computed(() => candidates.value.length > 0);
  const totalCandidates = computed(() => pagination.value.count);
  const hasNextPage = computed(() => !!pagination.value.next);
  const hasPreviousPage = computed(() => !!pagination.value.previous);

  // Actions
  const fetchCandidates = async (params = {}) => {
    try {
      loading.value = true;
      error.value = null;
      errorMessages.value = [];

      // Only include non-empty parameters
      const queryParams = Object.fromEntries(
        Object.entries(params).filter(([_, value]) => value !== '' && value !== null && value !== undefined)
      );

      const response = await candidateService.getCandidates(queryParams);
      
      // Handle paginated response
      if (response.results) {
        candidates.value = response.results;
        pagination.value = {
          count: response.count || 0,
          next: response.next,
          previous: response.previous,
          page: params.page || 1,
          pageSize: params.page_size || 10,
        };
        console.log('Pinia: candidates updated:', candidates.value.length, candidates.value);
      } else {
        // Handle non-paginated response (fallback)
        candidates.value = Array.isArray(response) ? response : [response];
        pagination.value = {
          count: candidates.value.length,
          next: null,
          previous: null,
          page: 1,
          pageSize: candidates.value.length,
        };
      }
    } catch (err) {
      error.value = err.message || 'Failed to fetch candidates';
      if (err.errorMessages) {
        errorMessages.value = err.errorMessages;
      }
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const fetchCandidate = async (id) => {
    try {
      loading.value = true;
      error.value = null;
      errorMessages.value = [];

      const candidate = await candidateService.getCandidate(id);
      currentCandidate.value = candidate;
      
      return candidate;
    } catch (err) {
      error.value = err.message || 'Failed to fetch candidate';
      if (err.errorMessages) {
        errorMessages.value = err.errorMessages;
      }
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const createCandidate = async (candidateData) => {
    try {
      loading.value = true;
      error.value = null;
      errorMessages.value = [];

      const candidate = await candidateService.createCandidate(candidateData);
      
      // Add to candidates list
      candidates.value.unshift(candidate);
      pagination.value.count += 1;
      
      return candidate;
    } catch (err) {
      error.value = err.message || 'Failed to create candidate';
      if (err.errorMessages) {
        errorMessages.value = err.errorMessages;
      }
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const updateCandidate = async (id, candidateData) => {
    try {
      loading.value = true;
      error.value = null;
      errorMessages.value = [];

      const updatedCandidate = await candidateService.updateCandidate(id, candidateData);
      
      // Update in candidates list
      const index = candidates.value.findIndex(c => c.id === id);
      if (index !== -1) {
        candidates.value[index] = updatedCandidate;
      }
      
      // Update current candidate if it's the same
      if (currentCandidate.value?.id === id) {
        currentCandidate.value = updatedCandidate;
      }
      
      return updatedCandidate;
    } catch (err) {
      error.value = err.message || 'Failed to update candidate';
      if (err.errorMessages) {
        errorMessages.value = err.errorMessages;
      }
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const deleteCandidate = async (id) => {
    try {
      loading.value = true;
      error.value = null;
      errorMessages.value = {};

      await candidateService.deleteCandidate(id);
      
      // Remove from candidates list
      const index = candidates.value.findIndex(c => c.id === id);
      if (index !== -1) {
        candidates.value.splice(index, 1);
        pagination.value.count -= 1;
      }
      
      // Clear current candidate if it's the same
      if (currentCandidate.value?.id === id) {
        currentCandidate.value = null;
      }
    } catch (err) {
      error.value = err.message || 'Failed to delete candidate';
      if (err.errorMessages) {
        errorMessages.value = err.errorMessages;
      }
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const updateCandidateStatus = async (id, statusData) => {
    try {
      loading.value = true;
      error.value = null;
      errorMessages.value = [];

      const updatedCandidate = await candidateService.updateCandidateStatus(id, statusData);
      // Only update in candidates list if API call succeeded
      const index = candidates.value.findIndex(c => c.id === id);
      if (index !== -1) {
        candidates.value[index] = updatedCandidate;
      }
      // Update current candidate if it's the same
      if (currentCandidate.value?.id === id) {
        currentCandidate.value = updatedCandidate;
      }
      return updatedCandidate;
    } catch (err) {
      // Do NOT set error.value here!
      if (err.errorMessages) {
        errorMessages.value = err.errorMessages;
      }
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const getCandidateStatus = async (email) => {
    try {
      loading.value = true;
      error.value = null;
      errorMessages.value = [];

      const status = await candidateService.getCandidateStatus(email);
      return status;
    } catch (err) {
      error.value = err.message || 'Failed to get candidate status';
      if (err.errorMessages) {
        errorMessages.value = err.errorMessages;
      }
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const downloadResume = async (id, name) => {
    try {
      loading.value = true;
      error.value = null;
      errorMessages.value = [];

      // Get the download URL from the API
      const { download_url } = await candidateService.downloadResume(id);
      if (download_url) {
        // Download the file using the URL
        const link = document.createElement('a');
        link.href = download_url;
        link.download = `${name || 'resume'}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } else {
        throw new Error('Resume download URL not found');
      }
    } catch (err) {
      error.value = err.message || 'Failed to download resume';
      if (err.errorMessages) {
        errorMessages.value = err.errorMessages;
      }
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const setActiveFilters = (filters) => {
    activeFilters.value = { ...filters };
  };

  const clearActiveFilters = () => {
    activeFilters.value = {};
  };

  const clearError = () => {
    error.value = null;
    errorMessages.value = [];
  };

  const clearCurrentCandidate = () => {
    currentCandidate.value = null;
  };

  return {
    // State
    candidates: readonly(candidates),
    currentCandidate: readonly(currentCandidate),
    loading: readonly(loading),
    error: readonly(error),
    errorMessages: readonly(errorMessages),
    pagination: readonly(pagination),
    activeFilters: readonly(activeFilters),

    // Computed
    hasCandidates,
    totalCandidates,
    hasNextPage,
    hasPreviousPage,

    // Actions
    fetchCandidates,
    fetchCandidate,
    createCandidate,
    updateCandidate,
    deleteCandidate,
    updateCandidateStatus,
    getCandidateStatus,
    downloadResume,
    setActiveFilters,
    clearActiveFilters,
    clearError,
    clearCurrentCandidate,
  };
}); 