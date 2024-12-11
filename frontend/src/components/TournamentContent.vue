<template>
  <div class="tournament-content-wrapper">
    <v-row class="mt-6">
      <!-- Left Column: Prizes and Teams -->
      <v-col cols="12" md="4">
        <!-- Prizes Section -->
        <div class="prizes-card">
          <h3 class="section-title">
            <v-icon icon="mdi-cat" class="mr-2"></v-icon>
            Prizes
            <v-icon
              v-if="canEdit"
              icon="mdi-pencil"
              class="edit-icon ml-2"
              @click="openPrizeEdit"
            ></v-icon>
          </h3>
          <div class="prizes-list">
            <div v-for="prize in tournament.prizes" :key="prize.id" class="prize-item">
              <div class="prize-trophy" :class="{ 'gold': prize.place === 1, 'silver': prize.place === 2 }">
                <v-icon :icon="prize.place === 1 ? 'mdi-trophy' : 'mdi-trophy-variant'" size="32"></v-icon>
              </div>
              <div class="prize-details">
                <span class="prize-place">{{ formatPlace(prize.place) }} place</span>
                <span class="prize-amount">{{ prize.prize_cut }} kitty kibbles</span>
              </div>
              <v-tooltip location="top">
                <template v-slot:activator="{ props }">
                  <router-link
                    v-if="prize.team_id"
                    :to="`/teams/${prize.team_id}`"
                    class="winner-team"
                    v-bind="props"
                  >
                    <v-avatar size="50" class="prize-avatar">
                      <v-img
                        v-if="prize.team_logo"
                        :src="prize.team_logo"
                        alt="Winner team logo"
                      ></v-img>
                      <v-icon v-else icon="mdi-shield" color="#42DDF2FF"></v-icon>
                    </v-avatar>
                  </router-link>
                </template>
                {{ prize.team_name }}
              </v-tooltip>
            </div>
          </div>
        </div>

        <!-- Teams List Section -->
        <div class="teams-card">
          <h3 class="section-title">
            <v-icon icon="mdi-account-group" class="mr-2"></v-icon>
            Participating Teams
          </h3>
          <div class="teams-list">
            <router-link
              v-for="team in tournament.teams"
              :key="team.id"
              :to="`/teams/${team.id}`"
              class="team-item"
            >
              <v-avatar size="40" class="team-avatar">
                <v-img v-if="team.logo" :src="team.logo" alt="Team logo"></v-img>
                <v-icon v-else icon="mdi-shield" color="#42DDF2FF"></v-icon>
              </v-avatar>
              <span class="team-name">{{ team.name }}</span>
            </router-link>
          </div>
        </div>
      </v-col>

      <!-- Right Column: Brackets -->
        <v-col cols="12" md="8">
          <div class="brackets-card">
            <div v-if="tournament.current_stage !== 'finished'" class="stage-header">
              <h3 class="section-title">
                <v-icon icon="mdi-tournament" class="mr-2"></v-icon>
                {{ formatStage(tournament.current_stage) }}
              </h3>
            </div>
            <div class="brackets-content">

              <!-- Current Stage Matches -->
              <div v-if="tournament.matches_of_current_stage?.length" class="stage-section current-stage">
                <h5 class="stage-subtitle">Current Stage Matches</h5>
                <div class="matches-grid">
                  <div v-for="match in tournament.matches_of_current_stage"
                       :key="match.id"
                       class="match-card"
                       :class="{ 'match-finished': match.is_finished }"
                       @click="openMatchDialog(match)">
                    <div class="match-content">
                      <div class="match-layout">
                        <div class="team-left">
                          <v-tooltip location="top">
                            <template v-slot:activator="{ props }">
                              <v-avatar class="team-avatar" size="60" v-bind="props">
                                <v-img v-if="match.team1_logo" :src="match.team1_logo" :alt="match.team1_name"></v-img>
                                <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>
                              </v-avatar>
                            </template>
                            {{ match.team1_name }}
                          </v-tooltip>
                          <span class="team-score">{{match.team1_score}}</span>
                        </div>

                        <div class="score-divider">:</div>

                        <div class="team-right">
                          <span class="team-score">{{match.team2_score}}</span>
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

                      <v-divider class="match-divider"></v-divider>

                      <div class="match-footer">
                        <div class="match-time">
                          <v-icon icon="mdi-clock-outline" class="mr-2 neon-text"></v-icon>
                          <span class="time-text">{{ format(new Date(match.start_time), 'HH:mm, dd MMM yyyy') }}</span>
                        </div>

                        <div class="match-winner">
                        <v-icon
                          :icon="match.winner_id ? 'mdi-crown' : 'mdi-crown-outline'"
                          class="winner-icon"
                          :color="match.winner_id ? '#FED854FF' : '#808080'"
                        ></v-icon>
                        <span v-if="match.winner_id" class="winner-text">
                          {{ match.winner_id === match.team1_id ? match.team1_name : match.team2_name }}
                        </span>
                        <span v-else class="winner-text pending">
                          pending...
                        </span>
                      </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Past Matches -->
              <div v-if="pastMatches.length" class="past-matches-section">
                <h5 class="section-title">
                  <v-icon icon="mdi-history" class="mr-2"></v-icon>
                  Previous Matches
                </h5>

                <!-- Group matches by stage -->
                <div v-for="stage in getUniqueStages(pastMatches)"
                     :key="stage"
                     class="stage-section">
                  <h6 class="stage-subtitle">{{ formatStage(stage) }}</h6>
                  <div class="matches-grid">
                    <div v-for="match in filterMatchesByStage(pastMatches, stage)"
                         :key="match.id"
                         class="match-card past-match"
                         @click="openMatchDialog(match)">
                      <div class="match-content">
                        <!-- Використовуємо той самий template що й для поточних матчів -->
                        <div class="match-layout">
                          <div class="team-left">
                            <v-tooltip location="top">
                              <template v-slot:activator="{ props }">
                                <v-avatar class="team-avatar" size="60" v-bind="props">
                                  <v-img v-if="match.team1_logo" :src="match.team1_logo" :alt="match.team1_name"></v-img>
                                  <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>
                                </v-avatar>
                              </template>
                              {{ match.team1_name }}
                            </v-tooltip>
                            <span class="team-score">{{match.team1_score}}</span>
                          </div>

                          <div class="score-divider">:</div>

                          <div class="team-right">
                            <span class="team-score">{{match.team2_score}}</span>
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

                        <v-divider class="match-divider"></v-divider>

                        <div class="match-footer">
                          <div class="match-time">
                            <v-icon icon="mdi-clock-outline" class="mr-2 neon-text"></v-icon>
                            <span class="time-text">{{ format(new Date(match.start_time), 'HH:mm, dd MMM yyyy') }}</span>
                          </div>

                          <div class="match-winner" v-if="match.winner_id">
                            <v-icon icon="mdi-crown" color="#fed854" size="24"></v-icon>
                            <span class="winner-text">
                              {{ match.winner_id === match.team1_id ? match.team1_name : match.team2_name }}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Loading States -->
              <div v-if="isPastMatchesLoading" class="loading-state">
                <v-progress-circular indeterminate color="#42DDF2FF"></v-progress-circular>
              </div>
            </div>
          </div>
        </v-col>
    </v-row>
  </div>
