<template>
  <div class="form-container">
    <h2 class="form-title">Candidate Registration</h2>
    
    <div v-if="alert" :class="['alert', alert.type]">
      {{ alert.message }}
    </div>
    
    <form @submit.prevent="submitForm" enctype="multipart/form-data">
      <div class="form-group">
        <label class="form-label" for="fullName">Full Name *</label>
        <input
          id="fullName"
          v-model="form.full_name"
          type="text"
          class="form-input"
          required
        />
      </div>
      
      <div class="form-group">
        <label class="form-label" for="dateOfBirth">Date of Birth *</label>
        <input
          id="dateOfBirth"
          v-model="form.date_of_birth"
          type="date"
          class="form-input"
          required
        />
      </div>
      
      <div class="form-group">
        <label class="form-label" for="yearsExperience">Years of Experience *</label>
        <input
          id="yearsExperience"
          v-model="form.years_of_experience"
          type="number"
          min="0"
          max="50"
          class="form-input"
          required
        />
      </div>
      
      <div class="form-group">
        <label class="form-label" for="department">Department *</label>
        <select
          id="department"
          v-model="form.department"
          class="form-select"
          required
        >
          <option value="">Select Department</option>
          <option value="IT">IT</option>
          <option value="HR">HR</option>
          <option value="Finance">Finance</option>
        </select>
      </div>
      
      <div class="form-group">
        <label class="form-label" for="email">Email *</label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          class="form-input"
          required
        />
      </div>
      
      <div class="form-group">
        <label class="form-label" for="phone">Phone</label>
        <input
          id="phone"
          v-model="form.phone"
          type="tel"
          class="form-input"
        />
      </div>
      
      <div class="form-group">
        <label class="form-label" for="resume">Resume (PDF or DOCX) *</label>
        <input
          id="resume"
          type="file"
          accept=".pdf,.docx"
          @change="handleFileChange"
          class="form-file"
          required
        />
        <small style="color: #6c757d; margin-top: 0.25rem; display: block;">
          Maximum file size: 5MB
        </small>
      </div>
      
      <button type="submit" class="btn btn-primary" :disabled="loading">
        {{ loading ? 'Registering...' : 'Register Candidate' }}
      </button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CandidateRegistration',
  data() {
    return {
      form: {
        full_name: '',
        date_of_birth: '',
        years_of_experience: '',
        department: '',
        email: '',
        phone: '',
        resume: null
      },
      loading: false,
      alert: null
    }
  },
  methods: {
    handleFileChange(event) {
      const file = event.target.files[0]
      if (file) {
        // Check file size (5MB = 5 * 1024 * 1024 bytes)
        if (file.size > 5 * 1024 * 1024) {
          this.alert = {
            type: 'alert-error',
            message: 'File size must be less than 5MB'
          }
          event.target.value = ''
          return
        }
        
        // Check file type
        const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        if (!allowedTypes.includes(file.type)) {
          this.alert = {
            type: 'alert-error',
            message: 'Only PDF and DOCX files are allowed'
          }
          event.target.value = ''
          return
        }
        
        this.form.resume = file
        this.alert = null
      }
    },
    
    async submitForm() {
      this.loading = true
      this.alert = null
      
      try {
        const formData = new FormData()
        formData.append('full_name', this.form.full_name)
        formData.append('date_of_birth', this.form.date_of_birth)
        formData.append('years_of_experience', this.form.years_of_experience)
        formData.append('department', this.form.department)
        formData.append('email', this.form.email)
        formData.append('phone', this.form.phone)
        formData.append('resume', this.form.resume)
        
        const response = await axios.post('/api/v1/candidates/register/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        this.alert = {
          type: 'alert-success',
          message: `Registration successful! Candidate ID: ${response.data.candidate_id}`
        }
        
        // Reset form
        this.form = {
          full_name: '',
          date_of_birth: '',
          years_of_experience: '',
          department: '',
          email: '',
          phone: '',
          resume: null
        }
        
        // Reset file input
        document.getElementById('resume').value = ''
        
      } catch (error) {
        console.error('Registration error:', error)
        
        if (error.response?.data) {
          const errors = error.response.data
          let errorMessage = 'Registration failed. '
          
          if (typeof errors === 'object') {
            const errorList = Object.values(errors).flat()
            errorMessage += errorList.join(', ')
          } else {
            errorMessage += errors
          }
          
          this.alert = {
            type: 'alert-error',
            message: errorMessage
          }
        } else {
          this.alert = {
            type: 'alert-error',
            message: 'Registration failed. Please try again.'
          }
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script> 