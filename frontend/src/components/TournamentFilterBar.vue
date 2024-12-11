<template>
  <v-row class="filter-row">
        <v-col cols="12" md="3">
          <v-select
            v-model="selectedPeriod"
            :items="periodOptions"
            item-title="text"
            item-value="value"
            label="Period"
            variant="outlined"
            density="comfortable"
            bg-color="rgba(45, 55, 75, 0.4)"
            color="#42DDF2FF"
            clearable
            @update:model-value="emitFilterChange"
          />
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
            class="filter-select"
            bg-color="rgba(45, 55, 75, 0.4)"
            color="#42DDF2FF"
            clearable
            @update:model-value="emitFilterChange"
          ></v-select>
        </v-col>

        <v-col cols="12" md="3">
          <v-select
            v-model="selectedFormat"
            :items="formatOptions"
            item-title="text"
            item-value="value"
            label="Format"
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

const emit = defineEmits<{
  (event: 'filter-change', filters: {
    period: string | null
    status: string | null
    format: string | null
  }): void
}>()

const selectedPeriod = ref<string | null>(null)
const selectedStatus = ref<string | null>(null)
const selectedFormat = ref<string | null>(null)

const periodOptions: FilterOption[] = [
  { text: 'Upcoming', value: 'future' },
  { text: 'Current', value: 'present' },
  { text: 'Past', value: 'past' }
]

const statusOptions: FilterOption[] = [
  { text: 'Active', value: 'active' },
  { text: 'Finished', value: 'finished' }
]

const formatOptions: FilterOption[] = [
  { text: 'Single Elimination', value: 'single elimination' },
  { text: 'Round Robin', value: 'round robin' },
  { text: 'One Off Match', value: 'one off match' }
]

const emitFilterChange = () => {
  emit('filter-change', {
    period: selectedPeriod.value,
    status: selectedStatus.value,
    format: selectedFormat.value
  })
}

watch([selectedPeriod, selectedStatus, selectedFormat], () => {
  emitFilterChange()
})
</script>

<style scoped>
.filter-row {
  display: flex;
  justify-content: center;
  margin-bottom: 8px;
}

.filter-row .v-col {
  max-width: 300px;
}
</style>
