<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container mx-auto px-4 max-w-2xl">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Candidate Registration</h1>
        <p class="text-gray-600">Submit your application for consideration</p>
      </div>

      <!-- Registration Form -->
      <div class="bg-white rounded-lg shadow-md p-8">
        <Form 
          :validation-schema="candidateRegistrationSchema" 
          @submit="onSubmit" 
          v-slot="{ errors, meta, setFieldValue, setFieldError, touched }" 
          novalidate
        >
          <!-- Full Name -->
          <div>
            <label for="full_name" class="block text-sm font-medium text-gray-700 mb-2">
              Full Name *
            </label>
            <Field
              id="full_name"
              name="full_name"
              as="input"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.full_name }"
              placeholder="Enter your full name"
            />
            <ErrorMessage name="full_name" v-slot="{ message }">
              <p class="mt-1 text-sm text-red-600">{{ message }}</p>
            </ErrorMessage>
          </div>

          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Email Address *
            </label>
            <Field
              id="email"
              name="email"
              as="input"
              type="email"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.email }"
              placeholder="Enter your email address"
            />
            <ErrorMessage name="email" v-slot="{ message }">
              <p class="mt-1 text-sm text-red-600">{{ message }}</p>
            </ErrorMessage>
          </div>

          <!-- Phone -->
          <div>
            <label for="phone" class="block text-sm font-medium text-gray-700 mb-2">
              Phone Number *
            </label>
            <Field
              id="phone"
              name="phone"
              as="input"
              type="tel"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.phone }"
              placeholder="Enter your phone number"
            />
            <ErrorMessage name="phone" v-slot="{ message }">
              <p class="mt-1 text-sm text-red-600">{{ message }}</p>
            </ErrorMessage>
          </div>

          <!-- Date of Birth -->
          <div>
            <label for="date_of_birth" class="block text-sm font-medium text-gray-700 mb-2">
              Date of Birth *
            </label>
            <Field
              id="date_of_birth"
              name="date_of_birth"
              as="input"
              type="date"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.date_of_birth }"
            />
            <ErrorMessage name="date_of_birth" v-slot="{ message }">
              <p class="mt-1 text-sm text-red-600">{{ message }}</p>
            </ErrorMessage>
          </div>

          <!-- Years of Experience -->
          <div>
            <label for="years_of_experience" class="block text-sm font-medium text-gray-700 mb-2">
              Years of Experience *
            </label>
            <Field
              id="years_of_experience"
              name="years_of_experience"
              as="input"
              type="number"
              min="0"
              max="50"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.years_of_experience }"
              placeholder="Enter years of experience"
            />
            <ErrorMessage name="years_of_experience" v-slot="{ message }">
              <p class="mt-1 text-sm text-red-600">{{ message }}</p>
            </ErrorMessage>
          </div>

          <!-- Department -->
          <div>
            <label for="department" class="block text-sm font-medium text-gray-700 mb-2">
              Department *
            </label>
            <Field
              id="department"
              name="department"
              as="select"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.department }"
            >
              <option value="">Select department</option>
              <option value="it">Information Technology</option>
              <option value="hr">Human Resources</option>
              <option value="finance">Finance</option>
            </Field>
            <ErrorMessage name="department" v-slot="{ message }">
              <p class="mt-1 text-sm text-red-600">{{ message }}</p>
            </ErrorMessage>
          </div>

          <!-- Resume Upload -->
          <div>
            <label for="resume" class="block text-sm font-medium text-gray-700 mb-2">
              Resume *
            </label>
            <div
              class="border-2 border-dashed border-gray-300 rounded-md p-6 text-center"
              :class="{ 'border-red-500': errors?.resume }"
            >
              <input
                id="resume"
                ref="fileInput"
                type="file"
                accept=".pdf,.doc,.docx"
                @change="(event) => handleFileChange(event, setFieldValue, setFieldError)"
                class="hidden"
              />
              <div v-if="!selectedFile" class="space-y-2">
                <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                  <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <div class="text-sm text-gray-600">
                  <button
                    type="button"
                    @click="$refs.fileInput.click()"
                    class="font-medium text-blue-600 hover:text-blue-500"
                  >
                    Click to upload
                  </button>
                  <span class="ml-1">or drag and drop</span>
                </div>
                <p class="text-xs text-gray-500">PDF, DOC, DOCX up to 10MB</p>
              </div>
              <div v-else class="space-y-2">
                <div class="flex items-center justify-center">
                  <svg class="h-8 w-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                </div>
                <p class="text-sm text-gray-600">{{ selectedFile.name }}</p>
                <p class="text-xs text-gray-500">{{ formatFileSize(selectedFile.size) }}</p>
                <button
                  type="button"
                  @click="() => removeFile(setFieldValue)"
                  class="text-sm text-red-600 hover:text-red-500"
                >
                  Remove file
                </button>
              </div>
            </div>
            <ErrorMessage name="resume" v-slot="{ message }">
              <p v-if="message" class="mt-1 text-sm text-red-600">{{ message }}</p>
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
              class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="meta.submitting">Submitting...</span>
              <span v-else>Submit Application</span>
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

          <!-- Success Message -->
          <div v-if="submitSuccess" class="bg-green-50 border border-green-200 rounded-md p-4 mt-4">
            <p class="text-sm text-green-600">
              Application submitted successfully! You will receive a confirmation email shortly.
            </p>
          </div>
        </Form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import { Form, Field, ErrorMessage } from 'vee-validate';
