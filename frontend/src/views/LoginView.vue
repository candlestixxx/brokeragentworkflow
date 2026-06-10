<template>
  <div class="min-h-[80vh] flex items-center justify-center p-4 animate-fade-in">
    <div class="max-w-md w-full relative group">
      <!-- Decorative background blur -->
      <div class="absolute -inset-1 bg-gradient-to-r from-brand-calm to-brand-accent rounded-[3rem] blur opacity-25 group-hover:opacity-40 transition duration-1000"></div>
      
      <div class="relative bg-white dark:bg-slate-800 rounded-[2.5rem] shadow-2xl border border-slate-100 dark:border-slate-700 overflow-hidden">
        <div class="p-10 md:p-12">
          <div class="flex flex-col items-center text-center mb-10">
            <div class="p-4 bg-brand-calm rounded-[2rem] mb-6 shadow-lg shadow-brand-calm/20">
              <RocketLaunchIcon class="h-10 w-10 text-white" />
            </div>
            <h2 class="text-4xl font-black text-slate-900 dark:text-white tracking-tighter uppercase mb-2">Welcome Back</h2>
            <p class="text-slate-500 dark:text-slate-400 font-medium leading-relaxed">Identity verification required to access mission control.</p>
          </div>

          <form @submit.prevent="handleLogin" class="space-y-6">
            <div class="space-y-4">
              <div>
                <label class="block text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-2 pl-1">Username</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none">
                    <UserIcon class="h-5 w-5 text-slate-300" />
                  </div>
                  <input 
                    v-model="loginForm.username" 
                    type="text" 
                    required 
                    placeholder="Enter your handle"
                    class="w-full pl-12 pr-6 py-4 bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-700 rounded-2xl focus:ring-2 focus:ring-brand-calm outline-none transition-all dark:text-white font-medium"
                  >
                </div>
              </div>

              <div>
                <label class="block text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-2 pl-1">Secret Key</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none">
                    <KeyIcon class="h-5 w-5 text-slate-300" />
                  </div>
                  <input 
                    v-model="loginForm.password" 
                    type="password" 
                    required 
                    placeholder="••••••••"
                    class="w-full pl-12 pr-6 py-4 bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-700 rounded-2xl focus:ring-2 focus:ring-brand-calm outline-none transition-all dark:text-white font-medium"
                  >
                </div>
              </div>
            </div>

            <button 
              type="submit" 
              class="w-full bg-slate-900 dark:bg-slate-700 hover:bg-black dark:hover:bg-slate-600 text-white py-5 rounded-2xl font-black text-xs uppercase tracking-widest shadow-xl transition-all active:scale-95 flex items-center justify-center gap-3"
            >
              Initialize System
              <ArrowRightIcon class="h-4 w-4" />
            </button>
          </form>

          <div class="mt-10 pt-10 border-t border-slate-50 dark:border-slate-700/50 text-center">
            <p class="text-sm font-medium text-slate-400">
              New here? 
              <router-link to="/register" class="text-brand-calm font-black uppercase tracking-widest text-xs hover:underline ml-2">Request Access</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { 
  RocketLaunchIcon, 
  UserIcon, 
  KeyIcon, 
  ArrowRightIcon 
} from '@heroicons/vue/24/outline'
import { login as storeLogin, showToast, fetchData } from '../store'

const router = useRouter()
const loginForm = reactive({
  username: '',
  password: ''
})

const handleLogin = async () => {
  const success = await storeLogin(loginForm.username, loginForm.password)
  if (success) {
    await fetchData()
    router.push({ name: 'dashboard' })
    showToast("System access granted.")
  } else {
    showToast("Identity verification failed.", true)
  }
}
</script>
