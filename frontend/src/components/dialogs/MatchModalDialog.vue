<template>
  <v-dialog v-model="showDialog" max-width="800px" height="550" class="match-dialog">
    <v-card class="custom-dialog-card">
      <v-card-title class="headline text-center">
        {{ match?.team1_name }} vs {{ match?.team2_name }}
      </v-card-title>
      <v-card-text>
        <div class="match-details-centered">
          <router-link
            :to="`/events/${match?.tournament_id}`"
            class="tournament-title tournament-link"
          >
            {{ match?.tournament_title }}
          </router-link>
          <div class="tournament-stage">{{ match?.stage }}</div>
          <div class="is-finished">{{ match?.is_finished ? 'Finished' : 'Not finished' }}</div>

          <div class="match-layout">
            <div class="team-info-left">
              <div class="avatar-container">
                <div class="edit-container" v-if="canEdit" @click="openTeamEdit">
                  <v-icon icon="mdi-pencil" class="edit-icon"></v-icon>
                  <span class="edit-text">Edit Teams</span>
                </div>
                <v-tooltip location="top">
                  <template v-slot:activator="{ props }">
                    <router-link :to="`/teams/${match?.team1_id}`" class="team-avatar-link">
                      <v-avatar class="team-avatar" size="150" v-bind="props">
                        <v-img v-if="match?.team1_logo" :src="match.team1_logo" :alt="match.team1_name"></v-img>
                        <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>
                      </v-avatar>
                    </router-link>
                  </template>
                  {{ match?.team1_name }}
                </v-tooltip>
              </div>
              <span
                class="team-score"
                :class="{ 'clickable': canEdit }"
                @click="canEdit && handleScoreIncrement('team1')"
              >
                {{ match?.team1_score }}
              </span>
            </div>

            <div class="score-divider">:</div>

            <div class="team-info-right">
              <span
                class="team-score"
                :class="{ 'clickable': canEdit }"
                @click="canEdit && handleScoreIncrement('team2')"
              >
                {{ match?.team2_score }}
              </span>
              <div class="avatar-container">
                <v-tooltip location="top">
                  <template v-slot:activator="{ props }">
                    <router-link :to="`/teams/${match?.team2_id}`" class="team-avatar-link">
                      <v-avatar class="team-avatar" size="150" v-bind="props">
                        <v-img v-if="match?.team2_logo" :src="match.team2_logo" :alt="match.team2_name"></v-img>
                        <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="40"></v-icon>
                      </v-avatar>
                    </router-link>
                  </template>
                  {{ match?.team2_name }}
                </v-tooltip>
              </div>
            </div>
          </div>

          <div class="match-time">
            <v-icon icon="mdi-clock-outline" class="mr-2 neon-text"></v-icon>
            <span class="time-text">
              {{ match ? format(new Date(match.start_time), 'HH:mm, dd MMM yyyy') : '' }}
            </span>
            <v-icon
              v-if="canEdit"
              icon="mdi-pencil"
              class="edit-icon ml-2"
              @click="openTimeEdit"
            ></v-icon>
          </div>

          <div v-if="match?.winner_id" class="winner">
            <v-icon icon="mdi-crown" color="#fed854" size="24"></v-icon>
            <span class="winner-name">
              {{ match.winner_id === match.team1_id ? match.team1_name : match.team2_name }}
            </span>
          </div>
        </div>
      </v-card-text>
      <v-card-actions>
          <!-- Score Error Alert -->
          <v-alert
            v-if="scoreUpdateError"
            type="error"
            variant="tonal"
            class="mb-4 error-alert"
            closable
            @click:close="scoreUpdateError = ''"
          >
            {{ scoreUpdateError }}
          </v-alert>
        <v-btn @click="closeDialog">Close</v-btn>
      </v-card-actions>
    </v-card>

    <!-- Time Edit Dialog -->
    <v-dialog v-model="showTimeEdit" max-width="500px" class="time-edit-dialog">
      <v-card class="edit-dialog">
        <div class="dialog-content">
          <v-card-title class="dialog-title">Edit Match Time</v-card-title>
          <v-card-text>
          <v-alert
            v-if="editError"
            type="error"
            variant="tonal"
            class="mb-4 error-alert"
            closable
            @click:close="editError = ''"
          >
            {{ editError }}
          </v-alert>
            <v-text-field
              v-model="editedStartTime"
              label="Match Time"
              type="datetime-local"
              variant="outlined"
              :rules="dateRules"
              :error="!isValidDate && !!editedStartTime"
              :error-messages="getDateErrorMessage"
              class="time-field custom-time-field"
              persistent-hint
            ></v-text-field>
          </v-card-text>
          <v-card-actions class="dialog-actions">
            <v-spacer></v-spacer>
            <v-btn
              class="cancel-btn"
              variant="text"
              @click="showTimeEdit = false"
            >
              Cancel
            </v-btn>
            <v-btn
              class="submit-btn"
              @click="updateTime"
              :loading="isUpdatingTime"
              :disabled="!hasTimeChanges"
            >
              {{ hasTimeChanges ? 'Save' : 'No Changes' }}
            </v-btn>
          </v-card-actions>
        </div>
      </v-card>
    </v-dialog>

     <!-- Team Edit Dialog -->
    <v-dialog v-model="showTeamEdit" max-width="500px" class="team-edit-dialog">
      <v-card class="dialog-card">
        <div class="dialog-content">
          <v-card-title class="dialog-title">Edit Teams</v-card-title>
          <v-card-text>
            <v-alert
              v-if="editError"
              type="error"
              variant="tonal"
              class="mb-4"
            >
              {{ editError }}
            </v-alert>

            <v-form ref="teamForm">
              <div class="team-slot">
                <div class="d-flex align-center">
                  <v-autocomplete
                    v-model="newTeam1"
                    :items="availableTeams"
                    item-title="name"
                    item-value="id"
                    label="Team 1"
                    variant="outlined"
                    :loading="loadingTeams"
                    :model-value="newTeam1"
                    clearable
                    class="custom-autocomplete"
                    :menu-props="{ contentClass: 'teams-menu' }"
                  >
                    <template v-slot:item="{ props, item }">
                      <v-list-item
                        v-bind="props"
                        :title="item.raw.name"
                        class="team-list-item"
                        :class="{ 'team-list-item--selected': item.raw.id === newTeam1 }"
                      ></v-list-item>
                    </template>
                  </v-autocomplete>
                </div>
              </div>

              <div class="team-slot">
                <div class="d-flex align-center">
                  <v-autocomplete
                    v-model="newTeam2"
                    :items="availableTeams"
                    item-title="name"
                    item-value="id"
                    label="Team 2"
                    variant="outlined"
                    :loading="loadingTeams"
                    :model-value="newTeam2"
                    clearable
                    class="custom-autocomplete"
                    :menu-props="{ contentClass: 'teams-menu' }"
                  >
                    <template v-slot:item="{ props, item }">
                      <v-list-item
                        v-bind="props"
                        :title="item.raw.name"
                        class="team-list-item"
                        :class="{ 'team-list-item--selected': item.raw.id === newTeam2 }"
                      ></v-list-item>
                    </template>
                  </v-autocomplete>
                </div>
              </div>
            </v-form>
          </v-card-text>
          <v-card-actions class="dialog-actions">
            <v-spacer></v-spacer>
            <v-btn
              class="cancel-btn"
              variant="text"
              @click="showTeamEdit = false"
            >
              Cancel
            </v-btn>
            <v-btn
              class="submit-btn"
              @click="updateTeams"
              :loading="isUpdatingTeams"
              :disabled="!hasTeamChanges"
            >
              {{ hasTeamChanges ? 'Save' : 'No Changes' }}
            </v-btn>
          </v-card-actions>
        </div>
      </v-card>
    </v-dialog>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { format } from 'date-fns'
