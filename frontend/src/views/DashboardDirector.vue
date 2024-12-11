<template>
  <HeaderSection />

  <div class="content-wrapper">
    <v-container>
      <!-- Director Welcome Section -->
      <DashboardWelcome :userRole="'Director'" />

      <!-- Actions and Filters Wrapper -->
      <div class="tournaments-section">

        <!-- Action Buttons Section -->
        <AdminActions
          :openAddTournamentDialog="openAddTournamentDialog"
          :openAddTeamDialog="openAddTeamDialog"
          :openAddPlayerDialog="openAddPlayerDialog"
          :openUpdatePlayerDialog="openUpdatePlayerDialog"
          @open-tournament="openAddTournamentDialog"
          @open-team="openAddTeamDialog"
          @open-player="openAddPlayerDialog"
          @open-update-player="openUpdatePlayerDialog"
        />

        <!-- Filter section -->
        <FilterBar @filter-change="handleFiltersChange"/>
      </div>

      <!-- Tournaments Content -->
      <div class="tournaments-section">
        <!-- Loading state -->
        <div v-if="isLoadingTournaments" class="d-flex justify-center align-center" style="height: 200px">
          <v-progress-circular indeterminate color="#00ff9d"></v-progress-circular>
        </div>

        <!-- Error state -->
        <div v-else-if="tournamentsError" class="error-text pa-4">
          {{ tournamentsError }}
        </div>

        <!-- Empty state -->
        <div v-else-if="!tournaments.length" class="empty-state">
          <v-icon icon="mdi-tournament" size="64" color="#42DDF2FF" class="mb-4"></v-icon>
          <div class="empty-text">No tournaments created yet</div>
          <div class="empty-subtext">Get started by clicking the "Add Tournament" button</div>
        </div>

        <!-- Tournament Cards Grid -->
        <v-row v-else>
          <v-col v-for="tournament in tournaments"
             :key="tournament.id"
             cols="12"
             md="6"
             class="tournament-column">
            <TournamentCard :tournament="tournament" />
          </v-col>
        </v-row>

        <!-- Load More Button -->
        <LoadMoreButton
          v-if="!isLoadingTournaments && hasMoreTournaments"
          :is-loading="isLoadingMore"
          button-text="Load More Tournaments"
          @load-more="loadMoreTournaments"
        />
      </div>

      <!-- Dialogs -->
      <AddTournamentDialog
        v-model="showAddTournamentDialog"
        @tournament-added="handleTournamentAdded"
      />
      <AddTeamDialog
        v-model="showAddTeamDialog"
        @team-added="handleTeamAdded"
      />
      <AddPlayerDialog
        v-model="showAddPlayerDialog"
        @player-added="handlePlayerAdded"
      />
      <UpdatePlayerDialog
        v-model="showUpdatePlayerDialog"
        @player-updated="handlePlayerUpdated"
      />

      <!-- Success Snackbar -->
      <v-snackbar v-model="showSuccessAlert" color="success" timeout="3000">
        {{ successMessage }}
      </v-snackbar>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { API_URL } from '@/config'
import DashboardWelcome from "@/components/DashboardWelcome.vue";
import AdminActions from "@/components/AdminActions.vue";
import FilterBar from "@/components/TournamentFilterBar.vue";
import TournamentCard from "@/components/TournamentCard.vue";
import AddTournamentDialog from "@/components/dialogs/AddTournamentDialog.vue";
import AddTeamDialog from "@/components/dialogs/AddTeamDialog.vue";
import UpdatePlayerDialog from "@/components/dialogs/UpdatePlayerDialog.vue";
import AddPlayerDialog from "@/components/dialogs/AddPlayerDialog.vue";
import type { Tournament, Player, FilterValuesTournament } from '@/types/types'
import LoadMoreButton from "@/components/LoadMoreButton.vue";
import HeaderSection from "@/components/HeaderSection.vue";
import {useAuthStore} from "@/stores/auth";

const tournaments = ref<Tournament[]>([])
const tournamentsError = ref<string | null>(null)
const showSuccessAlert = ref(false)
const successMessage = ref('')
const selectedPeriod = ref('all')
const selectedStatus = ref('all')
const tournamentError = ref('')
const currentLimit = ref(10);
const usernameError = ref('')
const firstNameError = ref('')
const lastNameError = ref('')
const countryError = ref('')
const authStore = useAuthStore()

const clearErrors = () => {
  usernameError.value = ''
  firstNameError.value = ''
  lastNameError.value = ''
  countryError.value = ''
}

const showAddTournamentDialog = ref(false)
const tournamentName = ref('')
const showUpdatePlayerDialog = ref(false)
const playerUsername = ref('')
const playerError = ref('')
const selectedPlayer = ref<Player | null>(null)
const playerFirstName = ref('')
const playerLastName = ref('')
const playerCountry = ref('')
const playerAvatar = ref<File | null>(null)
const previewAvatar = ref<string | null>(null)
const selectedTeam = ref<string>('')

const isFiltered = ref(false);
const isLoadingTournaments = ref(false);
const hasMoreTournaments = ref(true);
const isLoadingMore = ref(false);
const selectedFormat = ref<string | null>(null);
const showAddTeamDialog = ref(false)
const teamName = ref('')
const teamError = ref('')
const teamLogo = ref<File | null>(null)

const showAddPlayerDialog = ref(false)
const currentFilters = ref<FilterValuesTournament>({
  period: null,
  status: null,
  format: null
});

