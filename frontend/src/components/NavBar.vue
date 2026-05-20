<template>
  <header class="bg-white shadow-sm sticky top-0 z-10">
    <nav class="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
      <h1 class="text-xl font-bold text-gray-800 tracking-tight">One-Minute Manager</h1>
      <div v-if="user.authenticated" class="flex items-center gap-4">
        <div class="flex items-center gap-2 relative group cursor-pointer" @click="showAvatarModal = true">
          <img :src="user.avatar_url || `https://ui-avatars.com/api/?name=${user.username}&background=random`" alt="Avatar" class="w-8 h-8 rounded-full shadow-sm object-cover border border-gray-200">
          <span class="text-gray-600">Hello, {{ user.username }}</span>
          <!-- Hover overlay -->
          <div class="absolute inset-0 bg-black bg-opacity-10 rounded-full opacity-0 group-hover:opacity-100 flex items-center justify-center transition" style="width: 2rem;">
            <span class="text-white text-xs font-bold">Edit</span>
          </div>
        </div>
        <button @click="logout" class="text-red-600 hover:text-red-800 transition duration-150 font-medium ml-2 border-l border-gray-300 pl-4">Logout</button>
      </div>
      <div v-else>
        <button @click="currentView = 'login'" :class="{'underline': currentView === 'login'}" class="text-blue-600 hover:text-blue-800 mr-4">Login</button>
        <button @click="currentView = 'register'" :class="{'underline': currentView === 'register'}" class="text-blue-600 hover:text-blue-800">Register</button>
      </div>
    </nav>
  </header>

  <!-- Avatar Modal -->
  <div v-if="showAvatarModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white p-6 rounded-lg shadow-lg max-w-sm w-full">
      <h3 class="text-xl font-bold mb-4">Update Avatar</h3>
      <form @submit.prevent="updateAvatar" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Image URL</label>
          <input v-model="newAvatarUrl" type="url" placeholder="https://example.com/photo.jpg" class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
        </div>
        <div class="flex justify-end gap-2">
          <button type="button" @click="showAvatarModal = false" class="px-4 py-2 text-gray-600 hover:text-gray-800">Cancel</button>
          <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 font-medium shadow">Save</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { user, currentView, logout, showToast } from '../store.js'

const showAvatarModal = ref(false)
const newAvatarUrl = ref('')

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
