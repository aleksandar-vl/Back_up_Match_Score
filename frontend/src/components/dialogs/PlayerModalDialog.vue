<template>
  <v-dialog v-model="showDialog" max-width="600px" class="request-player-dialog">
    <v-card>
      <v-card-title class="request-dialog-title">
        {{ player?.username }}
      </v-card-title>
      <v-card-text class="request-dialog-content">
        <v-avatar size="150" class="mb-6">
          <v-img v-if="player?.avatar" :src="player.avatar" alt="Player avatar"></v-img>
          <v-icon v-else icon="mdi-account" color="#42DDF2FF" size="100"></v-icon>
        </v-avatar>

        <div class="request-stats-grid">
          <div class="request-stat-item">
            <div class="request-stat-label">Nickname</div>
            <div class="request-stat-value">{{ player?.username }}</div>
          </div>

          <div class="request-stat-item">
            <div class="request-stat-label">Full Name</div>
            <div class="request-stat-value" style="text-align: right;">{{ player?.first_name }} {{ player?.last_name }}</div>
          </div>

          <div class="request-stat-item">
            <div class="request-stat-label">Country</div>
            <div class="request-stat-value">{{ player?.country }}</div>
          </div>

          <div class="request-stat-item">
            <div class="request-stat-label">Win Ratio</div>
            <div class="request-stat-value" style="color: #FED854FF;">{{ player?.game_win_ratio }}</div>
          </div>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-btn
          block
          class="request-close-btn"
          @click="$emit('update:modelValue', false)"
          max-width="30px"
        >
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { computed, defineProps, defineEmits } from 'vue'
import type { Player } from "@/types/types";

// Props & Emits
const props = defineProps<{
  modelValue: boolean;
  player: Player | null;
}>()

const emit = defineEmits(['update:modelValue'])

const showDialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})
</script>

<style scoped>
.request-player-link {
  cursor: pointer;
  color: #42DDF2FF;
  transition: transform 0.2s;
  margin-left: 4px;
}

.request-player-link:hover {
  transform: scale(1.1);
}

.request-player-dialog :deep(.v-card) {
  width: 400px;
  margin: 0 auto;
  border-radius: 50px !important;
  background: rgba(45, 55, 75, 0.8) !important;
  backdrop-filter: blur(10px);
  border: 2px solid #42DDF2FF !important;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
}


.request-dialog-title {
  color: #42DDF2FF !important;
  font-size: 1.5rem !important;
  text-align: center;
  padding: 20px !important;
}

.request-dialog-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px;
  gap: 2px;
   max-height: 80vh;
  overflow-y: auto;
}

.request-dialog-content::-webkit-scrollbar {
  width: 6px;
}

.request-dialog-content::-webkit-scrollbar-track {
  background: transparent;
  margin: 4px;
}

.request-dialog-content::-webkit-scrollbar-thumb {
  background: #42DDF2FF;
  border-radius: 20px;
}

.request-dialog-content::-webkit-scrollbar-thumb:hover {
  background: #42DDF2FF;
  opacity: 0.8;
}

.request-stats-grid {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.request-stat-item {
  background: rgba(30, 40, 55, 0.5);
  border: 1px solid rgba(66, 221, 242, 0.3);
  border-radius: 10px;
  padding: 12px 20px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
}

.request-stat-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin-bottom: 0;
  justify-self: start;
}

.request-stat-value {
  color: white;
  font-size: 1.1rem;
  justify-self: end;
}

.request-close-btn {
  background: transparent !important;
  color: #42DDF2FF !important;
  border: 2px solid #42DDF2FF !important;
  border-radius: 50px !important;
  margin: 20px !important;
  padding: 10px 40px !important;
  font-size: 1.1rem !important;
}

.request-close-btn:hover {
  background: rgba(66, 221, 242, 0.1) !important;
}

.request-player-dialog :deep(.v-card-actions) {
  display: flex;
  justify-content: center;
}

.request-player-dialog :deep(.v-card-actions .v-btn) {
  background: rgba(17, 78, 112, 0.56) !important;
  color: #42DDF2FF !important;
  border: 2px solid #42DDF2FF !important;
  min-width: 120px;
  font-weight: bold;
  letter-spacing: 1px;
  transition: all 0.2s;
  margin: 20px auto;
}

.request-player-dialog :deep(.v-card-actions .v-btn:hover) {
  background: rgba(66, 221, 242, 0.1) !important;
  transform: translateY(-2px);
}

.request-close-btn {
  min-width: 120px !important;
  padding: 8px 24px !important;
  border: 2px solid #42DDF2FF !important;
  color: #42DDF2FF !important;
  background: transparent !important;
  border-radius: 50px !important;
  font-size: 0.9rem !important;
  text-transform: none !important;
  transition: all 0.2s !important;
}

.request-close-btn:hover {
  background: rgba(66, 221, 242, 0.1) !important;
}
</style>
