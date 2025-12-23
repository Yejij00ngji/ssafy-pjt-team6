<template>
  <div>
    <p>네이버 로그인 중입니다. 잠시만 기다려 주세요...</p>
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
  const urlParams = new URLSearchParams(window.location.search)
  const code = urlParams.get('code')
  const state = urlParams.get('state') // 네이버는 state도 함께 옵니다.
  
  if (code) {
    try {
      // Django 백엔드의 NaverLogin 뷰로 코드 전송
      const res = await axios.post(`${accountStore.API_URL}/accounts/naver/`, {
        code: code,
        state: state
      })

      // 토큰 및 유저 정보 저장 (기존 카카오 방식과 동일)
      accountStore.token = res.data.key
      accountStore.user = res.data.user
      
      console.log('네이버 로그인 성공!')
      router.push({ name: 'Home' }) 
    } catch (err) {
      console.error('네이버 로그인 실패:', err)
      alert('네이버 로그인에 실패했습니다.')
      router.push({ name: 'LoginView' })
    }
  }
})
</script>