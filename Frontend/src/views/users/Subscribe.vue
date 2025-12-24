<template>
  <div class="auth-page"> <div class="auth-container"> <button class="back-link-btn" @click="router.back()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        돌아가기
      </button>

      <header class="auth-header">
        <h1 class="auth-title">상품 가입하기</h1>
        <p class="auth-description">
          선택하신 옵션을 확인하고 <br />
          가입하실 <strong>금액</strong>을 입력해 주세요.
        </p>
      </header>

      <div class="auth-form">
        <div class="input-wrapper">
          <label for="amounts">가입 금액 (원)</label>
          <div class="input-relative">
            <input 
              id="amounts"
              v-model.number="payload.amounts" 
              type="number" 
              placeholder="가입하실 금액을 입력하세요"
              class="toss-input"
            >
          </div>
        </div>

        <div class="info-summary-box">
          <div class="summary-row">
            <span class="label">선택 옵션 번호</span>
            <span class="value">{{ payload.product_option }}</span>
          </div>
          <div class="summary-row total">
            <span class="label">최종 가입 금액</span>
            <span class="value-highlight">{{ payload.amounts.toLocaleString() }} 원</span>
          </div>
        </div>

        <div class="button-group">
          <button 
            @click="onSubscribe" 
            class="submit-btn"
            :disabled="payload.amounts <= 0"
          >
            가입 완료
          </button>
          
          <!-- <button @click="$router.back()" class="cancel-text-btn">
            취소하기
          </button> -->
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useProductStore } from '@/stores/products'
import { ref } from 'vue'

const route = useRoute()
const router = useRouter()
const productStore = useProductStore()

const payload = ref({
  product_option: route.params.id,
  amounts: 0,
})

const onSubscribe = async () => {
  if (payload.value.amounts <= 0) {
    alert('가입 금액을 0원 이상 입력해 주세요.')
    return
  }

  if (confirm('정말로 이 상품에 가입하시겠습니까?')) {
    try {
      await productStore.subscribeProduct({
        product_option: payload.value.product_option,
        amounts: payload.value.amounts
      })
      alert('가입이 완료되었습니다!')
      router.push({ name: 'Profile' }) 
    } catch (err) {
      console.error(err)
      alert('가입 처리 중 오류가 발생했습니다.')
    }
  }
}
</script>

<style scoped>
/* 로그인 페이지(auth-page)와 동일한 기본 베이스 */
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 100px);
  padding: 20px;
  background-color: #FFFFFF;
}

.auth-container {
  width: 100%;
  max-width: 400px; /* 로그인 페이지와 동일한 너비 */
}

/* 상단 뒤로가기 버튼 */
.back-link-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  color: #8B95A1;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  margin-bottom: 32px;
}

/* 로그인 페이지 헤더 스타일 이식 */
.auth-header {
  margin-bottom: 40px;
}

.auth-title {
  font-size: 28px;
  font-weight: 700;
  color: #191F28;
  margin-bottom: 12px;
}

.auth-description {
  font-size: 16px;
  color: #4E5968;
  line-height: 1.5;
}

.auth-description strong {
  color: #3182F6;
}

/* 로그인 페이지 폼/인풋 스타일 이식 */
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
  color: #333D4B;
}

.toss-input {
  width: 100%;
  box-sizing: border-box;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid #E5E8EB;
  background-color: #F9FAFB;
  font-size: 16px;
  transition: all 0.2s;
}

.toss-input:focus {
  outline: none;
  border-color: #3182F6;
  background-color: #FFFFFF;
  box-shadow: 0 0 0 1px #3182F6;
}

/* 정보 요약 박스 (로그인 페이지의 정갈한 느낌 유지) */
.info-summary-box {
  background-color: #F9FAFB;
  border-radius: 16px;
  padding: 20px;
  margin-top: 8px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 14px;
}

.summary-row.total {
  margin-bottom: 0;
  padding-top: 10px;
  border-top: 1px solid #E5E8EB;
  margin-top: 10px;
}

.label { color: #8B95A1; }
.value { color: #191F28; font-weight: 600; }
.value-highlight { color: #3182F6; font-weight: 700; font-size: 16px; }

/* 로그인 페이지 버튼 스타일 이식 */
.button-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 16px;
}

.submit-btn {
  padding: 16px;
  border-radius: 12px;
  border: none;
  background-color: #3182F6; /* 토스 블루 */
  color: white;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.2s;
}

.submit-btn:disabled {
  background-color: #E5E8EB;
  cursor: not-allowed;
  color: #B0B8C1;
}

.submit-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.cancel-text-btn {
  padding: 12px;
  background: none;
  border: none;
  color: #8B95A1;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}

.cancel-text-btn:hover {
  color: #4E5968;
}

/* 숫자 화살표 제거 */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>