<template>
  <div class="welcome-card">
    <div class="welcome-content">
      <h2 class="welcome-text">Welcome, {{ userRole }}</h2>
    </div>
  </div>
</template>

<script setup lang="ts">
interface WelcomeProps {
  userRole: string
}

defineProps<WelcomeProps>()
</script>

<style scoped>
.welcome-card {
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(2px);
  position: relative;
  overflow: hidden;
  margin-bottom: 24px;
  padding: 24px;
  width: 55%;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

.welcome-content {
  position: relative;
  justify-items: center;
  z-index: 2;
}

.welcome-text {
  color: #42DDF2FF;
  font-size: 1.8rem;
  text-align: center;
  margin: 0;
}
</style>
