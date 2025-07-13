<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow">
      <div class="container mx-auto px-4 py-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
            <p class="text-gray-600">Manage candidates and review applications</p>
          </div>
          <router-link
            to="/"
            class="text-blue-600 hover:text-blue-500 font-medium"
          >
            Back to Home
          </router-link>
        </div>
      </div>
    </div>

    <div class="container mx-auto px-4 py-8">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-2 bg-blue-100 rounded-lg">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Total Candidates</p>
              <p class="text-2xl font-semibold text-gray-900">{{ totalCandidates }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-2 bg-green-100 rounded-lg">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Accepted</p>
              <p class="text-2xl font-semibold text-gray-900">{{ getStatusCount('accepted') }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-2 bg-yellow-100 rounded-lg">
              <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Under Review</p>
              <p class="text-2xl font-semibold text-gray-900">{{ getStatusCount('under_review') }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-2 bg-orange-100 rounded-lg">
              <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Interview Scheduled</p>
              <p class="text-2xl font-semibold text-gray-900">{{ getStatusCount('interview_scheduled') }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="bg-white rounded-lg shadow p-6 mb-8">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Filters</h2>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Name</label>
            <input
              v-model="filters.full_name"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Search by name"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input
              v-model="filters.email"
              type="email"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Search by email"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
            <select
              v-model="filters.current_status"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Statuses</option>
              <option value="submitted">Submitted</option>
              <option value="under_review">Under Review</option>
              <option value="interview_scheduled">Interview Scheduled</option>
              <option value="accepted">Accepted</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Department</label>
            <select
              v-model="filters.department"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Departments</option>
              <option value="it">IT</option>
              <option value="hr">HR</option>
              <option value="finance">Finance</option>
            </select>
          </div>
        </div>
        <div class="flex justify-end mt-4 space-x-3">
          <button
            @click="clearFilters"
            class="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
          >
            Clear Filters
          </button>
          <button
            @click="applyFilters"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Apply Filters
          </button>
          <button
            @click="() => fetchCandidates()"
            class="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300"
            title="Refresh candidate list"
          >
            Refresh
          </button>
        </div>
      </div>

      <!-- Candidates Table -->
      <div class="bg-white rounded-lg shadow">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">Candidates</h2>
        </div>
        
        <div v-if="loading" class="p-8 text-center">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p class="mt-2 text-gray-600">Loading candidates...</p>
        </div>

        <div v-else-if="error" class="p-8 text-center">
          <p class="text-red-600">{{ error }}</p>
          <button
            @click="fetchCandidates"
            class="mt-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Retry
          </button>
        </div>

        <div v-else-if="!hasCandidates" class="p-8 text-center">
          <p class="text-gray-600">No candidates found.</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider max-w-md whitespace-nowrap">
                  Candidate
                </th>
                <th class="px-2 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider max-w-md whitespace-nowrap">
                  Contact
                </th>
                <th class="px-2 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider max-w-xs whitespace-nowrap">
                  Department
                </th>
                <th class="px-2 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider max-w-xs whitespace-nowrap">
                  Experience
                </th>
                <th class="px-2 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider max-w-xs whitespace-nowrap">
                  Status
                </th>
                <th class="px-2 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider max-w-xs whitespace-nowrap">
                  Applied
                </th>
                <th class="px-2 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider max-w-xs whitespace-nowrap">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="candidate in candidates" :key="candidate.id" class="hover:bg-gray-50">
                <td class="px-3 py-4 whitespace-nowrap max-w-md overflow-hidden text-ellipsis">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10">
                      <div class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                        <span class="text-sm font-medium text-gray-700">
                          {{ candidate.full_name ? candidate.full_name.charAt(0) : '' }}
                        </span>
                      </div>
                    </div>
                    <div class="ml-2">
                      <div class="text-sm font-medium text-gray-900 truncate max-w-[12rem]">{{ candidate.full_name || 'N/A' }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-2 py-4 whitespace-nowrap max-w-md overflow-hidden text-ellipsis">
                  <div class="text-sm text-gray-900 truncate max-w-[12rem]">{{ candidate.email || 'N/A' }}</div>
                  <div class="text-sm text-gray-500 truncate max-w-[12rem]">{{ candidate.phone || 'N/A' }}</div>
                </td>
                <td class="px-2 py-4 whitespace-nowrap text-sm text-gray-900 max-w-xs overflow-hidden text-ellipsis">
                  {{ candidate.department || 'N/A' }}
                </td>
                <td class="px-2 py-4 whitespace-nowrap text-sm text-gray-900 max-w-xs overflow-hidden text-ellipsis">
                  {{ candidate.years_of_experience != null ? candidate.years_of_experience + ' years' : 'N/A' }}
                </td>
                <td class="px-2 py-4 whitespace-nowrap max-w-xs overflow-hidden text-ellipsis">
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="getStatusColorClass(candidate.current_status)"
                  >
                    {{ getStatusLabel(candidate.current_status) }}
                  </span>
                </td>
                <td class="px-2 py-4 whitespace-nowrap text-sm text-gray-500 max-w-xs overflow-hidden text-ellipsis">
                  {{ formatAppliedDate(candidate.created_at) }}
                </td>
                <td class="px-2 py-4 whitespace-nowrap text-sm font-medium max-w-xs overflow-hidden text-ellipsis">
                  <div class="flex space-x-2">
                    <button
                      @click="downloadResume(candidate.id, candidate.full_name)"
                      class="text-green-600 hover:text-green-900 p-1 rounded"
                      title="Download Resume"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                      </svg>
                    </button>
                    <button
                      @click="openStatusModal(candidate)"
                      class="text-purple-600 hover:text-purple-900 p-1 rounded"
                      title="Update Status"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="hasCandidates" class="px-6 py-4 border-t border-gray-200">
          <div class="flex items-center justify-between">
            <div class="text-sm text-gray-700">
              Showing {{ candidates.length }} of {{ totalCandidates }} candidates
            </div>
            <div class="flex space-x-2">
              <button
                @click="previousPage"
                :disabled="!hasPreviousPage"
                class="px-3 py-1 border border-gray-300 rounded-md text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <button
                @click="nextPage"
                :disabled="!hasNextPage"
                class="px-3 py-1 border border-gray-300 rounded-md text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Status Update Modal -->
    <div v-if="showStatusModal" :key="selectedCandidate?.id" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Update Status</h3>
          <form @submit="handleStatusUpdate" class="space-y-4" novalidate>
            <div v-if="formErrors.backend" class="text-red-600 text-sm mb-2 p-2 bg-red-50 border border-red-200 rounded">{{ formErrors.backend }}</div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">New Status</label>
              <select
                v-model="statusFormData.new_status"
                class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                :class="formErrors.new_status ? 'border-red-300 focus:ring-red-500' : 'border-gray-300'"
                @blur="validateField('new_status', statusFormData.new_status)"
                @input="formErrors.backend = ''"
                required
              >
                <option value="">Select status</option>
                <option value="submitted">Submitted</option>
                <option value="under_review">Under Review</option>
                <option value="interview_scheduled">Interview Scheduled</option>
                <option value="accepted">Accepted</option>
                <option value="rejected">Rejected</option>
              </select>
              <div v-if="formErrors.new_status" class="text-red-600 text-xs mt-1">{{ formErrors.new_status }}</div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Admin Name</label>
              <input
                v-model="statusFormData.admin_name"
                type="text"
                class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                :class="formErrors.admin_name ? 'border-red-300 focus:ring-red-500' : 'border-gray-300'"
                @blur="validateField('admin_name', statusFormData.admin_name)"
                @input="formErrors.backend = ''"
                required
              />
              <div v-if="formErrors.admin_name" class="text-red-600 text-xs mt-1">{{ formErrors.admin_name }}</div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Admin Email</label>
              <input
                v-model="statusFormData.admin_email"
                type="email"
                class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                :class="formErrors.admin_email ? 'border-red-300 focus:ring-red-500' : 'border-gray-300'"
                @blur="validateField('admin_email', statusFormData.admin_email)"
                @input="formErrors.backend = ''"
                required
              />
              <div v-if="formErrors.admin_email" class="text-red-600 text-xs mt-1">{{ formErrors.admin_email }}</div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Feedback</label>
              <textarea
                v-model="statusFormData.feedback"
                rows="3"
                class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                :class="formErrors.feedback ? 'border-red-300 focus:ring-red-500' : 'border-gray-300'"
                @blur="validateField('feedback', statusFormData.feedback)"
                @input="formErrors.backend = ''"
                required
              ></textarea>
              <div v-if="formErrors.feedback" class="text-red-600 text-xs mt-1">{{ formErrors.feedback }}</div>
            </div>
            <div class="flex justify-end space-x-3">
              <button
                type="button"
                @click="closeStatusModal"
                class="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="!canSubmit"
              >
                {{ isSubmitting ? 'Updating...' : 'Update Status' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useCandidateStore } from '../stores/candidateStore';
import { storeToRefs } from 'pinia';

const candidateStore = useCandidateStore();
const {
  candidates,
  loading,
  error,
  totalCandidates,
  hasCandidates,
  hasNextPage,
  hasPreviousPage,
  pagination,
} = storeToRefs(candidateStore);

// Reactive data
const filters = reactive({
  full_name: '',
  email: '',
  current_status: '',
  department: '',
});

// Status update form data
const statusFormData = reactive({
  new_status: '',
  admin_name: '',
  admin_email: '',
  feedback: '',
});

// Form validation errors
const formErrors = reactive({
  new_status: '',
  admin_name: '',
  admin_email: '',
  feedback: '',
  backend: '',
});

const showStatusModal = ref(false);
const selectedCandidate = ref(null);
const isSubmitting = ref(false);

// Add this computed property after your other refs
const canSubmit = computed(() => !formErrors.backend && !isSubmitting.value);

// Validation functions
const validateField = (field, value) => {
  formErrors[field] = '';
  
  switch (field) {
    case 'new_status':
      if (!value) formErrors[field] = 'Status is required.';
      break;
    case 'admin_name':
      if (!value) formErrors[field] = 'Admin name is required.';
      else if (value.length < 2) formErrors[field] = 'Admin name must be at least 2 characters.';
      break;
    case 'admin_email':
      if (!value) formErrors[field] = 'Admin email is required.';
      else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) formErrors[field] = 'Please enter a valid email address.';
      break;
    case 'feedback':
      if (!value) formErrors[field] = 'Feedback is required.';
      else if (value.length < 10) formErrors[field] = 'Feedback must be at least 10 characters.';
      break;
  }
};

const validateForm = () => {
  validateField('new_status', statusFormData.new_status);
  validateField('admin_name', statusFormData.admin_name);
  validateField('admin_email', statusFormData.admin_email);
  validateField('feedback', statusFormData.feedback);
  
  return !Object.values(formErrors).some(error => error !== '');
};

const openStatusModal = (candidate) => {
  selectedCandidate.value = candidate;
  showStatusModal.value = true;
  
  // Initialize form data
  statusFormData.new_status = candidate.current_status || '';
  statusFormData.admin_name = '';
  statusFormData.admin_email = '';
  statusFormData.feedback = '';
  
  // Clear all errors
  Object.keys(formErrors).forEach(key => {
    formErrors[key] = '';
  });
};

const closeStatusModal = () => {
  showStatusModal.value = false;
  selectedCandidate.value = null;
  isSubmitting.value = false;
  
  // Clear form data
  Object.keys(statusFormData).forEach(key => {
    statusFormData[key] = '';
  });
  
  // Clear all errors
  Object.keys(formErrors).forEach(key => {
    formErrors[key] = '';
  });
};

const handleStatusUpdate = async (event) => {
  event.preventDefault();
  console.log('Submitting status update:', JSON.parse(JSON.stringify(statusFormData)));

  if (!selectedCandidate.value) return;

  // Validate form
  if (!validateForm()) {
    return;
  }

  try {
    isSubmitting.value = true;
    formErrors.backend = '';
    await candidateStore.updateCandidateStatus(selectedCandidate.value.id, statusFormData);
    closeStatusModal();
    fetchCandidates(); // Only refresh after success
  } catch (error) {
    console.error('Error updating status:', error);
    isSubmitting.value = false;
    // Handle backend errors
    if (candidateStore.errorMessages && candidateStore.errorMessages.length > 0) {
      formErrors.backend = candidateStore.errorMessages.join(', ');
    } else if (error.message) {
      formErrors.backend = error.message;
    } else {
      formErrors.backend = 'Failed to update status. Please try again.';
    }
    // Do NOT reset/clear form data here
  }
};

// Methods
const fetchCandidates = (params = {}) => {
  // Only include non-empty parameters
  const queryParams = {};
  Object.entries(params).forEach(([key, value]) => {
    if (value !== '' && value !== null && value !== undefined) {
      queryParams[key] = value;
    }
  });
  candidateStore.fetchCandidates(queryParams);
};

const applyFilters = () => {
  // Only include non-empty filters
  const queryParams = {};
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== '' && value !== null && value !== undefined) {
      queryParams[key] = value;
    }
  });
  
  // Set active filters in store
  candidateStore.setActiveFilters(queryParams);
  
  // Fetch with filters
  fetchCandidates(queryParams);
};

const clearFilters = () => {
  candidateStore.clearActiveFilters();
  Object.assign(filters, {
    full_name: '',
    email: '',
    current_status: '',
    department: '',
  });
  fetchCandidates(); // No filters
};

const nextPage = () => {
  if (hasNextPage.value) {
    const nextPageNum = pagination.value.page + 1;
    const params = { page: nextPageNum };
    
    // Include active filters if any
    if (Object.keys(candidateStore.activeFilters).length > 0) {
      Object.assign(params, candidateStore.activeFilters);
    }
    
    fetchCandidates(params);
  }
};

const previousPage = () => {
  if (hasPreviousPage.value) {
    const prevPageNum = pagination.value.page - 1;
    const params = { page: prevPageNum };
    
    // Include active filters if any
    if (Object.keys(candidateStore.activeFilters).length > 0) {
      Object.assign(params, candidateStore.activeFilters);
    }
    
    fetchCandidates(params);
  }
};

const downloadResume = async (id, name) => {
  try {
    await candidateStore.downloadResume(id, name);
  } catch (error) {
    console.error('Error downloading resume:', error);
  }
};

const getStatusCount = (status) => {
  return (candidates.value || []).filter(c => c.current_status === status).length;
};

const getStatusColorClass = (status) => {
  const colorMap = {
    submitted: 'bg-blue-100 text-blue-800',
    under_review: 'bg-yellow-100 text-yellow-800',
    interview_scheduled: 'bg-orange-100 text-orange-800',
    accepted: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800',
  };
  return colorMap[status] || 'bg-gray-100 text-gray-800';
};

const getStatusLabel = (status) => {
  const labelMap = {
    submitted: 'Submitted',
    under_review: 'Under Review',
    interview_scheduled: 'Interview Scheduled',
    accepted: 'Accepted',
    rejected: 'Rejected',
  };
  return labelMap[status] || status;
};

const formatAppliedDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  // Format: YYYY-MM-DD hh:mm am/pm
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  let h = date.getHours();
  const min = String(date.getMinutes()).padStart(2, '0');
  const ampm = h >= 12 ? 'pm' : 'am';
  h = h % 12;
  h = h ? h : 12;
  return `${y}-${m}-${d} ${String(h).padStart(2, '0')}:${min} ${ampm}`;
};

// Lifecycle
onMounted(() => {
  fetchCandidates(); // Initial load with no filters
});
</script> 