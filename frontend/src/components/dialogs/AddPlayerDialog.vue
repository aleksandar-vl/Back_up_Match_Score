<template>
  <v-dialog v-model="showAddPlayerDialog" max-width="450">
    <v-card class="dialog-card">
      <div class="dialog-content">
        <v-card-title class="dialog-title">
          <span>Add New Player</span>
        </v-card-title>

        <v-card-text>
          <div class="file-upload-section">
            <v-avatar size="120" class="preview-avatar">
              <v-img
                v-if="previewAvatar"
                :src="previewAvatar"
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
              :show-size="true"
              prepend-icon="mdi-camera"
              class="upload-input"
              @change="onAvatarChange"
              @click:clear="clearAvatar"
              hide-details
            ></v-file-input>
          </div>

          <v-form ref="addPlayerForm" v-model="isFormValid">
            <v-text-field
              v-model="addPlayerUsername"
              label="Username"
              variant="outlined"
              :rules="rules.username"
              :error-messages="addPlayerUsernameError"
              @input="clearAddPlayerErrors"
            ></v-text-field>

            <v-text-field
              v-model="addPlayerFirstName"
              label="First Name"
              variant="outlined"
              :rules="rules.firstName"
              :error-messages="addPlayerFirstNameError"
              @input="clearAddPlayerErrors"
            ></v-text-field>

            <v-text-field
              v-model="addPlayerLastName"
              label="Last Name"
              variant="outlined"
              :rules="rules.lastName"
              :error-messages="addPlayerLastNameError"
              @input="clearAddPlayerErrors"
            ></v-text-field>

            <v-text-field
              v-model="addPlayerCountry"
              label="Country"
              variant="outlined"
              :rules="rules.country"
              :error-messages="addPlayerCountryError"
              @input="clearAddPlayerErrors"
            ></v-text-field>
          </v-form>

          <v-autocomplete
            v-model="selectedTeam"
            :items="teams"
            item-title="name"
            item-value="id"
            label="Team (Optional)"
            variant="outlined"
            :loading="loadingTeams"
            clearable
            :menu-props="{ contentClass: 'teams-menu' }"
            >
            <template v-slot:item="{ props, item }">
              <v-list-item
                v-bind="props"
                :title="item.title"
                class="team-list-item"
              ></v-list-item>
            </template>
          ></v-autocomplete>
        </v-card-text>

        <v-card-actions class="dialog-actions">
          <v-spacer></v-spacer>
          <v-btn
            class="cancel-btn"
            variant="text"
            @click="closeAddPlayerDialog"
          >
            Cancel
          </v-btn>
          <v-btn
            class="submit-btn"
            @click="submitAddPlayer"
            :loading="isSubmitting"
            :disabled="!canSubmitPlayer || hasValidationErrors "
          >
            Create Player
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

const emit = defineEmits(['update:modelValue', 'player-added'])

// Computed
const showAddPlayerDialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const hasValidationErrors = computed(() => {

  const usernameErrors = !rules.username.every(rule => {
    const result = rule(addPlayerUsername.value);
    return typeof result === 'boolean' ? result : false;
  });

  const firstNameErrors = !rules.firstName.every(rule => {
    const result = rule(addPlayerFirstName.value);
    return typeof result === 'boolean' ? result : false;
  });

  const lastNameErrors = !rules.lastName.every(rule => {
    const result = rule(addPlayerLastName.value);
    return typeof result === 'boolean' ? result : false;
  });

  const countryErrors = !rules.country.every(rule => {
    const result = rule(addPlayerCountry.value);
    return typeof result === 'boolean' ? result : false;
  });

  return usernameErrors || firstNameErrors || lastNameErrors || countryErrors;
});


// State
const playerAvatar = ref<File | null>(null)
const previewAvatar = ref<string | null>(null)
const addPlayerUsername = ref('')
const addPlayerFirstName = ref('')
const addPlayerLastName = ref('')
const addPlayerCountry = ref('')
const selectedTeam = ref<string | null>(null)
const isFormValid = ref(false)
const isSubmitting = ref(false)
const loadingTeams = ref(false)
const teams = ref([])
const addPlayerForm = ref(null)
const successMessage = ref('')
const showSuccessAlert = ref(false)

// Error states
const addPlayerUsernameError = ref('')
const addPlayerFirstNameError = ref('')
const addPlayerLastNameError = ref('')
const addPlayerCountryError = ref('')

// Computed
const canSubmitPlayer = computed(() => {
  return addPlayerUsername.value.trim() &&
         addPlayerFirstName.value.trim() &&
         addPlayerLastName.value.trim() &&
         addPlayerCountry.value.trim() &&
         !addPlayerUsernameError.value &&
         !addPlayerFirstNameError.value &&
         !addPlayerLastNameError.value &&
         !addPlayerCountryError.value
})

// Validation rules
const rules = {
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

// Methods
const clearAddPlayerErrors = () => {
  addPlayerUsernameError.value = ''
  addPlayerFirstNameError.value = ''
  addPlayerLastNameError.value = ''
  addPlayerCountryError.value = ''
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
      previewAvatar.value = e.target?.result as string;
    };
    reader.readAsDataURL(file);
    playerAvatar.value = file;
  } else {
    previewAvatar.value = null;
    playerAvatar.value = null;
  }
}

const clearAvatar = () => {
  playerAvatar.value = null;
  if (previewAvatar.value) {
    URL.revokeObjectURL(previewAvatar.value);
  }
  previewAvatar.value = null;
}

