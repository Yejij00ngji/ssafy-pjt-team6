<template>
  <div>
    <p>카카오 로그인 중입니다. 잠시만 기다려 주세요...</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

const router = useRouter()
const accountStore = useAccountStore()

onMounted(async () => {
  // 1. URL에서 카카오가 보내준 'code' 추출
  const code = new URL(window.location.href).searchParams.get('code')
  
  if (code) {
    try {
      // 2. Django 백엔드의 KakaoLogin 뷰로 코드 전송
      // 주소는 Django urls.py에서 설정한 카카오 로그인 경로여야 합니다.
      const res = await axios.post(`${accountStore.API_URL}/accounts/kakao/`, {
        code: code
      })

      // 3. 토큰 및 유저 정보 저장
      accountStore.token = res.data.key
      accountStore.user = res.data.user
      // 유저 정보 저장 방식은 store의 구조에 따라 다를 수 있습니다.
      // 예: localStorage.setItem('token', res.data.key)
      
      console.log('카카오 로그인 성공!')
      router.push({ name: 'Home' }) 
    } catch (err) {
      console.error('카카오 로그인 실패:', err)
      alert('로그인에 실패했습니다.')
      router.push({ name: 'LoginView' })
    }
  }
})
</script>