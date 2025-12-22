<template>
  <div>
    <p>구글 로그인 중입니다. 잠시만 기다려 주세요...</p>
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
  // 1. URL에서 구글이 보내준 'code' 추출
  const code = new URL(window.location.href).searchParams.get('code')
  
  if (code) {
    try {
      // 2. Django 백엔드의 GoogleLogin 뷰로 코드 전송
      const res = await axios.post(`${accountStore.API_URL}/accounts/google/token/`, {
        code: code
      })

      // 3. 응답으로 받은 토큰과 유저 정보 저장 (Pinia store 활용)
      accountStore.token = res.data.key
      accountStore.user = res.data.user
      
      console.log('로그인 성공!')
      router.push({ name: 'Home' }) // 메인 페이지로 이동
    } catch (err) {
      console.error('구글 로그인 실패:', err)
      alert('로그인에 실패했습니다.')
      router.push({ name: 'LoginView' })
    }
  }
})
</script>