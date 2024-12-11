<template>
  <v-dialog
    v-model="showEditDialog"
    max-width="400px"
    class="dialog-radius"
  >
  <v-card class="edit-dialog">
    <div class="edit-dialog-content">
      <v-card-title class="dialog-title">{{ editDialogTitle }}</v-card-title>
      <v-card-text>

        <!-- Name Edit -->
        <div v-if="props.editField === 'name'" class="d-flex gap-2">
          <v-text-field
            :model-value="props.editFirstName"
            @update:model-value="updateFirstName"
            label="First Name"
            variant="outlined"
            :rules="rules.firstName"
            :error-messages="firstNameError"
          ></v-text-field>

          <v-text-field
            :model-value="props.editLastName"
            @update:model-value="updateLastName"
            label="Last Name"
            variant="outlined"
            :rules="rules.lastName"
            :error-messages="lastNameError"
          ></v-text-field>
        </div>

        <!-- Country Edit -->
        <v-text-field
          v-if="props.editField === 'country'"
          :model-value="props.editValue"
          @update:model-value="updateValue"
          label="Country"
          variant="outlined"
          :rules="rules.country"
          :error-messages="countryError"
        ></v-text-field>

        <!-- Team Edit -->
        <div v-if="props.editField === 'team'">
          <v-select
            :model-value="props.editValue"
            @update:model-value="updateValue"
            :items="teams"
            item-title="name"
            item-value="name"
            label="Select Team"
            variant="outlined"
            :loading="isLoadingTeams"
            clearable
            :menu-props="{ contentClass: 'teams-menu' }"
          >
            <template v-slot:item="{ props, item }">
              <v-list-item
                v-bind="props"
                :title="item.raw.name"
                class="team-list-item"
              >
              </v-list-item>
            </template>
          </v-select>
          <div v-if="teamsError" class="text-caption error-text mt-2">
            {{ teamsError }}
          </div>
        </div>
      </v-card-text>
      <v-card-actions class="dialog-actions">
        <v-spacer></v-spacer>
        <v-btn
          class="cancel-btn"
          @click="closeEditDialog"
        >
          Cancel
        </v-btn>
        <v-btn
          class="submit-btn"
          @click="saveEdit"
          :loading="isSaving"
          :disabled="!hasValidChanges"
        >
          Save
        </v-btn>
      </v-card-actions>
    </div>
  </v-card>
</v-dialog>
</template>

<script setup lang="ts">
import { computed, defineEmits, ref, watch } from "vue";
import { useAuthStore } from "@/stores/auth";
import { API_URL } from "@/config";
import type { Player, Team } from "@/types/types";

const props = defineProps<{
  modelValue: boolean
  player: Player | null
  editField: string
  editValue: string
  editFirstName: string
  editLastName: string
}>()

console.log('EditDialog props:', {
  editField: props.editField,
  editValue: props.editValue,
  editFirstName: props.editFirstName,
  editLastName: props.editLastName
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'update:editValue', value: string): void
  (e: 'update:editFirstName', value: string): void
  (e: 'update:editLastName', value: string): void
  (e: 'profile-updated'): void
}>()

const showEditDialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const updateValue = (value: string) => {
  emit('update:editValue', value)
}

const updateFirstName = (value: string) => {
  emit('update:editFirstName', value)
}

const updateLastName = (value: string) => {
  emit('update:editLastName', value)
}

const authStore = useAuthStore()
const teams = ref<Team[]>([])
const isLoadingTeams = ref(false)
const isSaving = ref(false)
const isLoading = ref(true)
const error = ref<string | null>(null)

// Errors
const firstNameError = ref('')
const lastNameError = ref('')
const countryError = ref('')
const teamsError = ref('')
const editError = ref('')

