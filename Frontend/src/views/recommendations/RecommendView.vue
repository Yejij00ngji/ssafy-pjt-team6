<template>
  <div class="recommend-wrapper">
    <div class="toss-container-narrow">
      <transition name="slide-fade" mode="out-in">
        <component 
          :is="currentStepComponent" 
          :recommendations="recommendations"
          :cluster="userCluster"
          :is-my-data="isMyData"
          @next="handleNextStep"
          @retry="resetAll"
        />
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { useRecommendationStore } from '@/stores/recommendations'
import { useRoute } from 'vue-router'
import axios from 'axios'
import StartStepItem from '@/components/recommendations/StartStepItem.vue'
import ResultsStepItem from '@/components/recommendations/ResultsStepItem.vue'
import LoadingItem from '@/components/recommendations/LoadingItem.vue'
import SurveyItem from '@/components/recommendations/SurveyItem.vue'

const route = useRoute()

const accountStore = useAccountStore()
const recommendationStore = useRecommendationStore()

const currentStep = ref('intro') // intro -> survey(선택) -> loading -> result
const isMyData = ref(false)
const recommendations = ref([]) // API 결과를 저장할 상태
const userPersona = ref(null)

const isLoadingError = ref(false)
const API_URL = "http://localhost:8000" // 환경에 맞춰 수정


// 현재 단계에 따른 컴포넌트 계산
const currentStepComponent = computed(() => {
  switch (currentStep.value) {
    case 'intro': return StartStepItem
    case 'survey': return SurveyItem
    case 'loading': return LoadingItem
    case 'result': return ResultsStepItem
    default: return StartStepItem
  }
})

// 유저 상태(마이데이터 연동 여부) 조회
const fetchUserStatus = async () => {
  try {
    const response = await axios.get(`${accountStore.API_URL}/user/status/`, {
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    isMyData.value = response.data.is_mydata_linked
  } catch (error) {
    console.error("User status load failed:", error)
  }
}

// 실제 API 호출 함수
const getRecommendations = async () => {

  try {
    isLoadingError.value = false
    const response = await axios.get(`${accountStore.API_URL}/recommendations/`, {
      headers: { Authorization: `Token ${accountStore.token}` },
      timeout: 60000 // OpenAI 응답을 위해 넉넉히 설정
    })

    // 🔥 여기서 로그를 찍어보세요!
    console.log("✅ 백엔드 전체 응답 데이터:", response.data);
    console.log("📦 추천 리스트 추출:", response.data.recommendations);

    // 결과 저장 및 다음 단계 이동
    // ✅ 백엔드 응답에서 데이터 추출
    recommendations.value = response.data.recommendations || []
    userPersona.value = response.data.persona || null
    isMyData.value = response.data.is_mydata_linked || false

    recommendationStore.setRecommendations(recommendations.value)

    currentStep.value = 'result'
  } catch (error) {
    console.error("추천 데이터 로드 실패:", error)
    isLoadingError.value = true
    // 에러 발생 시 처리 (예: 경고창을 띄우고 다시 intro로 보내기 등)
    alert("추천 결과를 가져오는 데 실패했습니다. 다시 시도해 주세요.")
    currentStep.value = 'intro'
  }
}

// 단계 이동 핸들러
const handleNextStep = async (data) => {
  if (currentStep.value === 'intro') {
    if (data && data.agreed === false) {
      currentStep.value = 'survey'
      return
    } else {
      currentStep.value = 'loading'
    }
  } else if (currentStep.value === 'survey') {
    try {
      const payload = JSON.parse(JSON.stringify(data))
      await axios.post(`${accountStore.API_URL}/recommendations/survey/`, payload, { 
        headers: { Authorization: `Token ${accountStore.token}` }
      })
      currentStep.value = 'loading'
    } catch (error) {
      const errorMsg = error.response?.data?.error || "설문 처리 중 오류가 발생했습니다."
      alert(errorMsg)
      return
    }
  } 

  if (currentStep.value === 'loading') {
    await getRecommendations()
  }
}

// 초기화
const resetAll = () => {
  currentStep.value = 'intro'
  recommendations.value = []
  userPersona.value = null
  fetchUserStatus()
}

onMounted(() => {
  fetchUserStatus()
  if (route.query.step === 'survey') {
    currentStep.value = 'survey'
  }
})

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