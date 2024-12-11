<template>
  <v-card class="match-card" @click="openMatchDialog(match)">
    <div class="match-card-content match-list-card">
      <div class="tournament-header-section">
        <h3 class="match-card-tournament-title">{{ match.tournament_title }}</h3>
        <div class="tournament-format">
          {{ tournamentFormat.toUpperCase() }}
        </div>
      </div>
      <v-card-text>
        <div class="match-layout">
          <div class="team-info-left">
            <v-tooltip location="top">
              <template v-slot:activator="{ props }">
                <v-avatar class="team-avatar" size="60" v-bind="props">
                  <v-img v-if="match.team1_logo" :src="match.team1_logo" :alt="match.team1_name"></v-img>
                  <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>
                </v-avatar>
              </template>
              {{ match.team1_name }}
            </v-tooltip>
            <span class="team-score">{{ match.team1_score }}</span>
          </div>

          <div class="score-divider">:</div>

          <div class="team-info-right">
            <span class="team-score">{{ match.team2_score }}</span>
            <v-tooltip location="top">
              <template v-slot:activator="{ props }">
                <v-avatar class="team-avatar" size="60" v-bind="props">
                  <v-img v-if="match.team2_logo" :src="match.team2_logo" :alt="match.team2_name"></v-img>
                  <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>
                </v-avatar>
              </template>
              {{ match.team2_name }}
            </v-tooltip>
          </div>
        </div>
      </v-card-text>
      <v-divider class="match-divider"></v-divider>
      <v-card-actions class="justify-center pa-4">
        <v-icon icon="mdi-clock-outline" class="mr-2 neon-text"></v-icon>
        <span class="time-text">{{ format(new Date(match.start_time), 'HH:mm, dd MMM yyyy') }}</span>
      </v-card-actions>
      </div>
</v-card>

</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';
import { format } from 'date-fns'
import type { Match } from '@/types/types'


// Props
const props = defineProps<{
  match: Match,
  tournamentFormat: string
}>()

const emit = defineEmits<{
  (e: 'open-match-dialog', match: Match): void
}>()

const openMatchDialog = (match: Match) => {
  emit('open-match-dialog', match)
}
</script>

<style scoped>
/* Card base styles */
.match-card {
  height: 300px;
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  background: rgba(45, 55, 75, 0.4);
  backdrop-filter: blur(10px);
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
  width: 500px;
}

.match-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 0 20px rgba(8, 117, 176, 0.4);
}

.match-card-content {
  position: relative;
  z-index: 3;
  height: 100%;
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

/* Tournament header */
.tournament-header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  height: 100px;
}

.match-card-tournament-title {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.5rem;
  margin: 0;
  font-weight: 600;
  font-family: Orbitron, sans-serif;
  max-width: 250px;
}

.tournament-format {
  display: inline-block;
  background: rgba(17, 78, 112, 0.56);
  color: #42DDF2FF;
  padding: 6px 16px;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 500;
  border: 1px solid rgba(8, 87, 144, 0.8);
  cursor: pointer;
  text-transform: uppercase;
  margin-top: 5px;
}

.tournament-format:hover {
  background: rgba(66, 221, 242, 0.1);
}

/* Match layout */
.match-layout {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 0 10px;
}

.team-info-left, .team-info-right {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
}

.team-avatar {
  min-width: 60px;
  min-height: 60px;
  border: 2px solid #42ddf2;
  background: rgba(8, 87, 144, 0.1);
  transition: transform 0.2s ease;
}

.team-score {
  font-size: 2rem;
  font-weight: bold;
  color: #fed854;
  text-shadow: 0 0 10px rgba(238, 173, 60, 0.5);
}

.team-info-left .team-score {
  margin-left: auto;
  margin-right: 10px;
}

.team-info-right .team-score {
  margin-right: auto;
  margin-left: 10px;
}

.score-divider {
  font-size: 2rem;
  color: #fed854;
  text-shadow: 0 0 10px rgba(238, 173, 60, 0.5);
  margin: 0 8px;
  align-self: center;
}

/* Footer elements */
.match-divider {
  opacity: 0.2;
  margin: 5px 0;
}

.neon-text {
  color: #fed854 !important;
}

.time-text {
  color: rgba(255, 255, 255, 0.7);
}

/* Dialog styles */
:deep(.v-card-title) {
  color: #42DDF2FF !important;
}

.custom-dialog-card {
  width: 600px;
  margin: 0 auto;
  border-radius: 50px;
  background: rgba(45, 55, 75, 0.8);
  backdrop-filter: blur(10px);
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  padding: 10px;
}

.custom-dialog-card .v-btn {
  background: rgba(17, 78, 112, 0.56) !important;
  color: #42DDF2FF !important;
  border: 2px solid #42DDF2FF !important;
  border-radius: 50px;
  min-width: 120px;
  font-weight: bold;
  letter-spacing: 1px;
  transition: all 0.2s ease;
}

.custom-dialog-card .v-btn:hover {
  background: rgba(66, 221, 242, 0.1) !important;
  transform: translateY(-2px);
}
</style>
