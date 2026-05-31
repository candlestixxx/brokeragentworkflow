<template>
  <div class="max-w-md mx-auto mt-12 animate-fade-in">
    <div class="bg-white dark:bg-slate-800 rounded-3xl shadow-2xl shadow-brand-calm/10 border border-slate-100 dark:border-slate-700 overflow-hidden">
      <div class="bg-brand-calm p-8 text-center relative overflow-hidden">
        <SparklesIcon class="absolute -right-4 -top-4 h-32 w-32 text-white/10 -rotate-12" />
        <h2 class="text-3xl font-black text-white uppercase tracking-tighter">Start Winning</h2>
        <p class="text-brand-accent font-bold text-sm mt-2 uppercase tracking-widest">Join the focus community</p>
      </div>
      
      <form @submit.prevent="register" class="p-8 space-y-6">
        <div class="space-y-2">
          <label class="block text-xs font-black text-slate-500 dark:text-slate-400 uppercase tracking-widest ml-1">Username</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <UserPlusIcon class="h-5 w-5 text-slate-400" />
            </div>
            <input 
              v-model="registerForm.username" 
              type="text" 
              required 
              class="block w-full pl-11 pr-4 py-3 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-2xl focus:ring-2 focus:ring-brand-calm outline-none transition-all dark:text-white font-medium"
              placeholder="Pick a handle"
            >
          </div>
        </div>

        <div class="space-y-2">
          <label class="block text-xs font-black text-slate-500 dark:text-slate-400 uppercase tracking-widest ml-1">Password</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <ShieldCheckIcon class="h-5 w-5 text-slate-400" />
            </div>
            <input 
              v-model="registerForm.password" 
              type="password" 
              required 
              class="block w-full pl-11 pr-4 py-3 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-2xl focus:ring-2 focus:ring-brand-calm outline-none transition-all dark:text-white font-medium"
              placeholder="Make it strong"
            >
          </div>
        </div>

        <button 
          type="submit" 
          class="w-full bg-brand-calm hover:bg-brand-calm/90 text-white py-4 rounded-2xl font-black uppercase tracking-widest shadow-xl shadow-brand-calm/20 transition-all active:scale-95 transform"
        >
          Create Account
        </button>

        <p class="text-center text-sm font-bold text-slate-500 dark:text-slate-400">
          Already a member? 
          <router-link to="/login" class="text-brand-calm dark:text-brand-accent hover:underline">Sign In</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { SparklesIcon, UserPlusIcon, ShieldCheckIcon } from '@heroicons/vue/24/outline'
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
    showToast("Registration successful.")
    router.push({ name: 'login' })
  } else {
    showToast(data.error || "Registration failed", true)
  }
}
</script>
