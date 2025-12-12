import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const API_URL = 'http://127.0.0.1:8000'
  
  const user = ref(null)
  const token = ref(null)

  const isLogin = ref(false)
  const isMyData = ref(false)

  const subscriptions = ref(null)
  const cluster_info = ref(null)

  return { API_URL, user, isLogin, isMyData, subscriptions, cluster_info }
}, { persist: true })