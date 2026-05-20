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

      <!-- UNAUTHENTICATED VIEW -->
      <div v-if="!user.authenticated">
        <AuthTabs />
      </div>

      <!-- AUTHENTICATED DASHBOARD VIEW -->
      <div v-else>
        <h2 class="text-3xl font-bold text-gray-800 mb-8 text-center">One-Minute Manager Dashboard</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Daily Goals Column -->
          <div class="flex flex-col h-full">
            <section class="bg-white rounded-lg shadow-md p-6 mb-8 flex-1">
              <div class="flex flex-col gap-3 lg:flex-row lg:justify-between border-b border-gray-100 pb-3 mb-4">
                <h2 class="text-2xl font-semibold text-gray-800">Daily One-Minute Goals</h2>
                <div class="flex gap-2">
                  <button @click="activeTab = 'active'" :class="{'bg-blue-100 text-blue-800': activeTab === 'active', 'text-gray-500 hover:text-gray-700': activeTab !== 'active'}" class="px-3 py-1 rounded font-medium text-sm transition">Active</button>
                  <button @click="activeTab = 'completed'" :class="{'bg-blue-100 text-blue-800': activeTab === 'completed', 'text-gray-500 hover:text-gray-700': activeTab !== 'completed'}" class="px-3 py-1 rounded font-medium text-sm transition">History</button>
                  <button @click="activeTab = 'calendar'" :class="{'bg-blue-100 text-blue-800': activeTab === 'calendar', 'text-gray-500 hover:text-gray-700': activeTab !== 'calendar'}" class="px-3 py-1 rounded font-medium text-sm transition">Calendar</button>
                </div>
              </div>

              <!-- Active Goals Tab -->
              <div v-if="activeTab === 'active'">
                <ActiveGoals />
              </div>

              <!-- Completed Goals Tab -->
              <div v-if="activeTab === 'completed'">
                <CompletedGoals />
              </div>

              <!-- Calendar Goals Tab -->
              <div v-if="activeTab === 'calendar'">
                <CalendarGoals />
              </div>
            </section>
          </div>

          <!-- Quarterly Initiatives Column -->
          <div class="flex flex-col h-full">
            <QuarterlyInitiatives />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { io } from 'socket.io-client'
import { user, activeTab, toastState, checkAuth, fetchData } from './store.js'

import NavBar from './components/NavBar.vue'
import AuthTabs from './components/AuthTabs.vue'
import ActiveGoals from './components/ActiveGoals.vue'
import CompletedGoals from './components/CompletedGoals.vue'
import CalendarGoals from './components/CalendarGoals.vue'
import QuarterlyInitiatives from './components/QuarterlyInitiatives.vue'

const socket = io() // Automatically connects to the host that serves the page

onMounted(() => {
  checkAuth()

  socket.on('data_updated', (data) => {
    console.log("Real-time update received:", data)
    // Whenever a data_updated event is received, re-fetch all data.
    fetchData()
  })
})
</script>
