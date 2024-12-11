<template>
  <v-dialog v-model="showLogoEdit" max-width="500px" class="edit-dialog">
    <v-card>
      <v-card-title class="dialog-title">Update Team Logo</v-card-title>
      <v-card-text>
        <v-text-field
          v-if="logoError"
          type="error"
          variant="tonal"
          class="mb-4"
          :messages="logoError"
        ></v-text-field>
        <v-file-input
          v-model="logoFile"
          label="Choose logo"
          accept="image/*"
          variant="outlined"
          prepend-icon="mdi-camera"
          :error-messages="fileError"
        ></v-file-input>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn class="cancel-btn" @click="handleClose">Cancel</v-btn>
        <v-btn
          class="submit-btn"
          :disabled="!logoFile"
          @click="updateLogo"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { API_URL } from '@/config'
import { useAuthStore } from '@/stores/auth'

interface Props {
  modelValue: boolean
  teamId: string
}

const props = defineProps<Props>()
const emit = defineEmits(['update:modelValue', 'logoUpdated'])

const logoFile = ref<File | null>(null)
const logoError = ref('')
const fileError = ref('')
const authStore = useAuthStore()

const showLogoEdit = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})


const handleClose = () => {
  logoFile.value = null
  logoError.value = ''
  fileError.value = ''
  showLogoEdit.value = false
}

const updateLogo = async () => {
  if (!logoFile.value) {
    fileError.value = 'Please select a logo image'
    return
  }

  try {
    logoError.value = ''
    fileError.value = ''
    const formData = new FormData()
    formData.append('logo', logoFile.value)

    const response = await fetch(
      `${API_URL}/teams/${props.teamId}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        },
        body: formData
      }
    )

    if (!response.ok) {
      const error = await response.text()
      throw new Error(error)
    }

    emit('logoUpdated')
    handleClose()
  } catch (e) {
    console.error('Error updating team logo:', e)
    logoError.value = (e as Error).message || 'Failed to update team logo'
  }
}

watch(() => props.modelValue, (newValue) => {
  if (!newValue) {
    logoFile.value = null
    logoError.value = ''
    fileError.value = ''
  }
})
</script>

<style scoped>
.edit-dialog :deep(.v-card) {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 2px solid #42DDF2FF !important;
  backdrop-filter: blur(10px);
  width: 100%;
  max-width: 400px;
  align-self: center;
  padding: 10px;
  border-radius: 35px;
}

.dialog-title {
  color: #42DDF2FF !important;
  font-size: 1.5rem !important;
  text-align: center;
  padding: 20px !important;
}

/* File Input Styles */
:deep(.v-file-input) {
  color: white !important;

  .v-field {
    background: rgba(45, 55, 75, 0.8) !important;
    color: white !important;
    border-color: rgba(255, 255, 255, 0.7) !important;
  }

  .v-field__outline {
    color: rgba(66, 221, 242, 0.3) !important;
  }

  .v-label {
    color: rgba(255, 255, 255, 0.7) !important;
  }

  .v-field__input {
    color: white !important;
  }

  .v-icon {
    color: #42DDF2FF !important;
  }
}

/* Button Styles */
:deep(.v-btn) {
  text-transform: none !important;
  border-radius: 50px !important;
}

:deep(.v-card-actions .v-btn) {
  background: rgba(17, 78, 112, 0.56) !important;
  color: #42DDF2FF !important;
  border: 2px solid #42DDF2FF !important;
  min-width: 120px;
  font-weight: bold;
  letter-spacing: 1px;
  transition: all 0.2s;

  &:hover {
    background: rgba(66, 221, 242, 0.1) !important;
    transform: translateY(-2px);
  }
}

/* Error Alert */
:deep(.v-alert) {
  background-color: rgba(254, 216, 84, 0.1) !important;
  color: #fed854 !important;
  border-color: #fed854 !important;
  border-radius: 8px;

  &__close-button,
  &__prepend {
    color: #fed854 !important;
  }
}

:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 0.85rem;
  line-height: 1.2;
}

:deep(.v-field--error) {
  --v-field-border-color: #fed854 !important;
}

:deep(.v-field--error .v-field__outline),
:deep(.v-field--error .v-label),
:deep(.v-field--error input::placeholder) {
  border-color: #fed854 !important;
  color: #fed854 !important;
}
</style>
