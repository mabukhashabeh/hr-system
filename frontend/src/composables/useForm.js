import { ref, reactive, readonly } from 'vue';
import { useForm, useField } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/yup';

/**
 * Form Composable
 * Provides reusable form functionality with Vee-Validate integration
 */

export function useFormHandler(schema, initialValues = {}) {
  const isSubmitting = ref(false);
  const submitError = ref(null);
  const submitSuccess = ref(false);

  // Create form with validation
  const { handleSubmit, resetForm, setErrors, setFieldValue, values, errors } = useForm({
    validationSchema: toTypedSchema(schema),
    initialValues,
  });

  // Reset form state
  const resetFormState = () => {
    isSubmitting.value = false;
    submitError.value = null;
    submitSuccess.value = false;
  };

  // Handle form submission with error handling
  const handleFormSubmit = (onSubmit) => {
    return handleSubmit(async (values) => {
      try {
        resetFormState();
        isSubmitting.value = true;
        
        await onSubmit(values);
        
        submitSuccess.value = true;
        resetForm();
        
        return { success: true };
      } catch (error) {
        // Handle API errors
        if (error.errorMessages && error.errorMessages.length > 0) {
          // Show API error messages
          submitError.value = error.errorMessages.join('. ');
        } else {
          // Show general error message
          submitError.value = error.message || 'An error occurred while submitting the form. Please try again.';
        }
        
        return { success: false, error: submitError.value };
      } finally {
        isSubmitting.value = false;
      }
    });
  };

  // Clear form errors
  const clearErrors = () => {
    submitError.value = null;
    setErrors({});
  };

  // Reset form to initial values
  const resetToInitial = () => {
    resetForm();
    resetFormState();
  };

  return {
    // Form state
    isSubmitting: readonly(isSubmitting),
    submitError: readonly(submitError),
    submitSuccess: readonly(submitSuccess),
    values: readonly(values),
    errors: readonly(errors),
    
    // Form methods
    handleFormSubmit,
    resetForm,
    resetToInitial,
    setErrors,
    setFieldValue,
    clearErrors,
  };
}

/**
 * Field Composable
 * Provides individual field functionality with validation
 */
export function useFieldHandler(fieldName, schema) {
  const { value, errorMessage, handleBlur, handleChange, meta } = useField(
    fieldName,
    toTypedSchema(schema)
  );

  return {
    value,
    errorMessage,
    handleBlur,
    handleChange,
    meta,
  };
}

/**
 * File Upload Composable
 * Handles file upload with validation and preview
 */
export function useFileUpload(options = {}) {
  const {
    maxSize = 10 * 1024 * 1024, // 10MB
    allowedTypes = ['.pdf', '.doc', '.docx'],
    maxFiles = 1,
  } = options;

  const files = ref([]);
  const uploadProgress = ref(0);
  const isUploading = ref(false);
  const uploadError = ref(null);

  // Validate file
  const validateFile = (file) => {
    const errors = [];

    // Check file size
    if (file.size > maxSize) {
      errors.push(`File size must be less than ${formatFileSize(maxSize)}`);
    }

    // Check file type
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    if (!allowedTypes.includes(fileExtension)) {
      errors.push(`File type not allowed. Allowed types: ${allowedTypes.join(', ')}`);
    }

    return errors;
  };

  // Handle file selection
  const handleFileSelect = (event) => {
    const selectedFiles = Array.from(event.target.files);
    const errors = [];

    selectedFiles.forEach(file => {
      const fileErrors = validateFile(file);
      errors.push(...fileErrors);
    });

    if (errors.length > 0) {
      uploadError.value = errors.join(', ');
      return false;
    }

    files.value = selectedFiles.slice(0, maxFiles);
    uploadError.value = null;
    return true;
  };

  // Clear files
  const clearFiles = () => {
    files.value = [];
    uploadError.value = null;
    uploadProgress.value = 0;
  };

  // Format file size
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return {
    files: readonly(files),
    uploadProgress: readonly(uploadProgress),
    isUploading: readonly(isUploading),
    uploadError: readonly(uploadError),
    handleFileSelect,
    clearFiles,
    validateFile,
    formatFileSize,
  };
} 