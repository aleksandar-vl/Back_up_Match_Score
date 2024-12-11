<template>
  <div class="history-card">
    <div class="history-content">

      <!-- Filter Options -->
      <div class="filter-options">
        <v-select
          v-model="filterStatus"
          :items="statusOptions"
          item-title="text"
          item-value="value"
          label="Filter by Status"
          variant="outlined"
          density="comfortable"
          bg-color="rgba(45, 55, 75, 0.4)"
          color="#42DDF2FF"
          clearable
          @update:model-value="fetchRequests"
        ></v-select>
      </div>

      <!-- Loading state -->
      <div
        v-if="isLoading"
        class="d-flex justify-center align-center"
        style="height: 200px"
      >
        <v-progress-circular indeterminate color="#42DDF2FF"></v-progress-circular>
      </div>

      <!-- Error state -->
      <div v-else-if="requestHistoryError" class="error-message">
        {{ requestHistoryError }}
      </div>

      <!-- Request list -->
      <div v-else-if="requests.length > 0" class="request-list">
        <div
          v-for="request in requests"
          :key="request.id"
          class="request-item"
        >
          <div class="request-header">
            <div class="request-type">
              <v-icon
                :icon="getRequestTypeIcon(request.request_type)"
                class="request-icon"
              ></v-icon>
              {{ formatRequestType(request.request_type) }}
            </div>
            <div :class="['status-tag', `status-${request.status}`]">
              {{ formatStatus(request.status) }}
            </div>
          </div>

          <div class="request-details">
            <div class="detail-item">
              <v-icon
                icon="mdi-calendar"
                size="small"
                class="detail-icon"
              ></v-icon>
              {{ formatDate(request.request_date) }}
            </div>
            <div class="detail-item">
              <v-icon
                icon="mdi-email"
                size="small"
                class="detail-icon"
              ></v-icon>
              User Email: {{ request.email }}
            </div>
            <div v-if="request.username" class="detail-item">
              <v-icon
                icon="mdi-account"
                size="small"
                class="detail-icon"
              ></v-icon>
              Player:
              <span
                class="request-player-link"
                @click="handlePlayerClick(request.username)"
              >
                {{ request.username }}
              </span>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="request-actions">
            <v-btn
              class="approve-btn"
              @click="approveRequest(request.id)"
              :loading="isApprovingRequest[request.id]"
              :disabled="request.status !== 'pending' || isApprovingRequest[request.id] || isRejectingRequest[request.id]"
            >
              Approve
            </v-btn>
            <v-btn
              class="reject-btn"
              @click="rejectRequest(request.id)"
              :loading="isRejectingRequest[request.id]"
              :disabled="request.status !== 'pending' || isApprovingRequest[request.id] || isRejectingRequest[request.id]"
            >
              Reject
            </v-btn>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else class="error-message">
        No requests found.
      </div>
    </div>
  </div>

  <!-- Player Modal -->
  <PlayerModal
    v-model="showPlayerModal"
    :player="selectedPlayer"
  />
</template>

<script setup lang="ts">
import {ref, onMounted} from "vue";
import { format } from 'date-fns'
import { useAuthStore } from '@/stores/auth'
import { API_URL } from '@/config'
import type { Request, Player } from "@/types/types";
import PlayerModal from "@/components/dialogs/PlayerModalDialog.vue";

const authStore = useAuthStore()

// State
const isLoading = ref(true)
const requestHistoryError = ref<string | null>(null)
const actionsError = ref<string | null>(null)
const filterStatus = ref('');
const isApprovingRequest = ref<{ [key: string]: boolean }>({});
const isRejectingRequest = ref<{ [key: string]: boolean }>({});
const statusOptions = ['Pending', 'Accepted', 'Rejected'];
const isSubmitting = ref(false)
const showSuccessAlert = ref(false)
const successMessage = ref('')
const isLoadingPlayer = ref(false)
const selectedPlayer = ref<Player | null>(null)
const showPlayerModal = ref(false)

const props = defineProps<{
  requests: Request[]
  limit?: number
  isLoadMore: boolean
}>()

// Emits
const emit = defineEmits(['player-click', 'update:requests'])


// Helper functions
const formatDate = (date: string): string => {
  return format(new Date(date), 'dd MMM yyyy, HH:mm');
};

