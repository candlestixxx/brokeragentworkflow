<template>
  <header class="bg-white dark:bg-gray-800 shadow-sm sticky top-0 z-10 transition-colors">
    <nav class="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
      <h1 class="text-xl font-bold text-gray-800 dark:text-white tracking-tight transition-colors">One-Minute Manager</h1>
      <div class="flex items-center gap-4">
        <button @click="toggleTheme" class="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 transition-colors rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none" aria-label="Toggle Dark Mode">
          <SunIcon v-if="isDarkMode" class="w-5 h-5" />
          <MoonIcon v-else class="w-5 h-5" />
        </button>

        <div v-if="user.authenticated" class="flex items-center gap-4">
          <div class="flex items-center gap-2 relative group cursor-pointer" @click="showAvatarModal = true">
            <img :src="user.avatar_url || `https://ui-avatars.com/api/?name=${user.username}&background=random`" alt="Avatar" class="w-8 h-8 rounded-full shadow-sm object-cover border border-gray-200 dark:border-gray-600 transition-colors">
            <span class="text-gray-600 dark:text-gray-300 transition-colors">Hello, {{ user.username }}</span>
            <!-- Hover overlay -->
            <div class="absolute inset-0 bg-black bg-opacity-10 rounded-full opacity-0 group-hover:opacity-100 flex items-center justify-center transition" style="width: 2rem;">
              <span class="text-white text-xs font-bold">Edit</span>
            </div>
          </div>
          <div class="ml-2 border-l border-gray-300 dark:border-gray-600 pl-4 flex gap-4">
            <router-link to="/" class="text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300 transition duration-150 font-medium" active-class="text-blue-600 dark:text-blue-400">Dashboard</router-link>
            <router-link to="/community" class="text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300 transition duration-150 font-medium" active-class="text-blue-600 dark:text-blue-400">Community</router-link>
            <router-link to="/analytics" class="text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300 transition duration-150 font-medium" active-class="text-blue-600 dark:text-blue-400">Analytics</router-link>
            <router-link to="/settings" class="text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300 transition duration-150 font-medium" active-class="text-blue-600 dark:text-blue-400">Settings</router-link>
            <button @click="logout" class="text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 transition duration-150 font-medium">Logout</button>
          </div>
        </div>
        <div v-else class="flex items-center">
          <router-link to="/login" class="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 mr-4 transition-colors" active-class="underline">Login</router-link>
          <router-link to="/register" class="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 transition-colors" active-class="underline">Register</router-link>
        </div>
      </div>
    </nav>
  </header>

  <!-- Avatar Modal via Headless UI -->
  <Dialog :open="showAvatarModal" @close="showAvatarModal = false" class="relative z-50">
    <div class="fixed inset-0 bg-black/50" aria-hidden="true" />

    <div class="fixed inset-0 flex items-center justify-center p-4">
      <DialogPanel class="w-full max-w-sm rounded-lg bg-white p-6 shadow-xl">
        <div class="flex items-center gap-3 mb-4">
          <UserCircleIcon class="h-6 w-6 text-blue-600" />
          <DialogTitle class="text-xl font-bold">Update Avatar</DialogTitle>
        </div>

        <form @submit.prevent="updateAvatar" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Image URL</label>
            <input v-model="newAvatarUrl" type="url" placeholder="https://example.com/photo.jpg" class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
          </div>
          <div class="flex justify-end gap-2 mt-4">
            <button type="button" @click="showAvatarModal = false" class="px-4 py-2 text-gray-600 hover:text-gray-800 font-medium transition">Cancel</button>
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 font-medium shadow transition">Save</button>
          </div>
        </form>
      </DialogPanel>
    </div>
  </Dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/vue'
import { UserCircleIcon, SunIcon, MoonIcon } from '@heroicons/vue/24/outline'
import { user, logout as storeLogout, showToast, toggleTheme, isDarkMode } from '../store'

const router = useRouter()
const showAvatarModal = ref(false)
const newAvatarUrl = ref('')

const logout = async () => {
  await storeLogout()
  router.push({ name: 'login' })
}

const updateAvatar = async () => {
  const res = await fetch('/api/me/avatar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ avatar_url: newAvatarUrl.value })
  })
  if (res.ok) {
    user.avatar_url = newAvatarUrl.value
    showAvatarModal.value = false
    showToast("Avatar updated successfully.")
  } else {
    showToast("Failed to update avatar.", true)
  }
}
</script>
