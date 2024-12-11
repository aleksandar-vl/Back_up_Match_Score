<template>
  <div class="home-wrapper">
<!--     Header with fade effect-->
    <div class="header-image"></div>
    <div class="header-overlay"></div>


    <div class="content-wrapper">
      <v-container class="matches-container">
        <div class="matches-container-title">Latest Matches</div>
          <!-- Loading -->
          <div v-if="isLoading" class="d-flex justify-center align-center" style="height: 200px">
            <v-progress-circular indeterminate color="#00ff9d"></v-progress-circular>
          </div>

          <!-- Error -->
          <div v-else-if="error" class="error-text pa-4">
            {{ error }}
          </div>

          <!-- When data is present -->
          <v-row v-else no-gutters>
            <v-col
              v-for="match in matches"
              :key="match.id"
              cols="12"
              sm="4"
            >
              <v-sheet class="ma-2 pa-2 transparent">
                <v-card class="match-card">
                  <div class="match-background"></div>
                  <div class="match-content">
                    <div class="tournament-tag">{{ match.tournament_title }}</div>
                    <v-card-text>
                      <div class="match-layout">
                        <div class="team-left">
                          <v-tooltip location="top">
                            <template v-slot:activator="{ props }">
                              <router-link :to="`/teams/${match.team1_id}`" class="foreign-link">
                                <v-avatar class="team-avatar" size="60" v-bind="props">
                                  <v-img v-if="match.team1_logo" :src="match.team1_logo" :alt="match.team1_name"></v-img>
                                  <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>
                                </v-avatar>
                              </router-link>
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
                              <router-link :to="`/teams/${match.team1_id}`" class="foreign-link">
                                <v-avatar class="team-avatar" size="60" v-bind="props">
                                  <v-img v-if="match.team2_logo" :src="match.team2_logo" :alt="match.team2_name"></v-img>
                                  <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>
                                </v-avatar>
                              </router-link>
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
              </v-sheet>
            </v-col>
          </v-row>
      </v-container>


      <!-- Bottom containers -->
      <div class="bottom-containers">
        <!-- Teams -->
        <v-container class="side-container">
          <div class="container-title">Top Teams</div>

          <!-- Loading state -->
          <div v-if="isLoadingTeams" class="d-flex justify-center align-center" style="height: 200px">
            <v-progress-circular indeterminate color="#00ff9d"></v-progress-circular>
          </div>

          <!-- Error state -->
          <div v-else-if="teamsError" class="error-text pa-4">
            {{ teamsError }}
          </div>

          <!-- Teams list -->
          <v-list v-else class="team-list">
            <v-list-item v-for="team in teams" :key="team.id" class="team-item">
              <router-link :to="`/teams/${team.id}`" class="foreign-link">
                <div class="team-header">
                  <div class="team-info-left">
                    <v-avatar class="team-avatar" size="40">
                      <v-img v-if="team.logo" :src="team.logo" alt="Team logo"></v-img>
                      <v-icon v-else icon="mdi-account" color="#42DDF2FF"></v-icon>
                    </v-avatar>
                    <div class="team-name">{{ team.name }}</div>
                  </div>

                    <div class="players-avatars">
                      <v-avatar
                        v-for="player in team.players"
                        :key="player.id"
                        size="30"
                        class="player-avatar"
                      >
                        <v-img v-if="player.avatar && player.avatar !== ''" :src="player.avatar" alt="Player avatar"></v-img>
                        <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="20"></v-icon>
                      </v-avatar>
                    </div>
                </div>
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
              </router-link>
            </v-list-item>
          </v-list>
        </v-container>

        <!-- Tournaments container -->
        <v-container class="side-container">
          <div class="container-title">Tournaments</div>

          <!-- Loading state -->
          <div v-if="isLoadingTournaments" class="d-flex justify-center align-center" style="height: 200px">
            <v-progress-circular indeterminate color="#00ff9d"></v-progress-circular>
          </div>

          <!-- Error state -->
          <div v-else-if="tournamentsError" class="error-text pa-4">
            {{ tournamentsError }}
          </div>

          <!-- Tournaments list -->
          <div v-else class="tournaments-list">
            <div v-for="tournament in tournaments" :key="tournament.id" class="tournament-item">
              <router-link :to="`/events/${tournament.id}`" class="foreign-link">
                <div class="tournament-header">
                  <div class="tournament-title">{{ tournament.title }}</div>
                  <div class="format-tag">{{ formatText(tournament.tournament_format) }}</div>
                </div>
                <div class="tournament-dates">
                  {{ formatDateRange(tournament.start_date, tournament.end_date) }}
                </div>
                <div class="tournament-footer">
                  <div class="stage-tag">
                    Stage: {{ formatStage(tournament.current_stage) }}
                  </div>
                  <div class="teams-count">
                    <span class="count-circle">{{ tournament.number_of_teams }}</span>
                    teams
                  </div>
                </div>
              </router-link>
            </div>
          </div>
        </v-container>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { API_URL } from '@/config'
