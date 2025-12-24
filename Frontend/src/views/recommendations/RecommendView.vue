<template>
  <div class="recommend-wrapper">
    <div class="toss-container-narrow">
      <transition name="slide-fade" mode="out-in">
        <component 
          :is="currentStepComponent" 
          :recommendations="recommendations"
          :is-my-data="isMyDataAgreed"
          @next="handleNextStep"
          @retry="resetAll"
        />
      </transition>
    </div>
  </div>
</template>
<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import StartStepItem from '@/components/recommendations/StartStepItem.vue'
import ResultsStepItem from '@/components/recommendations/ResultsStepItem.vue'
import LoadingItem from '@/components/recommendations/LoadingItem.vue'
import SurveyItem from '@/components/recommendations/SurveyItem.vue'

const currentStep = ref('intro') // intro -> survey(선택) -> loading -> result
const isMyDataAgreed = ref(false)
const recommendations = ref([]) // API 결과를 저장할 상태
const isLoadingError = ref(false)

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

// 실제 API 호출 함수
const getRecommendations = async () => {
  const token = localStorage.getItem("token")
  const API_URL = "http://localhost:8000" // 환경에 맞춰 수정

  try {
    isLoadingError.value = false
    const response = await axios.get(`${API_URL}/recommendations/`, {
      headers: { Authorization: `Token ${token}` },
      timeout: 60000 // OpenAI 응답을 위해 넉넉히 설정
    })

    // 🔥 여기서 로그를 찍어보세요!
    console.log("✅ 백엔드 전체 응답 데이터:", response.data);
    console.log("📦 추천 리스트 추출:", response.data.recommendations);

    // 결과 저장 및 다음 단계 이동
    recommendations.value = response.data.recommendations
    currentStep.value = 'result'
  } catch (error) {
    console.error("추천 데이터 로드 실패:", error)
    isLoadingError.value = true
    // 에러 발생 시 처리 (예: 경고창을 띄우고 다시 intro로 보내기 등)
    alert("추천 결과를 가져오는 데 실패했습니다. 다시 시도해 주세요.")
    currentStep.value = 'intro'
  }
}

// 흐름 제어 로직 (수정됨)
const handleNextStep = async (data) => {
  if (currentStep.value === 'intro') {
    isMyDataAgreed.value = data.agreed
    // 마이데이터 동의 시 바로 로딩, 미동의 시 설문조사
    currentStep.value = data.agreed ? 'loading' : 'survey'
  } else if (currentStep.value === 'survey') {
    currentStep.value = 'loading'
  }

  // 로딩 단계에 진입했을 때 API 호출 시작
  if (currentStep.value === 'loading') {
    await getRecommendations()
  }
}

// 재시도 로직
const resetAll = () => {
  currentStep.value = 'intro'
  recommendations.value = []
}
</script>

<style scoped>
.recommend-wrapper {
  background-color: var(--toss-white); /* 혹은 var(--toss-gray-bg) */
  min-height: 100vh;
}
.toss-container-narrow {
  max-width: 480px; /* 모바일 우선 너비 */
  margin: 0 auto;
  padding: 60px 24px;
}
/* 슬라이드 애니메이션 */
.slide-fade-enter-active, .slide-fade-leave-active { transition: all 0.3s ease-out; }
.slide-fade-enter-from { opacity: 0; transform: translateY(10px); }
.slide-fade-leave-to { opacity: 0; transform: translateY(-10px); }
</style>