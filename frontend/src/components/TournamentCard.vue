<template>
  <div class="tournament-card">
    <div class="tournament-content">
      <div class="tournament-header">
        <h3 class="tournament-title">{{ tournament.title }}</h3>
        <div class="format-tag">
          {{ formatText(tournament.tournament_format).toUpperCase() }}
        </div>
      </div>

      <div class="tournament-info">
        <div class="info-section">
          <v-icon icon="mdi-calendar" class="mr-2 info-icon"></v-icon>
          <span>{{ formatDateRange(tournament.start_date, tournament.end_date) }}</span>
        </div>

        <div class="info-section">
          <v-icon icon="mdi-flag" class="mr-2 info-icon"></v-icon>
          <span>Stage: {{ formatStage(tournament.current_stage) }}</span>
        </div>

        <div class="info-section">
          <v-icon icon="mdi-account-group" class="mr-2 info-icon"></v-icon>
          <span>{{ tournament.number_of_teams }} teams</span>
        </div>
      </div>

      <v-btn class="view-details-btn"
             variant="outlined"
             :to="'/events/' + tournament.id">
        View Details
      </v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
import { format } from 'date-fns'

interface TournamentProps {
  tournament: {
    id: string
    title: string
    tournament_format: string
    start_date: string
    end_date: string
    current_stage: string
    number_of_teams: number
  }
}

const props = defineProps<TournamentProps>()

const formatText = (text: string) => {
  return text.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
}

const formatDateRange = (startDate: string, endDate: string) => {
  const start = format(new Date(startDate), 'dd MMM yyyy')
  const end = format(new Date(endDate), 'dd MMM yyyy')
  return `${start} / ${end}`
}

const formatStage = (stage: string) => {
  return stage.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
}
</script>

<style scoped>
/* Card base */
.tournament-card {
  height: 300px;
  width: 500px;
  border-radius: 20px;
  background: rgba(45, 55, 75, 0.4);
  backdrop-filter: blur(10px);
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
  overflow: hidden;
}

.tournament-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 0 20px rgba(8, 117, 176, 0.4);
}

.tournament-content {
  height: 100%;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* Header */
.tournament-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  height: 100px;
}

.tournament-title {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.5rem;
  font-weight: 600;
  font-family: Orbitron, sans-serif;
  max-width: 250px;
}

/* Format tag */
.format-tag {
  background: rgba(17, 78, 112, 0.56);
  color: #42DDF2FF;
  padding: 6px 16px;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 500;
  border: 1px solid rgba(8, 87, 144, 0.8);
}

.format-tag:hover {
  background: rgba(66, 221, 242, 0.1);
}

/* Info section */
.tournament-info {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-section {
  display: flex;
  align-items: center;
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
}

.info-icon {
  color: rgba(66, 221, 242, 0.8) !important;
}

/* Button */
.view-details-btn {
  width: 40%;
  border-radius: 50px;
  margin-top: auto;
  align-self: center;
  color: #42DDF2FF !important;
  border-color: #42DDF2FF !important;
}

.view-details-btn:hover {
  background: rgba(66, 221, 242, 0.1);
}
</style>
