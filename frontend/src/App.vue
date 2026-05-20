<template>
  <div class="bg-gray-50 min-h-screen font-sans text-gray-900">
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
import { io } from 'socket.io-client'
import { toastState, checkAuth, fetchData } from './store'
import NavBar from './components/NavBar.vue'

const socket = io() // Automatically connects to the host that serves the page

onMounted(async () => {
  socket.on('data_updated', (data) => {
    console.log("Real-time update received:", data)
    // Whenever a data_updated event is received, re-fetch all data.
    fetchData()
  })
})
</script>
