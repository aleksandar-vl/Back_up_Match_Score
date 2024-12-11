<template>
  <div class="load-more-wrapper">
    <v-btn
      class="load-more-btn"
      variant="outlined"
      @click="$emit('load-more')"
      :loading="isLoading"
      :disabled="isLoading"
    >
      <v-icon left class="mr-2">mdi-refresh</v-icon>
      {{ buttonText }}
    </v-btn>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  isLoading: boolean
  buttonText: string
}>()

defineEmits(['load-more'])
</script>

<style scoped>

.load-more-wrapper {
  display: flex;
  justify-content: center;
  margin: 40px 0;
  position: relative;
  z-index: 4;
}

.load-more-btn {
  background: rgba(17, 78, 112, 0.56);
  color: #ffffff !important;
  border-color: #42DDF2FF !important;
  border-width: 2px !important;
  border-radius: 50px;
  transition: all 0.2s ease;
  padding: 5px 40px !important;
  font-size: 1.1rem !important;
}

.load-more-btn:hover {
  background: rgba(66, 221, 242, 0.1);
  border-color: #42DDF2FF !important;
  transform: translateY(-2px);
  box-shadow: 0 0 15px rgba(66, 221, 242, 0.3);
}

.load-more-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
