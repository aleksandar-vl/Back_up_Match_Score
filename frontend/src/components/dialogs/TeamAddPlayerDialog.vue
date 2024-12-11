<template>
  <v-dialog v-model="showAddPlayer" max-width="500px" class="edit-dialog">
    <v-card>
      <v-card-title class="dialog-title">Add Player to Team</v-card-title>
      <v-card-text>
        <v-alert
          v-if="addPlayerError"
          type="error"
          variant="tonal"
          class="mb-4 error-alert"
          closable
        >
          {{ formatErrorMessage(addPlayerError) }}
        </v-alert>
        <v-autocomplete
          v-model="selectedPlayerId"
          :items="availablePlayers"
          item-title="username"
          item-value="id"
          label="Select Player"
          variant="outlined"
          :loading="loadingPlayers"
        >
          <template v-slot:item="{ props, item }">
            <v-list-item v-bind="props" :title="item.raw.username">
              <template v-slot:prepend>
                <v-avatar size="32">
                  <v-img v-if="item.raw.avatar" :src="item.raw.avatar"></v-img>
                  <v-icon v-else>mdi-account</v-icon>
                </v-avatar>
              </template>
            </v-list-item>
          </template>
        </v-autocomplete>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn class="cancel-btn" @click="handleClose">Cancel</v-btn>
        <v-btn
          class="submit-btn"
          :disabled="!selectedPlayerId"
          @click="addPlayer"
        >
          Add Player
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { API_URL } from '@/config'
import { useAuthStore } from '@/stores/auth'
import type { Player } from '@/types/types'

// Props
interface Props {
  modelValue: boolean
  teamId: string
  teamName: string
}

const props = defineProps<Props>()
const emit = defineEmits(['update:modelValue', 'playerAdded'])

// State
const selectedPlayerId = ref('')
const availablePlayers = ref<Player[]>([])
const loadingPlayers = ref(false)
const addPlayerError = ref('')
const authStore = useAuthStore()

// Computed for v-model binding
const showAddPlayer = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const formatErrorMessage = (error: string) => {
  if (error.includes('Team has reached the player limit')) {
    return 'Team limit reached!'
  }
  return error
}

// Methods
const fetchAvailablePlayers = async () => {
  try {
    loadingPlayers.value = true
    addPlayerError.value = ''
    const response = await fetch(`${API_URL}/players/?is_available=true&offset=0&limit=100`)

    if (!response.ok) {
      throw new Error('Failed to load available players')
    }

    availablePlayers.value = await response.json()
  } catch (e) {
    console.error('Error fetching available players:', e)
    addPlayerError.value = 'Failed to load available players'
  } finally {
    loadingPlayers.value = false
  }
}

const handleClose = () => {
  selectedPlayerId.value = ''
  addPlayerError.value = ''
  showAddPlayer.value = false
}

const addPlayer = async () => {
  if (!selectedPlayerId.value) return

  try {
    addPlayerError.value = ''
    const response = await fetch(
      `${API_URL}/players/${selectedPlayerId.value}?team_name=${encodeURIComponent(props.teamName)}`,
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

    showAddPlayer.value = false
    emit('playerAdded')
  } catch (e) {
    console.error('Error adding player:', e)
    addPlayerError.value = (e as Error).message || 'Failed to add player'
  }
}

watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    fetchAvailablePlayers()
    selectedPlayerId.value = ''
    addPlayerError.value = ''
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

/* Autocomplete Styles */
:deep(.v-autocomplete) {
  .v-field {
    background: rgba(45, 55, 75, 0.8) !important;
  }

  .v-field__input {
    color: white !important;
  }

  .v-label {
    color: rgba(255, 255, 255, 0.7) !important;
  }

  .v-field__outline {
    color: rgba(66, 221, 242, 0.3) !important;
  }
}

/* List Item Styles */
:deep(.v-list-item) {
  background: transparent !important;

  &:hover {
    background: rgba(66, 221, 242, 0.1) !important;
  }

  &__title {
    color: white !important;
  }
}

/* Button Styles */
:deep(.v-card-actions .v-btn) {
  text-transform: none !important;
  border-radius: 50px !important;
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

/* Loading State */
:deep(.v-progress-circular) {
  color: #42DDF2FF !important;
}
</style>
