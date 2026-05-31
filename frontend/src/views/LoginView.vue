<template>
  <div class="max-w-md mx-auto mt-12 animate-fade-in">
    <div class="bg-white dark:bg-slate-800 rounded-3xl shadow-2xl shadow-brand-calm/10 border border-slate-100 dark:border-slate-700 overflow-hidden">
      <div class="bg-brand-calm p-8 text-center relative overflow-hidden">
        <RocketLaunchIcon class="absolute -right-4 -top-4 h-32 w-32 text-white/10 -rotate-12" />
        <h2 class="text-3xl font-black text-white uppercase tracking-tighter">Welcome Back</h2>
        <p class="text-brand-accent font-bold text-sm mt-2 uppercase tracking-widest">Master your focus</p>
      </div>
      
      <form @submit.prevent="login" class="p-8 space-y-6">
        <div class="space-y-2">
          <label class="block text-xs font-black text-slate-500 dark:text-slate-400 uppercase tracking-widest ml-1">Username</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <UserIcon class="h-5 w-5 text-slate-400" />
            </div>
            <input 
              v-model="loginForm.username" 
              type="text" 
              required 
              class="block w-full pl-11 pr-4 py-3 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-2xl focus:ring-2 focus:ring-brand-calm outline-none transition-all dark:text-white font-medium"
              placeholder="Your handle"
            >
          </div>
        </div>

        <div class="space-y-2">
          <label class="block text-xs font-black text-slate-500 dark:text-slate-400 uppercase tracking-widest ml-1">Password</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <KeyIcon class="h-5 w-5 text-slate-400" />
            </div>
            <input 
              v-model="loginForm.password" 
              type="password" 
              required 
              class="block w-full pl-11 pr-4 py-3 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-2xl focus:ring-2 focus:ring-brand-calm outline-none transition-all dark:text-white font-medium"
              placeholder="••••••••"
            >
          </div>
        </div>

        <button 
          type="submit" 
          class="w-full bg-brand-calm hover:bg-brand-calm/90 text-white py-4 rounded-2xl font-black uppercase tracking-widest shadow-xl shadow-brand-calm/20 transition-all active:scale-95 transform"
        >
          Sign In
        </button>

        <p class="text-center text-sm font-bold text-slate-500 dark:text-slate-400">
          New here? 
          <router-link to="/register" class="text-brand-calm dark:text-brand-accent hover:underline">Create an account</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { RocketLaunchIcon, UserIcon, KeyIcon } from '@heroicons/vue/24/outline'
import { login as storeLogin, showToast, fetchData } from '../store'

const router = useRouter()
const loginForm = reactive({ username: '', password: '' })

const login = async () => {
  const success = await storeLogin(loginForm.username, loginForm.password)
  if (success) {
    await fetchData()
    router.push({ name: 'dashboard' })
  } else {
    showToast("Invalid credentials", true)
  }
}
</script>
