<template>
  <div class="tournament-wrapper">
    <!-- Dynamic header based on tournament format -->
    <div
      class="header-image"
      :style="{ backgroundImage: `url(${getTournamentBackground(tournament?.tournament_format)})` }"
    ></div>
    <div class="header-overlay"></div>

    <div class="content-wrapper">
      <v-container v-if="tournament">
        <!-- Tournament Header Section -->
        <TournamentHeader
          :tournament="tournament"
          :canEdit="canEdit"
          @openTitleEdit="showTitleEdit = true"
          @openEndDateEdit="showEndDateEdit = true"
        />

        <!-- Tournament Content Grid -->
        <TournamentContent
          :tournament="tournament"
          :pastMatches="pastMatches"
          :isPastMatchesLoading="isPastMatchesLoading"
          :canEdit="canEdit"
          @openPrizeEdit="showPrizeEdit = true"
          @openMatchDialog="openMatchDialog"
        />
      </v-container>

      <!-- Loading State -->
      <div v-else-if="isLoading" class="loading-container">
        <v-progress-circular indeterminate color="#42DDF2FF"></v-progress-circular>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-container">
        {{ error }}
      </div>
    </div>

    <!-- Title Edit Dialog -->
    <TournamentTitleDialog
      v-model="showTitleEdit"
      :currentTitle="tournament?.title || ''"
      :error="titleError"
      @save="handleTitleUpdate"
    />

    <!-- End Date Edit Dialog -->
    <TournamentEndDateDialog
      v-model="showEndDateEdit"
      :current-end-date="tournament?.end_date || ''"
      :error="endDateError"
      @save="handleEndDateUpdate"
    />

    <!-- Prize Edit Dialog -->
    <TournamentPrizeDialog
      v-model="showPrizeEdit"
      :currentPrizePool="tournamentPrizePool"
      :error="prizeError"
      @save="handlePrizeUpdate"
    />

    <!-- Match Modal -->
    <MatchModalDialog
      v-model="showMatchModal"
      :match="selectedMatch"
      :tournamentDirectorId="tournament?.director_id"
      :onMatchUpdate="refreshMatch"
    />
  </div>
</template>

<script setup lang="ts">
import '@/styles/vuetify.css'
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { API_URL } from '@/config'
import singleEliminationBg from '@/assets/single-elimination.png'
import roundRobinBg from '@/assets/round-robin.png'
import oneOffMatchBg from '@/assets/one-off-match.png'
import MatchModalDialog from "@/components/dialogs/MatchModalDialog.vue";
import TournamentHeader from "@/components/TournamentHeader.vue";
import TournamentContent from "@/components/TournamentContent.vue";
import TournamentTitleDialog from "@/components/dialogs/TournamentTitleDialog.vue";
import TournamentEndDateDialog from "@/components/dialogs/TournamentEndDateDialog.vue";
import type { Match, Tournament } from '@/types/types'
import TournamentPrizeDialog from "@/components/dialogs/TournamentPrizeDialog.vue";

const route = useRoute()
const authStore = useAuthStore()

const isInitialized = ref(false)
const tournament = ref<Tournament | null>(null)
const isLoading = ref(true)
const error = ref<string | null>(null)

const showTitleEdit = ref(false)
const showEndDateEdit = ref(false)
const showPrizeEdit = ref(false)

const titleError = ref('')
const endDateError = ref('')
const prizeError = ref('')

const showMatchModal = ref(false)
const selectedMatch = ref<Match | null>(null)

const allTournamentMatches = ref<Match[]>([])
const isLoadingMatches = ref(false)
const matchesError = ref<string | null>(null)


const pastMatches = ref<Match[]>([])
const isPastMatchesLoading = ref(false)
const pastMatchesError = ref<string | null>(null)

const tournamentPrizePool = computed(() => {
  if (!tournament.value?.prizes?.length) return 0;
  return tournament.value.prizes.reduce((sum, prize) => sum + prize.prize_cut, 0);
});

const canEdit = computed(() => {
  if (!isInitialized.value || !tournament.value || !authStore.isAuthenticated) return false
  return authStore.userRole === 'admin' || tournament.value.director_id === authStore.userId
})

const getTournamentBackground = (format: string | undefined): string => {
  if (!format) return ''
  const formatMap: Record<string, string> = {
    'round robin': roundRobinBg,
    'one off match': oneOffMatchBg,
    'single elimination': singleEliminationBg
  }
  return formatMap[format] || ''
}