const rules = {
  required: (v: string) => !!v || 'This field is required',
  firstName: [
    (value: string) => !!value || 'First name is required',
    (value: string) => value.length >= 2 || 'First name must be at least 2 characters',
    (value: string) => value.length <= 25 || 'First name must not exceed 25 characters',
    (value: string) => /^[a-zA-Z]+(?:[-a-zA-Z]+)?$/.test(value) || 'Invalid first name format',
  ],
  lastName: [
    (value: string) => !!value || 'Last name is required',
    (value: string) => value.length >= 2 || 'Last name must be at least 2 characters',
    (value: string) => value.length <= 25 || 'Last name must not exceed 25 characters',
    (value: string) => /^[a-zA-Z]+(?:[-a-zA-Z]+)?$/.test(value) || 'Invalid last name format',
  ],
  country: [
    (value: string) => !!value || 'Country is required',
    (value: string) => value.length >= 2 || 'Country must be at least 2 characters',
    (value: string) => value.length <= 25 || 'Country must not exceed 25 characters',
    (value: string) => /^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$/.test(value) || 'Invalid country format',
  ],
}

const editDialogTitle = computed(() => {
  const titles: Record<string, string> = {
    name: 'Edit Name',
    country: 'Edit Country',
    team: 'Edit Team Name'
  }
  return titles[props.editField] || 'Edit Profile'
})

const closeEditDialog = () => {
  showEditDialog.value = false
  emit('update:editValue', '')
  emit('update:editFirstName', '')
  emit('update:editLastName', '')
  editError.value = ''
  clearErrors()
}

const clearErrors = () => {
  firstNameError.value = ''
  lastNameError.value = ''
  countryError.value = ''
}

