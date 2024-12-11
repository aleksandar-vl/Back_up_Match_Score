<template>
  <v-dialog v-model="dialogVisible" max-width="500">
    <v-card class="dialog-card">
      <div class="dialog-background"></div>
      <div class="dialog-content">
        <v-card-title class="dialog-title">
          <span>Link Player Profile</span>
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="username"
            label="Player Username"
            variant="outlined"
            :rules="[rules.required]"
            :error="!!error"
            class="player-username-input"
          ></v-text-field>

          <!-- Display Error for Player Link -->
          <div v-if="error" class="error-message">
            {{ error }}
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            class="cancel-btn"
            @click="handleClose"
          >
            Cancel
          </v-btn>
          <v-btn
            class="submit-btn"
            @click="handleSubmit"
            :loading="isSubmitting"
            :disabled="!!error || !username || isSubmitting"
          >
            Submit
          </v-btn>
        </v-card-actions>
      </div>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { API_URL } from '@/config'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const props = defineProps<{
  modelValue: boolean
  hasPendingRequest: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'submit-success': [message: string]
}>()

const username = ref('')
const error = ref<string | null>(null)
const isSubmitting = ref(false)

const rules = {
  required: (v: string) => !!v || 'This field is required'
}

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const handleClose = () => {
  username.value = ''
  error.value = null
  dialogVisible.value = false
}

const handleSubmit = async () => {
  console.log('Starting handleSubmit')
  if (props.hasPendingRequest) {
    error.value = 'You already have a pending request.'
    return
  }

  if (!username.value) {
    error.value = 'Player username is required.'
    return
  }

  try {
    isSubmitting.value = true
    error.value = null

    const response = await fetch(`${API_URL}/requests/players/${username.value}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
      },
    })

    const data = await response.json()

    if (!response.ok) {
      if (response.status === 404) {
        error.value = `Player with username "${username.value}" was not found.`
      } else if (response.status === 400 && data.detail?.includes('already linked')) {
        error.value = `Player "${username.value}" is already linked to another user.`
      } else {
        throw new Error('Failed to submit request')
      }
      return
    }

    emit('submit-success', 'Player link request submitted successfully. An admin will review your request shortly.')
    handleClose()
  } catch (e) {
    console.error('Error submitting player link request:', e)
    error.value = 'Failed to submit request. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}

watch(username, (newValue) => {
  if (newValue && error.value) {
    error.value = null
  }
})

watch(() => props.modelValue, (newVal) => {
  console.log('Dialog visibility changed:', newVal)
})
</script>

<style scoped>
/* Dialog base */
.dialog-card {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 2px solid #42DDF2FF;
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 10001 !important;
  border-radius: 35px !important;
}

.dialog-content {
  padding: 24px;
}

.dialog-title {
  color: #42ddf2;
  font-weight: bold;
  font-size: 1.25rem;
  text-align: center;
}

/* Form elements */
.player-username-input {
  margin-top: 16px;
}

/* Error states */
.error-message {
  color: #fed854;
  font-size: 0.9rem;
  margin-top: 8px;
  text-align: center;
}

/* Buttons */
.cancel-btn {
  color: #42DDF2FF !important;
}

.submit-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
  margin-left: 16px;
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Vuetify overrides */
:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 14px;
}

/* Field error states */
:deep(.v-field--error) {
  --v-field-border-color: #fed854 !important;
}

:deep(.v-field--error .v-field__outline),
:deep(.v-field--error .v-field__outline__start),
:deep(.v-field--error .v-field__outline__end),
:deep(.v-field--error .v-field__outline__notch),
:deep(.v-field--error input::placeholder),
:deep(.v-field--error .v-label.v-field-label) {
  border-color: #fed854 !important;
  color: #fed854 !important;
}
</style>
