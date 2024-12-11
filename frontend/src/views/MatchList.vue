<template>
  <div class="match-list-wrapper">
    <HeaderSection />

    <div class="content-wrapper">
      <v-container>
        <!-- Filter Fields -->
        <MatchFilterBar
          :teams="teams"
          @filter-change="handleFiltersChange"
        />

        <!-- Loading state -->
        <div v-if="isLoadingMatches" class="d-flex justify-center align-center" style="height: 200px">
          <v-progress-circular indeterminate color="#00ff9d"></v-progress-circular>
        </div>

        <!-- Error state -->
        <div v-else-if="matchesError" class="error-text pa-4">
          {{ matchesError }}
        </div>

        <!-- Matches Grid -->
        <v-row v-else justify="center">
          <v-col v-for="match in matches" :key="match.id" cols="12" md="6" class="match-column">
            <MatchCard
              :match="match"
              :tournament-format="getTournamentFormat(match.tournament_id)"
              @open-match-dialog="openMatchDialog"
            />
          </v-col>
        </v-row>

        <!-- Match Modal -->
        <MatchModalDialog
          v-model="showMatchModal"
          :match="selectedMatch"
          :tournamentDirectorId="selectedMatch ? getTournamentDirectorId(selectedMatch.tournament_id) : ''"
          :onMatchUpdate="refreshMatch"
        />

        <!-- Load More Button -->
        <div class="load-more-wrapper">
          <LoadMoreButton
            v-if="!isLoadingMatches && hasMoreMatches"
            :is-loading="isLoadingMore"
            button-text="Load More Matches"
            @load-more="loadMoreMatches"
          />
        </div>
      </v-container>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { API_URL } from '@/config'
import HeaderSection from "@/components/HeaderSection.vue";
import MatchFilterBar from "@/components/MatchFilterBar.vue";
import MatchCard from "@/components/MatchCard.vue";
import LoadMoreButton from "@/components/LoadMoreButton.vue";
import MatchModalDialog from "@/components/dialogs/MatchModalDialog.vue";
import type { Match, Tournament, Team, FilterOption, FilterValuesMatch } from '@/types/types'

const matches = ref<Match[]>([])
const tournaments = ref<Tournament[]>([])
const teams = ref<FilterOption[]>([])
const isLoadingMatches = ref(false)
const matchesError = ref<string | null>(null)
const hasMoreMatches = ref(true)
const isLoadingMore = ref(false)
const showMatchModal = ref(false)
const selectedMatch = ref<Match | null>(null)
const currentLimit = ref<number>(10)

const currentSearch = ref<string>('')
const currentFilters = ref<FilterValuesMatch>({
  stage: null,
  status: null,
  team: null
})

const getSearchFromURL = () => {
  const urlParams = new URLSearchParams(window.location.search)
  return urlParams.get('search') || ''
}

