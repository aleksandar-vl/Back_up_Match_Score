<template>
  <v-dialog v-model="showAddTeamDialog" max-width="450">
  <v-card class="dialog-card">
    <div class="dialog-content">
      <v-card-title class="dialog-title">
        <span>Add New Team</span>
      </v-card-title>

      <v-card-text>
        <div class="file-upload-section">
          <v-avatar size="120" class="preview-avatar">
            <v-img
              v-if="previewLogo"
              :src="previewLogo"
              alt="Team logo"
            ></v-img>
            <v-icon
              v-else
              icon="mdi-shield"
              color="#42DDF2FF"
              size="48"
            ></v-icon>
          </v-avatar>

          <v-file-input
            v-model="teamLogo"
            label="Team Logo"
            variant="outlined"
            accept="image/*"
            :show-size="true"
            prepend-icon="mdi-camera"
            class="upload-input"
            @change="onLogoChange"
            @click:clear="clearLogo"
            hide-details
          ></v-file-input>
        </div>

        <v-text-field
          v-model="teamName"
          label="Team Name"
          variant="outlined"
          :rules="rules.team"
          :error-messages="teamError"
          @update:model-value="teamError = ''"
          @keyup.enter="submitAddTeam"
        ></v-text-field>
      </v-card-text>

      <v-card-actions class="dialog-actions">
        <v-spacer></v-spacer>
        <v-btn
          class="cancel-btn"
          variant="text"
          @click="handleCancelTeam"
        >
          Cancel
        </v-btn>
        <v-btn
          class="submit-btn"
          @click="submitAddTeam"
          :loading="isSubmitting"
          :disabled="!teamName || hasValidationErrors"
        >
          Create Team
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

const emit = defineEmits(['update:modelValue', 'team-added'])

// Computed
const showAddTeamDialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const hasValidationErrors = computed(() => {
  if (!teamName.value) return true;

  return !rules.team.every(rule => {
    const result = rule(teamName.value);
    return typeof result === 'boolean' ? result : false;
  });
});

// State
const isSubmitting = ref(false)
const teamName = ref('')
const teamLogo = ref<File | null>(null)
const previewLogo = ref<string | null>(null)


// Error State
const teamError = ref('')


// Validation rules
const rules = {
  team: [
    (v: string) => !!v || 'Team name is required',
    (v: string) => v.length >= 5 || 'Team name must be at least 5 characters',
    (v: string) => v.length <= 50 || 'Team name must not exceed 50 characters',
    (v: string) => /^[a-zA-Z0-9\s-]+$/.test(v) || 'Team name can only contain letters, numbers, spaces and dashes'
  ],
};

// Methods
const clearLogo = () => {
  teamLogo.value = null;
  previewLogo.value = null;
};

const handleCancelTeam = () => {
  resetTeamForm();
  showAddTeamDialog.value = false;
};

const onLogoChange = (event: Event | File[] | File) => {
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
      previewLogo.value = e.target.result as string;
    };
    reader.readAsDataURL(file);
    teamLogo.value = file;
  } else {
    previewLogo.value = null;
    teamLogo.value = null;
  }
};

const resetTeamForm = () => {
  teamName.value = '';
  teamLogo.value = null;
  previewLogo.value = null;
  teamError.value = '';
};

const submitAddTeam = async () => {
  try {
    isSubmitting.value = true;
    teamError.value = '';

    if (!teamName.value?.trim()) {
      teamError.value = 'Team name is required';
      return;
    }

    if (teamName.value.length < 3) {
      teamError.value = 'Team name must be at least 3 characters long';
      return;
    }

    const params = new URLSearchParams({
      name: teamName.value.trim()
    });

    let headers = {
      'Authorization': `Bearer ${authStore.token}`
    };

    let body;

    if (teamLogo.value) {
      const formData = new FormData();
      formData.append('logo', teamLogo.value);
      body = formData;
    } else {
      headers['Content-Type'] = 'application/json';
      body = JSON.stringify({ logo: null });
    }

    const response = await fetch(`${API_URL}/teams/?${params.toString()}`, {
      method: 'POST',
      headers: headers,
      body: body
    });

    if (!response.ok) {
      const data = await response.json();
      if (data.detail) {
        if (Array.isArray(data.detail)) {
          teamError.value = data.detail[0].msg || 'Invalid team data';
        } else {
          teamError.value = data.detail;
        }
      } else {
        teamError.value = 'Failed to create team';
      }
      return;
    }

    showAddTeamDialog.value = false;
    const newTeam = await response.json();
    emit('team-added', newTeam);
    resetTeamForm();

  } catch (e) {
    console.error('Error creating team:', e);
    teamError.value = 'Failed to connect to server. Please try again.';
  } finally {
    isSubmitting.value = false;
  }
};

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

/* File upload section */
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
  margin-top: -20px;
}

.preview-avatar .v-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-input {
  width: 100%;
}

/* Dialog actions */
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

/* Error messages */
.error-message {
  color: #fed854;
  font-size: 0.9rem;
  margin-top: 8px;
  text-align: center;
}

/* Deep selectors for Vuetify overrides */
:deep(.v-field) {
  background: rgba(45, 55, 75, 0.8) !important;
}

:deep(.v-field__input),
:deep(.v-input input),
:deep(.v-list-item__content),
:deep(.v-select__selection) {
  color: white !important;
}

:deep(.v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}

:deep(.v-text-field), :deep(.v-select) {
  margin-bottom: 16px;
}

:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 0.85rem;
  line-height: 1.2;
  display: block !important;
}

/* List styles */
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

/* Error states */
:deep(.v-field--error) {
  --v-field-border-color: #fed854 !important;
}

:deep(.v-field--error .v-field__outline),
:deep(.v-field--error .v-label),
:deep(.v-field--error input::placeholder),
:deep(.v-field--error .v-field__outline__start),
:deep(.v-field--error .v-field__outline__end),
:deep(.v-field--error .v-field__outline__notch) {
  border-color: #fed854 !important;
  color: #fed854 !important;
}

/* Custom scrollbar */
:deep(.v-overlay__content) {
  scrollbar-width: thin;
  scrollbar-color: rgba(66, 221, 242, 0.5) transparent;
}

:deep(.v-overlay__content::-webkit-scrollbar) {
  width: 8px;
}

:deep(.v-overlay__content::-webkit-scrollbar-thumb) {
  background-color: rgba(66, 221, 242, 0.5);
  border-radius: 4px;
}

:deep(.v-overlay__content::-webkit-scrollbar-thumb:hover) {
  background-color: rgba(66, 221, 242, 0.7);
}

:deep(.v-field__outline) {
  color: rgba(66, 221, 242, 0.3) !important;
}

/* Add this to your existing styles */
:deep(.v-file-input .v-input__prepend) {
  color: rgba(255, 255, 255, 0.7) !important; /* Default state */
}

:deep(.v-file-input:hover .v-input__prepend) {
  color: rgba(255, 255, 255, 0.9) !important; /* Hover state */
}
</style>