import { format } from 'date-fns'

interface Match {
  id: string
  match_format: string
  start_time: string
  is_finished: boolean
  stage: string
  team1_id: string
  team2_id: string
  team1_score: number
  team2_score: number
  team1_name: string
  team1_logo: string
  team2_name: string
  team2_logo: string
  winner_id: string | null
  tournament_id: string
  tournament_title: string
}

interface Player {
  id: string
  username: string
  first_name: string
  last_name: string
  country: string
  user_email: string | null
  team_name: string
  avatar: string | null
}

interface Team {
  id: string
  name: string
  logo: string | null
  game_win_ratio: string
  players: Player[]
}

interface Tournament {
  id: string
  title: string
  tournament_format: string
  start_date: string
  end_date: string
  current_stage: string
  number_of_teams: number
}

const matches = ref<Match[]>([])
const isLoading = ref(true)
const error = ref<string | null>(null)

const teams = ref<Team[]>([])
const isLoadingTeams = ref(true)
const teamsError = ref<string | null>(null)

const tournaments = ref<Tournament[]>([])
const isLoadingTournaments = ref(true)
const tournamentsError = ref<string | null>(null)

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

const fetchMatches = async () => {
  try {
    isLoading.value = true
    error.value = null
    const response = await fetch(
      `${API_URL}/matches/?is_finished=true&offset=0&limit=3`
    )
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    matches.value = Array.isArray(data) ? data : (data.results || [])
  } catch (e) {
    console.error('Error fetching matches:', e)
    error.value = 'Failed to load matches. Please try again later.'
  } finally {
    isLoading.value = false
  }
}

const fetchTeams = async () => {
  try {
    isLoadingTeams.value = true
    teamsError.value = null
    const response = await fetch(
      `${API_URL}/teams/?sort_by=desc&offset=0&limit=5`
    )
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    teams.value = Array.isArray(data) ? data : (data.results || [])
  } catch (e) {
    console.error('Error fetching teams:', e)
    teamsError.value = 'Failed to load teams. Please try again later.'
  } finally {
    isLoadingTeams.value = false
  }
}

const fetchTournaments = async () => {
  try {
    isLoadingTournaments.value = true
    tournamentsError.value = null
    const response = await fetch(
      `${API_URL}/tournaments/?status=active&offset=0&limit=5`
    )
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    tournaments.value = Array.isArray(data) ? data : (data.results || [])
  } catch (e) {
    console.error('Error fetching tournaments:', e)
    tournamentsError.value = 'Failed to load tournaments. Please try again later.'
  } finally {
    isLoadingTournaments.value = false
  }
}

onMounted(() => {
  fetchMatches()
  fetchTeams()
  fetchTournaments()
})
</script>

<style scoped>

.matches-container {
  background: rgba(30, 30, 30, 0);
  border-radius: 20px;
  border: 2px solid #42ddf2;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  height: 350px;
  width: 80%;
  max-width: 1500px;
}

.matches-container-title {
  color: #42DDF2FF;
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 10px;
  text-align: center;
  text-shadow: 0 0 10px rgba(8, 87, 144, 0.3);
  justify-self: center;
}

.transparent {
  background: transparent !important;
}

.match-card {
  height: 260px;
  margin-top: -16px;
  position: relative;
  border-radius: 15px;
  overflow: hidden;
  background: rgba(45, 55, 75, 0.8);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  padding: 10px;
  justify-items: center;
}

.match-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-position: center;
  background-size: cover;
  opacity: 0.1;
  z-index: 1;
}

.match-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: auto;
}

.match-layout {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 20px;
  gap: 20px;
}

.team-left, .team-right {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
  gap: 20px;
}

.team-left .team-score {
  margin-left: auto;
}

.team-right .team-score {
  margin-right: auto;
}
.team-left .team-avatar,
.team-right .team-avatar {
  transition: transform 0.2s ease;
}