const handleFiltersChange = async (filters: FilterValuesMatch) => {
  try {
    currentSearch.value = ''
    currentFilters.value = filters
    isLoadingMatches.value = true
    matchesError.value = null
    currentLimit.value = 10

    const params = new URLSearchParams()
    params.append('offset', '0')
    params.append('limit', currentLimit.value.toString())

    if (filters.stage) {
      params.append('stage', filters.stage)
    }
    if (filters.status === 'active') {
      params.append('is_finished', 'false')
    }
    if (filters.status === 'finished') {
      params.append('is_finished', 'true')
    }
    if (filters.team) {
      params.append('team_name', filters.team)
    }

    const response = await fetch(`${API_URL}/matches/?${params}`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    const results = Array.isArray(data) ? data : data.results || []
    matches.value = results
    hasMoreMatches.value = results.length === currentLimit.value

  } catch (e) {
    console.error('Error fetching matches:', e)
    matchesError.value = 'Failed to load matches. Please try again later.'
  } finally {
    isLoadingMatches.value = false
  }
}

const fetchMatches = async (loadMore = false) => {
  try {
    if (loadMore) {
      isLoadingMore.value = true
    } else {
      isLoadingMatches.value = true
    }
    matchesError.value = null

    const params = new URLSearchParams()
    const offset = loadMore ? matches.value.length : 0
    params.append('offset', offset.toString())
    params.append('limit', '10')

    const searchTerm = getSearchFromURL()
    if (searchTerm) {
      params.append('search', searchTerm)
    }

    if (currentFilters.value.stage) {
      params.append('stage', currentFilters.value.stage)
    }
    if (currentFilters.value.status === 'active') {
      params.append('is_finished', 'false')
    }
    if (currentFilters.value.status === 'finished') {
      params.append('is_finished', 'true')
    }
    if (currentFilters.value.team) {
      params.append('team_name', currentFilters.value.team)
    }

    const response = await fetch(`${API_URL}/matches/?${params}`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    const results = Array.isArray(data) ? data : (data.results || [])

    if (loadMore) {
      matches.value = [...matches.value, ...results]
    } else {
      matches.value = results
    }
    hasMoreMatches.value = results.length === 10

  } catch (e) {
    console.error('Error fetching matches:', e)
    matchesError.value = 'Failed to load matches. Please try again later.'
  } finally {
    isLoadingMatches.value = false
    isLoadingMore.value = false
  }
}

const loadMoreMatches = async () => {
  await fetchMatches(true);
}


const fetchTournaments = async () => {
  try {
    const response = await fetch(`${API_URL}/tournaments/?offset=0&limit=100`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    tournaments.value = Array.isArray(data) ? data : (data.results || [])
  } catch (e) {
    console.error('Error fetching tournaments:', e)
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

      matches.value = matches.value.map(match =>
        match.id === updatedMatch.id ? updatedMatch : match
      )

      selectedMatch.value = updatedMatch
    } catch (e) {
      console.error('Error refreshing match:', e)
    }
  }
}

const fetchTeams = async () => {
  try {
    const response = await fetch(`${API_URL}/teams/?offset=0&limit=100`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()

    const teamsData = Array.isArray(data) ? data : (data.results || [])

    teams.value = teamsData.map((team: Team) => ({
      text: team.name,
      value: team.name
    }))
  } catch (e) {
    console.error('Error fetching teams:', e)
  }
}

const openMatchDialog = async (match: Match) => {
  try {
    await fetchTournaments()
    const response = await fetch(`${API_URL}/matches/${match.id}`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    selectedMatch.value = await response.json()
    showMatchModal.value = true
  } catch (e) {
    console.error('Error fetching match details:', e)
  }
}

const getTournamentFormat = (tournamentId: string) => {
  const tournament = tournaments.value.find(t => t.id === tournamentId)
  return tournament ? tournament.tournament_format : 'Unknown Format'
}

const getTournamentDirectorId = (tournamentId: string | undefined) => {
  if (!tournamentId) return ''
  console.log('Looking for tournament with ID:', tournamentId)
  console.log('Available tournaments:', tournaments.value)
  const tournament = tournaments.value.find(t => t.id === tournamentId)
  console.log('Full tournament object:', tournament)
  return tournament?.director_id || ''
}

onMounted(() => {
  fetchMatches()
  fetchTournaments()
  fetchTeams()
  window.addEventListener('search-results', ((event: CustomEvent) => {
    if (event.detail.route === '/matches') {
      const searchResults = event.detail.results.filter(result => {
        let matches = true;

        if (currentFilters.value.stage) {
          matches = matches && result.stage === currentFilters.value.stage;
        }
        if (currentFilters.value.status === 'active') {
          matches = matches && !result.is_finished;
        }
        if (currentFilters.value.status === 'finished') {
          matches = matches && result.is_finished;
        }
        if (currentFilters.value.team) {
          matches = matches && (result.team1_name === currentFilters.value.team ||
                              result.team2_name === currentFilters.value.team);
        }

        return matches;
      });

      matches.value = searchResults;
      isLoadingMatches.value = false;
      matchesError.value = null;
    }
  }) as EventListener)
})

onUnmounted(() => {
  window.removeEventListener('search-results', ((event: CustomEvent) => {
    if (event.detail.route === '/matches') {
      const searchResults = event.detail.results.filter(result => {
        let matches = true;
        if (currentFilters.value.stage) {
          matches = matches && result.stage === currentFilters.value.stage;
        }
        if (currentFilters.value.status === 'active') {
          matches = matches && !result.is_finished;
        }
        if (currentFilters.value.status === 'finished') {
          matches = matches && result.is_finished;
        }
        if (currentFilters.value.team) {
          matches = matches && (result.team1_name === currentFilters.value.team ||
                              result.team2_name === currentFilters.value.team);
        }
        return matches;
      });
      matches.value = searchResults;
      isLoadingMatches.value = false;
      matchesError.value = null;
    }
  }) as EventListener)
})
</script>

<style scoped>
.content-wrapper {
  position: relative;
  z-index: 3;
  padding-top: 100px;
  min-height: 100vh;
  width: 100vw !important;
}

.match-column {
  display: flex;
  justify-content: flex-end;
  padding: 8px;
}

.match-column:nth-child(even) {
  justify-content: flex-start;
}

.error-text {
  text-align: center !important;
  color: rgba(255, 255, 255, 0.75);
  padding: 10px;
}

.load-more-wrapper {
  display: flex;
  justify-content: center;
  margin: 40px 0;
  position: relative;
  z-index: 4;
}
</style>
