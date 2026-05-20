<template>
  <div v-if="currentView === 'login'" class="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
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

  <div v-if="currentView === 'register'" class="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
    <h2 class="text-2xl font-semibold text-gray-800 border-b border-gray-100 pb-3 mb-4">Register</h2>
    <form @submit.prevent="register" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">Username</label>
        <input v-model="registerForm.username" type="text" required class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">Password</label>
        <input v-model="registerForm.password" type="password" required class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
      </div>
      <button type="submit" class="w-full bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded shadow font-medium">Register</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { currentView, showToast, checkAuth } from '../store'

const loginForm = reactive({ username: '', password: '' })
const registerForm = reactive({ username: '', password: '' })

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
  } else {
    showToast(data.error || "Login failed", true)
  }
}

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
    currentView.value = 'login'
  } else {
    showToast(data.error || "Registration failed", true)
  }
}
</script>
