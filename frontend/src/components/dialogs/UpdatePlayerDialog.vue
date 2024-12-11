<template>
  <v-dialog v-model="showUpdatePlayerDialog" max-width="450">
    <v-card class="dialog-card">
      <div class="dialog-content">
        <v-card-title class="dialog-title">
          <span>Update Player</span>
        </v-card-title>

        <v-card-text>
          <!-- Username Check Step -->
          <div v-if="!selectedPlayer" class="input-wrapper">
            <v-text-field
              v-model="playerUsername"
              label="Player Username"
              variant="outlined"
              :rules="[rules.required]"
              :error-messages="playerError"
              @keyup.enter="checkPlayer"
              @input="playerError = ''"
            ></v-text-field>
          </div>

          <!-- Player Update Form -->
          <div v-else>
            <div class="player-status mb-4 text-center">
              <v-chip
                :color="selectedPlayer.user_email ? 'error' : 'success'"
                class="status-chip"
              >
                {{ selectedPlayer.user_email ? 'Linked to User' : 'Available for Update' }}
              </v-chip>
            </div>

            <template v-if="!selectedPlayer.user_email">
              <div class="file-upload-section">
                <v-avatar size="120" class="preview-avatar">
                  <v-img
                    v-if="previewAvatar || selectedPlayer.avatar"
                    :src="previewAvatar || selectedPlayer.avatar"
                    alt="Player avatar"
                  ></v-img>
                  <v-icon
                    v-else
                    icon="mdi-account"
                    color="#42DDF2FF"
                    size="48"
                  ></v-icon>
                </v-avatar>

                <v-file-input
                  v-model="playerAvatar"
                  label="Player Avatar (Optional)"
                  variant="outlined"
                  accept="image/*"
                  prepend-icon="mdi-camera"
                  :show-size="true"
                  class="upload-input"
                  @change="onAvatarChange"
                  hide-details
                ></v-file-input>
              </div>

              <v-text-field
                v-model="playerUsername"
                label="Username"
                variant="outlined"
                :rules="rules.username"
                :error-messages="usernameError"
                @input="clearErrors"
              ></v-text-field>

              <v-text-field
                v-model="playerFirstName"
                label="First Name"
                variant="outlined"
                :rules="rules.firstName"
                :error-messages="firstNameError"
                @input="clearErrors"
              ></v-text-field>

              <v-text-field
                v-model="playerLastName"
                label="Last Name"
                variant="outlined"
                :rules="rules.lastName"
                :error-messages="lastNameError"
                @input="clearErrors"
              ></v-text-field>

              <v-text-field
                v-model="playerCountry"
                label="Country"
                variant="outlined"
                :rules="rules.country"
                :error-messages="countryError"
                @input="clearErrors"
              ></v-text-field>

              <v-autocomplete
                v-model="selectedTeam"
                :items="teams"
                item-title="name"
                item-value="name"
                label="Team"
                variant="outlined"
                :loading="loadingTeams"
                clearable
                :menu-props="{ contentClass: 'teams-menu' }"
                :return-object="false"
                :model-value="selectedTeam"
                @update:model-value="handleTeamChange"
              >
                <template v-slot:item="{ props, item }">
                  <v-list-item
                    v-bind="props"
                    :title="item.raw.name"
                    class="team-list-item"
                  >
                  </v-list-item>
                </template>
              </v-autocomplete>
            </template>

            <v-card-text>
              <div v-if="selectedPlayer?.user_email" class="text-center linked-player-message">
                This player is linked to a user and cannot be updated.
              </div>
            </v-card-text>
          </div>
        </v-card-text>

        <v-card-actions class="dialog-actions">
          <v-spacer></v-spacer>
          <v-btn
            class="cancel-btn"
            variant="text"
            @click="closeUpdatePlayerDialog"
          >
            Cancel
          </v-btn>
          <v-btn
            v-if="!selectedPlayer"
            class="next-btn"
            @click="checkPlayer"
            :loading="isCheckingPlayer"
            :disabled="!playerUsername"
          >
            Next
          </v-btn>
          <v-btn
            v-if="selectedPlayer && !selectedPlayer.user_email"
            class="submit-btn"
            @click="submitUpdatePlayer"
            :loading="isSubmitting"
            :disabled="!hasChanges"
          >
            {{ hasChanges ? 'Update Player' : 'No Changes' }}
          </v-btn>
        </v-card-actions>
      </div>
    </v-card>
  </v-dialog>

