<template>
<div>
    <h1>로그인</h1>
    <form @submit.prevent="logIn">
      <label for="email">email: </label><br>
      <input type="text" id="email" v-model.trim="email">
      <br>
      <label for="password">password: </label><br>
      <input type="password" id="password" v-model.trim="password">
      <br>
      <input type="submit" value="LogIn">
      <hr>
      <div class="social-login-buttons">
        <button type="button" @click="googleLogin">Google Login</button>
        <hr>
        <button type="button" @click="kakaoLogin" style="background-color: #FEE500; border: none; padding: 5px 10px;">
          Kakao Login
        </button>
        <hr>
        <button type="button" @click="naverLogin" style="background-color: #03C75A; color: white; border: none; padding: 5px 10px;">
          Naver Login
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/accounts';
import { ref } from 'vue';

const accountStore = useAccountStore()

const email = ref(null)
const password = ref(null)

const logIn = () => {
  const payload = {
    email: email.value,
    password: password.value,
  }

  accountStore.logIn(payload)
}

const googleLogin = () => {
  const GOOGLE_CLIENT_ID = '59174330604-ovkfbnke8jb8e9fs3bbmrtf9jlfcuqlg.apps.googleusercontent.com'
  const REDIRECT_URI = 'http://localhost:5173/login/callback'
  
  const googleAuthUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${GOOGLE_CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=code&scope=email profile`
  
  window.location.href = googleAuthUrl
}

const kakaoLogin = () => {
  const KAKAO_CLIENT_ID = 'f296cf770fce87aa5f7c1d0d43cd33ad' // .env 혹은 직접 입력 (카카오 디벨로퍼스 REST API 키)
  const REDIRECT_URI = 'http://localhost:5173/login/kakao/callback' // 카카오 디벨로퍼스에 등록한 URI와 일치해야 함
  
  const kakaoAuthUrl = `https://kauth.kakao.com/oauth/authorize?client_id=${KAKAO_CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=code`
  
  window.location.href = kakaoAuthUrl
}

const naverLogin = () => {
  const NAVER_CLIENT_ID = 'NswjJzAdve_QTD730ovk' // 여기에 발급받은 Client ID 입력
  const REDIRECT_URI = 'http://localhost:5173/login/naver/callback'
  // 네이버는 보안을 위해 state 값이 필요합니다 (여기서는 간단히 random string 사용)
  const STATE = Math.random().toString(36).substring(3, 14)
  
  const naverAuthUrl = `https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=${NAVER_CLIENT_ID}&redirect_uri=${REDIRECT_URI}&state=${STATE}`
  
  window.location.href = naverAuthUrl
}
</script>

<style scoped>

</style>