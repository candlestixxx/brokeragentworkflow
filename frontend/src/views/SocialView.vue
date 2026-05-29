<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface SocialUser {
  id: number
  username: string
  avatar_url: string | null
}

interface CompletedGoal {
  id: number
  description: string
  created_at: string
}

interface SocialProfile {
  id: number
  username: string
  avatar_url: string | null
  recent_completed_goals: CompletedGoal[]
  badges?: string[]
}

const users = ref<SocialUser[]>([])
const selectedProfile = ref<SocialProfile | null>(null)
const errorMsg = ref('')

const fetchPublicUsers = async () => {
  try {
    const res = await fetch('/api/social/users')
    if (res.ok) {
      users.value = await res.json()
    } else {
      errorMsg.value = 'Failed to load public users.'
    }
  } catch (e) {
    errorMsg.value = 'Connection error.'
  }
}

const viewProfile = async (id: number) => {
  try {
    const res = await fetch(`/api/social/users/${id}/profile`)
    if (res.ok) {
      selectedProfile.value = await res.json()
    } else {
      errorMsg.value = 'Failed to load profile.'
    }
  } catch (e) {
    errorMsg.value = 'Connection error.'
  }
}

onMounted(() => {
  fetchPublicUsers()
})
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <h2 class="text-2xl font-bold dark:text-white">Community Progress</h2>
    <p class="text-gray-600 dark:text-gray-400">See what your teammates are accomplishing.</p>

    <div v-if="errorMsg" class="bg-red-100 text-red-700 p-3 rounded-lg">{{ errorMsg }}</div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- User List -->
      <div class="col-span-1 bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
        <h3 class="text-lg font-semibold mb-4 dark:text-white">Public Users</h3>
        <ul class="space-y-2">
          <li v-for="u in users" :key="u.id" @click="viewProfile(u.id)" class="cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700 p-2 rounded-lg flex items-center space-x-3 transition-colors">
            <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold overflow-hidden border border-blue-200">
              <img v-if="u.avatar_url" :src="u.avatar_url" class="w-full h-full object-cover" />
              <span v-else>{{ u.username.charAt(0).toUpperCase() }}</span>
            </div>
            <span class="dark:text-gray-200 font-medium">{{ u.username }}</span>
          </li>
          <li v-if="users.length === 0" class="text-gray-500 dark:text-gray-400 text-sm">No public profiles found.</li>
        </ul>
      </div>

      <!-- Profile View -->
      <div class="col-span-1 md:col-span-2 bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
        <div v-if="selectedProfile">
          <div class="flex items-center space-x-4 mb-6 pb-4 border-b border-gray-100 dark:border-gray-700">
             <div class="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold overflow-hidden border-2 border-blue-200 text-2xl">
                <img v-if="selectedProfile.avatar_url" :src="selectedProfile.avatar_url" class="w-full h-full object-cover" />
                <span v-else>{{ selectedProfile.username.charAt(0).toUpperCase() }}</span>
              </div>
            <div>
              <h3 class="text-2xl font-bold dark:text-white mb-2">{{ selectedProfile.username }}</h3>
              <div class="flex space-x-1" v-if="selectedProfile.badges && selectedProfile.badges.length > 0">
                 <span v-for="badge in selectedProfile.badges" :key="badge" class="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs font-bold rounded-full border border-yellow-300" :title="badge">🏆 {{badge}}</span>
              </div>
            </div>
          </div>

          <h4 class="text-lg font-semibold mb-3 dark:text-gray-200">Recent Completed Goals</h4>
          <ul class="space-y-3">
            <li v-for="g in selectedProfile.recent_completed_goals" :key="g.id" class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg flex justify-between items-center">
              <span class="dark:text-gray-200">{{ g.description }}</span>
              <span class="text-xs text-gray-500 dark:text-gray-400">{{ new Date(g.created_at).toLocaleDateString() }}</span>
            </li>
            <li v-if="selectedProfile.recent_completed_goals.length === 0" class="text-gray-500 dark:text-gray-400 text-sm">No recently completed goals.</li>
          </ul>
        </div>
        <div v-else class="h-full flex flex-col items-center justify-center text-gray-400">
          <svg class="w-16 h-16 mb-4 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
          <p>Select a user to view their progress.</p>
        </div>
      </div>
    </div>
  </div>
</template>
