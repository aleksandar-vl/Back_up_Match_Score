<template>
  <v-dialog
    :modelValue="modelValue"
    @update:modelValue="$emit('update:modelValue', $event)"
    max-width="500px"
    class="end-date-dialog"
  >
    <v-card class="dialog-card">
      <div class="dialog-content">
        <v-card-title class="dialog-title">Edit End Date</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="editedEndDate"
            label="End Date"
            type="datetime-local"
            variant="outlined"
            :error="!!endDateError"
            :error-messages="endDateError"
          ></v-text-field>
        </v-card-text>
        <v-card-actions class="dialog-actions">
          <v-spacer></v-spacer>
          <v-btn
            class="cancel-btn"
            variant="text"
            @click="$emit('update:modelValue', false)"
          >
            Cancel
          </v-btn>
          <v-btn
            class="submit-btn"
            @click="updateEndDate"
            :disabled="!editedEndDate"
          >
            Save
          </v-btn>
        </v-card-actions>
      </div>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface Props {
  modelValue: boolean
  currentEndDate: string
  error?: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'save', newEndDate: string): void
}>()

const editedEndDate = ref(props.currentEndDate)
const endDateError = ref('')

watch(() => props.currentEndDate, (newValue) => {
  editedEndDate.value = newValue
})

watch(() => props.error, (newError) => {
  if (newError) {
    endDateError.value = newError
  }
})
const updateEndDate = () => {
  if (!editedEndDate.value?.trim()) {
    endDateError.value = 'End date cannot be empty'
    return
  }
  emit('save', editedEndDate.value)
}
</script>

<style scoped>
.dialog-card {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 2px solid #42DDF2FF;
  backdrop-filter: blur(10px);
  border-radius: 12px;
}

.dialog-card :deep(.v-card) {
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

.end-date-dialog :deep(.v-card) {
  border-radius: 35px !important;
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

/* Date Input Field Specific Styles */
:deep(.v-field__input::-webkit-calendar-picker-indicator) {
  filter: invert(1);
  opacity: 0.5;
}

:deep(.v-field__input::-webkit-calendar-picker-indicator:hover) {
  opacity: 0.8;
  cursor: pointer;
}
</style>
