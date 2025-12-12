import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const API_URL = 'http://127.0.0.1:8000'

  const router = useRouter()
  
  const user = ref(null)
  const token = ref(null)

  const isLogin = computed(() => {
    return token.value ? true : false
  })

  const isMyData = ref(false)

  const subscriptions = ref(null)
  const cluster_info = ref(null)

  const signUp = async ({username,password1,password2}) => {
    const response = await axios.post(`${API_URL}/accounts/signup/`,{username,password1,password2})
    token.value = response.data.key

    router.push({ name: 'Home' })

    console.log(token.value)
  }

  const logIn = async ({username,password}) => {
    const response = await axios.post(`${API_URL}/accounts/login/`,{username,password})
    token.value = response.data.key

    router.push({ name: 'Home' })

    console.log(token.value)
  }

  const logOut = async () => {
    await axios.post(`${API_URL}/accounts/logout/`)
    token.value = null

    router.push({ name: 'LoginView' })

    console.log(token.value)
  }

  return { API_URL, user, isLogin, isMyData, subscriptions, cluster_info, signUp, logIn, logOut }
}, { persist: true })