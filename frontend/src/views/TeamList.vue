<template>
  <HeaderSection />

  <div class="content-wrapper">
    <v-container>

      <!-- Loading state -->
      <div v-if="isLoadingTeams" class="d-flex justify-center align-center" style="height: 200px">
        <v-progress-circular indeterminate color="#00ff9d"></v-progress-circular>
      </div>

      <!-- Error state -->
      <div v-else-if="teamsError" class="error-text pa-4">
        {{ teamsError }}
      </div>

      <!-- Teams Grid -->
      <v-row v-else class="row-width">
        <v-col v-for="team in teams" :key="team.id" cols="12" md="4" class="team-column">
          <TeamCard
            :key="team.id"
            :team="team"
            @player-click="handlePlayerClick"
          />
        </v-col>
      </v-row>

      <!-- Player Modal -->
      <PlayerModalDialog
        v-model="showPlayerModal"
        :player="selectedPlayer"
      />

      <!-- Load More Button -->
      <div v-if="!isLoadingTeams && hasMoreTeams" class="load-more-wrapper">
        <LoadMoreButton
          v-if="!isLoadingTeams && hasMoreTeams"
          :is-loading="isLoadingMore"
          button-text="Load More Teams"
          @load-more="loadMoreTeams"
        />
      </div>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { API_URL } from '@/config'
import PlayerModalDialog from "@/components/dialogs/PlayerModalDialog.vue";
import TeamCard from "@/components/TeamCard.vue";
import HeaderSection from "@/components/HeaderSection.vue";
import LoadMoreButton from "@/components/LoadMoreButton.vue";
import type { Player, Team } from '@/types/types'

const teams = ref<Team[]>([])
const isLoadingTeams = ref(false)
const teamsError = ref<string | null>(null)
const currentLimit = ref(9)
const hasMoreTeams = ref(true)
const isLoadingMore = ref(false)
const showPlayerModal = ref(false)
const selectedPlayer = ref<Player | null>(null)
const isLoadingPlayer = ref(false)
const playerError = ref<string | null>(null)

const fetchTeams = async (loadMore = false) => {
  try {
    if (loadMore) {
      isLoadingMore.value = true;
    } else {
      isLoadingTeams.value = true;
      teamsError.value = null;
    }

    const params = new URLSearchParams();
    const offset = loadMore ? teams.value.length : 0;
    params.append('offset', offset.toString());
    params.append('limit', '9'); // Фиксиран лимит от 9 за отбори
    params.append('sort_by', 'desc');

    const response = await fetch(`${API_URL}/teams/?${params}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    const results = Array.isArray(data) ? data : (data.results || []);

    if (loadMore) {
      // Добавяме новите отбори към съществуващите
      teams.value = [...teams.value, ...results];
    } else {
      // При първоначално зареждане презаписваме изцяло
      teams.value = results;
    }

    // Има още за зареждане ако броят на върнатите резултати е равен на лимита
    hasMoreTeams.value = results.length === 9;

  } catch (e) {
    console.error('Error fetching teams:', e);
    teamsError.value = 'Failed to load teams. Please try again later.';
  } finally {
    isLoadingTeams.value = false;
    isLoadingMore.value = false;
  }
}

const loadMoreTeams = async () => {
  await fetchTeams(true);
}

const fetchPlayer = async (playerId: string) => {
  try {
    isLoadingPlayer.value = true
    playerError.value = null
    const response = await fetch(`${API_URL}/players/${playerId}`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    selectedPlayer.value = await response.json()
  } catch (e) {
    console.error('Error fetching player:', e)
    playerError.value = 'Failed to load player. Please try again later.'
  } finally {
    isLoadingPlayer.value = false
  }
}

const handlePlayerClick = (playerId: string) => {
  fetchPlayer(playerId)
  showPlayerModal.value = true
}

onMounted(() => {
  fetchTeams();
  window.addEventListener('search-results', ((event: CustomEvent) => {
    if (event.detail.route === '/teams') {
      // Add any filtering logic here if you add filters later
      teams.value = event.detail.results;
      isLoadingTeams.value = false;
      teamsError.value = null;
      hasMoreTeams.value = event.detail.results.length === 9;
    }
  }) as EventListener);
});

onUnmounted(() => {
  window.removeEventListener('search-results', ((event: CustomEvent) => {
    if (event.detail.route === '/teams') {
      teams.value = event.detail.results;
      isLoadingTeams.value = false;
      teamsError.value = null;
      hasMoreTeams.value = event.detail.results.length === 9;
    }
  }) as EventListener);
});
</script>

<style scoped>
.content-wrapper {
  position: relative;
  z-index: 3;
  padding-top: 100px;
  min-height: 100vh;
  width: 100vw !important;
  margin-top: 100px;
}

.row-width {
  max-width: 1030px;
  margin: 0 auto;
}

.team-column {
  display: flex;
  justify-content: center;
  padding: 8px;
}
</style>