</template>


<script setup lang="ts">
import { format } from 'date-fns'
import type { Prize, Team, Match, Tournament } from '@/types/types'

// Props
interface Props {
  tournament: Tournament
  pastMatches: Match[]
  isPastMatchesLoading: boolean
  canEdit: boolean
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  'openPrizeEdit': []
  'openMatchDialog': [match: Match]
}>()

// Methods
const formatPlace = (place: number): string => {
  return place === 1 ? '1st' : place === 2 ? '2nd' : `${place}th`
}

const formatStage = (stage: string): string => {
  if (stage === 'finished') return 'Tournament Completed'
  if (stage === 'final') return 'Finals'
  return stage.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
}

const getUniqueStages = (matches: Match[]) => {
  return [...new Set(matches.map(match => match.stage))].sort((a, b) => {
    const stageOrder = {
      'group_stage': 1,
      'quarter_finals': 2,
      'semi_finals': 3,
      'final': 4
    }
    return (stageOrder[a as keyof typeof stageOrder] || 99) - (stageOrder[b as keyof typeof stageOrder] || 99)
  })
}

const filterMatchesByStage = (matches: Match[], stage: string) => {
  return matches.filter(match => match.stage === stage)
}

const openPrizeEdit = () => {
  emit('openPrizeEdit')
}

const openMatchDialog = (match: Match) => {
  emit('openMatchDialog', match)
}
</script>

<style scoped>
.tournament-content-wrapper {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

/* Card Styles */
.prizes-card, .teams-card, .brackets-card {
  background: rgba(45, 55, 75, 0.4);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 24px;
}

.prizes-card {
  margin-bottom: 24px;
}

.brackets-card {
  height: 100%;
  min-height: 600px;
  padding: 24px 10px;
}

.brackets-content {
  padding: 24px;
  height: auto;
  min-height: 500px;
  background: rgba(45, 55, 75, 0);
  border-radius: 12px;
  margin-top: 0;
}

/* Section Titles */
.section-title {
  text-align: center;
  width: 100%;
  margin-bottom: 16px;
  color: #42DDF2FF;
  font-size: 1.4rem;
  display: flex;
  align-items: center;
}

.stage-subtitle {
  color: #FED854FF;
  font-size: 1.2rem;
  margin-bottom: 20px;
  padding-left: 16px;
  border-left: 3px solid #FED854FF;
}

/* Teams List */
.teams-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.team-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(45, 55, 75, 0.8);
  border: 1px solid rgba(8, 87, 144, 0.5);
  border-radius: 10px;
  transition: all 0.2s;
  text-decoration: none;
}