</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { API_URL } from '@/config'

// Auth Store
const authStore = useAuthStore()

// Props & Emits
const props = defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'player-updated'])

// Computed
const showUpdatePlayerDialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// State
const playerUsername = ref('')
const playerError = ref('')
const isCheckingPlayer = ref(false)
const selectedPlayer = ref<any>(null)
const playerFirstName = ref('')
const playerLastName = ref('')
const playerCountry = ref('')
const playerAvatar = ref<File | null>(null)
const previewAvatar = ref<string | null>(null)
const selectedTeam = ref<string>('')
const isSubmitting = ref(false)
const loadingTeams = ref(false)
const teams = ref([])
const successMessage = ref('')
const showSuccessAlert = ref(false)

// Error states
const usernameError = ref('')
const firstNameError = ref('')
const lastNameError = ref('')
const countryError = ref('')

// Validation rules
const rules = {
  required: (v: string) => !!v || 'This field is required',
  username: [
    (v: string) => !!v || 'Username is required',
    (v: string) => v.length >= 5 || 'Username must be at least 5 characters',
    (v: string) => v.length <= 15 || 'Username must not exceed 15 characters',
    (v: string) => /^[a-zA-Z0-9_-]+$/.test(v) || 'Username can only contain letters, numbers, underscores, or dashes',
  ],
  firstName: [
    (v: string) => !!v || 'First name is required',
    (v: string) => v.length >= 2 || 'First name must be at least 2 characters',
    (v: string) => v.length <= 25 || 'First name must not exceed 25 characters',
    (v: string) => /^[a-zA-Z]+(?:[-a-zA-Z]+)?$/.test(v) || 'Invalid first name format',
  ],
  lastName: [
    (v: string) => !!v || 'Last name is required',
    (v: string) => v.length >= 2 || 'Last name must be at least 2 characters',
    (v: string) => v.length <= 25 || 'Last name must not exceed 25 characters',
    (v: string) => /^[a-zA-Z]+(?:[-a-zA-Z]+)?$/.test(v) || 'Invalid last name format',
  ],
  country: [
    (v: string) => !!v || 'Country is required',
    (v: string) => v.length >= 2 || 'Country must be at least 2 characters',
    (v: string) => v.length <= 25 || 'Country must not exceed 25 characters',
    (v: string) => /^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$/.test(v) || 'Invalid country format',
  ]
}

const hasValidationErrors = computed(() => {
  const isRequiredFieldEmpty = !playerUsername.value ||
                             !playerFirstName.value ||
                             !playerLastName.value ||
                             !playerCountry.value;

  const hasUsernameError = playerUsername.value && !rules.username.every(rule => rule(playerUsername.value) === true);
  const hasFirstNameError = playerFirstName.value && !rules.firstName.every(rule => rule(playerFirstName.value) === true);
  const hasLastNameError = playerLastName.value && !rules.lastName.every(rule => rule(playerLastName.value) === true);
  const hasCountryError = playerCountry.value && !rules.country.every(rule => rule(playerCountry.value) === true);

  return isRequiredFieldEmpty ||
         hasUsernameError ||
         hasFirstNameError ||
         hasLastNameError ||
         hasCountryError;
})


const hasChanges = computed(() => {
  if (!selectedPlayer.value) return false;

  const hasPlayerDataChanges =
    (playerUsername.value !== selectedPlayer.value.username) ||
    (playerFirstName.value !== selectedPlayer.value.first_name) ||
    (playerLastName.value !== selectedPlayer.value.last_name) ||
    (playerCountry.value !== selectedPlayer.value.country) ||
    (selectedTeam.value !== (selectedPlayer.value.team_name || ''));

  const hasAvatarChanges = playerAvatar.value !== null;

  return (hasPlayerDataChanges || hasAvatarChanges) && !hasValidationErrors.value;
})

// Methods
const clearErrors = () => {
  usernameError.value = ''
  firstNameError.value = ''
  lastNameError.value = ''
  countryError.value = ''
}

const onAvatarChange = (event: Event | File[] | File) => {
  let file: File | null = null;

  if (Array.isArray(event)) {
    file = event[0];
  } else if (event instanceof File) {
    file = event;
  } else if (event?.target instanceof HTMLInputElement && event.target.files) {
    file = event.target.files[0];
  }

  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      previewAvatar.value = e.target.result as string;
    };
    reader.readAsDataURL(file);
    playerAvatar.value = file;
  } else {
    previewAvatar.value = null;
    playerAvatar.value = null;
  }
}

