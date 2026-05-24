<template>
  <div class="bg-gray-50 dark:bg-gray-900 min-h-screen font-sans text-gray-900 dark:text-gray-100 transition-colors">
    <NavBar />

    <main class="max-w-4xl mx-auto px-4 py-8">
      <!-- Flash Messages equivalent (Toast) -->
      <div v-if="toastState.message" class="mb-6 space-y-2">
        <div :class="toastState.error ? 'bg-red-100 border-red-500 text-red-700' : 'bg-green-100 border-green-500 text-green-700'" class="border-l-4 p-4 rounded shadow-sm flex justify-between">
          <p>{{ toastState.message }}</p>
          <button @click="toastState.message = ''" class="font-bold">&times;</button>
        </div>
      </div>

      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { toastState, checkAuth, fetchData, goals, getSocket } from './store'
import NavBar from './components/NavBar.vue'

const socket = getSocket() // Automatically connects and is globally tracked

onMounted(async () => {
  // Legacy handler fallback
  socket.on('data_updated', (data: any) => {
    console.log("Real-time update received (legacy):", data)
    fetchData()
  })

  // When socket connects, force a join emission using existing state if possible.
  // This covers the case where the socket connects/reconnects after authentication.
  socket.on('connect', () => {
    if (store.user && store.user.authenticated && store.user.user_id) {
      socket.emit('join', { user_id: store.user.user_id })
    }
  })

  // Granular handlers
  socket.on('goal_added', (data: any) => {
    console.log("Goal added:", data)
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
    console.log("Goal deleted:", data)
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
    console.log("Goal completed:", data)
    if (data.id) {
      // Find the goal before removing it to push to completedGoals natively
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
         const finalGoal = targetGoal; // explicitly type assert safely
         // Push to the top of completed list organically

         // ensure it conforms strictly to the base Goal type required by completedGoals
         const safeGoal = {
           id: finalGoal.id,
           description: finalGoal.description,
           parent_id: finalGoal.parent_id
         };
         import('./store').then(store => {
             store.completedGoals.value.unshift(safeGoal)
             // We also adjust the analytic count immediately
             store.analytics.value.completed_goals += 1
         })
      }
    }
  })
})
</script>