import { useAuthStore } from '@/stores/auth'
import { API_URL } from '@/config'
import type { Match } from '@/types/types'

interface Props {
  modelValue: boolean
  match: Match | null
  tournamentDirectorId?: string
  onMatchUpdate?: () => Promise<void>
}

const props = defineProps<Props>()
const emit = defineEmits(['update:modelValue', 'match-updated'])

const authStore = useAuthStore()

// Refs
const showDialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const showTimeEdit = ref(false)
const showTeamEdit = ref(false)
const editedStartTime = ref('')
const newTeam1 = ref('')
const newTeam2 = ref('')
const availableTeams = ref([])
const loadingTeams = ref(false)
const teamForm = ref(null)
const editError = ref('')
const scoreUpdateError = ref('')
const isUpdatingTime = ref(false)
const isUpdatingTeams = ref(false)

const dateRules = [
  (v: string) => {
    const selectedDate = new Date(v)
    const now = new Date()
    return selectedDate > now || 'Match time cannot be in the past'
  },
  (v: string) => {
    const selectedDate = new Date(v)
    const tomorrow = new Date()
    tomorrow.setDate(tomorrow.getDate() + 1)
    tomorrow.setHours(selectedDate.getHours(), selectedDate.getMinutes(), selectedDate.getSeconds())
    return selectedDate > tomorrow || 'Match time must be at least 1 day in the future'
  }
]