const closeAddPlayerDialog = () => {
  emit('update:modelValue', false)
  addPlayerUsername.value = ''
  addPlayerFirstName.value = ''
  addPlayerLastName.value = ''
  addPlayerCountry.value = ''
  selectedTeam.value = null
  clearAvatar()
  clearAddPlayerErrors()
}

const submitAddPlayer = async () => {
  const { valid } = await addPlayerForm.value.validate();

  if (!valid) {
    return;
  }

  try {
    isSubmitting.value = true;

    const playerData = {
      username: addPlayerUsername.value,
      first_name: addPlayerFirstName.value,
      last_name: addPlayerLastName.value,
      country: addPlayerCountry.value,
    };

    if (selectedTeam.value) {
      const teamName = teams.value.find(t => t.id === selectedTeam.value)?.name
      if (teamName) {
        playerData.team_name = teamName;
      }
    }

    const params = new URLSearchParams(playerData);
    let url = `${API_URL}/players/?${params.toString()}`;
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
      method: "POST",
      headers: headers,
      body: body,
    });

    if (!response.ok) {
      const data = await response.json();
      if (data.detail) {
        if (typeof data.detail === 'string') {
          if (data.detail.includes("username")) {
            addPlayerUsernameError.value = "Player with this username already exists";
          }
          if (data.detail.includes("first_name")) {
            addPlayerFirstNameError.value = "Invalid first name";
          }
          if (data.detail.includes("last_name")) {
            addPlayerLastNameError.value = "Invalid last name";
          }
          if (data.detail.includes("country")) {
            addPlayerCountryError.value = "Invalid country";
          }
        }
      } else {
        throw new Error(data.detail || "Failed to create player");
      }
      return;
    }

    showAddPlayerDialog.value = false;
    const newPlayer = await response.json();
    emit('player-added', newPlayer);
    closeAddPlayerDialog();

  } catch (e) {
    console.error("Error adding player:", e.message);
  } finally {
    isSubmitting.value = false;
  }
};

const fetchTeamsForPlayer = async () => {
  try {
    loadingTeams.value = true;
    const response = await fetch(`${API_URL}/teams?has_space=true&offset=0&limit=100`);

    if (!response.ok) throw new Error('Failed to fetch teams');
    const data = await response.json();
    teams.value = data;
    console.log('Loaded teams:', teams.value);
  } catch (e) {
    console.error('Error fetching teams:', e);
  } finally {
    loadingTeams.value = false;
  }
};

onMounted(() => {
  fetchTeamsForPlayer();
})
</script>

<style scoped>
/* Base dialog styles */
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
  font-size: 1.4rem;
  font-weight: 500;
  text-align: center;
  margin-bottom: 16px;
}

.dialog-actions {
  padding: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: -32px;
}

/* Avatar upload section */
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

/* Team section */
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

/* Buttons */
.cancel-btn {
  color: #42DDF2FF !important;
}

.submit-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
  margin-left: 16px;
}

/* Error states */
.error-message {
  color: #fed854;
  font-size: 0.9rem;
  margin-top: 8px;
  text-align: center;
}

/* Deep selectors for Vuetify components */
:deep(.v-text-field), :deep(.v-select) {
  margin-bottom: 16px;
}

:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 0.85rem;
  line-height: 1.2;
  display: block !important;
}

:deep(.v-field__input), :deep(.v-input input), :deep(.v-list-item__content) {
  color: white !important;
}

:deep(.v-list) {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 1px solid rgba(66, 221, 242, 0.3);
}

:deep(.v-list-item) {
  background: transparent !important;
  color: #ffffff !important;
}

:deep(.v-list-item:hover) {
  background: rgba(66, 221, 242, 0.2) !important;
  color: #42DDF2FF !important;
}

/* Error states for form fields */
:deep(.v-field--error) {
  --v-field-border-color: #fed854 !important;
}

:deep(.v-field--error .v-field__outline),
:deep(.v-field--error .v-label),
:deep(.v-field--error input::placeholder) {
  color: #fed854 !important;
}

:deep(.v-field--error .v-field__outline__start),
:deep(.v-field--error .v-field__outline__end),
:deep(.v-field--error .v-field__outline__notch) {
  border-color: #fed854 !important;
}

/* Field outlines */
:deep(.v-field__outline) {
  color: rgba(66, 221, 242, 0.3) !important;
}

:deep(.v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}

:deep(.v-overlay__content) {
  scrollbar-width: thin;
  scrollbar-color: rgba(66, 221, 242, 0.5) transparent;
}

:deep(.v-overlay__content::-webkit-scrollbar) {
  width: 8px;
}

:deep(.v-overlay__content::-webkit-scrollbar-track) {
  background: transparent;
}

:deep(.v-overlay__content::-webkit-scrollbar-thumb) {
  background-color: #42DDF2FF;
  border-radius: 20px;
  border: 2px solid transparent;
  background-clip: padding-box;
}

:deep(.v-overlay__content::-webkit-scrollbar-thumb:hover) {
  background-color: #42DDF2FF;
  opacity: 0.8;
}

/* Add this to your existing styles */
:deep(.v-file-input .v-input__prepend) {
  color: rgba(255, 255, 255, 0.7) !important; /* Default state */
}

:deep(.v-file-input:hover .v-input__prepend) {
  color: rgba(255, 255, 255, 0.9) !important; /* Hover state */
}
</style>