const fetchAllTournamentMatches = async () => {
  if (!tournament.value?.title) {
    console.log('No tournament title available:', tournament.value);
    return;
  }

  try {
    isLoadingMatches.value = true;
    matchesError.value = null;

    const url = `${API_URL}/matches/?tournament_title=${encodeURIComponent(tournament.value.title)}`;
    console.log('Attempting to fetch matches from URL:', url);

    const response = await fetch(url, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        ...(authStore.token ? { 'Authorization': `Bearer ${authStore.token}` } : {})
      }
    });

    console.log('Response status:', response.status);
    console.log('Response headers:', Object.fromEntries(response.headers.entries()));

    if (!response.ok) {
      console.log('Response not OK. Full response:', response);
      const errorText = await response.text();
      console.log('Error response text:', errorText);
      throw new Error('Failed to fetch tournament matches');
    }

    const data = await response.json();
    console.log('Received matches data:', data);
    allTournamentMatches.value = data;

  } catch (e) {
    console.error('Detailed error in fetchAllTournamentMatches:', e);
    console.error('Error stack:', e.stack);
    matchesError.value = 'Failed to load tournament matches';
  } finally {
    isLoadingMatches.value = false;
  }
}

const refreshMatch = async () => {
  if (selectedMatch.value) {
    try {
      const response = await fetch(`${API_URL}/matches/${selectedMatch.value.id}`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const updatedMatch = await response.json()

      if (pastMatches.value) {
        pastMatches.value = pastMatches.value.map(match =>
          match.id === updatedMatch.id ? updatedMatch : match
        )
      }

      if (allTournamentMatches.value) {
        allTournamentMatches.value = allTournamentMatches.value.map(match =>
          match.id === updatedMatch.id ? updatedMatch : match
        )
      }

      selectedMatch.value = updatedMatch
    } catch (e) {
      console.error('Error refreshing match:', e)
    }
  }
}

const fetchPastMatches = async () => {
  if (!tournament.value?.title) return

  try {
    isPastMatchesLoading.value = true
    pastMatchesError.value = null

    const url = `${API_URL}/matches/?tournament_title=${encodeURIComponent(tournament.value.title)}&is_finished=true`
    console.log('Fetching past matches from:', url)

    const response = await fetch(url, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        ...(authStore.token ? { 'Authorization': `Bearer ${authStore.token}` } : {})
      }
    })

    if (!response.ok) {
      throw new Error('Failed to fetch past matches')
    }

    const data = await response.json()
    pastMatches.value = data
    console.log('Past matches loaded:', pastMatches.value)
  } catch (e) {
    console.error('Error fetching past matches:', e)
    pastMatchesError.value = 'Failed to load past matches'
  } finally {
    isPastMatchesLoading.value = false
  }
}

const fetchTournament = async () => {
  try {
    isLoading.value = true
    error.value = null
    const response = await fetch(`${API_URL}/tournaments/${route.params.id}`)
    if (!response.ok) throw new Error('Failed to fetch tournament details')
    const data = await response.json()
    tournament.value = data
  } catch (e) {
    console.error('Error fetching tournament:', e)
    error.value = 'Failed to load tournament details'
  } finally {
    isLoading.value = false
  }
}

const handleTitleUpdate = async (newTitle: string) => {
  try {
    if (!tournament.value) return

    console.log('Updating title with:', {
      tournamentId: tournament.value.id,
      newTitle: newTitle
    })

    const response = await fetch(
      `${API_URL}/tournaments/${tournament.value.id}?title=${encodeURIComponent(newTitle)}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      }
    )

    const responseText = await response.text()

    if (!response.ok) {
      let errorMessage
      try {
        const errorData = JSON.parse(responseText)
        console.log('Error data:', errorData)
        console.log('Error data type:', typeof errorData)

        if (errorData.detail && Array.isArray(errorData.detail) && errorData.detail[0]?.msg) {
          errorMessage = errorData.detail[0].msg
        } else {
          errorMessage = errorData.detail || 'Failed to update tournament title'
        }
      } catch {
        errorMessage = 'Failed to update tournament title'
      }

      titleError.value = errorMessage
      return
    }

    await fetchTournament()
    showTitleEdit.value = false
  } catch (e) {
    console.error('Update error:', e)
    titleError.value = 'An unexpected error occurred while updating the title'
  }
}

const handleEndDateUpdate = async (newEndDate: string) => {
  try {
    if (!tournament.value) return

    const response = await fetch(
      `${API_URL}/tournaments/${tournament.value.id}?end_date=${encodeURIComponent(newEndDate)}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      }
    )

    const responseText = await response.text()

    if (!response.ok) {
      let errorMessage
      try {
        const errorData = JSON.parse(responseText)

        // FastAPI validation error
        if (errorData.detail && Array.isArray(errorData.detail) && errorData.detail[0]?.msg) {
          errorMessage = errorData.detail[0].msg
        } else {
          // HTTP error
          errorMessage = errorData.detail || 'Failed to update end date'
        }
      } catch {
        errorMessage = 'Failed to update end date'
      }

      endDateError.value = errorMessage
      return
    }

    await fetchTournament()
    showEndDateEdit.value = false
  } catch (e) {
    console.error('Update error:', e)
    endDateError.value = 'An unexpected error occurred while updating the end date'
  }
}

