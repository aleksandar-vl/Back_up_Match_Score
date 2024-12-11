<template>
  <v-app>
    <!-- Navigation Drawer -->
    <v-navigation-drawer
      expand-on-hover
      rail
      class="transparent-drawer">

      <!-- Avatar/Logo -->
      <v-list-item
        prepend-icon="mdi-cat"
        title="Kitten Strike"
      ></v-list-item>

      <!-- Search bar - conditionally rendered -->
      <v-list-item>
        <v-text-field
          v-model="searchQuery"
          density="compact"
          variant="outlined"
          prepend-icon="mdi-magnify"
          :placeholder="shouldShowSearch ? 'Search...' : ''"
          hide-details
          rounded
          class="mt-2"
          @update:model-value="handleSearch"
          :disabled="!shouldShowSearch"
          :readonly="!shouldShowSearch"
          :class="{ 'search-disabled': !shouldShowSearch }"
        ></v-text-field>
      </v-list-item>

      <v-divider></v-divider>

      <!-- Common menu items (Home, Events, Matches, Teams) -->
      <v-list nav>
        <v-list-item
          v-for="(item, index) in menuItems.slice(0, 4)"
          :key="index"
          :to="item.path"
          :prepend-icon="item.icon"
          link
        >
          {{ item.title }}
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

        <!-- Authenticated menu items -->
        <div v-if="authStore.isAuthenticated">
          <v-list nav>
            <!-- Dashboard -->
            <v-list-item
              :to="menuItems[4].path"
              :prepend-icon="menuItems[4].icon"
              link
            >
              {{ menuItems[4].title }}
            </v-list-item>

          <!-- Logout button -->
          <v-list-item
            @click="handleLogout"
            prepend-icon="mdi-logout"
            link
            color="error"
          >
            Logout
          </v-list-item>
        </v-list>
      </div>

      <!-- Non-authenticated menu items -->
      <div v-else>
        <v-list nav>
          <v-list-item
            v-for="(item, index) in menuItems.slice(5, 7)"
            :key="index"
            :to="item.path"
            :prepend-icon="item.icon"
            link
          >
            {{ item.title }}
          </v-list-item>
        </v-list>
      </div>

      <v-divider></v-divider>

      <!-- About (always visible) -->
      <v-list nav>
        <v-list-item
          :to="menuItems[7].path"
          :prepend-icon="menuItems[7].icon"
          link
        >
          {{ menuItems[7].title }}
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <router-view></router-view>
    </v-main>

    <!-- Footer -->
    <v-footer class="app-footer">
      <div class="footer-content">
        <div class="footer-left">
          <span class="footer-text">© 2024 Kitten Strike. All rights reserved.</span>
        </div>

        <div class="footer-right">
          <v-btn icon variant="text">
            <v-icon>mdi-github</v-icon>
          </v-btn>
        </div>
      </div>
    </v-footer>
  </v-app>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter, useRoute } from 'vue-router'
import { API_URL } from '@/config'


const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const searchQuery = ref('')

// Pages where search should be hidden
const noSearchPages = [
  '/', '/login', '/register', '/dashboard', '/about', '/dashboard-player',
  'dashboard-user', '/dashboard-admin', '/dashboard-director', '/events/:id', '/teams/:id']