const handleTeamAdded = () => {
  showSuccessAlert.value = true
  successMessage.value = 'Team added successfully!'
}

const handleTournamentAdded = async () => {
  showSuccessAlert.value = true
  successMessage.value = 'Tournament created successfully!'
  await fetchTournaments()
}

const handlePlayerAdded = (newPlayer: Player) => {
  showSuccessAlert.value = true
  successMessage.value = `Player ${newPlayer.username} was successfully added!`
}

const handlePlayerUpdated = (updatedPlayer: Player) => {
  showSuccessAlert.value = true
  successMessage.value = `Player ${updatedPlayer.username} was successfully updated!`
}

const handleFiltersChange = async (filters: FilterValuesTournament) => {
  try {
    currentFilters.value = filters;
    isLoadingTournaments.value = true;
    tournamentsError.value = null;
    currentLimit.value = 10;

    const params = new URLSearchParams();
    params.append('author_id', authStore.userId || '');
    params.append('offset', '0');
    params.append('limit', currentLimit.value.toString());

    if (filters.period) {
      params.append('period', filters.period);
    }

    if (filters.status) {
      params.append('status', filters.status);
    }

    if (filters.format) {
      params.append('tournament_format', filters.format);
    }

    const response = await fetch(`${API_URL}/tournaments/?${params}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    const results = Array.isArray(data) ? data : data.results || [];
    tournaments.value = results;

    isFiltered.value = !!(selectedPeriod.value || selectedStatus.value || selectedFormat.value);
    hasMoreTournaments.value = results.length === currentLimit.value;

  } catch (e) {
    console.error('Error fetching tournaments:', e);
    tournamentsError.value = 'Failed to load tournaments. Please try again later.';
  } finally {
    isLoadingTournaments.value = false;
  }
};

const fetchTournaments = async (loadMore = false) => {
  try {
    if (loadMore) {
      isLoadingMore.value = true;
    } else {
      isLoadingTournaments.value = true;
      isFiltered.value = false;
    }
    tournamentsError.value = null;

    const params = new URLSearchParams();
    params.append('author_id', authStore.userId || '');
    params.append('offset', '0');
    params.append('limit', currentLimit.value.toString());

    if (currentFilters.value.period) {
      params.append('period', currentFilters.value.period);
    }
    if (currentFilters.value.status) {
      params.append('status', currentFilters.value.status);
    }
    if (currentFilters.value.format) {
      params.append('tournament_format', currentFilters.value.format);
    }

    const response = await fetch(`${API_URL}/tournaments/?${params}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    const results = Array.isArray(data) ? data : (data.results || []);

    if (loadMore) {
      tournaments.value = [...tournaments.value, ...results];
    } else {
      tournaments.value = results;
    }
    hasMoreTournaments.value = results.length === 10;

  } catch (e) {
    console.error('Error fetching tournaments:', e);
    tournamentsError.value = 'Failed to load tournaments. Please try again later.';
  } finally {
    isLoadingTournaments.value = false;
    isLoadingMore.value = false;
  }
};

const loadMoreTournaments = async () => {
  currentLimit.value += 10;
  await fetchTournaments(true);
};


const openAddPlayerDialog = async () => {
  playerAvatar.value = null;
  if (previewAvatar.value) {
    URL.revokeObjectURL(previewAvatar.value);
  }
  previewAvatar.value = null;
  playerUsername.value = ''
  playerError.value = ''
  playerFirstName.value = ''
  playerLastName.value = ''
  playerCountry.value = ''
  playerAvatar.value = null
  selectedTeam.value = ''
  showAddPlayerDialog.value = true
}

const openAddTournamentDialog = () => {
  tournamentName.value = '';
  tournamentError.value = null;
  showAddTournamentDialog.value = true;
};

const openAddTeamDialog = () => {
  teamName.value = ''
  teamLogo.value = null
  teamError.value = ''
  showAddTeamDialog.value = true
}

const openUpdatePlayerDialog = async () => {
  clearErrors()
  playerError.value = ''
  usernameError.value = ''
  firstNameError.value = ''
  lastNameError.value = ''
  countryError.value = ''

  playerUsername.value = ''
  playerError.value = ''
  selectedPlayer.value = null
  playerFirstName.value = ''
  playerLastName.value = ''
  playerCountry.value = ''
  playerAvatar.value = null
  selectedTeam.value = ''
  showUpdatePlayerDialog.value = true

  if (selectedPlayer.value && selectedPlayer.value.team_id) {
    selectedTeam.value = selectedPlayer.value.team_id;
  }
}

const initializeTeam = () => {
  if (selectedPlayer.value?.team_id) {
    selectedTeam.value = selectedPlayer.value.team_id;
  } else {
    selectedTeam.value = '';
  }
}

onMounted(() => {
  initializeTeam()
  fetchTournaments()
})


</script>

<style scoped>
.content-wrapper {
  position: relative;
  z-index: 3;
  padding-top: 100px;
  width: 100vw;
}

.tournaments-section {
  width: 85%;
  max-width: 1400px;
  margin: 8px auto 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px;
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(2px);
}

.empty-text {
  color: #42DDF2FF;
  font-size: 1.5rem;
  text-align: center;
  margin-bottom: 8px;
}

.empty-subtext {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.1rem;
  text-align: center;
}

.tournament-column {
  display: flex;
  justify-content: flex-end;
  padding: 8px;
}

.tournament-column:nth-child(even) {
  justify-content: flex-start;
}

:deep(.v-container) {
  padding: 0 !important;
}

:deep(.v-row) {
  margin: 0;
}


</style>
