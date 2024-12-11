<template>
  <div class="tournament-header-card">
    <div class="tournament-title-section">
      <h1 class="tournament-title">
        {{ tournament.title }}
        <v-icon
          v-if="canEdit"
          icon="mdi-pencil"
          class="edit-icon ml-2"
          @click="openTitleEdit"
        ></v-icon>
      </h1>
      <div class="format-tag">
        {{ formatText(tournament.tournament_format.toUpperCase()) }}
      </div>
    </div>

    <div class="tournament-dates">
      <v-icon icon="mdi-calendar" class="mr-2"></v-icon>
      {{ formatDateRange(tournament.start_date, tournament.end_date) }}
      <v-icon
        v-if="canEdit"
        icon="mdi-pencil"
        class="edit-icon ml-2"
        @click="openEndDateEdit"
      ></v-icon>
    </div>

    <div class="stage-indicator">
      <v-icon icon="mdi-flag-checkered" class="mr-2"></v-icon>
      Current Stage: {{ formatStage(tournament.current_stage) }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { format } from 'date-fns'
import type { Tournament } from '@/types/types'

interface Props {
  tournament: Tournament
  canEdit: boolean
}

// Define props
const props = defineProps<Props>()

// Define emits
const emit = defineEmits<{
  'openTitleEdit': []
  'openEndDateEdit': []
}>()

const formatText = (text: string): string => {
  return text.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
}

const formatDateRange = (startDate: string, endDate: string): string => {
  return `${format(new Date(startDate), 'dd MMM yyyy')} - ${format(new Date(endDate), 'dd MMM yyyy')}`
}

const formatStage = (stage: string): string => {
  if (stage === 'finished') return 'Tournament Completed'
  if (stage === 'final') return 'Finals'
  return stage.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
}

const openTitleEdit = () => {
  emit('openTitleEdit')
}

const openEndDateEdit = () => {
  emit('openEndDateEdit')
}
</script>

<style scoped>
.tournament-header-card {
  background: rgba(45, 55, 75, 0.4);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 24px;
  margin-bottom: 24px;
  width: 100%;
  margin-left: auto;
  margin-right: auto;
}

.tournament-title-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.tournament-title {
  color: #42DDF2FF;
  font-size: 2rem;
  margin: 0;
  display: flex;
  align-items: center;
  font-weight: 700;
}

.format-tag {
  background: rgba(17, 78, 112, 0.56);
  color: #42DDF2FF;
  padding: 6px 16px;
  border-radius: 50px;
  font-size: 0.9rem;
  border: 1px solid rgba(8, 87, 144, 0.8);
}

.tournament-dates {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.1rem;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.stage-indicator {
  color: #FED854FF;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
}

.edit-icon {
  color: #42DDF2FF;
  cursor: pointer;
  opacity: 0.7;
  transition: all 0.2s;
}

.edit-icon:hover {
  opacity: 1;
  transform: scale(1.1);
}
</style>
