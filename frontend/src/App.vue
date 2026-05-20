<template>
  <div class="bg-gray-50 min-h-screen font-sans text-gray-900">
    <header class="bg-white shadow-sm sticky top-0 z-10">
      <nav class="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
        <h1 class="text-xl font-bold text-gray-800 tracking-tight">One-Minute Manager</h1>
        <div v-if="user.authenticated" class="flex items-center">
          <span class="text-gray-600 mr-4">Hello, {{ user.username }}</span>
          <button @click="logout" class="text-red-600 hover:text-red-800 transition duration-150 font-medium">Logout</button>
        </div>
        <div v-else>
          <button @click="currentView = 'login'" :class="{'underline': currentView === 'login'}" class="text-blue-600 hover:text-blue-800 mr-4">Login</button>
          <button @click="currentView = 'register'" :class="{'underline': currentView === 'register'}" class="text-blue-600 hover:text-blue-800">Register</button>
        </div>
      </nav>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-8">
      <!-- Flash Messages equivalent (Toast) -->
      <div v-if="toastMessage" class="mb-6 space-y-2">
        <div :class="toastError ? 'bg-red-100 border-red-500 text-red-700' : 'bg-green-100 border-green-500 text-green-700'" class="border-l-4 p-4 rounded shadow-sm flex justify-between">
          <p>{{ toastMessage }}</p>
          <button @click="toastMessage = ''" class="font-bold">&times;</button>
        </div>
      </div>

      <!-- UNAUTHENTICATED VIEW -->
      <div v-if="!user.authenticated">
        <!-- Login View -->
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

        <!-- Register View -->
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
      </div>

      <!-- AUTHENTICATED DASHBOARD VIEW -->
      <div v-else>
        <h2 class="text-3xl font-bold text-gray-800 mb-8 text-center">One-Minute Manager Dashboard</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Daily Goals Column -->
          <div class="flex flex-col h-full">
            <section class="bg-white rounded-lg shadow-md p-6 mb-8 flex-1">
              <h2 class="text-2xl font-semibold text-gray-800 border-b border-gray-100 pb-3 mb-4">Daily One-Minute Goals</h2>
              <ul class="divide-y divide-gray-100">
                <li v-for="goal in goals" :key="goal.id" class="py-4 flex flex-col group">
                  <div class="flex justify-between items-center w-full">
                    <span class="text-gray-700">
                      <span class="text-gray-400 font-mono text-sm mr-2">[{{ goal.id }}]</span>
                      {{ goal.description }}
                    </span>
                    <div>
                      <button @click="addSubGoalForm(goal.id)" class="bg-gray-200 hover:bg-gray-300 text-gray-700 px-3 py-1 rounded shadow transition duration-150 font-medium mr-2 text-sm">
                        + Sub-goal
                      </button>
                      <button @click="completeGoal(goal.id)" class="bg-green-500 hover:bg-green-600 text-white px-4 py-1 rounded shadow transition duration-150 font-medium text-sm">
                        Complete
                      </button>
                    </div>
                  </div>

                  <!-- Subgoals List -->
                  <ul v-if="goal.subgoals && goal.subgoals.length > 0" class="mt-2 ml-6 border-l-2 border-gray-200 pl-4">
                    <li v-for="sub in goal.subgoals" :key="sub.id" class="py-2 flex justify-between items-center">
                      <span class="text-gray-600 text-sm">
                        <span class="text-gray-400 font-mono text-xs mr-2">[{{ sub.id }}]</span>
                        {{ sub.description }}
                      </span>
                      <button @click="completeGoal(sub.id)" class="bg-green-400 hover:bg-green-500 text-white px-3 py-1 rounded shadow transition duration-150 font-medium text-xs">
                        Complete
                      </button>
                    </li>
                  </ul>

                  <!-- Add Subgoal Form -->
                  <form v-if="activeSubGoalParent === goal.id" @submit.prevent="submitSubGoal(goal.id)" class="mt-3 ml-6 flex gap-2">
                    <input v-model="newSubGoalDescription" type="text" placeholder="Sub-goal description..." required autofocus class="flex-1 px-3 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500">
                    <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-1 rounded shadow font-medium text-sm">Save</button>
                    <button type="button" @click="activeSubGoalParent = null" class="text-gray-500 hover:text-gray-700 px-2 text-sm">Cancel</button>
                  </form>
                </li>
                <li v-if="goals.length === 0" class="py-4 text-gray-500 italic text-center">No pending goals. Great job!</li>
              </ul>

              <form @submit.prevent="submitGoal" class="mt-6 flex gap-3">
                <input v-model="newGoal" type="text" placeholder="New daily goal..." required class="flex-1 px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded shadow font-medium">Add Goal</button>
              </form>
            </section>
          </div>

          <!-- Quarterly Initiatives Column -->
          <div class="flex flex-col h-full">
            <section class="bg-white rounded-lg shadow-md p-6 mb-8 flex-1">
              <h2 class="text-2xl font-semibold text-gray-800 border-b border-gray-100 pb-3 mb-4">Quarterly Initiatives</h2>
              <ul class="divide-y divide-gray-100">
                <li v-for="initiative in initiatives" :key="initiative.id" class="py-4 flex justify-between items-center group">
                  <span class="text-gray-700">
                    <span class="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded font-semibold mr-2">{{ initiative.quarter }}</span>
                    {{ initiative.description }}
                  </span>
                  <button @click="completeInitiative(initiative.id)" class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded shadow transition duration-150 font-medium">
                    Complete
                  </button>
                </li>
                <li v-if="initiatives.length === 0" class="py-4 text-gray-500 italic text-center">No pending initiatives. Time to plan!</li>
              </ul>

              <form @submit.prevent="addInitiative" class="mt-6 flex flex-col gap-3">
                <div class="flex gap-3">
                  <select v-model="newInitiative.quarter" required class="w-1/3 px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white">
                    <option value="" disabled>Quarter</option>
                    <option value="Q1">Q1</option>
                    <option value="Q2">Q2</option>
                    <option value="Q3">Q3</option>
                    <option value="Q4">Q4</option>
                  </select>
                  <input v-model="newInitiative.description" type="text" placeholder="Initiative description..." required class="flex-1 px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>
                <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded shadow font-medium">Add Initiative</button>
              </form>
            </section>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { io } from 'socket.io-client'

