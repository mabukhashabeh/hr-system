<template>
  <div>
    <div class="form-container">
      <h2 class="form-title">Admin Dashboard</h2>
      
      <div v-if="alert" :class="['alert', alert.type]">
        {{ alert.message }}
      </div>
      
      <!-- Admin Header Toggle -->
      <div class="form-group">
        <label class="form-label">
          <input
            type="checkbox"
            v-model="adminMode"
            @change="toggleAdminMode"
          />
          Enable Admin Mode (X-ADMIN header)
        </label>
      </div>
      
      <!-- Department Filter -->
      <div class="form-group">
        <label class="form-label" for="departmentFilter">Filter by Department</label>
        <select
          id="departmentFilter"
          v-model="selectedDepartment"
          class="form-select"
          @change="loadCandidates"
        >
          <option value="">All Departments</option>
          <option value="IT">IT</option>
          <option value="HR">HR</option>
          <option value="Finance">Finance</option>
        </select>
      </div>
      
      <!-- Status Update Modal -->
      <div v-if="showStatusModal" class="modal-overlay" @click="closeStatusModal">
        <div class="modal-content" @click.stop>
          <h3>Update Status</h3>
          <div class="form-group">
            <label class="form-label">New Status</label>
            <select v-model="statusUpdate.new_status" class="form-select">
              <option value="Submitted">Submitted</option>
              <option value="Under Review">Under Review</option>
              <option value="Interview Scheduled">Interview Scheduled</option>
              <option value="Rejected">Rejected</option>
              <option value="Accepted">Accepted</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Feedback</label>
            <textarea
              v-model="statusUpdate.feedback"
              class="form-input"
              rows="3"
              placeholder="Enter feedback..."
            ></textarea>
          </div>
          <div class="form-group">
            <label class="form-label">Admin User</label>
            <input
              v-model="statusUpdate.admin_user"
              type="text"
              class="form-input"
              placeholder="Enter admin user name"
            />
          </div>
          <div class="modal-actions">
            <button @click="closeStatusModal" class="btn btn-secondary">Cancel</button>
            <button @click="updateStatus" class="btn btn-primary" :disabled="updating">
              {{ updating ? 'Updating...' : 'Update Status' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Candidates Table -->
    <div class="table">
      <div class="table-header">
        <div class="table-row">
          <div class="table-cell">Name</div>
          <div class="table-cell">Department</div>
          <div class="table-cell">Experience</div>
          <div class="table-cell">Status</div>
          <div class="table-cell">Registered</div>
          <div class="table-cell">Actions</div>
        </div>
      </div>
      
      <div v-if="loading" class="loading">
        Loading candidates...
      </div>
      
      <div v-else-if="candidates.length === 0" class="empty-state">
        <h3>No candidates found</h3>
        <p>No candidates match the current filter criteria.</p>
      </div>
      
      <div v-else>
        <div
          v-for="candidate in candidates"
          :key="candidate.id"
          class="table-row"
        >
          <div class="table-cell">{{ candidate.full_name }}</div>
          <div class="table-cell">{{ candidate.department }}</div>
          <div class="table-cell">{{ candidate.years_of_experience }} years</div>
          <div class="table-cell">
            <span :class="['status-badge', `status-${candidate.current_status.toLowerCase().replace(' ', '-')}`]">
              {{ candidate.current_status }}
            </span>
          </div>
          <div class="table-cell">
            {{ new Date(candidate.created_at).toLocaleDateString() }}
          </div>
          <div class="table-cell">
            <button
              @click="openStatusModal(candidate)"
              class="btn btn-secondary"
              style="margin-right: 0.5rem;"
            >
              Update Status
            </button>
            <button
              @click="downloadResume(candidate.id, candidate.full_name)"
              class="btn btn-success"
            >
              Download Resume
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Pagination -->
    <div v-if="candidates.length > 0" style="margin-top: 2rem; text-align: center;">
      <button
        @click="previousPage"
        class="btn btn-secondary"
        :disabled="currentPage === 1"
        style="margin-right: 1rem;"
      >
        Previous
      </button>
      <span style="margin: 0 1rem;">Page {{ currentPage }}</span>
      <button
        @click="nextPage"
        class="btn btn-secondary"
        :disabled="!hasNextPage"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      candidates: [],
      loading: false,
      alert: null,
      adminMode: false,
      selectedDepartment: '',
      currentPage: 1,
      hasNextPage: false,
      showStatusModal: false,
      selectedCandidate: null,
      statusUpdate: {
        new_status: '',
        feedback: '',
        admin_user: ''
      },
      updating: false
    }
  },
  
  async mounted() {
    await this.loadCandidates()
  },
  
  methods: {
    toggleAdminMode() {
      if (this.adminMode) {
        axios.defaults.headers.common['X-ADMIN'] = '1'
      } else {
        delete axios.defaults.headers.common['X-ADMIN']
      }
    },
    
    async loadCandidates() {
      this.loading = true
      this.alert = null
      
      try {
        let url = `/api/v1/admin/candidates/?page=${this.currentPage}`
        if (this.selectedDepartment) {
          url += `&department=${this.selectedDepartment}`
        }
        
        const response = await axios.get(url)
        this.candidates = response.data.results
        this.hasNextPage = !!response.data.next
        
      } catch (error) {
        console.error('Error loading candidates:', error)
        
        if (error.response?.status === 403) {
          this.alert = {
            type: 'alert-error',
            message: 'Access denied. Please enable admin mode.'
          }
        } else {
          this.alert = {
            type: 'alert-error',
            message: 'Failed to load candidates. Please try again.'
          }
        }
      } finally {
        this.loading = false
      }
    },
    
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--
        this.loadCandidates()
      }
    },
    
    nextPage() {
      if (this.hasNextPage) {
        this.currentPage++
        this.loadCandidates()
      }
    },
    
    openStatusModal(candidate) {
      this.selectedCandidate = candidate
      this.statusUpdate = {
        new_status: candidate.current_status,
        feedback: '',
        admin_user: ''
      }
      this.showStatusModal = true
    },
    
    closeStatusModal() {
      this.showStatusModal = false
      this.selectedCandidate = null
      this.statusUpdate = {
        new_status: '',
        feedback: '',
        admin_user: ''
      }
    },
    
    async updateStatus() {
      if (!this.selectedCandidate) return
      
      this.updating = true
      
      try {
        await axios.post(
          `/api/v1/admin/candidates/${this.selectedCandidate.id}/status/`,
          this.statusUpdate
        )
        
        this.alert = {
          type: 'alert-success',
          message: 'Status updated successfully!'
        }
        
        this.closeStatusModal()
        await this.loadCandidates()
        
      } catch (error) {
        console.error('Error updating status:', error)
        
        if (error.response?.data) {
          const errors = error.response.data
          let errorMessage = 'Failed to update status. '
          
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
            message: 'Failed to update status. Please try again.'
          }
        }
      } finally {
        this.updating = false
      }
    },
    
    async downloadResume(candidateId, candidateName) {
      try {
        const response = await axios.get(
          `/api/v1/admin/candidates/${candidateId}/resume/`,
          {
            responseType: 'blob'
          }
        )
        
        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `${candidateName}_resume.pdf`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(url)
        
        this.alert = {
          type: 'alert-success',
          message: 'Resume downloaded successfully!'
        }
        
      } catch (error) {
        console.error('Error downloading resume:', error)
        
        if (error.response?.status === 404) {
          this.alert = {
            type: 'alert-error',
            message: 'No resume found for this candidate.'
          }
        } else {
          this.alert = {
            type: 'alert-error',
            message: 'Failed to download resume. Please try again.'
          }
        }
      }
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 90%;
}

.modal-content h3 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

textarea.form-input {
  resize: vertical;
  min-height: 80px;
}
</style> 