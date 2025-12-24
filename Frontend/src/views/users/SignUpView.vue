<template>
  <div class="toss-container-narrow">
    <div class="signup-header">
      <h1 class="toss-title">회원가입</h1>
      <p class="toss-desc">Money:Bee에서 스마트한 자산 관리를 시작하세요</p>
    </div>

    <form @submit.prevent="handleSignUp" class="signup-form">
      <div class="form-section">
        <div class="input-group">
          <label for="email">이메일</label>
          <input type="email" id="email" v-model.trim="email" placeholder="user@example.com" class="toss-input" required>
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
      </div>

      <button 
        type="submit" 
        class="toss-btn-main w-full mt-8" 
        :disabled="!isFormValid"
        :class="{ 'btn-disabled': !isFormValid }"
      >
        가입하기
      </button>
    </form>
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
const is_mydata_agreed = ref(false);

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
    is_mydata_agreed: is_mydata_agreed.value,
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
/* style에 scoped를 추가하여 다른 컴포넌트와 스타일 충돌 방지 */
.toss-input, .toss-input-fixed {
  width: 100%;
  box-sizing: border-box;
  padding: 16px 20px;
  border-radius: 14px;
  background-color: var(--toss-gray-bg);
  border: 1.5px solid transparent;
  font-size: 16px;
  outline: none;
}

.toss-input:focus, .toss-input-fixed:focus {
  border-color: var(--toss-blue);
  background-color: #fff;
}

.input-success { border-color: #2ecc71 !important; background-color: #fff; }
.input-error { border-color: #f04452 !important; background-color: #fff; }

.password-wrapper { position: relative; width: 100%; }

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