const socket = io() // Automatically connects to the host that serves the page

const user = reactive({ authenticated: false, username: null })
const currentView = ref('login') // 'login' or 'register'

const loginForm = reactive({ username: '', password: '' })
const registerForm = reactive({ username: '', password: '' })

const toastMessage = ref('')
const toastError = ref(false)

const goals = ref([])
const newGoal = ref('')

const initiatives = ref([])
const newInitiative = reactive({ quarter: '', description: '' })

const activeSubGoalParent = ref(null)
const newSubGoalDescription = ref('')

const showToast = (msg, isError=false) => {
  toastMessage.value = msg
  toastError.value = isError
  setTimeout(() => toastMessage.value = '', 4000)
}

const checkAuth = async () => {
  try {
    const res = await fetch('/api/me')
    const data = await res.json()
    user.authenticated = data.authenticated
    user.username = data.username
    if (user.authenticated) {
      await fetchData()
    }
  } catch (err) {
    console.error("Auth check failed", err)
  }
}

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

const logout = async () => {
  const res = await fetch('/api/logout', { method: 'POST' })
  if (res.ok) {
    user.authenticated = false
    user.username = null
    goals.value = []
    initiatives.value = []
    showToast("Logged out successfully.")
  }
}

const fetchData = async () => {
  if (!user.authenticated) return
  const [goalsRes, initRes] = await Promise.all([
    fetch('/api/goals'),
    fetch('/api/initiatives')
  ])
  if (goalsRes.ok) {
    const gData = await goalsRes.json()
    goals.value = gData.goals
  }
  if (initRes.ok) {
    const iData = await initRes.json()
    initiatives.value = iData.initiatives
  }
}

const submitGoal = async () => {
  const res = await fetch('/api/goals', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ description: newGoal.value })
  })
  if (res.ok) {
    newGoal.value = ''
    showToast("Goal added.")
  }
}

const addSubGoalForm = (parentId) => {
  activeSubGoalParent.value = parentId
  newSubGoalDescription.value = ''
}

const submitSubGoal = async (parentId) => {
  const res = await fetch('/api/goals', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ description: newSubGoalDescription.value, parent_id: parentId })
  })
  if (res.ok) {
    activeSubGoalParent.value = null
    newSubGoalDescription.value = ''
    showToast("Sub-goal added.")
  }
}

const completeGoal = async (id) => {
  const res = await fetch(`/api/goals/${id}/complete`, { method: 'POST' })
  if (res.ok) {
    showToast("Goal completed! Excellent work.")
  }
}

const addInitiative = async () => {
  const res = await fetch('/api/initiatives', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(newInitiative)
  })
  if (res.ok) {
    newInitiative.quarter = ''
    newInitiative.description = ''
    showToast("Initiative added.")
  }
}

const completeInitiative = async (id) => {
  const res = await fetch(`/api/initiatives/${id}/complete`, { method: 'POST' })
  if (res.ok) {
    showToast("Initiative completed!")
  }
}

onMounted(() => {
  checkAuth()

  socket.on('data_updated', (data) => {
    console.log("Real-time update received:", data)
    // Whenever a data_updated event is received, re-fetch all data.
    fetchData()
  })
})
</script>
