<template>
  <v-dialog
    :modelValue="modelValue"
    @update:modelValue="handleDialogUpdate"
    max-width="500px"
    class="title-dialog"
  >
    <v-card class="dialog-card">
      <div class="dialog-content">
        <v-card-title class="dialog-title">Edit Tournament Title</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="editedTitle"
            label="Tournament Title"
            variant="outlined"
            :rules="[rules.required, rules.length]"
            :error="!!titleError"
            :error-messages="titleError"
          ></v-text-field>
        </v-card-text>
        <v-card-actions class="dialog-actions">
          <v-spacer></v-spacer>
          <v-btn
            class="cancel-btn"
            variant="text"
            @click="handleClose"
          >
            Cancel
          </v-btn>
          <v-btn
            class="submit-btn"
            @click="updateTitle"
            :disabled="!isValid || !hasChanges"
          >
            Save
          </v-btn>
        </v-card-actions>
      </div>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'

interface Props {
  modelValue: boolean
  currentTitle: string
  error?: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'save', newTitle: string): void
}>()

const editedTitle = ref(props.currentTitle)
const titleError = ref('')

const rules = {
  required: (v: string) => !!v?.trim() || 'Title is required',
  length: (v: string) => {
    const length = v?.trim().length || 0
    return (length >= 3 && length <= 50) || 'Title must be between 3 and 50 characters'
  }
}

const isValid = computed(() => {
  const value = editedTitle.value?.trim() || ''
  return rules.required(value) === true && rules.length(value) === true
})

const hasChanges = computed(() => {
  return editedTitle.value?.trim() !== props.currentTitle?.trim()
})

// Reset the state when dialog opens
watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    editedTitle.value = props.currentTitle
    titleError.value = ''
  }
})

watch(() => props.currentTitle, (newValue) => {
  if (props.modelValue) {
    editedTitle.value = newValue
  }
})

watch(() => props.error, (newError) => {
  if (newError) {
    titleError.value = newError
  }
})

const resetDialog = () => {
  editedTitle.value = props.currentTitle
  titleError.value = ''
}

const handleClose = () => {
  resetDialog()
  emit('update:modelValue', false)
}

const handleDialogUpdate = (value: boolean) => {
  if (!value) {
    resetDialog()
  }
  emit('update:modelValue', value)
}

const updateTitle = () => {
  const trimmedTitle = editedTitle.value?.trim()

  if (!isValid.value) {
    titleError.value = !trimmedTitle ? 'Title is required' : 'Title must be between 3 and 50 characters'
    return
  }

  emit('save', trimmedTitle)
}
</script>

<style scoped>
.dialog-card {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 2px solid #42DDF2FF;
  backdrop-filter: blur(10px);
}
.title-dialog :deep(.v-card) {
  border-radius: 35px !important;
}

.dialog-content {
  padding: 24px;
}

.dialog-title {
  color: #42ddf2;
  font-size: 1.4rem;
  font-weight: 500;
  text-align: center;
  margin-bottom: 16px;
}

.dialog-actions {
  padding: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: -32px;
}

/* Button Styles */
.cancel-btn {
  color: #42DDF2FF !important;
}

.submit-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
  margin-left: 16px;
}

/* Vuetify Field Overrides */
:deep(.v-field) {
  background: rgba(45, 55, 75, 0.8) !important;
}

:deep(.v-field__input),
:deep(.v-input input) {
  color: white !important;
}

:deep(.v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}

:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 0.85rem;
  line-height: 1.2;
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

:deep(.v-field__outline) {
  color: rgba(66, 221, 242, 0.3) !important;
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
:deep(.v-field--error input::placeholder),
:deep(.v-field--error .v-field__outline__start),
:deep(.v-field--error .v-field__outline__end),
:deep(.v-field--error .v-field__outline__notch) {
  border-color: #fed854 !important;
  color: #fed854 !important;
}
</style>

