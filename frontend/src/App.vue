<template>
  <div class="bg-brand-neutral dark:bg-brand-neutral-dark min-h-screen font-sans text-slate-900 dark:text-slate-100 transition-colors duration-300">
    <NavBar />
    <OnboardingGuide />

    <main class="max-w-6xl mx-auto px-4 py-8">
      <!-- Global Toast Notifications -->
      <transition 
        enter-active-class="transform ease-out duration-300 transition" 
        enter-from-class="translate-y-8 opacity-0" 
        enter-to-class="translate-y-0 opacity-100" 
        leave-active-class="transition ease-in duration-200" 
        leave-from-class="opacity-100 translate-y-0" 
        leave-to-class="opacity-0 translate-y-8"
      >
        <div v-if="toastState.message" :class="['fixed bottom-8 right-8 px-6 py-4 rounded-2xl shadow-2xl z-50 flex items-center gap-3 border transition-all duration-300', toastState.error ? 'bg-red-500 border-red-400 text-white' : 'bg-slate-900 border-slate-700 text-white']">
          <div :class="['w-2 h-2 rounded-full animate-pulse', toastState.error ? 'bg-white' : 'bg-brand-calm']" />
          <span class="font-bold text-sm uppercase tracking-widest">{{ toastState.message }}</span>
          <button @click="toastState.message = ''" class="ml-2 hover:opacity-70 transition-opacity">
            <XMarkIcon class="h-4 w-4" />
          </button>
        </div>
      </transition>

      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { toastState, checkAuth, fetchData, goals, user, getSocket } from './store'
import NavBar from './components/NavBar.vue'
import OnboardingGuide from './components/OnboardingGuide.vue'
import { CheckCircleIcon, XCircleIcon, XMarkIcon } from '@heroicons/vue/24/outline'

const socket = getSocket()

onMounted(async () => {
  await checkAuth()
  if (user.authenticated) {
    fetchData()
  }

  socket.on('data_updated', (data: any) => {
    fetchData()
  })

  socket.on('connect', () => {
    if (user && user.authenticated && user.user_id) {
      socket.emit('join', { user_id: user.user_id })
    }
  })

  socket.on('goal_added', (data: any) => {
    if (data.goal) {
      if (data.goal.parent_id) {
        const parent = goals.value.find(g => g.id === data.goal.parent_id)
        if (parent) {
          if (!parent.subgoals) parent.subgoals = []
          parent.subgoals.push(data.goal)
        }
      } else {
        goals.value.push(data.goal)
      }
    }
  })

  socket.on('goal_deleted', (data: any) => {
    if (data.id) {
      goals.value = goals.value.filter(g => g.id !== data.id)
      goals.value.forEach(g => {
        if (g.subgoals) {
          g.subgoals = g.subgoals.filter(s => s.id !== data.id)
        }
      })
    }
  })

  socket.on('goal_completed', (data: any) => {
    if (data.id) {
      let targetGoal = goals.value.find(g => g.id === data.id)
      if (!targetGoal) {
        goals.value.forEach(g => {
          if (g.subgoals) {
            const sg = g.subgoals.find(s => s.id === data.id)
            if (sg) targetGoal = sg
          }
        })
      }

      goals.value = goals.value.filter(g => g.id !== data.id)
      goals.value.forEach(g => {
        if (g.subgoals) {
          g.subgoals = g.subgoals.filter(s => s.id !== data.id)
        }
      })

      if (targetGoal) {
         const goalToMove = targetGoal as any
         import('./store').then(store => {
             store.completedGoals.value.unshift(goalToMove)
             store.analytics.value.completed_goals += 1
         })
      }
    }
  })
})
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
