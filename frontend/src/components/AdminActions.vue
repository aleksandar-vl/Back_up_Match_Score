<template>
  <div class="actions-card">
    <div class="actions-content">
      <div class="actions-grid">
        <div class="actions-row">
          <v-btn class="action-btn" prepend-icon="mdi-tournament" @click="handleTournamentClick">
            Add Tournament
          </v-btn>
          <v-btn class="action-btn" prepend-icon="mdi-account-group" @click="handleTeamClick">
            Add Team
          </v-btn>
        </div>
        <div class="actions-row">
          <v-btn class="action-btn" prepend-icon="mdi-account" @click="handlePlayerClick">
            Add Player
          </v-btn>
          <v-btn class="action-btn" prepend-icon="mdi-account-edit" @click="handleUpdatePlayerClick">
            Update Player
          </v-btn>
        </div>
      </div>

      <!-- Display Error for Director Actions -->
      <div v-if="actionsError" class="error-message">
        {{ actionsError }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// State
const actionsError = ref<string | null>(null)

// Props
const props = defineProps<{
  openAddTournamentDialog: () => void
  openAddTeamDialog: () => void
  openAddPlayerDialog: () => void
  openUpdatePlayerDialog: () => void
}>()

// Emits
const emit = defineEmits<{
  (e: 'open-tournament'): void
  (e: 'open-team'): void
  (e: 'open-player'): void
  (e: 'open-update-player'): void
}>()

// Methods
const handleTournamentClick = () => {
  try {
    emit('open-tournament')
  } catch (e) {
    console.error('Error opening tournament dialog:', e)
    actionsError.value = 'Failed to open tournament dialog'
  }
}

const handleTeamClick = () => {
  try {
    emit('open-team')
  } catch (e) {
    console.error('Error opening team dialog:', e)
    actionsError.value = 'Failed to open team dialog'
  }
}

const handlePlayerClick = () => {
  try {
    emit('open-player')
  } catch (e) {
    console.error('Error opening player dialog:', e)
    actionsError.value = 'Failed to open player dialog'
  }
}

const handleUpdatePlayerClick = () => {
  try {
    emit('open-update-player')
  } catch (e) {
    console.error('Error opening update player dialog:', e)
    actionsError.value = 'Failed to open update player dialog'
  }
}
</script>

<style scoped>
.actions-card {
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(2px);
  position: relative;
  overflow: hidden;
  padding: 24px;
  width: 65%;
  max-width: 1400px;
  margin: 0 auto 24px;
}

.actions-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.actions-row {
  display: flex;
  gap: 16px;
  justify-content: center;
  width: 100%;
}

.action-btn {
  flex: 1;
  min-width: 200px;
  max-width: 300px;
  height: 56px !important;
  background: #42DDF2FF !important;
  color: #171c26 !important;
  font-weight: bold;
  padding: 0 32px !important;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background: #FED854FF !important;
  box-shadow: 0 0 15px rgba(254, 216, 84, 0.3);
}
</style>
