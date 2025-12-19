import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const API_URL = 'http://127.0.0.1:8000'

  const router = useRouter()
  
  const token = ref(null)
  const user = ref(null)

  const isLogin = computed(() => {
    return token.value ? true : false
  })

  const isMyData = computed(() => {
    if (user.value){
      return user.value.is_mydata_agreed ? true : false
    }
    
    else {
      return false
    }
  })

  const subscriptions = ref(null)
  const cluster_info = ref(null)

  const signUp = async ({username,password1,password2,birth_date,salary,possessions,is_mydata_agreed}) => {
    const response = await axios.post(`${API_URL}/accounts/signup/`,{username,password1,password2,birth_date,salary,possessions,is_mydata_agreed})

    token.value = response.data.key
    user.value = response.data.user

    router.push({ name: 'Home' })
  }

  const logIn = async ({username,password}) => {
    const response = await axios.post(`${API_URL}/accounts/login/`,{username,password})

    token.value = response.data.key
    user.value = response.data.user

    router.push({ name: 'Home' })
  }

  const logOut = async () => {
    await axios.post(`${API_URL}/accounts/logout/`)
    
    token.value = null
    user.value = null

    router.push({ name: 'LoginView' })
  }

  return { API_URL, token, user, isLogin, isMyData, subscriptions, cluster_info, signUp, logIn, logOut }
}, { persist: true })