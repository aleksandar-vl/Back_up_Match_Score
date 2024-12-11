<template>
  <v-dialog v-model="showNameEdit" max-width="500px" class="edit-dialog">
    <v-card>
      <v-card-title class="dialog-title">Edit Team Name</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="editedName"
          label="Team Name"
          variant="outlined"
          :rules="[rules.required, rules.minLength]"
          :error="!!nameError"
          :error-messages="nameError"
        ></v-text-field>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn class="cancel-btn" @click="handleClose">Cancel</v-btn>
        <v-btn
          class="submit-btn"
          @click="updateName"
          :disabled="!isValid || !hasChanges"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits, computed } from 'vue'
import { API_URL } from '@/config'
import { useAuthStore } from '@/stores/auth'

// Props
interface Props {
  modelValue: boolean // for v-model
  teamId: string
  currentName: string
}

const props = defineProps<Props>()

// Emit events
const emit = defineEmits(['update:modelValue', 'nameUpdated'])

// State
const editedName = ref(props.currentName)
const nameError = ref('')
const authStore = useAuthStore()

// Validation rules
const rules = {
  required: (v: string) => !!v?.trim() || 'Team name is required',
  minLength: (v: string) => {
    const length = v?.trim().length || 0
    return length >= 5 || 'Team name must be at least 5 characters'
  }
}

// Computed for v-model binding
const showNameEdit = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Computed for validation state
const isValid = computed(() => {
  const value = editedName.value?.trim() || ''
  return rules.required(value) === true && rules.minLength(value) === true
})

// Computed for changes check
const hasChanges = computed(() => {
  return editedName.value?.trim() !== props.currentName?.trim()
})

// Methods
const handleClose = () => {
  editedName.value = props.currentName
  nameError.value = ''
  showNameEdit.value = false
}

const updateName = async () => {
  const trimmedName = editedName.value?.trim()

  if (!isValid.value) {
    nameError.value = !trimmedName
      ? 'Team name is required'
      : 'Team name must be at least 5 characters'
    return
  }

  try {
    nameError.value = ''

    const response = await fetch(
      `${API_URL}/teams/${props.teamId}?name=${encodeURIComponent(trimmedName)}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      }
    )

    if (!response.ok) {
      const error = await response.text()
      throw new Error(error)
    }

    emit('nameUpdated', trimmedName)
    handleClose()
  } catch (e) {
    console.error('Error updating team name:', e)
    nameError.value = (e as Error).message || 'Failed to update team name'
  }
}

// Reset state when dialog opens
watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    editedName.value = props.currentName
    nameError.value = ''
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

/* Text Field Styles */
:deep(.v-text-field) {
  .v-field {
    background: rgba(45, 55, 75, 0.8) !important;
    color: white !important;
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
}

/* Alert Styles */
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

/* Error State Styles */
:deep(.v-field--error) {
  --v-field-border-color: #fed854 !important;
}

:deep(.v-field--error .v-field__outline),
:deep(.v-field--error .v-label),
:deep(.v-field--error input::placeholder),
:deep(.v-field--error .v-field__outline__start),
:deep(.v-field--error .v-field__outline__end),
:deep(.v-field--error .v-field__outline__notch) {
  border-color: #fed854 !important;
  color: #fed854 !important;
}

:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 0.85rem;
  line-height: 1.2;
}

</style>
