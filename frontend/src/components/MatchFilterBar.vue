<template>
  <v-row class="filter-row">
    <v-col cols="12" md="3">
      <v-select
        v-model="selectedStage"
        :items="stages"
        item-title="text"
        item-value="value"
        label="Stage"
        variant="outlined"
        density="comfortable"
        bg-color="rgba(45, 55, 75, 0.4)"
        color="#42DDF2FF"
        clearable
        @update:model-value="emitFilterChange"
      ></v-select>
    </v-col>
    <v-col cols="12" md="3">
      <v-select
        v-model="selectedStatus"
        :items="statusOptions"
        item-title="text"
        item-value="value"
        label="Status"
        variant="outlined"
        density="comfortable"
        bg-color="rgba(45, 55, 75, 0.4)"
        color="#42DDF2FF"
        clearable
        @update:model-value="emitFilterChange"
      ></v-select>
    </v-col>
    <v-col cols="12" md="3">
      <v-select
        v-model="selectedTeam"
        :items="teams"
        item-title="text"
        item-value="value"
        label="Team"
        variant="outlined"
        density="comfortable"
        bg-color="rgba(45, 55, 75, 0.4)"
        color="#42DDF2FF"
        clearable
        @update:model-value="emitFilterChange"
      ></v-select>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { FilterOption } from '@/types/types'

const props = defineProps<{
  teams: FilterOption[]
}>()

const emit = defineEmits<{
  (event: 'filter-change', filters: {
    stage: string | null
    status: string | null
    team: string | null
  }): void
}>()

const selectedStage = ref<string | null>(null)
const selectedStatus = ref<string | null>(null)
const selectedTeam = ref<string | null>(null)

const stages: FilterOption[] = [
  { text: 'Group Stage', value: 'group stage' },
  { text: 'Quarter Final', value: 'quarter final' },
  { text: 'Semi Final', value: 'semi final' },
  { text: 'Final', value: 'final' }
]

const statusOptions: FilterOption[] = [
  { text: 'Active', value: 'active' },
  { text: 'Finished', value: 'finished' }
]

const emitFilterChange = () => {
  emit('filter-change', {
    stage: selectedStage.value,
    status: selectedStatus.value,
    team: selectedTeam.value
  })
}

watch([selectedStage, selectedStatus, selectedTeam], () => {
  emitFilterChange()
})
</script>

<style scoped>
/* Filter row styling */
.filter-row {
  display: flex;
  justify-content: center;
  margin-bottom: 8px;
}

.filter-row .v-col {
  max-width: 300px;
}

/* Custom deep selectors for Vuetify components */
:deep(.v-card-title) {
  color: #42DDF2FF !important;
}
</style>
