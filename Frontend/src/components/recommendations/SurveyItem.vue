<template>
  <div class="step-container">
    <div class="top-progress">
      <div class="bar" :style="{ width: (currentSubStep / 5) * 100 + '%' }"></div>
    </div>

    <div class="survey-content">
      <transition name="slide-fade" mode="out-in">
        <div v-if="currentSubStep === 1" :key="1" class="question-section">
          <h1 class="q-title">연간 총 수입은 <br/>어느 정도이신가요?</h1>
          <div class="option-list">
            <button v-for="opt in incomeOptions" :key="opt.text" @click="selectOption('inc', opt.val)" class="opt-btn">
              {{ opt.text }}
            </button>
          </div>
        </div>

        <div v-else-if="currentSubStep === 2" :key="2" class="question-section">
          <h1 class="q-title">자산 중 투자 상품의 <br/>비중은 얼마나 되나요?</h1>
          <div class="option-list">
            <button v-for="opt in invOptions" :key="opt.text" @click="selectOption('inv_ratio', opt.val)" class="opt-btn">
              {{ opt.text }}
            </button>
          </div>
        </div>

        <div v-else-if="currentSubStep === 3" :key="3" class="question-section">
          <h1 class="q-title">지금 당장 현금화 가능한 <br/>자산은 어느 정도인가요?</h1>
          <div class="option-list">
            <button v-for="opt in liquidOptions" :key="opt.text" @click="selectOption('withdrawable_ratio', opt.val)" class="opt-btn">
              {{ opt.text }}
            </button>
          </div>
        </div>

        <div v-else-if="currentSubStep === 4" :key="4" class="question-section">
          <h1 class="q-title">작년과 비교했을 때 <br/>소비가 늘어나셨나요?</h1>
          <div class="option-list">
            <button v-for="opt in growthOptions" :key="opt.text" @click="selectOption('growth', opt.val)" class="opt-btn">
              {{ opt.text }}
            </button>
          </div>
        </div>

        <div v-else-if="currentSubStep === 5" :key="5" class="question-section">
          <h1 class="q-title">수입 대비 한 달 생활비 <br/>비중은 어느 정도인가요?</h1>
          <div class="option-list">
            <button v-for="opt in expOptions" :key="opt.text" @click="selectOption('expense_ratio', opt.val)" class="opt-btn">
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

// 백엔드 KMeans 로직에 직접적으로 사용될 수치 데이터 모음
const surveyResult = ref({
  annual_income_amt: 0,        // 소득 (inc 대신)
  invest_eval_amt: 0,          // 투자 자산 (inv_ratio 계산용 베이스)
  balance_amt: 0,              // 현재 잔액
  withdrawable_amt: 0,         // 출금 가능 금액 (withdrawable_ratio 계산용 베이스)
  expense_growth_rate: 1.0,    // 지출 변동률 (growth 대신)
  expense_to_income_ratio: 0.0 // 지출 비율 (expense_ratio 대신)
})

// 1. 소득 옵션 (대표 숫자로 변환)
const incomeOptions = [
  { text: '3,000만원 미만', val: 24000000 },
  { text: '3,000만원 ~ 5,000만원', val: 40000000 },
  { text: '5,000만원 ~ 8,000만원', val: 65000000 },
  { text: '8,000만원 이상', val: 100000000 }
]

// 2. 투자 비중 (KMeans 피처: inv_ratio)
const invOptions = [
  { text: '안전자산 위주 (5% 미만)', val: 0.05 },
  { text: '적절한 투자 (30% 내외)', val: 0.3 },
  { text: '공격적 투자 (70% 이상)', val: 0.75 }
]

// 3. 유동성 비중 (KMeans 피처: withdrawable_ratio)
const liquidOptions = [
  { text: '대부분 묶여있음 (20% 미만)', val: 0.15 },
  { text: '절반 정도 여유 (50% 내외)', val: 0.5 },
  { text: '언제든 인출 가능 (90% 이상)', val: 0.9 }
]

// 4. 지출 변동성 (KMeans 피처: growth)
const growthOptions = [
  { text: '많이 줄었음', val: 0.85 },
  { text: '비슷하게 유지', val: 1.05 },
  { text: '많이 늘었음', val: 1.35 }
]

// 5. 소비 비율 (KMeans 피처: expense_ratio)
const expOptions = [
  { text: '절약형 (30% 이하)', val: 0.25 },
  { text: '평범형 (50% 내외)', val: 0.5 },
  { text: '소비형 (80% 이상)', val: 0.85 }
]

// 옵션 선택 시 매핑 로직 (필드명 수정)
const selectOption = (key, val) => {
  if (key === 'inc') surveyResult.value.annual_income_amt = val;
  else if (key === 'inv_ratio') {
    // 총자산을 연봉의 1.5배로 가정한 예시 계산
    const totalAsset = surveyResult.value.annual_income_amt * 1.5;
    surveyResult.value.invest_eval_amt = Math.floor(totalAsset * val);
    surveyResult.value.balance_amt = Math.floor(totalAsset * (1 - val));
  }
  else if (key === 'withdrawable_ratio') {
    surveyResult.value.withdrawable_amt = Math.floor(surveyResult.value.balance_amt * val);
  }
  else if (key === 'growth') surveyResult.value.expense_growth_rate = val;
  else if (key === 'expense_ratio') surveyResult.value.expense_to_income_ratio = val;

  // 단계 이동 로직...
  if (currentSubStep.value < 5) currentSubStep.value++;
  else emit('next', surveyResult.value); // 이제 필드명이 모델과 동일한 객체가 전달됨
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

/* 추가 디자인 */
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
.slide-fade-enter-active, .slide-fade-leave-active { transition: all 0.3s ease; }
.slide-fade-enter-from { opacity: 0; transform: translateX(30px); }
.slide-fade-leave-to { opacity: 0; transform: translateX(-30px); }
</style>