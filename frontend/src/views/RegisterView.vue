<template>
  <div class="max-w-md mx-auto bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 transition-colors">
    <h2 class="text-2xl font-semibold text-gray-800 dark:text-gray-100 border-b border-gray-100 dark:border-gray-700 pb-3 mb-4">Register</h2>
    <form @submit.prevent="register" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Username</label>
        <input v-model="registerForm.username" type="text" required class="mt-1 block w-full px-4 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Password</label>
        <input v-model="registerForm.password" type="password" required class="mt-1 block w-full px-4 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
      </div>
      <button type="submit" class="w-full bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded shadow font-medium transition-colors">Register</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from '../store'

const router = useRouter()
const registerForm = reactive({ username: '', password: '' })

const register = async () => {
  const res = await fetch('/api/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(registerForm)
  })
  const data = await res.json()
  if (res.ok) {
    showToast(data.message)
    registerForm.username = ''
    registerForm.password = ''
    router.push({ name: 'login' })
  } else {
    showToast(data.error || "Registration failed", true)
  }
}
</script>
