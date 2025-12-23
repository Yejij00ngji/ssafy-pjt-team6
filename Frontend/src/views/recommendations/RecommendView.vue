<template>
  <div class="recommend-layout">
    <transition name="slide-fade" mode="out-in">
      <component 
        :is="currentStepComponent" 
        @next="handleNextStep"
        :is-my-data="isMyDataAgreed"
      />
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import StartStepItem from '@/components/recommendations/StartStepItem.vue'
import ResultsStepItem from '@/components/recommendations/ResultsStepItem.vue'
import LoadingItem from '@/components/recommendations/LoadingItem.vue'
import SurveyItem from '@/components/recommendations/SurveyItem.vue'

const currentStep = ref('intro') // intro -> survey(선택) -> loading -> result
const isMyDataAgreed = ref(false)

// 단계별 컴포넌트 매핑
const currentStepComponent = computed(() => {
  const steps = {
    intro: StartStepItem,
    survey: SurveyItem,
    loading: LoadingItem,
    result: ResultsStepItem
  }
  return steps[currentStep.value]
})

// 흐름 제어 로직
const handleNextStep = (data) => {
  if (currentStep.value === 'intro') {
    isMyDataAgreed.value = data.agreed
    currentStep.value = data.agreed ? 'loading' : 'survey'
  } else if (currentStep.value === 'survey') {
    currentStep.value = 'loading'
  } else if (currentStep.value === 'loading') {
    currentStep.value = 'result'
  }
}
</script>

<style scoped>
.recommend-layout {
  max-width: 500px;
  margin: 0 auto;
  min-height: 100vh;
  background-color: #fff;
}

/* 토스 스타일의 부드러운 슬라이드 전환 애니메이션 */
.slide-fade-enter-active, .slide-fade-leave-active {
  transition: all 0.4s ease-out;
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>