const matchesPathPattern = (currentPath: string, pattern: string): boolean => {
  const regexPattern = pattern
    .replace(':id', '[0-9a-fA-F-]+')
    .replace(/\//g, '\\/');

  const regex = new RegExp(`^${regexPattern}$`);
  return regex.test(currentPath);
};

const dashboardPath = computed(() => {
  switch (authStore.userRole) {
    case 'ADMIN':
      return '/dashboard-admin'
    case 'USER':
      return '/dashboard-user'
    case 'PLAYER':
      return '/dashboard-player'
    case 'DIRECTOR':
      return '/dashboard-director'
    default:
      return '/login'
  }
})

// Computed property to determine if search should be shown
const shouldShowSearch = computed(() => {
  const currentPath = route.path;
  return !noSearchPages.some(pattern => matchesPathPattern(currentPath, pattern));
})

// Function to handle search based on current route
const handleSearch = async () => {
  const query = searchQuery.value.trim()

  try {
    let endpoint = ''

    // Determine which endpoint to use based on current route
    switch (route.path) {
      case '/teams':
        endpoint = query
          ? `${API_URL}/teams/?search=${query}&sort_by=desc&offset=0&limit=10`
          : `${API_URL}/teams/?sort_by=desc&offset=0&limit=10`
        break
      case '/events':
        endpoint = query
          ? `${API_URL}/tournaments/?search=${query}&offset=0&limit=10`
          : `${API_URL}/tournaments/?offset=0&limit=10`
        break
      case '/matches':
        endpoint = query
          ? `${API_URL}/matches/?tournament_title=${query}&offset=0&limit=10`
          : `${API_URL}/matches/?offset=0&limit=10`
        break
      default:
        return
    }

    const response = await fetch(endpoint)
    if (!response.ok) {
      throw new Error('Search failed')
    }

    const data = await response.json()

    window.dispatchEvent(new CustomEvent('search-results', {
      detail: {
        results: data,
        route: route.path
      }
    }))
  } catch (error) {
    console.error('Search error:', error)
  }
}

const menuItems = ref([
  { title: 'Home', path: '/', icon: 'mdi-home' },
  { title: 'Events', path: '/events', icon: 'mdi-trophy' },
  { title: 'Matches', path: '/matches', icon: 'mdi-gamepad-variant' },
  { title: 'Teams', path: '/teams', icon: 'mdi-account-group' },
  {
      title: 'Dashboard',
      path: dashboardPath.value,
      icon: 'mdi-paw'
    },
  { title: 'Login', path: '/login', icon: 'mdi-account' },
  { title: 'Register', path: '/register', icon: 'mdi-account-plus' },
  { title: 'About', path: '/about', icon: 'mdi-information' }
]);

const handleLogout = async () => {
  const success = await authStore.logout()

  if (success) {
    await router.push('/')
  } else {
    console.error('Failed to logout')
  }
}

onMounted(async () => {
  await authStore.initializeFromToken()
})
</script>

<style>

#app {
  min-height: 100vh;
  min-width: 100vw;
  background: #171c26;
  padding: 0 0 0 0 !important;
}

.v-application {
  background-color: #171c26 !important;
  display: flex;
  min-height: 100vh !important;
  width: 120vw !important;
  flex-direction: column;
  overflow-x: hidden;
}

.v-main {
  min-height: 100vh !important;
  height: auto !important;
  overflow-y: auto;
  padding: 0 !important;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 64px); /* Adjust 64px based on your footer height */
}

.v-navigation-drawer {
  height: 100vh !important;
}

.transparent-drawer {
  background-color: rgba(206, 214, 225, 0) !important;
  backdrop-filter: blur(10px);
  color: white !important;
}

.transparent-drawer .v-list {
  background-color: transparent !important;
  color: white !important;
}

.transparent-drawer .v-list-item {
  background-color: transparent !important;
  color: white !important;
}

.transparent-drawer .v-list-item__prepend > .v-icon {
  color: white !important;
}

.transparent-drawer .v-list-item-title {
  color: white !important;
}

.v-text-field {
  width: 100%;
  color: white !important;
}

.v-text-field input {
  font-size: 0.9rem;
  color: white !important;
}

.v-text-field input::placeholder {
  color: rgba(255, 255, 255, 0.7) !important;
}

.transparent-drawer .v-text-field .v-field__outline {
  color: rgba(255, 255, 255, 0.7) !important;
}

.transparent-drawer .v-divider {
  opacity: 0.5;
  border-color: rgba(255, 255, 255, 0.1) !important;
}

.transparent-drawer .v-list-item--active {
  color: #fed854 !important;
}

.transparent-drawer .v-list-item--active .v-icon {
  color: #fed854 !important;
}
/* Search bar */
.v-text-field {
  width: 100%;
}

/* Input for search bar */
.v-text-field input {
  font-size: 0.9rem;
}


.app-footer {
  background: rgba(45, 55, 75, 0.5) !important;
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(8, 117, 176, 0.4);
  min-height: 64px !important;
  padding: 12px 24px !important;
  position: relative;
  z-index: 1000;
  width: 100vw !important;
}

.footer-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-left: 70px;
  margin-right: 20px;
}

.footer-text {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.footer-right {
  display: flex;
  gap: 8px;
}

.footer-right .v-btn {
  color: rgba(255, 255, 255, 0.7) !important;
  transition: color 0.2s;
}

.footer-right .v-btn:hover {
  color: #fed854 !important;
}

.search-disabled {
  opacity: 0.2;
  pointer-events: none;
}

.search-disabled :deep(.v-field__outline) {
  opacity: 0.2;
}
</style>
