<template>
  <HeaderSection />

  <div class="content-wrapper">
    <v-container>
      <!-- User Welcome Section -->
      <DashboardWelcome :userRole="userEmail" />


      <!-- Request Buttons Section -->
      <UserRequestButtons
        :requests="requests"
        @update-requests="fetchRequests"
        @show-player-dialog="showPlayerLinkDialog = true"
        @show-success="handleSuccess"
      />

      <!-- Player Link Dialog -->
      <LinkPlayerRequestDialog
        v-model="showPlayerLinkDialog"
        :has-pending-request="hasPendingRequest"
        @submit-success="handleSuccess"
      />

      <!-- Request History Section -->
      <RequestHistory />
    </v-container>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted, computed, watch} from 'vue'
import { useAuthStore } from '@/stores/auth'
import { API_URL } from '@/config'
import HeaderSection from "@/components/HeaderSection.vue";
import DashboardWelcome from "@/components/DashboardWelcome.vue";
import UserRequestButtons from "@/components/UserRequestButtons.vue";
import LinkPlayerRequestDialog from "@/components/dialogs/LinkPlayerRequestDialog.vue";
import RequestHistory from "@/components/RequestHistory.vue";
import type { Request } from '@/types/types'

const authStore = useAuthStore()
const userEmail = ref(authStore.userEmail)

const requests = ref<Request[]>([])
const isLoading = ref(true)
const requestHistoryError = ref<string | null>(null)
const showPlayerLinkDialog = ref(false)
const showSuccessAlert = ref(false)
const successMessage = ref('')

// Methods
const handleSuccess = (message: string) => {
  successMessage.value = message
  showSuccessAlert.value = true
  fetchRequests()
  window.setTimeout(() => {
  window.location.reload();
}, 200);
}

const hasPendingRequest = computed(() => {
  const pendingRequests = requests.value.filter(request => request.status === 'pending');
  return requests.value.some(request =>
    request.status === 'pending' &&
    (request.request_type === 'link user to player' || request.request_type === 'promote user to director')
  );

});

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

onMounted(() => {
  fetchRequests();
});
</script>

<style scoped>
.content-wrapper {
  position: relative;
  z-index: 3;
  padding-top: 100px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100vw !important;
  margin-bottom: 100px;
}
</style>
