<template>
  <div class="step-container">
    <div class="top-progress">
      <div class="bar" :style="{ width: (currentSubStep / 3) * 100 + '%' }"></div>
    </div>

    <div class="survey-content">
      <transition name="slide-fade" mode="out-in">
        <div v-if="currentSubStep === 1" :key="1" class="question-section">
          <h1 class="q-title">돈을 모으는 <br/>가장 큰 이유가 무엇인가요?</h1>
          <div class="option-list">
            <button v-for="opt in goals" :key="opt.val" @click="selectOption('goal', opt.val)" class="opt-btn">
              {{ opt.text }}
            </button>
          </div>
        </div>

        <div v-else-if="currentSubStep === 2" :key="2" class="question-section">
          <h1 class="q-title">얼마 동안 <br/>저축하실 계획인가요?</h1>
          <div class="option-list">
            <button v-for="opt in periods" :key="opt.val" @click="selectOption('period', opt.val)" class="opt-btn">
              {{ opt.text }}
            </button>
          </div>
        </div>

        <div v-else-if="currentSubStep === 3" :key="3" class="question-section">
          <h1 class="q-title">한 달에 얼마 정도 <br/>저축할 수 있나요?</h1>
          <div class="option-list">
            <button v-for="opt in amounts" :key="opt.val" @click="selectOption('amount', opt.val)" class="opt-btn">
              {{ opt.text }}
            </button>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['next'])
const currentSubStep = ref(1)

// 사용자 응답 저장용
const surveyResult = ref({
  goal: '',
  period: '',
  amount: ''
})

const goals = [
  { text: '💰 목돈 만들기', val: 'save' },
  { text: '🏠 주거비 마련', val: 'house' },
  { text: '🚗 차량/여행 등 소비', val: 'spend' },
  { text: '🛡️ 비상금 저축', val: 'emergency' }
]

const periods = [
  { text: '6개월 미만 (단기)', val: '6' },
  { text: '1년 정도', val: '12' },
  { text: '2년 이상 (장기)', val: '24' }
]

const amounts = [
  { text: '30만원 미만', val: 'under30' },
  { text: '30만원 ~ 100만원', val: 'under100' },
  { text: '100만원 이상', val: 'over100' }
]

const selectOption = (key, val) => {
  surveyResult.value[key] = val
  if (currentSubStep.value < 3) {
    currentSubStep.value++
  } else {
    // 모든 질문 완료 시 부모에게 데이터 전달
    emit('next', surveyResult.value)
  }
}
</script>

<style scoped>
.step-container { padding: 40px 24px; height: 100vh; display: flex; flex-direction: column; }

.top-progress { width: 100%; height: 4px; background: #f2f4f6; border-radius: 2px; margin-bottom: 40px; }
.top-progress .bar { height: 100%; background: #00ad7c; transition: width 0.3s ease; }

.q-title { font-size: 26px; font-weight: 700; line-height: 1.4; color: #191f28; margin-bottom: 40px; }

.option-list { display: flex; flex-direction: column; gap: 12px; }

.opt-btn {
  padding: 20px; text-align: left; background: #f9fafb; border: none; border-radius: 16px;
  font-size: 17px; font-weight: 600; color: #333d4b; cursor: pointer; transition: all 0.2s;
}

.opt-btn:active { background: #e5e8eb; transform: scale(0.98); }

/* 질문 전환 애니메이션 */
.slide-fade-enter-active, .slide-fade-leave-active { transition: all 0.3s ease; }
.slide-fade-enter-from { opacity: 0; transform: translateX(30px); }
.slide-fade-leave-to { opacity: 0; transform: translateX(-30px); }
</style>