// Computed
const canEdit = computed(() => {
  console.log('director_id:', props.tournamentDirectorId)
  console.log('user_id:', authStore.userId)
  return authStore.isAuthenticated && (
    authStore.userRole === 'admin' ||
    props.tournamentDirectorId === authStore.userId
  )})

const hasTimeChanges = computed(() => {
  if (!props.match || !editedStartTime.value) return false

  const currentDate = new Date(props.match.start_time)
  const newDate = new Date(editedStartTime.value)

  return currentDate.getTime() !== newDate.getTime() && isValidDate.value
})

const isValidDate = computed(() => {
  if (!editedStartTime.value) return true

  const selectedDate = new Date(editedStartTime.value)
  const now = new Date()
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  tomorrow.setHours(selectedDate.getHours(), selectedDate.getMinutes(), selectedDate.getSeconds())

  return selectedDate > now && selectedDate > tomorrow
})

const getDateErrorMessage = computed(() => {
  if (!editedStartTime.value) return ''

  const selectedDate = new Date(editedStartTime.value)
  const now = new Date()
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  tomorrow.setHours(selectedDate.getHours(), selectedDate.getMinutes(), selectedDate.getSeconds())

  if (selectedDate <= now) {
    return 'Match time cannot be in the past'
  }
  if (selectedDate <= tomorrow) {
    return 'Match time must be at least 1 day in the future'
  }
  return ''
})

const hasTeamChanges = computed(() => {
  if (!props.match) return false

  const team1Changed = newTeam1.value && newTeam1.value !== props.match.team1_id
  const team2Changed = newTeam2.value && newTeam2.value !== props.match.team2_id

  return team1Changed || team2Changed
})


// Methods
const closeDialog = () => {
  showDialog.value = false
}

const extractErrorMessage = async (response: Response): Promise<string> => {
  try {
    const responseText = await response.text()
    const errorData = JSON.parse(responseText)

    // FastAPI validation error
    if (errorData.detail && Array.isArray(errorData.detail) && errorData.detail[0]?.msg) {
      return errorData.detail[0].msg
    }
    // HTTP error
    if (errorData.detail) {
      return errorData.detail
    }

    return 'An error occurred'
  } catch (e) {
    console.error('Error extracting message:', e)
    return 'An error occurred'
  }
}

// Match score update
const handleScoreIncrement = async (team: 'team1' | 'team2') => {
  if (!props.match) return
  try {
    scoreUpdateError.value = ''
    const response = await fetch(
      `${API_URL}/matches/${props.match.id}/team-scores?team_to_upvote_score=${team}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      }
    )

    if (!response.ok) {
      scoreUpdateError.value = await extractErrorMessage(response)
      return
    }

    if (props.onMatchUpdate) {
      await props.onMatchUpdate()
    }

  } catch (e) {
    console.error('Error updating score:', e)
    scoreUpdateError.value = 'An unexpected error occurred while updating the score'
  }
}

// Time edit
const updateTime = async () => {
  if (!props.match || !editedStartTime.value || !isValidDate.value) return

  try {
    editError.value = ''
    isUpdatingTime.value = true

    const selectedDate = new Date(editedStartTime.value)
    selectedDate.setHours(selectedDate.getHours() + 2)
    const formattedDate = selectedDate.toISOString()

    const response = await fetch(
      `${API_URL}/matches/${props.match.id}?start_time=${encodeURIComponent(formattedDate)}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      }
    )

    if (!response.ok) {
      editError.value = await extractErrorMessage(response)
      return
    }

    const updatedMatch = await response.json()

    if (props.match) {
      Object.assign(props.match, updatedMatch)
    }

    if (props.onMatchUpdate) {
      await props.onMatchUpdate()
    }

    showTimeEdit.value = false
  } catch (e) {
    console.error('Full error:', e)
    editError.value = 'Failed to update match time'
  } finally {
    isUpdatingTime.value = false
  }
}

const openTimeEdit = () => {
  if (!props.match) return

  const date = new Date(props.match.start_time)

  // Format date to local datetime-local input format
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')

  // Set the value in the format required by datetime-local input
  editedStartTime.value = `${year}-${month}-${day}T${hours}:${minutes}`
  showTimeEdit.value = true
}


