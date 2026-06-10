<template>
  <TransitionRoot appear :show="isOpen" as="template">
    <Dialog as="div" @close="close" class="relative z-[100]">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4 text-center">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full max-w-2xl transform overflow-hidden rounded-[2.5rem] bg-white dark:bg-slate-800 p-10 text-left align-middle shadow-2xl transition-all border border-slate-100 dark:border-slate-700">
              
              <div class="relative">
                <!-- Progress bar -->
                <div class="absolute -top-4 left-0 w-full h-1 bg-slate-100 dark:bg-slate-700 rounded-full overflow-hidden">
                  <div 
                    class="h-full bg-brand-calm transition-all duration-500" 
                    :style="{ width: `${((currentStep + 1) / steps.length) * 100}%` }"
                  />
                </div>

                <div class="mt-4">
                  <div class="flex items-center gap-4 mb-6">
                    <div class="p-3 bg-brand-calm/10 rounded-2xl">
                      <component :is="steps[currentStep].icon" class="h-8 w-8 text-brand-calm" />
                    </div>
                    <div>
                      <DialogTitle as="h3" class="text-3xl font-black text-slate-900 dark:text-white tracking-tighter uppercase">
                        {{ steps[currentStep].title }}
                      </DialogTitle>
                      <p class="text-sm font-bold text-slate-400 uppercase tracking-widest mt-1">Step {{ currentStep + 1 }} of {{ steps.length }}</p>
                    </div>
                  </div>

                  <div class="space-y-4">
                    <p class="text-lg text-slate-600 dark:text-slate-300 leading-relaxed font-medium">
                      {{ steps[currentStep].content }}
                    </p>
                    
                    <div v-if="steps[currentStep].tips" class="bg-slate-50 dark:bg-slate-900/50 p-6 rounded-2xl border border-slate-100 dark:border-slate-700/50">
                      <h4 class="text-xs font-black text-brand-calm uppercase tracking-widest mb-3">Pro Tips</h4>
                      <ul class="space-y-2">
                        <li v-for="tip in steps[currentStep].tips" :key="tip" class="flex items-start gap-3 text-sm text-slate-500 dark:text-slate-400 font-medium">
                          <div class="mt-1.5 w-1.5 h-1.5 rounded-full bg-brand-calm shrink-0" />
                          {{ tip }}
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>

                <div class="mt-10 flex items-center justify-between">
                  <button 
                    @click="prev" 
                    v-if="currentStep > 0"
                    class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 font-black text-xs uppercase tracking-widest transition-colors"
                  >
                    Back
                  </button>
                  <div v-else />

                  <button
                    type="button"
                    class="inline-flex justify-center rounded-2xl border border-transparent bg-brand-calm px-8 py-4 text-sm font-black uppercase tracking-widest text-white hover:bg-brand-calm/90 focus:outline-none transition-all active:scale-95 shadow-xl shadow-brand-calm/20"
                    @click="next"
                  >
                    {{ currentStep === steps.length - 1 ? 'Start Winning' : 'Next Step' }}
                  </button>
                </div>
              </div>

            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from '@headlessui/vue'
import { 
  RocketLaunchIcon, 
  BoltIcon, 
  FireIcon, 
  UsersIcon, 
  TrophyIcon,
  SparklesIcon
} from '@heroicons/vue/24/outline'
import { user, completeOnboarding } from '../store'

const isOpen = computed(() => user.authenticated && !user.has_completed_onboarding)
const currentStep = ref(0)

const steps = [
  {
    title: "Welcome to Focus",
    icon: RocketLaunchIcon,
    content: "One-Minute Manager is designed for high-performers who win the day, one minute at a time. We've simplified goal tracking so you can spend less time planning and more time executing.",
    tips: ["Focus on 'Micro-Wins' to build massive momentum.", "Use the dashboard as your mission control."]
  },
  {
    title: "The One-Minute Goal",
    icon: SparklesIcon,
    content: "The core of our philosophy is the One-Minute Goal. If a task takes longer than a few minutes, it's too big. Break it down until it's actionable and small.",
    tips: ["Add a goal at the top of your dashboard anytime.", "Press 'Enter' to quickly add without clicking."]
  },
  {
    title: "AI Power-Ups",
    icon: BoltIcon,
    content: "Stuck on a big project? Use the 'AI Breakdown' feature on any goal. Our engine will suggest granular sub-tasks to help you get started instantly.",
    tips: ["Click the 'Bolt' icon next to any goal.", "Sub-tasks are automatically added to your list."]
  },
  {
    title: "Daily Habits",
    icon: FireIcon,
    content: "Consistency beats intensity. Use the Habits Tracker to build long-term routines. We'll track your streaks and push you to beat your personal bests.",
    tips: ["Track things like hydration, deep work, or reading.", "Streaks reset if you miss a day—keep the fire alive!"]
  },
  {
    title: "Shared Momentum",
    icon: UsersIcon,
    content: "Accountability is your secret weapon. Join the Focus Community to share your progress with others and stay inspired by the wins of your peers.",
    tips: ["Toggle 'Public Profile' in Settings to join.", "Cheer on others in the Community tab."]
  },
  {
    title: "Badges & Glory",
    icon: TrophyIcon,
    content: "Success should be celebrated. Earn unique badges for hitting milestones, maintaining streaks, and crushing your initiatives.",
    tips: ["Check the Analytics tab to see your trophy case.", "New badges are added regularly."]
  }
]

const next = () => {
  if (currentStep.value < steps.length - 1) {
    currentStep.value++
  } else {
    complete()
  }
}

const prev = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const complete = async () => {
  await completeOnboarding()
}

const close = () => {
  // Prevent closing unless finished or explicitly allowed
}
</script>
