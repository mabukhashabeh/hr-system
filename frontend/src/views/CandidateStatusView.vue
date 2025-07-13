<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container mx-auto px-4 max-w-3xl">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Check Application Status</h1>
        <p class="text-gray-600">Enter your email address to track your application progress</p>
      </div>

      <!-- Status Check Form -->
      <div class="bg-white rounded-lg shadow-md p-8">
        <Form :validation-schema="statusCheckSchema" @submit="onSubmit" v-slot="{ errors, meta }" novalidate>
          <!-- Email Input -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Email Address *
            </label>
            <Field
              id="email"
              name="email"
              type="email"
              as="input"
              autocomplete="off"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.email }"
              placeholder="Enter your email address"
            />
            <ErrorMessage name="email" v-slot="{ message }">
              <p class="mt-1 text-sm text-red-600">{{ message }}</p>
            </ErrorMessage>
          </div>

          <!-- Submit Button -->
          <div class="flex items-center justify-between pt-6">
            <router-link
              to="/"
              class="text-blue-600 hover:text-blue-500 font-medium"
            >
              Back to Home
            </router-link>
            <button
              type="submit"
              :disabled="meta.validating || meta.submitting"
              class="bg-green-600 text-white px-6 py-2 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="meta.submitting">Checking...</span>
              <span v-else>Check Status</span>
            </button>
          </div>

          <!-- Error Messages -->
          <div v-if="errorMessages.length > 0" class="bg-red-50 border border-red-200 rounded-md p-4 mt-4">
            <ul class="list-disc list-inside text-sm text-red-600">
              <li v-for="message in errorMessages" :key="message">{{ message }}</li>
            </ul>
          </div>

          <!-- General Error Message -->
          <div v-if="submitError && errorMessages.length === 0" class="bg-red-50 border border-red-200 rounded-md p-4 mt-4">
            <p class="text-sm text-red-600">{{ submitError }}</p>
          </div>
        </Form>

        <!-- Status Results -->
        <div v-if="candidateStatus" class="mt-8 border-t pt-8">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Application Status</h2>
          <div class="bg-gray-50 rounded-lg p-6 space-y-4">
            <!-- Candidate Info -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <h3 class="text-sm font-medium text-gray-500">Full Name</h3>
                <p class="text-lg font-semibold text-gray-900">{{ candidateStatus?.full_name || 'N/A' }}</p>
              </div>
              <div>
                <h3 class="text-sm font-medium text-gray-500">Email</h3>
                <p class="text-lg font-semibold text-gray-900">{{ candidateStatus?.email || 'N/A' }}</p>
              </div>
              <div>
                <h3 class="text-sm font-medium text-gray-500">Phone</h3>
                <p class="text-lg font-semibold text-gray-900">{{ candidateStatus?.phone || 'N/A' }}</p>
              </div>
              <div>
                <h3 class="text-sm font-medium text-gray-500">Department</h3>
                <p class="text-lg font-semibold text-gray-900">{{ candidateStatus?.department || 'N/A' }}</p>
              </div>
              <div>
                <h3 class="text-sm font-medium text-gray-500">Years of Experience</h3>
                <p class="text-lg font-semibold text-gray-900">{{ candidateStatus?.years_of_experience != null ? candidateStatus.years_of_experience + ' years' : 'N/A' }}</p>
              </div>
              <div>
                <h3 class="text-sm font-medium text-gray-500">Application Date</h3>
                <p class="text-lg font-semibold text-gray-900">{{ formatDate(candidateStatus?.created_at) }}</p>
              </div>
            </div>

            <!-- Current Status -->
            <div class="border-t pt-4 mb-4">
              <h3 class="text-sm font-medium text-gray-500 mb-2">Current Status</h3>
              <div class="flex items-center space-x-2">
                <span
                  class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
                  :class="getStatusColorClass(candidateStatus?.current_status)"
                >
                  {{ candidateStatus?.current_status_display || getStatusLabel(candidateStatus?.current_status) }}
                </span>
              </div>
            </div>

            <!-- Status History -->
            <div v-if="candidateStatus?.status_history?.length" class="border-t pt-4">
              <h3 class="text-sm font-medium text-gray-500 mb-2">Status History</h3>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200 text-sm">
                  <thead class="bg-gray-100">
                    <tr>
                      <th class="px-4 py-2 text-left font-semibold">Date</th>
                      <th class="px-4 py-2 text-left font-semibold">Previous Status</th>
                      <th class="px-4 py-2 text-left font-semibold">New Status</th>
                      <th class="px-4 py-2 text-left font-semibold">Feedback</th>
                      <th class="px-4 py-2 text-left font-semibold">Admin Name</th>
                      <th class="px-4 py-2 text-left font-semibold">Admin Email</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="history in candidateStatus.status_history" :key="history.id" class="hover:bg-gray-50">
                      <td class="px-4 py-2">{{ formatDate(history.created_at) }}</td>
                      <td class="px-4 py-2">{{ history.previous_status || '-' }}</td>
                      <td class="px-4 py-2">{{ history.new_status || '-' }}</td>
                      <td class="px-4 py-2">{{ history.feedback || '-' }}</td>
                      <td class="px-4 py-2">{{ history.admin_name || '-' }}</td>
                      <td class="px-4 py-2">{{ history.admin_email || '-' }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Resume Download -->
            <div v-if="candidateStatus?.resume" class="border-t pt-4">
              <h3 class="text-sm font-medium text-gray-500 mb-2">Resume</h3>
              <button
                @click="downloadResume"
                class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                Download Resume
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {computed, ref} from 'vue';
import {ErrorMessage, Field, Form} from 'vee-validate';
import {statusCheckSchema} from '../validations/candidateSchemas';
import {useCandidateStore} from '../stores/candidateStore';

const candidateStore = useCandidateStore();
const candidateStatus = ref(null);
const submitError = ref(null);

// Get error messages from store
const errorMessages = computed(() => candidateStore.errorMessages);

const onSubmit = async (values, { resetForm }) => {
  submitError.value = null;
  candidateStore.clearError(); // Clear previous errors
  
  try {
    candidateStatus.value = await candidateStore.getCandidateStatus(values.email);
    resetForm();
  } catch (error) {
    // Check if there are specific error messages from API
    if (errorMessages.value.length > 0) {
      // Error messages are already set in the store
      return;
    }
    
    // Set general error message
    submitError.value = error.message || 'Failed to check status. Please try again.';
  }
};

const downloadResume = async () => {
  if (candidateStatus.value?.id) {
    try {
      await candidateStore.downloadResume(candidateStatus.value.id);
    } catch (error) {
      console.error('Resume download error:', error.message);
    }
  }
};

const getStatusColorClass = (status) => {
  const colorMap = {
    applied: 'bg-blue-100 text-blue-800',
    reviewing: 'bg-yellow-100 text-yellow-800',
    interviewed: 'bg-orange-100 text-orange-800',
    shortlisted: 'bg-purple-100 text-purple-800',
    hired: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800',
    submitted: 'bg-blue-100 text-blue-800',
    Submitted: 'bg-blue-100 text-blue-800',
  };
  return colorMap[status] || 'bg-gray-100 text-gray-800';
};

const getStatusLabel = (status) => {
  const labelMap = {
    applied: 'Applied',
    reviewing: 'Under Review',
    interviewed: 'Interviewed',
    rejected: 'Rejected',
    submitted: 'Submitted',
  };
  return labelMap[status] || status;
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};
</script> 