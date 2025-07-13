import * as yup from 'yup';
import config from '../config';

/**
 * Validation Schemas for Candidate Forms
 * Aligned with backend validation requirements
 */

// Base candidate validation schema
export const candidateSchema = yup.object({
  full_name: yup
    .string()
    .required('Full name is required')
    .min(2, 'Full name must be at least 2 characters')
    .max(100, 'Full name must not exceed 100 characters')
    .matches(/^[a-zA-Z\s]+$/, 'Full name must contain only letters and spaces'),

  email: yup
    .string()
    .required('Email address is required')
    .email('Please enter a valid email address')
    .max(254, 'Email address is too long'),

  phone: yup
    .string()
    .required('Phone number is required')
    .matches(/^[\+]?[1-9][\d]{0,15}$/, 'Please enter a valid phone number'),

  date_of_birth: yup
    .date()
    .required('Date of birth is required')
    .max(new Date(), 'Date of birth cannot be in the future')
    .test('age', 'Age must be between 16 and 100 years', function(value) {
      if (!value) return true; // Let required validation handle this
      const today = new Date();
      const birthDate = new Date(value);
      const age = today.getFullYear() - birthDate.getFullYear();
      const monthDiff = today.getMonth() - birthDate.getMonth();
      if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
      }
      return age >= 16 && age <= 100;
    }),

  years_of_experience: yup
    .number()
    .required('Years of experience is required')
    .min(0, 'Years of experience must be at least 0')
    .max(50, 'Years of experience must not exceed 50')
    .integer('Years of experience must be a whole number'),

  department: yup
    .string()
    .required('Please select a department')
    .oneOf(
      ['it', 'hr', 'finance'],
      'Please select a valid department'
    ),

  resume: yup
    .mixed()
    .required('Resume file is required')
    .test('fileSize', 'File size must be less than 5MB', function(value) {
      if (!value) return true; // Let required validation handle this
      return value.size <= 5242880;
    })
    .test('fileType', 'Only PDF, DOC, and DOCX files are allowed', function(value) {
      if (!value) return true; // Let required validation handle this
      const fileExtension = '.' + value.name.split('.').pop().toLowerCase();
      return config.upload.allowedTypes.includes(fileExtension);
    }),
});

// Schema for candidate registration (create)
export const candidateRegistrationSchema = candidateSchema;

// Schema for candidate update (partial update)
export const candidateUpdateSchema = yup.object({
  full_name: yup
    .string()
    .min(2, 'Full name must be at least 2 characters')
    .max(100, 'Full name must not exceed 100 characters')
    .matches(/^[a-zA-Z\s]+$/, 'Full name must contain only letters and spaces'),

  email: yup
    .string()
    .email('Please enter a valid email address')
    .max(254, 'Email address is too long'),

  phone: yup
    .string()
    .matches(/^[\+]?[1-9][\d]{0,15}$/, 'Please enter a valid phone number'),

  date_of_birth: yup
    .date()
    .max(new Date(), 'Date of birth cannot be in the future')
    .test('age', 'Age must be between 16 and 100 years', function(value) {
      if (!value) return true;
      const today = new Date();
      const birthDate = new Date(value);
      const age = today.getFullYear() - birthDate.getFullYear();
      const monthDiff = today.getMonth() - birthDate.getMonth();
      if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
      }
      return age >= 16 && age <= 100;
    }),

  years_of_experience: yup
    .number()
    .min(0, 'Years of experience must be at least 0')
    .max(50, 'Years of experience must not exceed 50')
    .integer('Years of experience must be a whole number'),

  department: yup
    .string()
    .oneOf(
      ['it', 'hr', 'finance'],
      'Please select a valid department'
    ),

  resume: yup
    .mixed()
    .test('fileSize', 'File size must be less than 10MB', function(value) {
      if (!value) return true; // Optional field, so return true if no file
      return value.size <= config.upload.maxSize;
    })
    .test('fileType', 'Only PDF, DOC, and DOCX files are allowed', function(value) {
      if (!value) return true; // Optional field, so return true if no file
      const fileExtension = '.' + value.name.split('.').pop().toLowerCase();
      return config.upload.allowedTypes.includes(fileExtension);
    }),
});

// Schema for status update (admin only)
export const statusUpdateSchema = yup.object({
  new_status: yup
    .string()
    .required('Please select a new status')
    .oneOf(
      ['submitted', 'under_review', 'interview_scheduled', 'accepted', 'rejected'],
      'Please select a valid status'
    ),

  admin_name: yup
    .string()
    .required('Admin name is required')
    .min(2, 'Admin name must be at least 2 characters')
    .max(100, 'Admin name must not exceed 100 characters'),

  admin_email: yup
    .string()
    .required('Admin email is required')
    .email('Please enter a valid admin email address'),

  feedback: yup
    .string()
    .required('Feedback is required')
    .min(10, 'Feedback must be at least 10 characters')
    .max(1000, 'Feedback must not exceed 1000 characters'),
});

// Schema for status check by email
export const statusCheckSchema = yup.object({
  email: yup
    .string()
    .required('Email address is required')
    .email('Please enter a valid email address'),
});

// Schema for status history filtering
export const statusHistoryFilterSchema = yup.object({
  candidate__email: yup
    .string()
    .email('Please enter a valid email address'),

  new_status: yup
    .string()
    .oneOf(
      ['submitted', 'under_review', 'interview_scheduled', 'accepted', 'rejected'],
      'Please select a valid status'
    ),

  admin_name: yup
    .string()
    .min(2, 'Admin name must be at least 2 characters'),

  date_from: yup
    .date()
    .max(new Date(), 'Date cannot be in the future'),

  date_to: yup
    .date()
    .max(new Date(), 'Date cannot be in the future'),
});

// Schema for candidate filtering
export const candidateFilterSchema = yup.object({
  full_name: yup.string(),
  email: yup.string().email('Please enter a valid email address'),
  current_status: yup
    .string()
    .oneOf(
      ['submitted', 'under_review', 'interview_scheduled', 'accepted', 'rejected'],
      'Please select a valid status'
    ),
  years_of_experience_min: yup
    .number()
    .min(0, 'Minimum experience must be at least 0'),
  years_of_experience_max: yup
    .number()
    .max(50, 'Maximum experience must not exceed 50'),
  date_from: yup
    .date()
    .max(new Date(), 'Date cannot be in the future'),
  date_to: yup
    .date()
    .max(new Date(), 'Date cannot be in the future'),
}); 