<template>
  <div class="team-header-card">
    <div class="team-title-section">
      <h1 class="team-title">
        {{ team.name }}
        <div v-if="canEdit" class="edit-controls">
          <v-icon
            icon="mdi-pencil"
            class="edit-icon ml-2"
            @click="openNameEdit"
            size="26"
          ></v-icon>
          <v-icon
            icon="mdi-camera"
            class="edit-icon ml-2"
            @click="openLogoEdit"
            size="26"
          ></v-icon>
        </div>
      </h1>
    </div>

    <!-- Team Players Section -->
    <div class="players-showcase">
      <div class="players-grid">
        <div v-for="player in team.players"
             :key="player.id"
             class="player-item"
             @click="showPlayerInfo(player)">
          <v-avatar size="80" class="player-avatar" @click="handlePlayerClick(player.id)">
            <v-img v-if="player.avatar" :src="player.avatar" :alt="player.username"></v-img>
            <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>

          </v-avatar>
          <span class="player-name">{{ player.username }}</span>
        </div>
        <!-- Add Player Button -->
        <div v-if="canEdit" class="player-item add-player" @click="openAddPlayerDialog">
          <v-avatar size="80" class="player-avatar add-avatar">
            <v-icon icon="mdi-plus" color="#42DDF2FF" size="40"></v-icon>
          </v-avatar>
          <span class="player-name">Add Player</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { API_URL } from '@/config'
import { useAuthStore } from '@/stores/auth'
import type { Player, Team } from '@/types/types'

// Props
const props = defineProps<{
  team: Team
}>()

// Store
const authStore = useAuthStore()

// State
const showNameEdit = ref(false)
const showLogoEdit = ref(false)
const editedName = ref('')
const logoFile = ref<File | null>(null)
const nameError = ref('')
const logoError = ref('')

// Add player state
const showAddPlayer = ref(false)
const selectedPlayerId = ref('')
const addPlayerError = ref('')

// Computed
const canEdit = computed(() => {
  if (!authStore.isAuthenticated) return false
  return authStore.userRole === 'admin' || authStore.userRole === 'director'
})

// Emit events for parent component
const emit = defineEmits([
  'update:team',
  'refresh',
  'openNameEdit',
  'openLogoEdit',
  'openAddPlayerDialog',
  'player-click',
  'show-player'
])


// Methods
const openNameEdit = () => {
  emit('openNameEdit')
}

const openLogoEdit = () => {
  emit('openLogoEdit')
}

const handlePlayerClick = (playerId: string) => {
  emit('player-click', playerId)
}

const showPlayerInfo = (player: Player) => {
  emit('show-player', player)
}

const openAddPlayerDialog = async () => {
  emit('openAddPlayer')
}

const updateName = async () => {
  try {
    nameError.value = ''
    const response = await fetch(
      `${API_URL}/teams/${props.team.id}?name=${encodeURIComponent(editedName.value)}`,
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

    emit('refresh')
    showNameEdit.value = false
  } catch (e) {
    console.error('Error updating team name:', e)
    nameError.value = (e as Error).message || 'Failed to update team name'
  }
}

const updateLogo = async () => {
  if (!logoFile.value) return
  try {
    logoError.value = ''
    const formData = new FormData()
    formData.append('logo', logoFile.value)

    const response = await fetch(
      `${API_URL}/teams/${props.team.id}`,
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

    emit('refresh')
    showLogoEdit.value = false
  } catch (e) {
    console.error('Error updating team logo:', e)
    logoError.value = (e as Error).message || 'Failed to update team logo'
  }
}

const addPlayer = async () => {
  if (!selectedPlayerId.value) return
  try {
    addPlayerError.value = ''
    const response = await fetch(
      `${API_URL}/players/${selectedPlayerId.value}?team_name=${encodeURIComponent(props.team.name)}`,
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

    emit('refresh')
    showAddPlayer.value = false
  } catch (e) {
    console.error('Error adding player:', e)
    addPlayerError.value = (e as Error).message || 'Failed to add player'
  }
}
</script>

<style scoped>
.team-header-card {
  background: rgba(45, 55, 75, 0.3);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 24px;
  margin-bottom: 24px;
  text-align: center;
  width: 100%;
  max-width: 1000px;
  justify-self: center;
}

/* Title Section */
.team-title-section {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.team-title {
  color: #42DDF2FF;
  font-size: 2.5rem;
  margin-bottom: 20px;
  font-weight: 700;
  text-shadow: 0 0 10px rgba(66, 221, 242, 0.3);
}

/* Edit Controls */
.edit-controls {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.edit-icon {
  color: #42DDF2FF;
  cursor: pointer;
  opacity: 0.7;
  transition: all 0.2s;

  &:hover {
    opacity: 1;
    transform: scale(1.1);
  }
}

/* Players Grid */
.players-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 20px;
  padding: 20px;
}

.player-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-5px);
  }
}

.player-name {
  color: white;
  font-size: 0.9rem;
  opacity: 0.9;
}

/* Avatar Styles */
.player-avatar {
  border: 2px solid #42DDF2FF;
  background: rgba(8, 87, 144, 0.1);
  transition: all 0.2s;

  &:hover {
    transform: scale(1.1);
    box-shadow: 0 0 5px rgba(66, 221, 242, 0.5);
  }
}

/* Add Player Button */
.add-avatar {
  border: 2px dashed #42DDF2FF;
  background: rgba(66, 221, 242, 0.1);
  transition: all 0.2s;

  &:hover {
    border-color: #42DDF2FF;
    background: rgba(66, 221, 242, 0.2);
    transform: scale(1.1);
  }
}

.add-player {
  cursor: pointer;
}
</style>