// Team edit
const openTeamEdit = async () => {
  try {
    loadingTeams.value = true
    editError.value = ''

    const response = await fetch(`${API_URL}/teams/?is_available=true&offset=0&limit=100`)
    if (!response.ok) throw new Error('Failed to load teams')
    const data = await response.json()
    availableTeams.value = data

    if (props.match) {
      const team1Exists = data.some(t => t.id === props.match?.team1_id)
      const team2Exists = data.some(t => t.id === props.match?.team2_id)

      if (!team1Exists && props.match.team1_id) {
        availableTeams.value.push({
          id: props.match.team1_id,
          name: props.match.team1_name
        })
      }
      if (!team2Exists && props.match.team2_id) {
        availableTeams.value.push({
          id: props.match.team2_id,
          name: props.match.team2_name
        })
      }

      newTeam1.value = props.match.team1_id
      newTeam2.value = props.match.team2_id
    }

    showTeamEdit.value = true
  } catch (e) {
    console.error('Error fetching teams:', e)
    editError.value = 'Failed to load teams'
  } finally {
    loadingTeams.value = false
  }
}

const updateTeams = async () => {
  if (!props.match) return

  try {
    editError.value = ''
    isUpdatingTeams.value = true

    let params = new URLSearchParams()

    if (newTeam1.value) {
      const team1 = availableTeams.value.find(t => t.id === newTeam1.value)
      if (team1) {
        params.append('team1_name', team1.name)
      }
    }

    if (newTeam2.value) {
      const team2 = availableTeams.value.find(t => t.id === newTeam2.value)
      if (team2) {
        params.append('team2_name', team2.name)
      }
    }

    if (params.toString()) {
      const response = await fetch(
        `${API_URL}/matches/${props.match.id}?${params.toString()}`,
        {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        }
      )

      if (!response.ok) {
        const error = await extractErrorMessage(response)
        throw new Error(error)
      }

      if (props.onMatchUpdate) {
        await props.onMatchUpdate()
      }

      showTeamEdit.value = false
    }
  } catch (e) {
    console.error('Error updating teams:', e)
    editError.value = e.message || 'Failed to update teams'
  } finally {
    isUpdatingTeams.value = false
  }
}
</script>

<style scoped>

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
.match-details-centered .team-avatar:hover {
  transform: none;
  cursor: pointer;
}

.match-time {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  text-align: center;
  margin-bottom: 16px;
}

.team-winner .team-score {
  color: #FED854FF;
}

.match-dialog :deep(.v-card) {
  border-radius: 35px !important;
}

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

.match-details-centered {
  text-align: center;
  display: flex;
  flex-direction: column;
}

.tournament-title {
  color: #42DDF2FF;
  font-size: 1.6rem;
  font-weight: bold;
  margin-top: -30px;
  align-self: center;
  transition: all 0.2s ease;
}

:deep(.tournament-link) {
  text-decoration: none;
  background: transparent !important;
}

:deep(.tournament-link:hover) {
  text-decoration: none;
  background: transparent !important;
}

.tournament-stage {
  color: #FED854FF;
  font-size: 1.2rem;
}

.is-finished {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
  margin-bottom: 8px;
}

.custom-dialog-card .match-layout {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 32px;
  margin: 24px 0;
  min-height: 150px;
}

.custom-dialog-card .team-info-left, .team-info-right {
  display: flex;
  align-items: center;
  gap: 16px;
  height: 150px;
}

.custom-dialog-card .score-container {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 48px;
}

.custom-dialog-card .score-divider {
  margin: 0 20px;
  font-size: 2.5rem;
  color: #FED854FF;
  text-shadow: 0 0 10px rgba(238, 173, 60, 0.5);
  align-self: center;
  padding-bottom: 10px;
}

.edit-container {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  padding: 4px 25px;
  border-radius: 50px;
  transition: all 0.2s;
}

.edit-container:hover {
  background: rgba(66, 221, 242, 0.1);
}

.edit-text {
  font-size: 0.8rem;
  color: #42DDF2FF;
  opacity: 0.8;
}

.edit-container:hover .edit-text {
  opacity: 1;
}

.winner {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
}

.winner-name {
  color: #FED854FF;
  font-size: 1.2rem;
  font-weight: bold;
}

.team-score.clickable {
  cursor: pointer;
  transition: all 0.2s;
}

.team-score.clickable:hover {
  color: #42DDF2FF;
  text-shadow: 0 0 15px rgba(66, 221, 242, 0.5);
  transform: scale(1.1);
}

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

.edit-dialog {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 2px solid #42DDF2FF;
  backdrop-filter: blur(10px);
}

.time-edit-dialog :deep(.v-card) {
  border-radius: 35px !important;
}

