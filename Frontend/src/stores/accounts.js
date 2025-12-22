import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useProductStore } from './products'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const API_URL = 'http://127.0.0.1:8000'

  const productStore = useProductStore()

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

  const cluster_info = ref(null)

  const signUp = async ({username,password1,password2,birth_date,is_mydata_agreed}) => {
    const response = await axios.post(`${API_URL}/accounts/signup/`,{username,password1,password2,birth_date,is_mydata_agreed})
//  const signUp = async ({username,password1,password2,birth_date,salary,possessions,is_mydata_agreed}) => {
//    const response = await axios.post(`${API_URL}/accounts/signup/`,{username,password1,password2,birth_date,salary,possessions,is_mydata_agreed})

    token.value = response.data.key
    user.value = response.data.user

    router.push({ name: 'Home' })
  }

  const logIn = async ({ email, password }) => {
    try {
      const response = await axios.post(`${API_URL}/accounts/login/`, { email, password })
      
      // 1. 토큰 먼저 저장
      token.value = response.data.key

      // 2. 토큰을 가지고 내 상세 정보(id, nickname 등) 가져오기
      // dj-rest-auth의 기본 유저 정보 엔드포인트는 /accounts/user/ 입니다.
      const userResponse = await axios.get(`${API_URL}/accounts/user/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      })

      // 3. 받아온 유저 정보를 저장 (이제 id가 들어옵니다!)
      user.value = userResponse.data
      console.log('로그인 성공 & 유저 정보 로드:', user.value)

      router.push({ name: 'Home' })
    } catch (err) {
      console.error('로그인 에러:', err)
      alert('아이디 또는 비밀번호를 확인해주세요.')
    }
  }

  const logOut = async () => {
    await axios.post(`${API_URL}/accounts/logout/`)
    
    token.value = null
    user.value = null
    productStore.subscriptions = null

    router.push({ name: 'LoginView' })
  }

  const updateProfile = async (payload) => {
    try {
      const res = await axios({
        method: 'patch',
        url: `${API_URL}/accounts/profile/`, // 백엔드 URL 경로에 맞게 수정
        data: payload,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      
      // 성공 시 스토어 데이터 업데이트 및 입력창 닫기
      user.value = res.data
      alert('수정되었습니다.')
      return true
    } catch (err) {
      console.error(err)
      alert('수정에 실패했습니다.')
      return false
    }
  }

  return { API_URL, token, user, isLogin, isMyData, cluster_info, signUp, logIn, logOut, updateProfile }
}, { persist: true })