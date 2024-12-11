<template>
  <div class="history-card">
    <div class="history-content">
      <h3 class="section-title">Request History</h3>

      <!-- Loading state -->
      <div v-if="isLoading" class="d-flex justify-center align-center" style="height: 200px">
        <v-progress-circular indeterminate color="#42DDF2FF"></v-progress-circular>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="error-message">
        {{ error }}
      </div>

      <!-- Request list -->
      <div v-else-if="requests.length > 0" class="request-list">
        <div v-for="request in requests" :key="request.request_date" class="request-item">
          <div class="request-header">
            <div class="request-type">
              <v-icon
                :icon="getRequestTypeIcon(request.request_type)"
                class="request-icon"
              ></v-icon>
              {{ formatRequestType(request.request_type) }}
            </div>
            <div :class="['status-tag', `status-${request.status}`]">
              {{ formatStatus(request.status) }}
            </div>
          </div>

          <div class="request-details">
            <div class="detail-item">
              <v-icon icon="mdi-calendar" size="small" class="detail-icon"></v-icon>
              {{ formatDate(request.request_date) }}
            </div>
            <div v-if="request.username" class="detail-item">
              <v-icon icon="mdi-account" size="small" class="detail-icon"></v-icon>
              Player: {{ request.username }}
            </div>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else class="error-message">
        You have not submitted any requests.
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { format } from 'date-fns'
import { useAuthStore } from '@/stores/auth'
import { API_URL } from '@/config'
import type { Request } from '@/types/types'

const authStore = useAuthStore()
const requests = ref<Request[]>([])
const isLoading = ref(true)
const error = ref<string | null>(null)

const formatRequestType = (type: string): string => {
  return type.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
}

const formatStatus = (status: string): string => {
  return status.charAt(0).toUpperCase() + status.slice(1)
}

const formatDate = (date: string): string => {
  return format(new Date(date), 'dd MMM yyyy, HH:mm')
}

const getRequestTypeIcon = (type: string): string => {
  return type === 'promote user to director' ? 'mdi-shield-account' : 'mdi-account-plus'
}

const fetchRequests = async () => {
  try {
    isLoading.value = true
    error.value = null

    const response = await fetch(
      `${API_URL}/requests/me?offset=0&limit=10`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
        },
      }
    )

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.message || 'Failed to fetch requests')
    }

    const data = await response.json()
    requests.value = [...data]

  } catch (e) {
    console.error('Error fetching requests:', e)
    error.value = e.message || 'Failed to load request history. Please try again later.'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchRequests()
})
</script>

<style scoped>
/* Card base */
.history-card {
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
  padding: 24px;
  width: 100%;
  max-width: 650px;
  min-height: 500px;
  margin: 0 auto 24px;
}

.section-title {
  color: #42DDF2FF;
  font-size: 1.4rem;
  margin-bottom: 24px;
  text-align: center;
}

.error-message {
  color: #fed854;
  font-size: 0.9rem;
  text-align: center;
  padding: 16px;
  margin-top: 8px;
}

/* Request list */
.request-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.request-item {
  background: rgba(45, 55, 75, 0.8);
  border: 1px solid rgba(8, 87, 144, 0.2);
  border-radius: 10px;
  padding: 16px;
  transition: all 0.2s;
}

.request-item:hover {
  background: rgb(45, 55, 75);
  border-color: #42DDF2FF;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(8, 117, 176, 0.2);
}

/* Request header */
.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.request-type {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  font-weight: 500;
}

.request-icon {
  color: #42DDF2FF !important;
}

/* Status tags */
.status-tag {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.9rem;
}

.status-pending {
  background: rgba(254, 216, 84, 0.1);
  color: #FED854FF;
  border: 1px solid rgba(254, 216, 84, 0.3);
}

.status-accepted {
  background: rgba(0, 255, 157, 0.1);
  color: #00ff9d;
  border: 1px solid rgba(0, 255, 157, 0.3);
}

.status-rejected {
  background: rgba(255, 99, 99, 0.1);
  color: #ff6363;
  border: 1px solid rgba(255, 99, 99, 0.3);
}

/* Details */
.request-details {
  display: flex;
  gap: 24px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.detail-icon {
  color: #42DDF2FF !important;
}
</style>