const handleFieldChange = async (field: string, value: any) => {
  if (!selectedPlayer.value) return

  try {
    playerError.value = ''
    const params = new URLSearchParams()
    params.append(field, value)

    const response = await fetch(
      `${API_URL}/players/${selectedPlayer.value.id}?${params.toString()}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
        }
      }
    )

    if (!response.ok) {
      const data = await response.json()
      handleError(data)
      return
    }

    selectedPlayer.value = {
      ...selectedPlayer.value,
      [field]: value
    }

  } catch (e) {
    console.error(`Error updating ${field}:`, e)
    playerError.value = 'Failed to update player'
  }
}

const handleTeamChange = (newTeam: string | null) => {
  handleFieldChange('team_id', newTeam)
}

const checkPlayer = async () => {
  playerError.value = ''

  if (!playerUsername.value?.trim()) {
    playerError.value = 'Username is required'
    return
  }

  try {
    isCheckingPlayer.value = true
    playerError.value = ''

    const response = await fetch(`${API_URL}/players?search=${encodeURIComponent(playerUsername.value)}`)
    const players = await response.json()

    const exactMatch = players.find(p => p.username.toLowerCase() === playerUsername.value.toLowerCase())

    if (!exactMatch) {
      playerError.value = 'Player not found.'
      return
    }

    selectedPlayer.value = exactMatch

    // Pre-fill form if player exists and is not linked
    if (!selectedPlayer.value.user_email) {
      playerFirstName.value = selectedPlayer.value.first_name || ''
      playerLastName.value = selectedPlayer.value.last_name || ''
      playerCountry.value = selectedPlayer.value.country || ''
      playerUsername.value = selectedPlayer.value.username || ''
      selectedTeam.value = selectedPlayer.value.team_name || ''

      if (selectedPlayer.value.avatar) {
        previewAvatar.value = selectedPlayer.value.avatar
      }

      // Load teams if not loaded yet
      if (teams.value.length === 0) {
        await fetchTeamsForPlayers()
      }
    }

  } catch (e) {
    console.error('Error checking player:', e)
    playerError.value = 'Failed to check player'
  } finally {
    isCheckingPlayer.value = false
  }
}

const submitUpdatePlayer = async () => {
  if (!selectedPlayer.value) {
    playerError.value = 'No player selected'
    return
  }

  try {
    clearErrors()
    isSubmitting.value = true
    playerError.value = ''

    if (playerUsername.value && !rules.username.every(rule => rule(playerUsername.value) === true)) {
      usernameError.value = 'Invalid username format'
      return
    }
    if (playerFirstName.value && !rules.firstName.every(rule => rule(playerFirstName.value) === true)) {
      firstNameError.value = 'Invalid first name format'
      return
    }
    if (playerLastName.value && !rules.lastName.every(rule => rule(playerLastName.value) === true)) {
      lastNameError.value = 'Invalid last name format'
      return
    }
    if (playerCountry.value && !rules.country.every(rule => rule(playerCountry.value) === true)) {
      countryError.value = 'Invalid country format'
      return
    }

    let url = `${API_URL}/players/${selectedPlayer.value.id}`
    const params = new URLSearchParams()

    if (playerUsername.value !== selectedPlayer.value.username) {
      params.append('username', playerUsername.value)
    }
    if (playerFirstName.value !== selectedPlayer.value.first_name) {
      params.append('first_name', playerFirstName.value)
    }
    if (playerLastName.value !== selectedPlayer.value.last_name) {
      params.append('last_name', playerLastName.value)
    }
    if (playerCountry.value !== selectedPlayer.value.country) {
      params.append('country', playerCountry.value)
    }
    if ((selectedPlayer.value.team_id && selectedTeam.value === '') ||
        (selectedTeam.value && selectedTeam.value !== selectedPlayer.value.team_id)) {
      if (selectedTeam.value === '') {
        params.append('team_name', '')
      } else {
        const team = teams.value.find(t => t.id === selectedTeam.value)
        if (team) {
          params.append('team_name', team.name)
        }
      }
    }

    if (params.toString()) {
      url += '?' + params.toString()
    }

    let headers = {
      'Authorization': `Bearer ${authStore.token}`
    };
    let body;

    if (playerAvatar.value) {
      const formData = new FormData();
      formData.append('avatar', playerAvatar.value);
      body = formData;
    } else {
      headers['Content-Type'] = 'application/json';
      body = JSON.stringify({ avatar: null });
    }

    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      },
      body: body
    })

    if (!response.ok) {
      const data = await response.json()
      console.log('Error updating player:', data)
      if (data.detail && typeof data.detail === 'string') {
        if (data.detail.includes('username')) {
          usernameError.value = data.detail
        } else if (data.detail.includes('first_name')) {
          firstNameError.value = data.detail
        } else if (data.detail.includes('last_name')) {
          lastNameError.value = data.detail
        } else if (data.detail.includes('country')) {
          countryError.value = data.detail
        } else {
          throw new Error(data.detail)
        }
        return
      }
      throw new Error(data.detail || 'Failed to update player')
    }

    showUpdatePlayerDialog.value = false
    const updatedPlayer = await response.json();
    emit('player-updated', updatedPlayer);
    closeUpdatePlayerDialog();

  } catch (e) {
    console.error('Error updating player:', e)
    playerError.value = e.message || 'Failed to connect to server. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}

const fetchTeamsForPlayers = async () => {
  try {
    loadingTeams.value = true;
    const response = await fetch(`${API_URL}/teams?has_space=true&offset=0&limit=100`);
    if (!response.ok) throw new Error('Failed to fetch teams');
    const data = await response.json();
    teams.value = data;
  } catch (e) {
    console.error('Error fetching teams:', e);
  } finally {
    loadingTeams.value = false;
  }
};

const closeUpdatePlayerDialog = () => {
  showUpdatePlayerDialog.value = false
  playerUsername.value = ''
  playerError.value = ''
  selectedPlayer.value = null
  playerFirstName.value = ''
  playerLastName.value = ''
  playerCountry.value = ''
  playerAvatar.value = null
  selectedTeam.value = ''
  if (previewAvatar.value) {
    URL.revokeObjectURL(previewAvatar.value)
  }
  previewAvatar.value = null
}

// Lifecycle
onMounted(async () => {
  fetchTeamsForPlayers()
})
</script>

<style scoped>
.dialog-card {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 2px solid #42DDF2FF;
  backdrop-filter: blur(10px);
  border-radius: 35px !important;
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


.file-upload-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin-bottom: 8px;
}

.preview-avatar {
  border: 2px solid #42DDF2FF;
  background: rgba(8, 87, 144, 0.1);
  transition: transform 0.2s;
}

.upload-input {
  width: 100%;
}

.next-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
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

:deep(.v-field) {
  background: rgba(45, 55, 75, 0.8) !important;
}

:deep(.v-select__selection) {
  color: white !important;
}

:deep(.v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}

.linked-player-message {
  color: white !important;
  font-size: 0.9rem;
  margin-bottom: 24px;
}


:deep(.v-messages) {
  min-height: 14px;
  padding-top: 2px;
  display: block !important;
}

:deep(.v-text-field) {
  margin-top: 16px;
}

:deep(.v-field__input input) {
  color: white !important;
  -webkit-text-fill-color: white !important;
}

:deep(.v-field__input input::selection) {
  background-color: rgba(66, 221, 242, 0.3) !important;
  color: white !important;
}

:deep(.v-field__input input::-moz-selection) {
  background-color: rgba(66, 221, 242, 0.3) !important;
  color: white !important;
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

.dialog-actions {
  padding: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.cancel-btn {
  color: #42DDF2FF !important;
}

.submit-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
  margin-left: 16px;
}

.upload-input {
  width: 100%;
}

.preview-avatar .v-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

:deep(.v-field__input) {
  color: white !important;
}

:deep(.v-file-input .v-field) {
  border-color: rgba(66, 221, 242, 0.3) !important;
}

:deep(.v-file-input .v-field:hover) {
  border-color: #42ddf2 !important;
}

.dialog-content .v-card-text > div > * {
  margin-top: 0 !important;
}

:deep(.teams-menu) {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 1px solid rgba(66, 221, 242, 0.3);
  max-height: 300px !important;
  overflow-y: auto;
}

:deep(.teams-menu::-webkit-scrollbar) {
  width: 8px;
}

:deep(.teams-menu::-webkit-scrollbar-track) {
  background: transparent;
}

:deep(.teams-menu::-webkit-scrollbar-thumb) {
  background: rgba(66, 221, 242, 0.3);
  border-radius: 4px;
}

:deep(.teams-menu::-webkit-scrollbar-thumb:hover) {
  background: rgba(66, 221, 242, 0.5);
}

:deep(.v-select__selection) {
  color: white !important;
  opacity: 1 !important;
}

:deep(.v-select .v-field__input) {
  min-height: 56px !important;
  opacity: 1 !important;
  color: white !important;
}

:deep(.v-select .v-field) {
  background: transparent !important;
}

:deep(.v-overlay__content) {
  scrollbar-width: thin;
  scrollbar-color: rgba(66, 221, 242, 0.5) transparent;
}

.custom-autocomplete :deep(.v-field__input) {
  color: rgb(255, 255, 255) !important;
}

.custom-autocomplete :deep(.v-field--focused) {
  color: #42DDF2FF !important;
}


.dialog-card {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 1px solid #42DDF2FF;
  backdrop-filter: blur(10px);
  border-radius: 12px;
}

.dialog-content {
  padding: 20px;
}

.dialog-actions {
  padding: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: -32px;
}

.dialog-title {
  color: #42ddf2;
  font-size: 1.4rem;
  font-weight: 500;
  text-align: center;
  margin-bottom: 16px;
}

:deep(.v-card-text) {
  padding-bottom: 8px;
}

:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 14px;
}

:deep(.v-field--error) {
  --v-field-border-color: #fed854 !important;
}

.error-message {
  color: #fed854;
  font-size: 0.9rem;
  margin-top: 8px;
  text-align: center;
}

.cancel-btn {
  color: #42DDF2FF !important;
}

.submit-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
  margin-left: 16px;
}

.team-slot {
  margin-bottom: 16px;
}

.team-slot .d-flex {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.team-slot .v-autocomplete,
.team-slot .v-text-field {
  flex: 1;
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

:deep(.v-autocomplete .v-field__input) {
  color: white !important;
  min-height: 56px;
}

:deep(.v-autocomplete .v-field__append-inner) {
  padding-top: 14px;
}

:deep(.v-list-item__content) {
  color: white;
}

:deep(.v-list) {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 1px solid rgba(66, 221, 242, 0.3);
}

:deep(.v-select) {
  background: transparent !important;
}

:deep(.v-text-field),
:deep(.v-select) {
  margin-bottom: 16px;
}

:deep(.filter-select) {
  background: transparent !important;
  color: #ffffff !important;
  border-color: #42DDF2FF !important;
}

:deep(.v-select:focus),
:deep(.v-select--active) {
  background: transparent !important;
  border-color: #42DDF2FF !important;
}

:deep(.v-menu__content) {
  background: transparent !important;
  box-shadow: none !important;
}

:deep(.v-list-item) {
  background: transparent !important;
  color: #ffffff !important;
}

:deep(.v-list-item:hover) {
  background: rgba(66, 221, 242, 0.2) !important;
  color: #42DDF2FF !important;
}

:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 0.85rem;
  line-height: 1.2;
  display: block !important;
}

:deep(.v-input input) {
  color: white !important;
}

:deep(.v-field--variant-outlined.v-field--error) {
  border-color: #fed854 !important;
}

:deep(.v-field--error .v-field__outline) {
  color: #fed854 !important;
}

:deep(.v-text-field .v-field--error) {
  --v-field-border-color: #fed854;
}

:deep(.v-field--error .v-label) {
  color: #FED854FF !important;
}

:deep(.v-field--error .v-field__outline__start),
:deep(.v-field--error .v-field__outline__end),
:deep(.v-field--error .v-field__outline__notch) {
  border-color: #fed854 !important;
}

:deep(.v-field--error input::placeholder),
:deep(.v-field--error .v-label.v-field-label) {
  color: #fed854 !important;
}

:deep(.v-field__outline) {
  color: rgba(66, 221, 242, 0.3) !important;
}

:deep(.v-file-input .v-field__input) {
  color: white !important;
  font-size: 0.9rem;
}

/* Add this to your existing styles */
:deep(.v-file-input .v-input__prepend) {
  color: rgba(255, 255, 255, 0.7) !important; /* Default state */
}

:deep(.v-file-input:hover .v-input__prepend) {
  color: rgba(255, 255, 255, 0.9) !important; /* Hover state */
}
</style>

