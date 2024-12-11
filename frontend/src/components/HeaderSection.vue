<template>
  <div class="header-wrapper">
    <div class="header-image"></div>
    <div class="header-overlay"></div>
  </div>
</template>

<script setup lang="ts">
// No props or logic needed
</script>

<style scoped>
.header-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 600px;
  background-image: url('@/assets/top-image.png');
  background-size: cover;
  background-position: center;
  z-index: 1;
  opacity: 0.6;
}

.header-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 600px;
  background: linear-gradient(
    to bottom,
    rgba(23, 28, 38, 0) 0%,
    rgba(23, 28, 38, 0.8) 25%,
    rgba(23, 28, 38, 1) 80%
  );
  z-index: 2;
}</style>
