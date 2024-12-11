<template>
  <div class="team-content-wrapper">
    <v-row class="mt-6">
      <!-- Stats Cards Row -->
      <v-col cols="12" md="4">
        <div class="stats-card">
          <h3 class="section-title">
            <v-icon icon="mdi-trophy" class="mr-2"></v-icon>
            Match Performance
          </h3>
          <div class="stats-list">
            <div class="stat-item">
              <span class="stat-label">Matches Played</span>
              <span class="stat-value">{{ team.team_stats.matches_played }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Matches Won</span>
              <span class="stat-value glow-text">{{ team.team_stats.matches_won }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Win/Loss Ratio</span>
              <span class="stat-value">{{ team.team_stats.match_win_loss_ratio.ratio }}</span>
            </div>
          </div>
        </div>
      </v-col>

      <v-col cols="12" md="4">
        <div class="stats-card">
          <h3 class="section-title">
            <v-icon icon="mdi-medal" class="mr-2"></v-icon>
            Tournament Stats
          </h3>
          <div class="stats-list">
            <div class="stat-item">
              <span class="stat-label">Tournaments Played</span>
              <span class="stat-value">{{ team.team_stats.tournaments_played }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Tournaments Won</span>
              <span class="stat-value glow-text">{{ team.team_stats.tournaments_won }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Win/Loss Ratio</span>
              <span class="stat-value">{{ team.team_stats.tournament_win_loss_ratio.ratio }}</span>
            </div>
          </div>
        </div>
      </v-col>

      <v-col cols="12" md="4">
        <div class="stats-card">
          <h3 class="section-title">
            <v-icon icon="mdi-sword-cross" class="mr-2"></v-icon>
            Rival Analysis
          </h3>
          <div class="stats-list">
            <div class="stat-item">
              <span class="stat-label">Most Frequent Rival</span>
              <span class="stat-value">{{ team.team_stats.most_often_played_opponent || 'N/A' }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Strongest Rival</span>
              <span class="stat-value accent-text">{{ team.team_stats.best_opponent || 'N/A' }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Favorable Matchup</span>
              <span class="stat-value">{{ team.team_stats.worst_opponent || 'N/A' }}</span>
            </div>
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Prizes and Matches Row -->
    <v-row class="mt-6">
      <v-col cols="12" md="6">
        <div class="content-card">
          <h3 class="section-title">
            <v-icon icon="mdi-cat" class="mr-2"></v-icon>
            Achievement Showcase
          </h3>
          <div class="prizes-list">
            <div v-for="prize in team.prize_cuts"
                 :key="prize.id"
                 class="prize-item"
                 :class="{ 'gold': prize.place === 1, 'silver': prize.place === 2 }">
              <div class="prize-trophy">
                <v-icon :icon="prize.place === 1 ? 'mdi-trophy' : 'mdi-trophy-variant'"
                       size="32"
                       :color="prize.place === 1 ? '#FED854FF' : '#C0C0C0'">
                </v-icon>
              </div>
              <div class="prize-details">
                <span class="tournament-name">{{ prize.tournament_name }}</span>
                <span class="prize-place">{{ formatPlace(prize.place) }} Place</span>
              </div>
            </div>
          </div>
        </div>
      </v-col>

      <v-col cols="12" md="6">
        <div class="content-card">
          <h3 class="section-title">
            <v-icon icon="mdi-sword" class="mr-2"></v-icon>
            Recent Matches
          </h3>
          <div class="matches-list">
            <div v-for="match in team.matches"
                 :key="match.id"
                 class="match-item"
                 :class="{ 'match-won': match.winner_id === team.id }">
              <div class="match-teams">
                <span class="team1" :class="{ 'winner': match.winner_id === match.team1_id }">
                  {{ match.team1_name }}
                </span>
                <span class="vs">vs</span>
                <span class="team2" :class="{ 'winner': match.winner_id === match.team2_id }">
                  {{ match.team2_name }}
                </span>
              </div>
              <div class="match-info">
                <span class="tournament-name">{{ match.tournament_title }}</span>
                <span class="match-stage">{{ match.stage }}</span>
              </div>
              <div class="match-result" :class="{ 'won': match.winner_id === team.id }">
                {{ match.winner_id === team.id ? 'Victory' : 'Defeat' }}
              </div>
            </div>
          </div>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import type { Team } from '@/types/types'

// Props
const props = defineProps<{
  team: Team
}>()

// Methods
const formatPlace = (place: number): string => {
  return place === 1 ? '1st' : place === 2 ? '2nd' : place === 3 ? '3rd' : `${place}th`
}
</script>

<style scoped>
/* Base Layout */
.team-content-wrapper {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

/* Card Styles */
.stats-card, .content-card {
  background: rgba(45, 55, 75, 0.4);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 24px;
  height: 100%;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 20px rgba(8, 87, 144, 0.4);
  }
}

/* Section Titles */
.section-title {
  color: #42DDF2FF;
  font-size: 1.4rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

/* Stats Section */
.stats-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: rgba(45, 55, 75, 0.8);
  border: 1px solid rgba(8, 87, 144, 0.5);
  border-radius: 10px;
  transition: all 0.2s;

  &:hover {
    background: rgba(45, 55, 75, 0.9);
    border-color: #42DDF2FF;
  }
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

.stat-value {
  color: white;
  font-weight: 500;
}

/* Text Effects */
.glow-text {
  color: #FED854FF;
  text-shadow: 0 0 10px rgba(254, 216, 84, 0.3);
}

.accent-text {
  color: #42DDF2FF;
  text-shadow: 0 0 10px rgba(66, 221, 242, 0.3);
}

/* Prizes Section */
.prizes-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.prize-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: rgba(45, 55, 75, 0.8);
  border: 1px solid rgba(8, 87, 144, 0.5);
  border-radius: 10px;
  transition: all 0.2s;

  &.gold {
    border-color: #FED854FF;
    background: rgba(254, 216, 84, 0.1);
  }

  &.silver {
    border-color: #C0C0C0;
    background: rgba(192, 192, 192, 0.1);
  }
}

.prize-trophy {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.prize-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.prize-place {
  color: #42DDF2FF;
  font-size: 0.9rem;
}

/* Matches Section */
.matches-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.match-item {
  padding: 16px;
  background: rgba(45, 55, 75, 0.8);
  border: 1px solid rgba(8, 87, 144, 0.5);
  border-radius: 10px;
  transition: all 0.2s;
}

.match-teams {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.team1, .team2 {
  color: white;
  font-size: 1rem;
}

.vs {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.9rem;
}

.winner {
  color: #FED854FF;
  text-shadow: 0 0 10px rgba(254, 216, 84, 0.3);
}

.match-info {
  display: flex;
  justify-content: space-between;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin-top: 8px;
}

.tournament-name {
  color: white;
  font-size: 1rem;
}

.match-stage {
  color: #42DDF2FF;
}

.match-result {
  text-align: center;
  margin-top: 8px;
  font-weight: 500;
  color: #ff4444;

  &.won {
    color: #FED854FF;
    text-shadow: 0 0 10px rgba(254, 216, 84, 0.3);
  }
}
</style>
