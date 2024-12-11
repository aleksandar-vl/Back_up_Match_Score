<template>
  <HeaderSection />

  <div class="content-wrapper">
    <v-container>
      <!-- Director Welcome Section -->
      <DashboardWelcome :userRole="player?.username" />

      <v-row class="dashboard-row">
        <!-- Player Profile Column -->
        <v-col cols="12" md="6">
          <PlayerCard
            :player="player"
            @edit="openEdit"
            @avatar-upload="openAvatarUpload"
          />
          <EditDialog
            v-model="showEditDialog"
            :player="player"
            :edit-field="editField"
            :edit-value="editValue"
            :edit-first-name="editFirstName"
            :edit-last-name="editLastName"
            @update:modelValue="showEditDialog = $event"
            @update:editValue="editValue = $event"
            @update:editFirstName="editFirstName = $event"
            @update:editLastName="editLastName = $event"
            @profile-updated="handleProfileUpdated"
          />
          <AvatarUploadDialog
            v-model="showAvatarDialog"
            :player="player"
            @avatar-updated="handleAvatarUpdated"
          />
          <v-snackbar
            v-model="showSuccessAlert"
            color="success"
            timeout="3000"
          >
            {{ successMessage }}
          </v-snackbar>
        </v-col>

        <!-- Request History Column -->
        <v-col cols="12" md="6">
          <RequestHistory />
        </v-col>

      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { API_URL } from '@/config'
import { useAuthStore } from '@/stores/auth'
import HeaderSection from "@/components/HeaderSection.vue";
import DashboardWelcome from "@/components/DashboardWelcome.vue";
import PlayerCard from "@/components/PlayerCard.vue";
import EditDialog from "@/components/dialogs/PlayerDashboardEditDialog.vue";
import AvatarUploadDialog from "@/components/dialogs/PlayerAvatarUpdateDialog.vue";
import RequestHistory from "@/components/RequestHistory.vue";
import type { Player, Team, Request } from '@/types/types'

const authStore = useAuthStore()

// State
const teams = ref<Team[]>([])
const isLoadingTeams = ref(false)
const teamsError = ref('')
const requests = ref<Request[]>([])
const requestHistoryError = ref<string | null>(null) // Scoped error for Request History

const player = ref<Player | null>(null)
const isLoading = ref(true)
const error = ref<string | null>(null)

// Edit Dialog State
const showEditDialog = ref(false)
const editField = ref('')
const editValue = ref('')
const editFirstName = ref('')
const editLastName = ref('')
const editError = ref('')

// Avatar Dialog State
const showAvatarDialog = ref(false)
const avatarFile = ref<File | null>(null)
const avatarPreview = ref<string | null>(null)
const avatarError = ref('')
const isUploading = ref(false)

// Success Alert State
const showSuccessAlert = ref(false)
const successMessage = ref('')

// Methods
const handleProfileUpdated = async () => {
  await fetchPlayer()
  showSuccessAlert.value = true
  successMessage.value = 'Profile updated successfully!'
}

const handleAvatarUpdated = async () => {
  await fetchPlayer()
  showSuccessAlert.value = true
  successMessage.value = 'Avatar updated successfully!'
}

const fetchTeams = async () => {
  try {
    isLoadingTeams.value = true
    teamsError.value = ''

    const response = await fetch(`${API_URL}/teams`, {
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

const fetchRequests = async () => {
  try {
    isLoading.value = true;
    requestHistoryError.value = null;

    const response = await fetch(
      `${API_URL}/requests/me?offset=0&limit=10`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
        },
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to fetch requests');
    }

    const data = await response.json();

    requests.value = [...data];

  } catch (e) {
    console.error('Error fetching requests:', e);
    requestHistoryError.value = e.message || 'Failed to load request history. Please try again later.';
  } finally {
    isLoading.value = false;
  }
};

const fetchPlayer = async () => {
  try {
    isLoading.value = true
    error.value = null
    const response = await fetch(`${API_URL}/players/users`, {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    if (!response.ok) throw new Error('Failed to fetch player details')
    player.value = await response.json()
  } catch (e) {
    console.error('Error fetching player:', e)
    error.value = 'Failed to load player details'
  } finally {
    isLoading.value = false
  }
}

const openEdit = async (field: string) => {
  console.log('Opening edit dialog with field:', field)
  editField.value = field
  editError.value = ''

  if (field === 'name') {
    editFirstName.value = player.value?.first_name || ''
    editLastName.value = player.value?.last_name || ''
    console.log('Setting name values:', {
      first: editFirstName.value,
      last: editLastName.value
    })
  } else if (field === 'team') {
    editValue.value = player.value?.team_name || ''
    await fetchTeams()
    console.log('Setting team value:', editValue.value)
  } else {
    editValue.value = player.value?.[field as keyof Player]?.toString() || ''
    console.log('Setting field value:', editValue.value)
  }

  showEditDialog.value = true
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

const openAvatarUpload = () => {
  avatarFile.value = null
  avatarPreview.value = null
  avatarError.value = ''
  showAvatarDialog.value = true
}

onMounted(() => {
  fetchRequests()
  fetchPlayer()
})
</script>


<style scoped>
.content-wrapper {
  position: relative;
  z-index: 3;
  padding-top: 100px;
  width: 100vw;
}

.dashboard-row {
  width: 1100px;
  align-self: center;
  justify-self: center;
}
</style>
