import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/events',
      name: 'events',
      component: () => import('../views/TournamentList.vue'),
    },
    {
      path: '/matches',
      name: 'matches',
      component: () => import('../views/MatchList.vue'),
    },
    {
      path: '/teams',
      name: 'teams',
      component: () => import('../views/TeamList.vue'),
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/dashboard-user',
      name: 'dashboard-user',
      component: () => import('../views/DashboardUser.vue'),
      meta: { requiresAuth: true, roles: ['user'] }
    },
    {
      path: '/dashboard-admin',
      name: 'dashboard-admin',
      component: () => import('../views/DashboardAdmin.vue'),
      meta: { requiresAuth: true, roles: ['admin'] }
    },
    {
      path: '/dashboard-player',
      name: 'dashboard-player',
      component: () => import('../views/DashboardPlayer.vue'),
      meta: { requiresAuth: true, roles: ['player'] }
    },
    {
      path: '/dashboard-director',
      name: 'dashboard-director',
      component: () => import('../views/DashboardDirector.vue'),
      meta: { requiresAuth: true, roles: ['director'] }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LogIn.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/events/:id',
      name: 'tournament-details',
      component: () => import('../views/SingleTournament.vue'),
    },
    {
      path: '/teams/:id',
      name: 'team-details',
      component: () => import('../views/SingleTeam.vue'),
    },
  ],
})

// Navigation Guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Ensure token and role are checked
  if (authStore.token && !authStore.userRole) {
    await authStore.fetchUserRole()
  }

  // Check for routes that require authentication
  if (to.meta.requiresAuth) {
    // User is not authenticated
    if (!authStore.isAuthenticated) {
      next('/login')
      return
    }

    // Check role-based access
    const requiredRoles = to.meta.roles as string[]
    if (requiredRoles && !requiredRoles.includes(authStore.userRole || '')) {
      // Redirect based on role
      if (authStore.userRole === 'admin') {
        next('/dashboard-admin')
      } else if (authStore.userRole === 'user') {
        next('/dashboard-user')
      } else if (authStore.userRole === 'player') {
        next('/dashboard-player')
      } else if (authStore.userRole === 'director') {
        next('/dashboard-director')
      } else {
        next('/login')
      }
      return
    }
  }

  // Routes that require guest (non-authenticated) access
  if (to.meta.requiresGuest) {
    if (authStore.isAuthenticated) {
      // Redirect authenticated users away from login/register
      if (authStore.userRole === 'admin') {
        next('/dashboard-admin')
      } else if (authStore.userRole === 'user') {
        next('/dashboard-user')
      } else if (authStore.userRole === 'player') {
        next('/dashboard-player')
      } else if (authStore.userRole === 'director') {
        next('/dashboard-director')
      } else {
        next('/')
      }
      return
    }
  }

  next()
})

export default router