const saveEdit = async () => {
  clearErrors()
  if (!props.player) return

  try {
    isSaving.value = true
    editError.value = ''
    if (props.editField === 'name') {
      if (!rules.firstName.every(rule => rule(props.editFirstName) === true)) {
        firstNameError.value = 'Invalid first name format'
        return
      }
      if (!rules.lastName.every(rule => rule(props.editLastName) === true)) {
        lastNameError.value = 'Invalid last name format'
        return
      }
    } else if (props.editField === 'country') {
      if (!rules.country.every(rule => rule(props.editValue) === true)) {
        countryError.value = 'Invalid country format'
        return
      }
    }

    let params = new URLSearchParams()

    if (props.editField === 'name') {
      params.append('first_name', props.editFirstName)
      params.append('last_name', props.editLastName)
    } else if (props.editField === 'team') {
      params.append('team_name', props.editValue)
    } else {
      params.append(props.editField, props.editValue)
    }

    const response = await fetch(
      `${API_URL}/players/${props.player.id}?${params.toString()}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      }
    )

    const responseData = await response.json()

    if (!response.ok) {
      editError.value = responseData.detail || responseData.message || 'Failed to update profile'
      throw new Error(editError.value)
    }

    showEditDialog.value = false
    emit('profile-updated', responseData)

  } catch (e) {
    console.error('Error updating profile:', e)
    if (!editError.value) {
      editError.value = 'Failed to update profile. Please try again.'
    }
  } finally {
    isSaving.value = false
  }
}

const hasValidChanges = computed(() => {
  if (!props.player) return false;

  if (firstNameError.value || lastNameError.value || countryError.value || teamsError.value || editError.value) {
    return false;
  }

  switch (props.editField) {
    case 'name':
      return (props.editFirstName !== props.player.first_name ||
              props.editLastName !== props.player.last_name) &&
              rules.firstName.every(rule => rule(props.editFirstName) === true) &&
              rules.lastName.every(rule => rule(props.editLastName) === true);

    case 'country':
      return props.editValue !== props.player.country &&
             rules.country.every(rule => rule(props.editValue) === true);

    case 'team':
      return props.editValue !== props.player.team_name;

    default:
      return false;
  }
});

const fetchTeams = async () => {
  try {
    isLoadingTeams.value = true
    teamsError.value = ''

    const response = await fetch(`${API_URL}/teams?has_space=true&offset=0&limit=100`, {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })

    if (!response.ok) {
      const errorMessage = await extractErrorMessage(response)
      throw new Error(errorMessage)
    }

    const data = await response.json()
    teams.value = data.map(team => ({
      name: team.name,
    }))
  } catch (e) {
    console.error('Error fetching teams:', e)
    teamsError.value = e.message || 'Failed to load teams'
  } finally {
    isLoadingTeams.value = false
  }
}

const extractErrorMessage = async (response: Response) => {
  try {
    const responseClone = response.clone()
    const text = await responseClone.text()
    const data = JSON.parse(text)

    // За FastAPI validation errors
    if (data.detail && Array.isArray(data.detail) && data.detail.length > 0) {
      return data.detail[0].msg
    }

    // За HTTP exceptions
    if (data.detail && typeof data.detail === 'string') {
      return data.detail
    }

    return 'An error occurred'
  } catch (e) {
    console.error('Error extracting message:', e)
    return 'An error occurred'
  }
}


watch(() => props.modelValue, (newValue) => {
  if (newValue && props.editField === 'team') {
    fetchTeams();
  }
});


watch(() => props.editFirstName, (newValue) => {
  if (newValue && firstNameError.value) {
    firstNameError.value = ''
  }
})

watch(() => props.editLastName, (newValue) => {
  if (newValue && lastNameError.value) {
    lastNameError.value = ''
  }
})

watch(() => props.editValue, (newValue) => {
  if (props.editField === 'country' && countryError.value) {
    countryError.value = ''
  }
  if (props.editField === 'team' && teamsError.value) {
    teamsError.value = ''
  }
})
</script>

<style scoped>
/* Dialog base styles */
.edit-dialog, .dialog-card {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 2px solid #42DDF2FF;
  backdrop-filter: blur(10px);
}

.dialog-radius :deep(.v-card) {
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
  margin-top: -20px;
}

/* Buttons */
.cancel-btn, .submit-btn {
  border-radius: 50px !important;
  padding: 0 24px !important;
  height: 40px !important;
  text-transform: none !important;
}

.cancel-btn {
  background: transparent !important;
  color: #42DDF2FF !important;
  border: 2px solid #42DDF2FF !important;
}

.cancel-btn:hover {
  background: rgba(66, 221, 242, 0.1) !important;
}

.submit-btn {
  background: #42DDF2FF !important;
  color: #171c26 !important;
}

.submit-btn:hover {
  background: #FED854FF !important;
  box-shadow: 0 0 15px rgba(254, 216, 84, 0.3);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: rgba(66, 221, 242, 0.5) !important;
}

/* Input fields */
:deep(.v-field) {
  background: rgba(45, 55, 75, 0.8) !important;
}

:deep(.v-field__input),
:deep(.v-input input) {
  color: white !important;
}

:deep(.v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}

:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 0.85rem;
  line-height: 1.2;
}

:deep(.v-field__outline) {
  color: rgba(66, 221, 242, 0.3) !important;
}

/* Alert styling */
:deep(.v-alert) {
  background-color: rgba(254, 216, 84, 0.1) !important;
  color: #fed854 !important;
  border-color: #fed854 !important;
}

:deep(.v-alert__close-button),
:deep(.v-alert__prepend) {
  color: #fed854 !important;
}

/* Error states */
:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 0.85rem;
  line-height: 1.2;
  display: block !important;
}

:deep(.v-field--error) {
  --v-field-border-color: #fed854 !important;
}

:deep(.v-field--error .v-field__outline) {
  color: #fed854 !important;
}

/* Teams menu */
:deep(.teams-menu) {
  background: rgba(45, 55, 75, 0.95) !important;
  border: 1px solid rgba(66, 221, 242, 0.3);
  max-height: 300px !important;
  overflow-y: auto;
}

:deep(.teams-menu::-webkit-scrollbar) {
  width: 8px;
}

:deep(.teams-menu::-webkit-scrollbar-thumb) {
  background: rgba(66, 221, 242, 0.3);
  border-radius: 4px;
}

:deep(.teams-menu::-webkit-scrollbar-thumb:hover) {
  background: rgba(66, 221, 242, 0.5);
}
</style>
