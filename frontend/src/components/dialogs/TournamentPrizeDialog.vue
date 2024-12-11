<template>
  <v-dialog
    v-model="isOpen"
    max-width="500px"
    class="prize-dialog"
  >
    <v-card class="dialog-card">
      <div class="dialog-content">
        <v-card-title class="dialog-title">Edit Prize Pool</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="editedPrizePool"
            label="Prize Pool (Kitty Kibbles)"
            type="number"
            variant="outlined"
            :rules="[rules.required, rules.positive]"
            :error="!!prizeError"
            :error-messages="prizeError"
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
            @click="updatePrizePool"
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
import { ref, computed, watch } from 'vue'

interface Props {
  modelValue: boolean
  currentPrizePool: number
  error?: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'save', newPrizePool: number): void
}>()

const editedPrizePool = ref(props.currentPrizePool)
const prizeError = ref('')

const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const rules = {
  required: (v: string | number) => !!v || 'Prize pool is required',
  positive: (v: string | number) => {
    const num = Number(v)
    return (!!num && num > 0) || 'Prize pool must be greater than 0'
  }
}

const isValid = computed(() => {
  const value = editedPrizePool.value
  const num = Number(value)
  return rules.required(value) === true && (!!num && num > 0)
})

const hasChanges = computed(() => {
  return Number(editedPrizePool.value) !== props.currentPrizePool
})

watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    editedPrizePool.value = props.currentPrizePool
    prizeError.value = ''
  }
})

watch(() => props.error, (newError) => {
  if (newError) {
    prizeError.value = newError
  }
})

const handleClose = () => {
  editedPrizePool.value = props.currentPrizePool
  prizeError.value = ''
  isOpen.value = false
}

const updatePrizePool = () => {
  const prizePool = Number(editedPrizePool.value)

  if (!prizePool || prizePool <= 0) {
    prizeError.value = !editedPrizePool.value
      ? 'Prize pool is required'
      : 'Prize pool must be greater than 0'
    return
  }

  emit('save', prizePool)
  handleClose()
}
</script>

<style scoped>
.dialog-card {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 2px solid #42DDF2FF;
  backdrop-filter: blur(10px);
  border-radius: 12px;
}

.prize-dialog :deep(.v-card) {
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
</style>