import { candidateRegistrationSchema } from '../validations/candidateSchemas';
import { useCandidateStore } from '../stores/candidateStore';
import config from '../config';

const router = useRouter();
const candidateStore = useCandidateStore();

// File handling
const selectedFile = ref(null);
const fileInput = ref(null);
const submitError = ref(null);
const submitSuccess = ref(false);

// Track if the form has been submitted
const formSubmitted = ref(false);

// Get error messages from store
const errorMessages = computed(() => candidateStore.errorMessages);

// Handle file change
const handleFileChange = (event, setFieldValue, setFieldError) => {
  const file = event.target.files[0];
  
  if (file) {
    // Validate file using config validation
    const validation = validateFile(file);
    
    if (validation.valid) {
      selectedFile.value = file;
      // Set the file in the form field
      setFieldValue('resume', file);
      // Clear any previous file errors
      setFieldError('resume', undefined);
    } else {
      // Set validation error in the form
      setFieldError('resume', validation.message);
      // Clear the file input
      event.target.value = '';
      selectedFile.value = null;
    }
  } else {
    // No file selected, clear the field
    selectedFile.value = null;
    setFieldValue('resume', undefined);
  }
};

// Remove file
const removeFile = (setFieldValue) => {
  selectedFile.value = null;
  if (fileInput.value) {
    fileInput.value.value = '';
  }
  // Clear the field value
  setFieldValue('resume', undefined);
};

// File validation using config
const validateFile = (file) => {
  const { maxSize, allowedTypes } = config.upload;
  
  if (file.size > maxSize) {
    return { 
      valid: false, 
      message: `File size must be less than ${formatFileSize(maxSize)}. Please choose a smaller file.` 
    };
  }
  
  const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
  if (!allowedTypes.includes(fileExtension)) {
    return { 
      valid: false, 
      message: `Only PDF, DOC, and DOCX files are allowed. Please select a different file.` 
    };
  }
  
  return { valid: true };
};

// Format file size
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// Handle form submission
const onSubmit = async (values, { resetForm }) => {
  submitError.value = null;
  candidateStore.clearError(); // Clear previous errors
  
  try {
    // Add the selected file to the form data
    if (selectedFile.value) {
      values.resume = selectedFile.value;
    }
    
    await candidateStore.createCandidate(values);
    
    // Reset form after successful submission
    resetForm();
    selectedFile.value = null;
    submitSuccess.value = true;
    
    // Redirect to status check page after a delay
    setTimeout(() => {
      router.push('/status');
    }, 2000);
  } catch (error) {
    // Check if there are specific error messages from API
    if (errorMessages.value.length > 0) {
      // Error messages are already set in the store
      return;
    }
    
    // Set general error message
    submitError.value = error.message || 'Failed to submit application. Please try again.';
  }
};
</script> 