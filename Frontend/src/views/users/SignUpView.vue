<template>
  <div class="auth-page">
    <div class="auth-container">
      <header class="auth-header">
        <h1 class="auth-title">회원가입</h1>
        <p class="auth-description">
          비교를 통한 똑똑한 머니 불리기 <br />
          <strong>머니:비</strong> 에 오신 것을 환영해요!
        </p>
      </header>

      <form @submit.prevent="handleSignUp" class="auth-form">
        <div class="input-wrapper">
          <label for="email">이메일</label>
          <input 
            id="email"
            v-model="email" 
            type="email" 
            placeholder="user@example.com"
            class="toss-input"
            required
          />
        </div>

        <div class="input-group">
          <label for="password1">비밀번호</label>
          <div class="password-wrapper">
            <input 
              :type="showPwd ? 'text' : 'password'" 
              id="password1" 
              v-model.trim="password1" 
              placeholder="8자 이상 입력해주세요" 
              class="toss-input-fixed"
              :class="{ 'input-error': password1 && !isPasswordValid }"
            >
            <span class="material-symbols-outlined eye-icon" @click="showPwd = !showPwd">
              {{ showPwd ? 'visibility' : 'visibility_off' }}
            </span>
          </div>
          <p v-if="password1 && !isPasswordValid" class="helper-text error">비밀번호는 8자 이상이어야 합니다.</p>
        </div>

        <div class="input-group">
          <label for="password2">비밀번호 확인</label>
          <div class="password-wrapper">
            <input 
              :type="showPwd ? 'text' : 'password'" 
              id="password2" 
              v-model.trim="password2" 
              placeholder="비밀번호를 한번 더 입력해주세요" 
              class="toss-input-fixed"
              :class="{ 
                'input-success': isPasswordMatch && password2, 
                'input-error': !isPasswordMatch && password2 
              }"
            >
            <span v-if="password2" class="material-symbols-outlined status-icon" :class="isPasswordMatch ? 'success' : 'error'">
              {{ isPasswordMatch ? 'check_circle' : 'cancel' }}
            </span>
          </div>
          <p v-if="password2" class="helper-text" :class="isPasswordMatch ? 'success' : 'error'">
            {{ isPasswordMatch ? '비밀번호가 일치합니다.' : '비밀번호가 일치하지 않습니다.' }}
          </p>
        </div>

        <button 
          type="submit" 
          class="submit-btn" 
          :disabled="!isFormValid"
          :class="{ 'btn-disabled': !isFormValid }"
        >
          가입하기
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/accounts';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const accountStore = useAccountStore();
const router = useRouter();

const showPwd = ref(false);
const email = ref('');
const password1 = ref('');
const password2 = ref('');
const is_mydata_linked = ref(false);

// 1. 비밀번호 유효성: 8자 이상
const isPasswordValid = computed(() => password1.value.length >= 8);

// 2. 일치 여부: 유효한 비번이면서 두 값이 같을 때
const isPasswordMatch = computed(() => {
  return isPasswordValid.value && password1.value === password2.value;
});

// 3. 전체 폼 유효성: 이메일(@포함) + 비번 일치
const isFormValid = computed(() => {
  return email.value.includes('@') && isPasswordMatch.value;
});

const handleSignUp = async () => {
  if (!isFormValid.value) return;

  // Postman 성공 데이터 규격과 100% 일치시킴
  const payload = {
    email: email.value,      // 이메일을 username으로
    password1: password1.value,
    password2: password2.value,
    // birth_date: null,           // 시리얼라이저 필드 존재 시 null이라도 전송
    is_mydata_linked: is_mydata_linked.value,
  };

  try {
    console.log('전송 데이터:', payload);
    await accountStore.signUp(payload);
    alert('회원가입이 완료되었습니다!');
    router.push({ name: 'Home' });
  } catch (err) {
    // 디버깅의 핵심: 서버가 준 에러 내용을 낱낱이 파악
    console.error('서버 에러 응답:', err.response?.data);
    
    if (err.response?.data) {
      const errors = err.response.data;
      // 특정 필드 에러가 있다면 첫 번째 메시지 출력
      const firstError = Object.values(errors)[0];
      alert(`가입 실패: ${Array.isArray(firstError) ? firstError[0] : firstError}`);
    } else {
      alert('가입 중 알 수 없는 오류가 발생했습니다.');
    }
  }
};
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

/* 1. 입력창 그룹 간격 유지 */
.input-group {
  display: flex;
  flex-direction: column;
  gap: 10px; /* 라벨과 인풋 사이 간격 */
}

/* 2. 비밀번호 입력창 감싸는 컨테이너 (아이콘 배치의 기준) */
.password-wrapper {
  position: relative; /* 중요: 아이콘이 이 안에서 절대 위치를 잡게 함 */
  width: 100%;
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

/* 3. 인풋 스타일 통일 (이메일 필드와 동일하게) */
.toss-input, .toss-input-fixed {
  width: 100%;
  padding: 16px;
  padding-right: 48px; /* 아이콘과 텍스트가 겹치지 않게 여백 확보 */
  border-radius: 12px;
  border: 1px solid #e5e8eb;
  background-color: #f9fafb;
  font-size: 16px;
  transition: all 0.2s ease;
  box-sizing: border-box; /* 패딩이 너비에 영향을 주지 않도록 */
}

/* 4. Focus 시 디자인 (머니비 메인 컬러 적용) */
.toss-input:focus, .toss-input-fixed:focus {
  outline: none;
  border-color: #00ad7c;
  background-color: white;
  box-shadow: 0 0 0 1px #00ad7c;
}

/* 5. 에러 상태 시 디자인 */
.input-error {
  border-color: #f04452 !important;
  box-shadow: 0 0 0 1px #f04452 !important;
}

/* 6. 아이콘 위치 및 디자인 세밀 조정 */
.eye-icon, .status-icon {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #8b95a1; /* 토스 그레이 컬러 */
  cursor: pointer;
  z-index: 10;
  user-select: none; /* 아이콘 클릭 시 텍스트 드래그 방지 */
}

/* 7. 라벨 스타일 (폰트 가독성 상향) */
.input-group label, .input-wrapper label {
  font-size: 14px;
  font-weight: 600;
  color: #4e5968;
  margin-left: 2px;
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

.eye-icon {
  position: absolute; right: 16px; top: 50%; transform: translateY(-50%);
  color: var(--toss-text-tertiary); cursor: pointer; z-index: 10;
}

.status-icon {
  position: absolute; right: 16px; top: 50%; transform: translateY(-50%);
  font-size: 20px;
}
.status-icon.success { color: #2ecc71; }
.status-icon.error { color: #f04452; }

.helper-text { font-size: 13px; margin-top: 6px; margin-left: 4px; font-weight: 500; }
.helper-text.success { color: #2ecc71; }
.helper-text.error { color: #f04452; }

.btn-disabled {
  background-color: #d1d6db !important;
  color: #fff !important;
  cursor: not-allowed !important;
  opacity: 1 !important;
}
</style>