.team-edit-dialog :deep(.v-card) {
  border-radius: 35px !important;
}
:deep(.v-card-title) {
  color: #42DDF2FF !important;
}

:deep(.v-field__input) {
  color: white !important;
}


.team-avatar-link {
  text-decoration: none;
  background: transparent !important;
}

.team-avatar-link:hover {
  text-decoration: none;
  background: transparent !important;
}


:deep(.v-alert) {
  background-color: rgba(254, 216, 84, 0.1) !important;
  color: #fed854 !important;
  border-color: #fed854 !important;
}

:deep(.v-alert__close-button) {
  color: #fed854 !important;
}

:deep(.v-alert__prepend) {
  color: #fed854 !important;
}

.team-avatar {
  min-width: 55px;
  min-height: 55px;
  border: 1px solid rgba(8, 117, 176, 0.3);
  background: rgba(8, 87, 144, 0.1);
  transition: transform 0.2s;
  cursor: pointer;
}


.dialog-card {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 2px solid #42DDF2FF;
  backdrop-filter: blur(10px);
}

.dialog-content {
  padding: 24px;
}

.dialog-title {
  color: #42ddf2;
  font-weight: bold;
  font-size: 1.25rem;
  text-align: center;
}

.error-alert {
  width: 100%;
  margin: 0 auto;
  background-color: rgba(255, 215, 0, 0.12) !important;
  color: #ffd700 !important;
  border-color: #ffd700 !important;
  border-radius: 8px;
}

.error-alert :deep(.v-alert__close-button) {
  color: #ffd700 !important;
}

.error-alert :deep(.v-alert__prepend) {
  color: #ffd700 !important;
}

.dialog-actions {
  padding: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: -32px;
}

.cancel-btn {
  color: #42DDF2FF !important;
}

.submit-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
  margin-left: 16px;
}

.team-list-item {
  padding: 8px 16px;
  transition: background-color 0.2s;
  border-radius: 4px;
  margin: 2px 0;
}

.team-list-item:hover {
  background: rgba(66, 221, 242, 0.1);
}

.team-list-item--selected {
  background: rgba(66, 221, 242, 0.15);
}

:deep(.v-btn) {
  border-radius: 50px !important;
  text-transform: none !important;
  font-weight: 500 !important;
  letter-spacing: 0.5px !important;
  min-width: 100px !important;
}

:deep(.v-btn:disabled) {
  opacity: 0.7 !important;
  background: rgba(66, 221, 242, 0.3) !important;
}

:deep(.custom-time-field) {
  margin-bottom: 16px;
}

:deep(.custom-time-field .v-field__input::-webkit-calendar-picker-indicator) {
  filter: invert(1);
  opacity: 0.5;
}

:deep(.custom-time-field .v-field__input::-webkit-calendar-picker-indicator:hover) {
  opacity: 0.8;
  cursor: pointer;
}

:deep(.custom-time-field .v-field__input input),
:deep(.custom-time-field.v-field--error .v-field__input input) {
  color: white !important;
}

:deep(.custom-time-field.v-field--error) {
  --v-field-border-color: #fed854 !important;
}

:deep(.custom-time-field.v-field--error .v-field__outline),
:deep(.custom-time-field.v-field--error .v-field__outline__start),
:deep(.custom-time-field.v-field--error .v-field__outline__end),
:deep(.custom-time-field.v-field--error .v-field__outline__notch) {
  border-color: #fed854 !important;
}

:deep(.custom-time-field.v-field--error .v-label) {
  color: #fed854 !important;
}

:deep(.custom-time-field .v-messages__message) {
  color: #fed854 !important;
  font-size: 0.85rem;
  line-height: 1.2;
  min-height: 0;
  padding-top: 4px;
}


:deep(.custom-time-field) {
  margin-bottom: 16px;
}

:deep(.v-field--error .v-field__outline) {
  --v-field-border-color: #fed854 !important;
  border-color: #fed854 !important;
}

:deep(.v-field--error .v-field__outline__start),
:deep(.v-field--error .v-field__outline__end),
:deep(.v-field--error .v-field__outline__notch) {
  border-color: #fed854 !important;
}

:deep(.v-field--error .v-label) {
  color: #fed854 !important;
}

:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 0.85rem;
  line-height: 1.2;
}

:deep(.v-field--error:not(.v-field--disabled) .v-field__outline) {
  color: #fed854 !important;
  border-color: #fed854 !important;
}


:deep(.v-field--error) {
  background-color: transparent !important;
}


:deep(.v-input--error) {
  --v-theme-error: #fed854 !important;
  color: #fed854 !important;
}

</style>
