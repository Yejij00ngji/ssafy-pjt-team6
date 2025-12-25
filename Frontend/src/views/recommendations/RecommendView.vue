<template>
  <div class="recommend-wrapper">
    <div class="toss-container-narrow">
      <transition name="slide-fade" mode="out-in">
        <component 
          :is="currentStepComponent" 
          :recommendations="recommendations"
          :cluster="userPersona"
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
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import StartStepItem from '@/components/recommendations/StartStepItem.vue'
import ResultsStepItem from '@/components/recommendations/ResultsStepItem.vue'
import LoadingItem from '@/components/recommendations/LoadingItem.vue'
import SurveyItem from '@/components/recommendations/SurveyItem.vue'
import NLPStepItem from '@/components/recommendations/NLPStepItem.vue'

const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()
const recommendationStore = useRecommendationStore()

const currentStep = ref('intro') // intro -> survey(선택) -> loading -> result
const isMyData = ref(false)
const recommendations = ref([]) // API 결과를 저장할 상태
const userPersona = ref(null)

// 설문 데이터를 임시로 저장할 객체
const temporarySurveyData = ref({})

const isLoadingError = ref(false)
const API_URL = "http://localhost:8000" // 환경에 맞춰 수정

// 현재 단계에 따른 컴포넌트 계산
const currentStepComponent = computed(() => {
  switch (currentStep.value) {
    case 'intro': return StartStepItem
    case 'survey': return SurveyItem
    case 'nlp': return NLPStepItem
    case 'loading': return LoadingItem
    case 'result': return ResultsStepItem
    default: return StartStepItem
  }
})

// 유저 상태(마이데이터 연동 여부) 조회
const fetchUserStatus = async () => {
  try {
    const response = await axios.get(`${accountStore.API_URL}/accounts/user/status/`, {
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    isMyData.value = response.data.is_mydata_linked
  } catch (error) {
    console.error("User status load failed:", error)
  }
}

// 인증 오류 처리: 로그아웃 하고 로그인 화면으로 이동
const handleAuthError = async () => {
  try {
    await accountStore.logOut()
  } catch (e) {
    // 안전하게 리다이렉트
  } finally {
    router.push({ name: 'Login' })
  }
}

// 실제 API 호출 함수
// 실제 API 호출 함수
const getRecommendations = async (userQueryText = "") => {
  if (!accountStore.token) {
    alert("로그인이 필요한 서비스입니다.")
    router.push({ name: 'Login' })
    return
  }

  try {
    // 마이데이터 연동 유저: GET /recommendations/?query=...
    if (isMyData.value || accountStore.isMyData) {
      const url = `${accountStore.API_URL}/recommendations/`
      const response = await axios.get(url, {
        headers: { Authorization: `Token ${accountStore.token}` },
        params: { query: userQueryText },
        timeout: 60000
      })

      recommendations.value = response.data.recommendations || []
      userPersona.value = response.data.persona || null
    } else {
      // 미동의자(설문): POST /recommendations/survey/
      const url = `${accountStore.API_URL}/recommendations/survey/`
      const payload = temporarySurveyData.value || {}
      const response = await axios.post(url, payload, {
        headers: { Authorization: `Token ${accountStore.token}`, 'Content-Type': 'application/json' },
        timeout: 60000
      })

      // 응답 처리: recommendations + persona + profile 스냅샷 반영
      recommendations.value = response.data.recommendations || []
      userPersona.value = {
        name: (response.data.cluster_name || '').trim() || null,
        label: response.data.cluster_label ?? null
      }

      // 서버가 보낸 profile 스냅샷이 있으면 Pinia 스토어에 즉시 반영
      if (response.data.profile) {
        accountStore.financial_profile = response.data.profile
        // 선택적: user 객체에 마이데이터 상태/라벨도 동기화
        if (accountStore.user) {
          accountStore.user.is_mydata_linked = accountStore.user.is_mydata_linked || false
        }
      }
    }

    recommendationStore.setRecommendations(recommendations.value)
    currentStep.value = 'result'
  } catch (error) {
    console.error("추천 데이터 로드 실패:", error)
    if (error.response?.status === 401) {
      await handleAuthError?.()
    } else {
      alert("추천 결과를 분석하는 중 오류가 발생했습니다.")
      currentStep.value = 'intro'
    }
  }
}

// 단계 이동 핸들러
const handleNextStep = async (data) => {
  if (currentStep.value === 'intro') {
    if (data && data.agreed === false) {
      currentStep.value = 'survey'
    } else {
      currentStep.value = 'nlp'
    }
  } else if (currentStep.value === 'survey') {
    temporarySurveyData.value = data
    currentStep.value = 'nlp'
  } else if (currentStep.value === 'nlp') {
    const userQueryText = data?.text || ""
    currentStep.value = 'loading'
    await getRecommendations(userQueryText)
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
  padding: 40px 24px;
}
/* 슬라이드 애니메이션 */
.slide-fade-enter-active, .slide-fade-leave-active { transition: all 0.3s ease-out; }
.slide-fade-enter-from { opacity: 0; transform: translateY(10px); }
.slide-fade-leave-to { opacity: 0; transform: translateY(-10px); }
</style>