<template>
  <div class="actions-card">
    <div class="actions-background"></div>
    <div class="actions-content">
      <h3 class="section-title">Available Actions</h3>
      <div class="actions-buttons">
        <v-btn
          class="action-btn"
          prepend-icon="mdi-shield-account"
          @click="handleDirectorRequest"
          :disabled="hasPendingRequest"
        >
          Request Director Role
        </v-btn>
        <v-btn
          class="action-btn"
          prepend-icon="mdi-account-plus"
          @click="handlePlayerLinkDialog"
          :disabled="hasPendingRequest"
        >
          Link Player Profile
        </v-btn>
      </div>

      <!-- Display Error for Available Actions -->
      <div v-if="actionsError" class="error-message">
        {{ actionsError }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { API_URL } from '@/config'

// Props
const props = defineProps<{
  requests: Array<{
    status: string
    request_type: string
  }>
}>()

// Emits
const emit = defineEmits<{
  'update-requests': []
  'show-player-dialog': []
  'show-success': [message: string]
}>()

// Store
const authStore = useAuthStore()

// Refs
const actionsError = ref<string | null>(null)
const isSubmitting = ref(false)

// Computed
const hasPendingRequest = computed(() => {
  return props.requests.some(request =>
    request.status === 'pending' &&
    (request.request_type === 'link user to player' || request.request_type === 'promote user to director')
  )
})

// Methods
const handleDirectorRequest = async () => {
  if (hasPendingRequest.value) {
    actionsError.value = 'You already have a pending request.'
    return
  }

  try {
    isSubmitting.value = true
    actionsError.value = null

    const response = await fetch(`${API_URL}/requests/directors/${authStore.userEmail}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
      },
    })

    if (!response.ok) throw new Error('Failed to submit request')

    emit('show-success', 'Director role request submitted successfully. An admin will review your request shortly.')
    emit('update-requests')
  } catch (e) {
    console.error('Error submitting director request:', e)
    actionsError.value = 'Failed to submit request. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}

const handlePlayerLinkDialog = () => {
  if (hasPendingRequest.value) {
    actionsError.value = 'You already have a pending request.'
    return
  }
  emit('show-player-dialog')
}
</script>

<style scoped>
.actions-card {
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(2px);
  padding: 24px;
  width: 55%;
  margin: 0 auto 24px;
}

.section-title {
  color: #42DDF2FF;
  font-size: 1.4rem;
  margin-bottom: 24px;
  text-align: center;
}

.actions-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.action-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
  font-weight: bold;
  padding: 2px 32px !important;
}

.action-btn:hover {
  background: #FED854FF !important;
  box-shadow: 0 0 15px rgba(254, 216, 84, 0.3);
}

.error-message {
  color: #fed854;
  text-align: center;
  padding: 16px;
}
</style>
