<template>
  <div class="team-card">
    <div class="team-content">
      <div class="team-header">
        <div class="team-left-section">
          <v-avatar class="team-avatar" size="100">
            <v-img v-if="team.logo" :src="team.logo" alt="Team logo"></v-img>
            <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="100"></v-icon>
          </v-avatar>
          <div class="team-info">
            <div class="team-title">{{ team.name }}</div>
            <div class="players-avatars">
              <v-avatar
                v-for="(player, index) in team.players.slice(0, 10)"
                :key="player.id"
                size="40"
                class="player-avatar"
                @click="handlePlayerClick(player.id)"
              >
                <v-img v-if="player.avatar && player.avatar !== ''" :src="player.avatar" alt="Player avatar"></v-img>
                <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="24"></v-icon>
              </v-avatar>
            </div>
          </div>
        </div>

        <div class="team-right-section">
          <div class="progress-wrapper">
            <v-progress-linear
              :model-value="parseInt(team.game_win_ratio)"
              color="#42DDF2FF"
              height="6"
              rounded
              class="progress-bar"
            ></v-progress-linear>
            <span class="win-ratio">{{ team.game_win_ratio }}</span>
          </div>
        </div>
      </div>

      <v-btn class="view-details-btn" variant="outlined" :to="'/teams/' + team.id">
        VIEW DETAILS
      </v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
import type { Player, Team } from '@/types/types'

interface Props {
  team: Team
}
const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  (e: 'player-click', playerId: string): void
}>()

// Methods
const handlePlayerClick = (playerId: string) => {
  emit('player-click', playerId)
}
</script>

<style scoped>
/* Card base */
.team-card {
  height: 400px;
  width: 500px;
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  background: rgba(45, 55, 75, 0.4);
  backdrop-filter: blur(10px);
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
}

.team-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 0 20px rgba(8, 117, 176, 0.4);
}

.team-content {
  height: 100%;
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

/* Team header and info */
.team-header {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
}

.team-left-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.team-title {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.5rem;
  font-weight: 600;
  font-family: Orbitron, sans-serif;
  text-align: center;
}

/* Avatars */
.team-avatar {
  width: 80px;
  height: 80px;
  border: 2px solid #42ddf2;
  background: rgba(8, 87, 144, 0.1);
}

.players-avatars {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  width: 260px;
  height: 110px;
  padding: 8px;
  border-radius: 12px;
  border: 2px solid rgba(66, 221, 242, 0.2);
  margin-bottom: -20px;
}

.player-avatar {
  border: 1px solid rgba(66, 221, 242, 0.3);
  background: rgba(8, 87, 144, 0.1);
  transition: transform 0.2s;
  cursor: pointer;
  align-self: center;
}

.player-avatar:hover {
  transform: scale(1.5);
}

/* Progress section */
.progress-wrapper {
  width: 60%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  justify-self: center;
}

.progress-bar {
  flex-grow: 1;
  border-radius: 8px;
  background: rgba(8, 87, 144, 0.2);
}

.win-ratio {
  color: #42ddf2;
  font-size: 1rem;
  font-weight: 500;
  min-width: 45px;
}

/* Button */
.view-details-btn {
  margin-top: auto;
  color: #42DDF2FF !important;
  border-color: #42DDF2FF !important;
  border-radius: 50px;
  width: 60%;
  align-self: center;
}

.view-details-btn:hover {
  background: rgba(66, 221, 242, 0.1);
}
</style>
