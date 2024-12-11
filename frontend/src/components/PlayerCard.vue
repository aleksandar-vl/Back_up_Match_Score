<template>
  <div class="player-card">
    <div class="player-background"></div>
    <div class="player-content">
      <!-- Top Section with Avatar and Main Info -->
      <div class="player-main-info">
        <!-- Avatar Section -->
        <div class="avatar-section">
          <v-avatar size="150" class="player-avatar" @click="openAvatarUpload">
            <v-img v-if="player?.avatar" :src="player.avatar" alt="Player avatar"></v-img>
            <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="80"></v-icon>
          </v-avatar>
        </div>

        <!-- Player Info -->
        <div class="info-section">
          <div class="info-row">
            <div class="username">{{ player?.username }}</div>
          </div>

          <div class="info-row">
            <div class="full-name">
              {{ player?.first_name }} {{ player?.last_name }}
              <v-icon
                icon="mdi-pencil"
                class="edit-icon"
                @click="openEdit('name')"
              ></v-icon>
            </div>
          </div>

          <div class="info-row">
            <div class="country">
              <v-icon icon="mdi-earth" class="info-icon"></v-icon>
              {{ player?.country }}
            </div>
            <v-icon
              icon="mdi-pencil"
              class="edit-icon"
              @click="openEdit('country')"
            ></v-icon>
          </div>

          <div class="info-row">
            <router-link
              :to="`/teams/${player?.team_id}`"
              class="link"
            >
              <div class="team">
                <v-icon icon="mdi-account-group" class="info-icon"></v-icon>
                {{ player?.team_name }}
              </div>
            </router-link>
            <v-icon
              icon="mdi-pencil"
              class="edit-icon"
              @click="openEdit('team')"
            ></v-icon>
          </div>
        </div>
      </div>

      <!-- Bottom Section with Stats and Tournament -->
      <div class="player-stats-section">
        <!-- Stats Section -->
        <div class="stats-container">
          <div class="stats-header">My stats</div>
          <div class="progress-wrapper">
            <v-progress-linear
              :model-value="parseInt(player?.game_win_ratio)"
              color="#42DDF2FF"
              height="8"
              rounded
              class="progress-bar"
            ></v-progress-linear>
            <span class="win-ratio">{{ player?.game_win_ratio }}</span>
          </div>
        </div>

        <!-- Tournament Section -->
        <div v-if="player?.current_tournament_title" class="tournament-container">
          <router-link
            :to="`/events/${player?.current_tournament_id}`"
            class="link"
          >
            <div class="tournament-header">Current tournament</div>
            <div class="tournament-name">
              <v-icon icon="mdi-trophy" class="tournament-icon"></v-icon>
              {{ player.current_tournament_title }}
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Player, Team } from '@/types/types'
import { useAuthStore } from '@/stores/auth'
import {API_URL} from "@/config";

interface Props {
  player: Player | null
  onEdit?: (field: string) => void
  onAvatarUpload?: () => void
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'edit', field: string): void
  (e: 'avatarUpload'): void
}>()

const authStore = useAuthStore()
const showAvatarDialog = ref(false)
const avatarFile = ref<File | null>(null)
const avatarPreview = ref<string | null>(null)
const avatarError = ref('')
const isLoadingTeams = ref(false)
const teams = ref<Team[]>([])
const teamsError = ref('')

const openAvatarUpload = () => {
  console.log('PlayerCard: Avatar click detected')
  avatarFile.value = null
  avatarPreview.value = null
  avatarError.value = ''
  showAvatarDialog.value = true
  emit('avatarUpload')
}

const openEdit = (field: string) => {
  console.log('PlayerCard: Emitting edit event with field:', field)
  emit('edit', field)
}

</script>

<style scoped>
/* Card base */
.player-card {
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
  padding: 24px;
  width: 100%;
  margin: 0 auto 24px;
  min-height: 500px;
}

.player-background {
  position: absolute;
  inset: 0;
  background-position: center;
  background-size: cover;
  opacity: 0.1;
  z-index: 1;
}

.player-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  height: 100%;
  gap: 32px;
}

/* Main info section */
.player-main-info {
  display: flex;
  gap: 32px;
}

.avatar-section {
  flex-shrink: 0;
}

.player-avatar {
  border: 3px solid #42DDF2FF;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.player-avatar:hover {
  transform: scale(1.05);
  box-shadow: 0 0 20px rgba(66, 221, 242, 0.4);
}

/* Info section */
.info-section {
  flex-grow: 1
}

.info-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.username {
  color: #42DDF2FF;
  font-size: 1.8rem;
  font-weight: 500;
  text-shadow: 0 0 10px rgba(66, 221, 242, 0.3);
}

.full-name {
  color: white;
  font-size: 1.4rem;
}

.country, .team {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Icons */
.info-icon {
  color: #42DDF2FF !important;
}

.edit-icon {
  color: #42DDF2FF;
  opacity: 0.7;
  cursor: pointer;
  transition: all 0.2s;
}

.edit-icon:hover {
  opacity: 1;
  transform: scale(1.1);
}

/* Stats section */
.player-stats-section {
  margin-top: auto;
  padding-top: 24px;
  border-top: 1px solid rgba(66, 221, 242, 0.2);
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.stats-container {
  background: rgba(45, 55, 75, 0.5);
  border-radius: 12px;
  padding: 16px;
  border: 1px solid rgba(66, 221, 242, 0.3);
}

.tournament-container {
  background: rgba(45, 55, 75, 0.5);
  border-radius: 12px;
  padding: 16px;
  border: 1px solid rgba(66, 221, 242, 0.3);
}

:deep(.link) {
  text-decoration: none;
  background: transparent !important;
}

:deep(.link:hover) {
  text-decoration: none;
  background: transparent !important;
}

.stats-header, .tournament-header {
  color: #42DDF2FF;
  font-size: 1.1rem;
  margin-bottom: 12px;
  font-weight: 500;
}

.progress-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-bar {
  flex-grow: 1;
}

.win-ratio {
  color: #42ddf2;
  font-size: 1.1rem;
  min-width: 45px;
  font-weight: 500;
}

.tournament-name {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #FED854FF;
  font-size: 1.1rem;
}

.tournament-icon {
  color: #FED854FF !important;
}
</style>
