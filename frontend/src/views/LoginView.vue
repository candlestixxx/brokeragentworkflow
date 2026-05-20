<template>
  <div class="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
    <h2 class="text-2xl font-semibold text-gray-800 border-b border-gray-100 pb-3 mb-4">Login</h2>
    <form @submit.prevent="login" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">Username</label>
        <input v-model="loginForm.username" type="text" required class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">Password</label>
        <input v-model="loginForm.password" type="password" required class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
      </div>
      <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded shadow font-medium">Login</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, checkAuth } from '../store'

const router = useRouter()
const loginForm = reactive({ username: '', password: '' })

const login = async () => {
  const res = await fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(loginForm)
  })
  const data = await res.json()
  if (res.ok) {
    showToast(data.message)
    loginForm.password = ''
    await checkAuth()
    router.push({ name: 'dashboard' })
  } else {
    showToast(data.error || "Login failed", true)
  }
}
</script>