.team-item:hover {
  background: rgb(45, 55, 75);
  border-color: #42DDF2FF;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(8, 117, 176, 0.2);
}

.team-name {
  color: white;
  font-size: 1.1rem;
}

/* Prizes Section */
.prize-avatar {
  min-width: 55px;
  min-height: 55px;
  border: 2px solid #42ddf2;
  background: rgba(8, 87, 144, 0.1);
  transition: transform 0.2s;
  cursor: pointer;
}

.prize-avatar:hover {
  transform: scale(1);
}

.prizes-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.prize-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 10px;
}

.prize-trophy {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.prize-trophy.gold {
  color: #FED854FF;
  background: rgba(254, 216, 84, 0.1);
  border: 2px solid #FED854FF;
}

.prize-trophy.silver {
  color: #c6c6c6;
  background: rgba(192, 192, 192, 0.1);
  border: 2px solid #C0C0C0;
}

.prize-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.prize-place {
  color: white;
  font-size: 1.1rem;
  font-weight: 500;
}

.prize-amount {
  color: rgba(64, 231, 237, 0.73);
  font-size: 0.9rem;
  font-weight: 550;
}

.winner-team {
  text-decoration: none;
  background: transparent !important;
}

.winner-team v-avatar {
  border: 2px solid #42DDF2FF;
  transition: transform 0.2s;
  background: transparent !important;
}

.winner-team:hover {
  background: transparent !important;
  transform: scale(1.2);
}

/* Match Card Styles */
.matches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.match-card {
  height: 250px;
  border-radius: 15px;
  overflow: hidden;
  background: rgba(45, 55, 75, 0);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  padding: 20px;
}

.match-card:hover {
  transform: translateY(-2px);
  border-color: #42DDF2FF;
  box-shadow: 0 4px 8px rgba(8, 117, 176, 0.2);
  cursor: pointer;
}

.match-card.match-finished {
  border: 2px solid #FED854FF !important;
  box-shadow: 0 0 15px rgba(254, 216, 84, 0.2);
}

.match-card.match-finished:hover {
  box-shadow: 0 0 20px rgba(254, 216, 84, 0.3);
}

.match-layout {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
  gap: 20px;
  padding: 0 10px;
}

.team-left, .team-right {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  flex: 1;
}

.team-left .team-score {
  margin-left: auto;
}

.team-right .team-score {
  margin-right: auto;
}

/* Team Avatar Styles */
.team-avatar {
  min-width: 55px;
  min-height: 55px;
  border: 2px solid #42ddf2;
  background: rgba(8, 87, 144, 0.1);
  transition: transform 0.2s;
  cursor: pointer;
}

.team-avatar:hover {
  transform: scale(1.2);
}

.team-avatar-link {
  text-decoration: none;
  background: transparent !important;
}

.team-avatar-link:hover {
  background: transparent !important;
}

/* Score Styles */
.team-score {
  font-size: 2rem;
  font-weight: bold;
  color: #fed854;
  text-shadow: 0 0 10px rgba(238, 173, 60, 0.5);
}

.score-divider {
  font-size: 2rem;
  color: #FED854FF;
  text-shadow: 0 0 10px rgba(238, 173, 60, 0.5);
  margin: 0 8px;
}

/* Match Footer */
.match-footer {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
}

.match-time {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  text-align: center;
  margin-bottom: 16px;
}

.match-winner {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #FED854FF;
  font-weight: 500;
}

.winner-text {
  font-size: 0.9rem;
}

.winner-text.pending {
  color: #808080;
  font-style: italic;
}

.neon-text {
  color: #fed854 !important;
}

/* Loading & Error States */
.loading-matches, .matches-error {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  color: #42DDF2FF;
}

/* Edit Controls */
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

/* Vuetify Overrides */
:deep(.v-card-title) {
  color: #42DDF2FF !important;
}

:deep(.v-text-field) {
  color: white !important;
}

:deep(.v-field__input) {
  color: white !important;
}

:deep(.v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}

:deep(.v-field__outline) {
  color: rgba(66, 221, 242, 0.3) !important;
}

:deep(.v-btn) {
  text-transform: none;
}

:deep(.v-alert) {
  background-color: rgba(254, 216, 84, 0.1) !important;
  color: #fed854 !important;
  border-color: #fed854 !important;
}

:deep(.v-alert__close-button),
:deep(.v-alert__prepend) {
  color: #fed854 !important;
}



/* Media Queries */
@media (max-width: 768px) {
  .matches-grid {
    grid-template-columns: 1fr;
  }
}
</style>