const formatRequestType = (type: string): string => {
  return type
    .split(' ')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

const formatStatus = (status: string): string => {
  return status.charAt(0).toUpperCase() + status.slice(1);
};

const getRequestTypeIcon = (type: string): string => {
  if (type === 'promote user to director') return 'mdi-shield-account';
  if (type === 'link user to player') return 'mdi-account-plus';
  return 'mdi-help';
};

// API calls
const fetchRequests = async () => {
  try {
    isLoading.value = true;
    requestHistoryError.value = null;

    const statusQuery = filterStatus.value && filterStatus.value !== 'All'
      ? `&status=${filterStatus.value.toLowerCase()}`
      : '';

    const offset = props.isLoadMore ? props.requests.length : 0;

    const response = await fetch(
      `${API_URL}/requests?offset=${offset}&limit=${props.limit || 5}${statusQuery}`,
      {
        headers: {
          Authorization: `Bearer ${authStore.token}`,
        },
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'No requests found.');
    }

    const data = await response.json();

    if (props.isLoadMore) {
      emit('update:requests', [...props.requests, ...data]);
    } else {
      emit('update:requests', data);
    }

  } catch (e) {
    console.error('Error fetching requests:', e);
    requestHistoryError.value = 'Failed to load request history. Please try again later.';
  } finally {
    isLoading.value = false;
  }
};

const approveRequest = async (requestId: string) => {
  try {
    isApprovingRequest.value[requestId] = true;
    isSubmitting.value = true;

    const response = await fetch(`${API_URL}/requests/${requestId}?status=accepted`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to approve request');
    }

    // 2. Get the approved request details
    const approvedRequest = props.requests.find(r => r.id === requestId);

    // 3. If it's a player link request, reject all other pending requests
    if (approvedRequest && approvedRequest.username) {
      const otherPendingRequests = props.requests.filter(r =>
        r.id !== requestId &&
        r.status === 'pending' &&
        r.username === approvedRequest.username
      );

      // Reject all other pending requests for this player
      for (const request of otherPendingRequests) {
        await fetch(`${API_URL}/requests/${request.id}?status=rejected`, {
          method: 'PUT',
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });
      }
    }

    successMessage.value = 'Request approved successfully.';
    showSuccessAlert.value = true;

    // Обновяваме списъка на заявките чрез родителския компонент
    await fetchRequests();

  } catch (e) {
    console.error('Error approving request:', e);
    actionsError.value = 'Failed to approve request. Please try again.';
  } finally {
    isSubmitting.value = false;
    isApprovingRequest.value[requestId] = false;
  }
};

const rejectRequest = async (requestId: string) => {
  try {
    isRejectingRequest.value[requestId] = true;
    isSubmitting.value = true;

    const response = await fetch(`${API_URL}/requests/${requestId}?status=rejected`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('API Error:', errorData);
      throw new Error(errorData.detail?.[0]?.msg || 'Failed to reject request');
    }

    successMessage.value = 'Request rejected successfully.';
    showSuccessAlert.value = true;

    await fetchRequests();

  } catch (e) {
    console.error('Error rejecting request:', e);
    actionsError.value = e.message || 'Failed to reject request. Please try again.';
  } finally {
    isSubmitting.value = false;
    isRejectingRequest.value[requestId] = false;
  }
};

const handlePlayerClick = async (username: string) => {
  try {
    isLoadingPlayer.value = true
    const response = await fetch(`${API_URL}/players?search=${encodeURIComponent(username)}`)
    if (!response.ok) {
      throw new Error('Failed to fetch player')
    }
    const players = await response.json()
    if (players.length > 0) {
      selectedPlayer.value = players[0]
      showPlayerModal.value = true
    }
  } catch (e) {
    console.error('Error fetching player:', e)
  } finally {
    isLoadingPlayer.value = false
  }
};


// Lifecycle
onMounted(() => {
  fetchRequests()
})
</script>

<style scoped>
.history-card {
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(2px);
  position: relative;
  overflow: hidden;
  padding: 24px;
  width: 65%;
  max-width: 1400px;
  margin: 0 auto 24px;
}

.filter-options {
  display: flex;
  gap: 16px;
  width: 400px;
  justify-self: center;
}

.error-message {
  color: #fed854;
  font-size: 0.9rem;
  margin-top: 8px;
  text-align: center;
}

.request-list {
  display: grid;
  gap: 16px;
  width: 100%;
}

.request-item {
  background: rgba(45, 55, 75, 0.8);
  border: 1px solid rgba(8, 87, 144, 0.2);
  border-radius: 10px;
  padding: 16px;
  transition: all 0.2s;
}

.request-item:hover {
  background: rgb(45, 55, 75);
  border-color: #42DDF2FF;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(8, 117, 176, 0.2);
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.request-type {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  font-weight: 500;
}

.request-icon {
  color: #42DDF2FF !important;
}

.status-tag {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.9rem;
}

.request-details {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.detail-icon {
  color: #42DDF2FF !important;
}

.request-player-link {
  cursor: pointer;
  color: #42DDF2FF;
  margin-left: 4px;
}

.request-player-link:hover {
  transform: scale(1.1);
}

/* Status styles */
.status-pending {
  background: rgba(254, 216, 84, 0.1);
  color: #FED854FF;
  border: 1px solid rgba(254, 216, 84, 0.3);
}

.status-accepted {
  background: rgba(0, 255, 157, 0.1);
  color: #00ff9d;
  border: 1px solid rgba(0, 255, 157, 0.3);
}

.status-rejected {
  background: rgba(255, 99, 99, 0.1);
  color: #ff6363;
  border: 1px solid rgba(255, 99, 99, 0.3);
}

.request-actions {
  display: flex;
  gap: 16px;
  margin-top: 16px;
}

/* Button styles */
.approve-btn, .reject-btn {
  transition: 0.2s;
}

.approve-btn {
  background: rgba(0, 255, 157, 0.1);
  color: #00ff9d;
  border: 1px solid rgba(0, 255, 157, 0.3);
}

.reject-btn {
  background: rgba(255, 99, 99, 0.1);
  color: #ff6363;
  border: 1px solid rgba(255, 99, 99, 0.3);
}

.approve-btn:disabled, .reject-btn:disabled {
  opacity: 0.3;
}

:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 14px;
}

:deep(.v-field--error) {
  --v-field-border-color: #fed854 !important;
}
</style>