const handlePrizeUpdate = async (newPrizePool: number) => {
  try {
    if (!tournament.value) return

    console.log('Updating prize pool with:', {
      tournamentId: tournament.value.id,
      newPrizePool: newPrizePool
    })

    const response = await fetch(
      `${API_URL}/tournaments/${tournament.value.id}?prize_pool=${newPrizePool}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      }
    )

    const responseText = await response.text()

    if (!response.ok) {
      let errorMessage
      try {
        const errorData = JSON.parse(responseText)

        // FastAPI validation error
        if (errorData.detail && Array.isArray(errorData.detail) && errorData.detail[0]?.msg) {
          errorMessage = errorData.detail[0].msg
        } else {
          // HTTP error
          errorMessage = errorData.detail || 'Failed to update prize pool'
        }
      } catch {
        errorMessage = 'Failed to update prize pool'
      }

      prizeError.value = errorMessage
      return
    }

    await fetchTournament()
    showPrizeEdit.value = false
  } catch (e) {
    console.error('Update error:', e)
    prizeError.value = 'An unexpected error occurred while updating the prize pool'
  }
}

const openMatchDialog = async (match: Match) => {
  selectedMatch.value = match
  showMatchModal.value = true
}

onMounted(async () => {
  console.log('Component mounted');
  await authStore.initializeFromToken();
  console.log('Auth initialized');
  isInitialized.value = true;

  await fetchTournament();
  console.log('Tournament fetched:', tournament.value);
  console.log('Current stage:', tournament.value?.current_stage);

  await fetchPastMatches();

  if (tournament.value?.current_stage === 'finished') {
    console.log('Tournament is finished, fetching all matches...');
    await fetchAllTournamentMatches();
  } else {
    console.log('Tournament is not finished, current stage:', tournament.value?.current_stage);
  }
});


</script>

<style scoped>
.tournament-wrapper {
  min-height: 100vh;
  position: relative;
}

/* Header Styles */
.header-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 700px;
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
  height: 700px;
  background: linear-gradient(
    to bottom,
    rgba(23, 28, 38, 0) 0%,
    rgba(23, 28, 38, 0.8) 20%,
    rgba(23, 28, 38, 1) 40%
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

/* Card Styles */
.tournament-header-card, .teams-card, .prizes-card, .brackets-card {
  background: rgba(45, 55, 75, 0.4);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 24px;
  margin-bottom: 24px;
}

.section-title {
  text-align: center;
  width: 100%;
  margin-bottom: 24px;
  color: #42DDF2FF;
  font-size: 1.4rem;
  display: flex;
  align-items: center;
}

/* Team Styles */
.team-avatar {
  min-width: 55px;
  min-height: 55px;
  border: 2px solid #42ddf2;
  background: rgba(8, 87, 144, 0.1);
  transition: transform 0.2s ease;
}

.team-avatar:hover {
  transform: scale(1.2);
}

.team-info-left, .team-info-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.team-score {
  font-size: 2rem;
  font-weight: bold;
  color: #fed854;
  text-shadow: 0 0 10px rgba(238, 173, 60, 0.5);
}

/* Match Styles */
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

.match-layout {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 0 10px;
}

.score-divider {
  font-size: 2rem;
  color: #FED854FF;
  text-shadow: 0 0 10px rgba(238, 173, 60, 0.5);
  margin: 0 8px;
}

/* Dialog Styles */
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

/* Loading and Error States */
.loading-container, .error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
}

.error-container {
  color: #FED854FF;
  font-size: 1.2rem;
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

/* Media Queries */
@media (max-width: 768px) {
  .matches-grid {
    grid-template-columns: 1fr;
  }
}

</style>
