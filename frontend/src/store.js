import { reactive, ref } from 'vue'

export const user = reactive({ authenticated: false, username: null, avatar_url: null })
export const currentView = ref('login') // 'login' or 'register'
export const activeTab = ref('active') // 'active', 'completed', or 'calendar'

export const goals = ref([])
export const completedGoals = ref([])
export const calendarGoals = ref({})
export const initiatives = ref([])

export const toastState = reactive({ message: '', error: false })

export const showToast = (msg, isError = false) => {
  toastState.message = msg
  toastState.error = isError
  setTimeout(() => toastState.message = '', 4000)
}

export const fetchData = async () => {
  if (!user.authenticated) return
  const [goalsRes, initRes, compRes, calRes] = await Promise.all([
    fetch('/api/goals'),
    fetch('/api/initiatives'),
    fetch('/api/goals/completed'),
    fetch('/api/goals/calendar')
  ])
  if (goalsRes.ok) {
    const gData = await goalsRes.json()
    goals.value = gData.goals
  }
  if (initRes.ok) {
    const iData = await initRes.json()
    initiatives.value = iData.initiatives
  }
  if (compRes.ok) {
    const cData = await compRes.json()
    completedGoals.value = cData.goals
  }
  if (calRes.ok) {
    const calData = await calRes.json()
    calendarGoals.value = calData.calendar
  }
}

export const checkAuth = async () => {
  try {
    const res = await fetch('/api/me')
    const data = await res.json()
    user.authenticated = data.authenticated
    user.username = data.username
    user.avatar_url = data.avatar_url
    if (user.authenticated) {
      await fetchData()
    }
  } catch (err) {
    console.error("Auth check failed", err)
  }
}

export const logout = async () => {
  const res = await fetch('/api/logout', { method: 'POST' })
  if (res.ok) {
    user.authenticated = false
    user.username = null
    user.avatar_url = null
    goals.value = []
    initiatives.value = []
    completedGoals.value = []
    calendarGoals.value = {}
    showToast("Logged out successfully.")
  }
}
