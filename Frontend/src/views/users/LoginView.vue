<template>
  <div class="auth-page">
    <div class="auth-container">
      <header class="auth-header">
        <h1 class="auth-title">로그인</h1>
        <p class="auth-description">
          비교를 통한 똑똑한 머니 불리기 <br />
          <strong>머니:비</strong> 에 다시 오신 것을 환영해요!
        </p>
      </header>

      <form @submit.prevent="logIn" class="auth-form">
        <div class="input-wrapper">
          <label for="email">이메일</label>
          <input 
            id="email"
            v-model="email" 
            type="email" 
            placeholder="example@email.com"
            class="toss-input"
            required
          />
        </div>

        <div class="input-wrapper">
          <label for="password">비밀번호</label>
          <input 
            id="password"
            v-model="password" 
            type="password" 
            placeholder="비밀번호를 입력하세요"
            class="toss-input"
            required
          />
        </div>

        <button 
          type="submit" 
          class="submit-btn" 
          :disabled="!isFormValid"
        >
          로그인
        </button>
      </form>

      <div class="divider">
        <span>또는 소셜 계정으로 로그인</span>
      </div>

      <div class="social-group">
        <button @click="kakaoLogin" class="social-btn kakao">
          <img src="@/assets/icons/kakao.svg" alt="카카오" class="social-icon" />
          <span>카카오로 시작하기</span>
        </button>
        
        <button @click="naverLogin" class="social-btn naver">
          <img src="@/assets/icons/naver.svg" alt="네이버" class="social-icon" />
          <span>네이버로 시작하기</span>
        </button>
        
        <button @click="googleLogin" class="social-btn google">
          <img src="@/assets/icons/google.svg" alt="구글" class="social-icon" />
          <span>구글로 시작하기</span>
        </button>
      </div>

      <footer class="auth-footer">
        <p>아직 회원이 아니신가요? <router-link to="/signup">회원가입</router-link></p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/accounts';
import { ref, computed } from 'vue';

const accountStore = useAccountStore()

const email = ref('')
const password = ref('')

// 버튼 활성화 로직
const isFormValid = computed(() => {
  return email.value?.length > 0 && password.value?.length > 0
})

const logIn = async () => {
  const payload = {
    email: email.value,
    password: password.value,
  }

  const response = await accountStore.logIn(payload)

  token.value = response.data.key
  localStorage.setItem("token", response.data.key)
}

const googleLogin = () => {
  const GOOGLE_CLIENT_ID = '59174330604-ovkfbnke8jb8e9fs3bbmrtf9jlfcuqlg.apps.googleusercontent.com'
  const REDIRECT_URI = 'http://localhost:5173/login/callback'
  const googleAuthUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${GOOGLE_CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=code&scope=email profile`
  window.location.href = googleAuthUrl
}

const kakaoLogin = () => {
  const KAKAO_CLIENT_ID = 'f296cf770fce87aa5f7c1d0d43cd33ad'
  const REDIRECT_URI = 'http://localhost:5173/login/kakao/callback'
  const kakaoAuthUrl = `https://kauth.kakao.com/oauth/authorize?client_id=${KAKAO_CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=code`
  window.location.href = kakaoAuthUrl
}

const naverLogin = () => {
  const NAVER_CLIENT_ID = 'NswjJzAdve_QTD730ovk'
  const REDIRECT_URI = 'http://localhost:5173/login/naver/callback'
  const STATE = Math.random().toString(36).substring(3, 14)
  const naverAuthUrl = `https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=${NAVER_CLIENT_ID}&redirect_uri=${REDIRECT_URI}&state=${STATE}`
  window.location.href = naverAuthUrl
}
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  padding: 20px;
}

.auth-container {
  width: 100%;
  max-width: 400px;
  background: white;
}

.auth-header {
  margin-bottom: 40px;
}

.auth-title {
  font-size: 28px;
  font-weight: 700;
  color: #191f28;
  margin-bottom: 12px;
}

.auth-description {
  font-size: 16px;
  color: #4e5968;
  line-height: 1.5;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-wrapper label {
  font-size: 14px;
  font-weight: 600;
  color: #333d4b;
}

.toss-input {
  padding: 16px;
  border-radius: 12px;
  border: 1px solid #e5e8eb;
  background-color: #f9fafb;
  font-size: 16px;
  transition: all 0.2s;
}

.toss-input:focus {
  outline: none;
  border-color: #00ad7c;
  background-color: white;
  box-shadow: 0 0 0 1px #00ad7c;
}

.submit-btn {
  padding: 16px;
  border-radius: 12px;
  border: none;
  background-color: #00ad7c;
  color: white;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.2s;
}

.submit-btn:disabled {
  background-color: #e5e8eb;
  cursor: not-allowed;
}

.divider {
  margin: 32px 0;
  text-align: center;
  position: relative;
}

.divider::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  height: 1px;
  background: #f2f4f6;
}

.divider span {
  position: relative;
  background: white;
  padding: 0 12px;
  font-size: 13px;
  color: #8b95a1;
}

.social-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}

.social-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 14px;
  border-radius: 12px;
  border: none;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  position: relative;
  transition: opacity 0.2s;
}

.social-btn:hover {
  opacity: 0.9;
}

/* 아이콘 공통 스타일 */
.social-icon {
  width: 18px;
  height: 18px;
  margin-right: 10px;
  object-fit: contain;
}

/* 1. 카카오 스타일 */
.kakao {
  background-color: #FEE500;
  color: #191919;
}

/* 2. 네이버 스타일: 배경이 초록일 때 아이콘을 하얗게 */
.naver {
  background-color: #03C75A;
  color: #FFFFFF;
}
/* SVG가 검은색 'N'일 경우 하얗게 반전시키는 매직 코드 */
.white-icon {
  filter: brightness(0) invert(1);
}

/* 3. 구글 스타일: 가이드에 따라 화이트 배경 권장 */
.google {
  background-color: #FFFFFF;
  color: #3C4043;
  border: 1px solid #E5E8EB;
}

.auth-footer {
  margin-top: 32px;
  text-align: center;
  font-size: 15px;
  color: #4e5968;
}

.auth-footer a {
  color: #00ad7c;
  text-decoration: none;
  font-weight: 600;
  margin-left: 8px;
}
</style>