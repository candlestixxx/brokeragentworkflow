import { registerSW } from 'virtual:pwa-register'
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

import { checkAuth, initTheme } from './store'
import { SplashScreen } from '@capacitor/splash-screen'
import { PushNotifications } from '@capacitor/push-notifications'
import { Capacitor } from '@capacitor/core'

const initPushNotifications = async () => {
  if (Capacitor.isNativePlatform()) {
    try {
      let permStatus = await PushNotifications.checkPermissions()
      if (permStatus.receive === 'prompt') {
        permStatus = await PushNotifications.requestPermissions()
      }
      if (permStatus.receive === 'granted') {
        await PushNotifications.register()
      }
    } catch (e) {
      console.warn('Push notifications not available:', e)
    }
  }
}

const initApp = async () => {
  initTheme()
  await checkAuth()

  const app = createApp(App)
  app.use(router)
  app.mount('#app')

  if (Capacitor.isNativePlatform()) {
    await SplashScreen.hide()
    await initPushNotifications()
  }
}

initApp()


registerSW({
  onOfflineReady() {
    console.log('App ready to work offline')
  }
})
