<template>
  <div class="recommend-wrapper">
    <div class="toss-container-narrow">
      <transition name="slide-fade" mode="out-in">
        <component 
          :is="currentStepComponent" 
          :recommendations="recommendations"
          :cluster="userCluster"
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
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'
import StartStepItem from '@/components/recommendations/StartStepItem.vue'
import ResultsStepItem from '@/components/recommendations/ResultsStepItem.vue'
import LoadingItem from '@/components/recommendations/LoadingItem.vue'
import SurveyItem from '@/components/recommendations/SurveyItem.vue'

const accountStore = useAccountStore()

const currentStep = ref('intro') // intro -> survey(선택) -> loading -> result
const isMyDataAgreed = ref(false)
const recommendations = ref([]) // API 결과를 저장할 상태
const isLoadingError = ref(false)
const userCluster = ref(null)  // 클러스터 번호 저장용 상태
const API_URL = "http://localhost:8000" // 환경에 맞춰 수정


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
  const token = accountStore.token

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
    // ✅ 백엔드 응답에서 데이터 추출
    recommendations.value = response.data.recommendations
    userCluster.value = response.data.cluster // 추가 저장
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
  // 1. 초기 진입 단계 (Intro -> Survey or Loading)
  if (currentStep.value === 'intro') {
    isMyDataAgreed.value = data.agreed;

    if (data.agreed === false) {
      currentStep.value = 'survey';
      return; // 설문 단계로 이동 후 중단
    } else {
      currentStep.value = 'loading';
      // 여기서 바로 getRecommendations()를 호출하지 않고 
      // 아래 공통 호출 로직(3번)에서 처리하도록 흐름을 유도합니다.
    }
  }

  // 2. 설문 완료 단계 (Survey -> Loading)
  else if (currentStep.value === 'survey') {
    try {
      // 🛑 주의: 여기서 바로 loading으로 바꾸면 화면이 넘어가버립니다.
      // API 성공 후에 loading 상태를 유지하거나, 진입 시점에 바꾸는 것이 좋습니다.
      const payload = JSON.parse(JSON.stringify(data));
      console.log("전송할 순수 데이터:", payload);

      await axios.post(`${API_URL}/recommendations/survey/`, payload, { 
        headers: { Authorization: `Token ${accountStore.token}` }
      });

      currentStep.value = 'loading'; // 성공 시에 로딩 단계로 변경
    } catch (error) {
      console.error("서버 응답 에러 데이터:", error.response?.data); // 🔥 이 부분을 꼭 확인하세요!
      const errorMsg = error.response?.data?.error || "설문 처리 중 오류가 발생했습니다.";
      console.error("설문 저장 실패:", error);
      alert(errorMsg);
      currentStep.value = 'survey';
      return; // 에러 시 함수 종료
    }
  } 

  // 3. 공통 로딩 및 추천 결과 호출
  // 위 1, 2단계에서 currentStep이 'loading'이 되었다면 실행됩니다.
  if (currentStep.value === 'loading') {
    await getRecommendations();
  }
};

// 재시도 로직
const resetAll = () => {
  currentStep.value = 'intro'
  recommendations.value = []
  userCluster.value = null // 초기화
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