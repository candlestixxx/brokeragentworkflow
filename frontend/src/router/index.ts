import { createRouter, createWebHistory } from 'vue-router'
import { user } from '../store'

import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import SettingsView from '../views/SettingsView.vue'
import AnalyticsView from '../views/AnalyticsView.vue'
import SocialView from '../views/SocialView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/settings',
      name: 'settings',
      component: SettingsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: AnalyticsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/community',
      name: 'community',
      component: SocialView,
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  // Wait a tick for auth to establish natively on boot if navigating directly
  if (to.meta.requiresAuth && !user.authenticated) {
    next({ name: 'login' })
  } else if ((to.name === 'login' || to.name === 'register') && user.authenticated) {
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router
