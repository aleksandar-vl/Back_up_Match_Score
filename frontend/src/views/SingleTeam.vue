<template>
  <div class="team-wrapper">
    <!-- Dynamic header based on team logo -->
    <div
      class="header-image"
      :style="{ backgroundImage: `url(${team?.logo})` }"
    ></div>
    <div class="header-overlay"></div>

    <div class="content-wrapper">
      <v-container v-if="team">
        <!-- Team Header Section -->
        <TeamHeader
          :team="team"
          @refresh="fetchTeamDetails"
          @player-click="handlePlayerClick"
          @show-player="showPlayerInfo"
          @openNameEdit="showNameEdit = true"
          @openLogoEdit="showLogoEdit = true"
          @openAddPlayer="showAddPlayer = true"
        />

        <!-- Team Content Grid -->
        <TeamContentGrid
          :team="team"
        />
      </v-container>

      <!-- Loading State -->
      <div v-else-if="loading" class="loading-container">
        <v-progress-circular indeterminate color="#42DDF2FF"></v-progress-circular>
      </div>
    </div>

    <!-- Player Modal -->
    <PlayerModalDialog
      v-model="showPlayerModal"
      :player="selectedPlayer"
    />
  </div>

  <v-container v-if="team">
    <!-- Name Edit Dialog -->
    <TeamNameDialog
      v-model="showNameEdit"
      :team-id="team.id"
      :current-name="team.name"
      @name-updated="handleNameUpdated"
    />

    <!-- Logo Edit Dialog -->
    <TeamLogoDialog
      v-if="team"
      v-model="showLogoEdit"
      :team-id="team.id"
      @logoUpdated="handleLogoUpdated"
    />

    <!-- Add Player Dialog -->
    <TeamAddPlayerDialog
      v-if="team"
      v-model="showAddPlayer"
      :team-id="team.id"
      :team-name="team.name"
      @playerAdded="handlePlayerAdded"
    />
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { API_URL } from '@/config'
import TeamHeader from "@/components/TeamHeader.vue";
import PlayerModalDialog from "@/components/dialogs/PlayerModalDialog.vue";
import TeamNameDialog from "@/components/dialogs/TeamNameDialog.vue";
import type { Player, Team } from '@/types/types'
import TeamContentGrid from "@/components/TeamContentGrid.vue";
import TeamLogoDialog from "@/components/dialogs/TeamLogoDialog.vue";
import TeamAddPlayerDialog from "@/components/dialogs/TeamAddPlayerDialog.vue";


const route = useRoute()
const team = ref<Team | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)
const playerDialog = ref(false)
const selectedPlayer = ref<Player | null>(null)
const showPlayerModal = ref(false)
const showNameEdit = ref(false)
const showLogoEdit = ref(false)
const showAddPlayer = ref(false)

// Edit handlers
const handlePlayerAdded = async () => {
  try {
    await fetchTeamDetails()
  } catch (error) {
    console.error('Error adding player:', error)
  }
}

const handleLogoUpdated = async () => {
  try {
    await fetchTeamDetails()
  } catch (error) {
    console.error('Error updating logo:', error)
  }
}

const handleNameUpdated = async (newName: string) => {
  try {
    if (team.value) {
      team.value.name = newName
    }
    await fetchTeamDetails()
  } catch (error) {
    console.error('Error handling name update:', error)
  }
}

const handlePlayerClick = (playerId: string) => {
  fetchPlayer(playerId)
  showPlayerModal.value = true
}

const fetchTeamDetails = async () => {
  try {
    loading.value = true
    console.log('Fetching team details...')
    console.log('Team ID:', route.params.id)

    const response = await fetch(`${API_URL}/teams/${route.params.id}`)
    console.log('Response:', response)

    if (!response.ok) {
      throw new Error('Failed to fetch team details')
    }

    const data = await response.json()
    console.log('Team data:', data)
    team.value = data
  } catch (err) {
    console.error('Error fetching team details:', err)
    error.value = 'Failed to load team details'
  } finally {
    loading.value = false
  }
}

const fetchPlayer = async (playerId: string) => {
  try {
    const response = await fetch(`${API_URL}/players/${playerId}`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    selectedPlayer.value = await response.json()
  } catch (e) {
    console.error('Error fetching player:', e)
  }
}

const showPlayerInfo = (player: Player) => {
  fetchPlayer(player.id)
  playerDialog.value = true
}

onMounted(fetchTeamDetails)
</script>

<style scoped>
/* Base Layout */
.team-wrapper {
  min-height: 100vh;
  position: relative;
}

/* Header Styles */
.header-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 900px;
  background-size: cover;
  background-position: center;
  z-index: 1;
  opacity: 0.2;
}

.header-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 900px;
  background: linear-gradient(
    to bottom,
    rgba(23, 28, 38, 0) 0%,
    rgba(23, 28, 38, 0.8) 20%,
    rgba(23, 28, 38, 1) 60%
  );
  z-index: 2;
}

.content-wrapper {
  position: relative;
  z-index: 3;
  padding-top: 100px;
  min-height: 100vh;
  width: 100vw !important;
}

/* Loading State */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
}
</style>