.team-left .team-avatar:hover,
.team-right .team-avatar:hover {
  transform: scale(1.2);
  cursor: pointer;
}

.match-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 0 20px rgba(8, 117, 176, 0.4) !important;
}

.tournament-tag {
  position: relative;
  top: 0;
  left: 0;
  width: auto;
  max-width: 300px;
  background: rgba(45, 55, 75, 0);
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 1.2rem;
  color: #42DDF2FF;
  border: 1px solid rgba(0, 255, 157, 0);
  font-weight: bold;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.team-name {
  font-size: 1.1rem;
  color: #ffffff;
}

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
  margin: 0;
  align-self: center;
}

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


.bottom-containers {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin: 20px auto 0;
  width: 80%;
  max-width: 1500px;
  padding: 0;
  align-items: flex-start;
}

.side-container {
  flex: 1;
  background: rgba(30, 30, 30, 0);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 20px;
  height: 820px;
  overflow-y: auto;
  min-width: 0;
}

.container-title {
  color: #42DDF2FF;
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
  text-shadow: 0 0 10px rgba(8, 87, 144, 0.3);
}

.team-list {
  margin-top: 27px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: transparent !important;
}

.team-item {
  padding: 16px !important;
  background: rgba(45, 55, 75, 0.8) !important;
  border: 1px solid rgba(8, 87, 144, 0.2) !important;
  border-radius: 10px !important;
  transition: all 0.2s !important;
  height: 130px;
}

.players-avatars {
  display: flex;
  gap: 4px;
  max-width: 200px;
}

.player-avatar {
  border: 1px solid rgba(8, 117, 176, 0.3);
  background: rgba(8, 87, 144, 0.1);
}

.team-item:hover {
  background: rgb(45, 55, 75) !important;
  border-color: #42ddf2 !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(8, 117, 176, 0.2) !important;
}

.team-avatar {
  min-width: 40px;
  min-height: 40px;
  border: 2px solid #42ddf2;
  background: rgba(8, 87, 144, 0.1);
  transition: transform 0.2s ease;
}

.team-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  margin-top: -10px;
}


.team-info-left {
  display: flex;
  align-items: center;
  gap: 12px;
  width: auto;
}

.team-name {
  color: white;
  font-weight: 500;
}

.progress-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.progress-bar {
  width: 200px;
}

.win-ratio {
  color: #42ddf2;
  font-size: 0.9rem;
  min-width: 45px;
  text-align: right;
}


.tournaments-list {
  margin-top: 37px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tournament-item {
  padding: 16px !important;
  background: rgba(45, 55, 75, 0.8) !important;
  border: 1px solid rgba(8, 87, 144, 0.2) !important;
  border-radius: 10px !important;
  transition: all 0.2s !important;
  height: 130px;
}

.tournament-item:hover {
  background: rgb(45, 55, 75) !important;
  border-color: #42ddf2 !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(8, 117, 176, 0.2) !important;
}

.tournament-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  margin-top: -25px;
}

.tournament-title {
  color: white;
  font-weight: 500;
  font-size: 1.1rem;
}

.format-tag {
  background: rgba(8, 117, 176, 0.1);
  color: #42ddf2;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.8rem;
  border: 1px solid rgba(8, 87, 144, 0.8);
}

.tournament-dates {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin-bottom: 12px;
}

.tournament-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stage-tag {
  color: #42ddf2;
  font-size: 0.9rem;
}

.teams-count {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.count-circle {
  background: rgba(8, 117, 176, 0.1);
  color: #42ddf2;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(8, 87, 144, 0.8);
  font-weight: bold;
}


.header-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 600px; /* Adjust height as needed */
  background-image: url('@/assets/top-image.png');
  background-size: cover;
  background-position: center;
  z-index: 1;
  opacity: 0.6;
}

.header-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 600px; /* Same as header-image */
  background: linear-gradient(
    to bottom,
    rgba(23, 28, 38, 0) 0%,
    rgba(23, 28, 38, 0.8) 80%,
    rgba(23, 28, 38, 1) 100%
  );
  z-index: 2;
}

.content-wrapper {
  position: relative;
  z-index: 3;
  padding-top: 400px; /* Adjust based on your needs */
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100vw !important;
  margin-bottom: 100px;
}

.error-text {
  text-align: center !important;
  color: rgba(255, 255, 255, 0.75);
  padding: 10px;
}

.foreign-link {
  text-decoration: none;
  background: transparent !important;
}

.foreign-link:hover {
  text-decoration: none;
  background: transparent !important;
}
</style>
