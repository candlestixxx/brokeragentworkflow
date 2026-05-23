import { reactive, ref } from 'vue'

export interface SubGoal {
  id: number;
  description: string;
}

export interface Goal {
  id: number;
  description: string;
  subgoals?: SubGoal[];
  status?: string;
  parent_id?: number | null;
}

export interface Initiative {
  id: number;
  quarter: string;
  description: string;
}

export interface Habit {
  id: number;
  description: string;
  current_streak: number;
  highest_streak: number;
  last_completed_date: string | null;
}

export interface UserState {
  authenticated: boolean;
  username: string | null;
  avatar_url: string | null;
  notifications_enabled: boolean;
}

export const user = reactive<UserState>({ authenticated: false, username: null, avatar_url: null, notifications_enabled: true })

// Dark Mode State
export const isDarkMode = ref<boolean>(false)

export const initTheme = () => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDarkMode.value = true
    document.documentElement.classList.add('dark')
  } else {
    isDarkMode.value = false
    document.documentElement.classList.remove('dark')
  }
}

export const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

export const goals = ref<Goal[]>([])
export const completedGoals = ref<Goal[]>([])
export const calendarGoals = ref<Record<string, Goal[]>>({})
export const initiatives = ref<Initiative[]>([])
export const habits = ref<Habit[]>([])

export const toastState = reactive({ message: '', error: false })

export const showToast = (msg: string, isError: boolean = false) => {
  toastState.message = msg
  toastState.error = isError
  setTimeout(() => toastState.message = '', 4000)
}

export const fetchData = async () => {
  if (!user.authenticated) return
  const [goalsRes, initRes, compRes, calRes, habitsRes] = await Promise.all([
    fetch('/api/goals'),
    fetch('/api/initiatives'),
    fetch('/api/goals/completed'),
    fetch('/api/goals/calendar'),
    fetch('/api/habits')
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
  if (habitsRes.ok) {
    const hData = await habitsRes.json()
    habits.value = hData.habits
  }
}

export const checkAuth = async () => {
  try {
    const res = await fetch('/api/me')
    const data = await res.json()
    user.authenticated = data.authenticated
    user.username = data.username
    user.avatar_url = data.avatar_url
    user.notifications_enabled = data.notifications_enabled ?? true
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
    habits.value = []
    showToast("Logged out successfully.")
  }
}
