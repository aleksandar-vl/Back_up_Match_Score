<template>
  <HeaderSection />

  <div class="content-wrapper">
    <v-container>
    <FilterBar @filter-change="handleFiltersChange"/>

      <!-- Loading state -->
      <div v-if="isLoadingTournaments" class="d-flex justify-center align-center" style="height: 200px">
        <v-progress-circular indeterminate color="#00ff9d"></v-progress-circular>
      </div>

      <!-- Error state -->
      <div v-else-if="tournamentsError" class="error-text pa-4">
        {{ tournamentsError }}
      </div>

      <!-- Tournaments Grid -->
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
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import type { Tournament, FilterValuesTournament } from '@/types/types'
import { API_URL } from '@/config'
import FilterBar from '@/components/TournamentFilterBar.vue';
import HeaderSection from '@/components/HeaderSection.vue';
import TournamentCard from '@/components/TournamentCard.vue';
import LoadMoreButton from '@/components/LoadMoreButton.vue';


const isFiltered = ref(false);
const tournaments = ref<Tournament[]>([]);
const isLoadingTournaments = ref(false);
const tournamentsError = ref<string | null>(null);
const currentLimit = ref(10);
const hasMoreTournaments = ref(true);
const isLoadingMore = ref(false);
const selectedPeriod = ref<string | null>(null);
const selectedStatus = ref<string | null>(null);
const selectedFormat = ref<string | null>(null);

const currentSearch = ref<string>('');
const currentFilters = ref<FilterValuesTournament>({
  period: null,
  status: null,
  format: null
});

const getSearchFromURL = () => {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('search') || '';
};

const handleFiltersChange = async (filters: FilterValuesTournament) => {
  console.log('handleFiltersChange called with filters:', filters);
  console.log('Current search term:', getSearchFromURL());
  try {
    currentFilters.value = filters;
    isLoadingTournaments.value = true;
    tournamentsError.value = null;
    currentLimit.value = 10;

    const params = new URLSearchParams();
    params.append('offset', '0');
    params.append('limit', currentLimit.value.toString());

    const searchTerm = getSearchFromURL();
    if (searchTerm) {
      params.append('search', searchTerm);
    }

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
  console.log('fetchTournaments called, loadMore:', loadMore);
  console.log('Current filters:', currentFilters.value);
  console.log('Current search:', getSearchFromURL());
  try {
    if (loadMore) {
      isLoadingMore.value = true;
    } else {
      isLoadingTournaments.value = true;
      isFiltered.value = false;
    }
    tournamentsError.value = null;

    const params = new URLSearchParams();
    params.append('offset', '0');
    params.append('limit', currentLimit.value.toString());


    const searchTerm = getSearchFromURL();
    if (searchTerm) {
      params.append('search', searchTerm);
      console.log('Adding search term to request:', searchTerm);
    }

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

onMounted(() => {
  fetchTournaments()
  window.addEventListener('search-results', ((event: CustomEvent) => {
    if (event.detail.route === '/events') {
      const searchResults = event.detail.results.filter(result => {
        if (currentFilters.value.format) {
          return result.tournament_format === currentFilters.value.format;
        }
        return true;
      });

      tournaments.value = searchResults;
      isLoadingTournaments.value = false;
      tournamentsError.value = null;
    }
  }) as EventListener)
})

onUnmounted(() => {
  window.removeEventListener('search-results', ((event: CustomEvent) => {
    if (event.detail.route === '/events') {
      tournaments.value = event.detail.results
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

.tournament-column {
  display: flex;
  justify-content: flex-end;
  padding: 8px;
}

.tournament-column:nth-child(even) {
  justify-content: flex-start;
}

.error-text {
  text-align: center;
  color: rgba(255, 255, 255, 0.75);
  padding: 20px;
  background: rgba(255, 215, 0, 0.25);
  border-radius: 10px;
  margin: 20px 0;
}
</style>
