<template>
<!-- <<<<<<< HEAD
  <div class="toss-detail-container">
    페르소나 정의 -->
    <!-- <section class="user-persona-card">
      <div class="persona-icon">{{ accountStore.financial_profile.icon }}</div>
      <div class="persona-info">
        <span class="persona-tag">{{ accountStore.financial_profile.tag }}</span>
        <h2 class="persona-title">{{ userName }}님은 <br/>{{ accountStore.financial_profile.title }}</h2>
        <p class="persona-desc">{{ accountStore.financial_profile.description }}</p> -->

  <div class="analysis-container">
    <section class="analysis-summary-grid">
      <div class="summary-card">
        <h3>나의 소비 DNA</h3>
        <div class="dna-item">
          <span class="dna-label">식비/배달</span>
          <div class="dna-bar-bg"><div class="dna-bar-fill" style="width: 80%"></div></div>
        </div>
        <p class="dna-nudge">"달콤한 간식에는 진심이시군요! 커피 할인 쿠폰을 주는 상품이 딱이에요."</p>
      </div>
      
      <div class="summary-card">
        <h3>평균 저축률 분석</h3>
        <div class="rate-comparison">
          <div class="my-rate">나 ({{ currentCluster.tag }}) <strong>22%</strong></div>
          <div class="avg-rate">또래 평균 <strong>12%</strong></div>
        </div>
        <div class="coach-mark">💡 <strong>꿀팁:</strong> 저축 여력이 높으시네요! 단기 상품보다는 금리가 높은 <strong>정기적금</strong>을 추천해요.</div>
      </div>
    </section>

    <section class="recommend-ranking-section">
      <h2 class="ranking-title">
        {{ userName }}님과 비슷한 성향의 분들은 <span class="blue-text">72%</span>나 가입했어요!
      </h2>

      <div class="ranking-cards">
        <div v-if="recommendations[1]" class="side-card rank-2">
          <span class="rank-badge">2위</span>
          <p class="bank-name">{{ recommendations[1].kor_co_nm }}</p>
          <h4 class="prod-name">{{ recommendations[1].fin_prdt_nm }}</h4>
          <div class="main-rate">{{ recommendations[1].intr_rate2 }}%</div>
          <button class="small-view-btn">자세히 보기</button>
        </div>

        <div v-if="recommendations[0]" class="main-card rank-1">
          <div class="crown-icon">👑 1위</div>
          <p class="bank-name">{{ recommendations[0].kor_co_nm }}</p>
          <h3 class="prod-name">{{ recommendations[0].fin_prdt_nm }}</h3>
          
          <div class="rate-display">
            <span class="big-rate">{{ recommendations[0].intr_rate2 }}%</span>
            <span class="rate-sub">최고 금리 (연)</span>
          </div>
          
          <div class="prod-tags">
            <span>{{ recommendations[0].save_trm }}개월 만기</span>
            <span>정액적립식</span>
          </div>

          <button class="apply-btn">가입하러 가기 →</button>
        </div>

        <div v-if="recommendations[2]" class="side-card rank-3">
          <span class="rank-badge">3위</span>
          <p class="bank-name">{{ recommendations[2].kor_co_nm }}</p>
          <h4 class="prod-name">{{ recommendations[2].fin_prdt_nm }}</h4>
          <div class="main-rate">{{ recommendations[2].intr_rate2 }}%</div>
          <button class="small-view-btn">자세히 보기</button>
        </div>
      </div>
    </section>
<!-- 
      <div class="button-group">
        <button class="toss-btn-blue" @click="goOptionApply(rec.product_option_id)">신청하기</button> -->
    <section v-if="recommendations[0]" class="ai-deep-analysis">
      <div class="analysis-header">
        <span class="sparkle-icon">✨</span>
        <h3>1위 상품, 왜 추천되었을까요?</h3>
      </div>

      <div class="analysis-grid">
        <div class="analysis-box reason-box">
          <p class="box-label">사용자님을 위한 AI 분석 포인트</p>
          <ul class="point-list">
            <li>✅ {{ recommendations[0].ai_analysis?.reason || '자축 여력이 높은 편이라 단기 고금리 상품에 유리해요.' }}</li>
            <li>✅ {{ recommendations[0].ai_analysis?.nudge || '유사 상품군 대비 금리가 0.5%p 더 높아요.' }}</li>
          </ul>
        </div>

        <div class="analysis-box group-box">
          <p class="box-label">유사 그룹 분석</p>
          <div class="group-text">
            {{ userName }}님과 비슷한 <strong>소득 수준 상위 30%</strong> 그룹의 
            <span class="yellow-text">72%</span>가 이 상품에 가입했어요!
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts';

const router = useRouter()
const accountStore = useAccountStore()

// 1. 클러스터 정보를 담을 반응형 변수 (초기 에러 방지용 빈 객체)
const currentCluster = ref({
  tag: '분석 중...',
  title: '',
  icon: '',
  description: ''
})

const props = defineProps({
  isMyData: Boolean,
  userName: { type: String, default: '사용자' },
  cluster: { type: [Number, String], default: 0 }, // 🟢 부모로부터 클러스터 번호 수신
  // 부모로부터 받은 실제 추천 데이터 리스트
  recommendations: {
    type: Array,
    default: () => []
  }
})

// 클러스터 정의
// clusterMapper.js 또는 ResultsStepItem.vue 내부
// const clusterMapper = {
//   0: {
//     title: "성실하게 모으는 저축왕",
//     tag: "안정저축형",
//     icon: "🌱",
//     description: "소득 대비 소비를 잘 관리하며 꾸준히 자산을 쌓아가고 계시네요!"
//   },
//   1: {
//     title: "현재의 행복이 중요한 욜로족",
//     tag: "소비중심형",
//     icon: "🌈",
//     description: "지출 비중이 다소 높지만, 지금부터 조금씩 미래를 위한 준비를 시작해볼까요?"
//   },
//   2: {
//     title: "현금을 든든하게 보유한 홀더",
//     tag: "현금보유형",
//     icon: "🏦",
//     description: "자산의 유동성이 매우 좋으시네요. 이제 더 높은 금리의 상품으로 눈을 돌릴 때입니다."
//   },
//   3: {
//     title: "여유로운 자산 관리 전문가",
//     tag: "자산관리형",
//     icon: "💼",
//     description: "높은 소득과 철저한 지출 관리로 가장 이상적인 금융 생활을 하고 계십니다."
//   },
//   4: {
//     title: "수익을 쫓는 공격적 투자자",
//     tag: "공격투자형",
//     icon: "🚀",
//     description: "자산의 대부분을 적극적으로 운용하시는군요. 고수익을 위한 최적의 상품을 추천합니다."
//   }
// };

// 🟢 클러스터 데이터 매핑
// const currentCluster = computed(() => {
//   return clusterMapper[props.cluster] || clusterMapper[0];
// })

// // 가장 점수가 높은 첫 번째 상품을 메인으로 노출
// const mainProduct = computed(() => {
//   return props.recommendations[0] || {}
// })

// const analysisSummary = computed(() => {
//   return props.isMyData 
//     ? '현재 보유하신 자산 현황과 지출 패턴을 고려하여 선정했습니다.'
//     : '답변하신 가입 목적과 선호 기간을 바탕으로 선정했습니다.'
// })

// const handleReAuth = () => {
//   console.log('Redirecting to MyData Auth...')
// }

const goOptionApply = (id) => {
  if (id) router.push({ name: 'Subscribe', params: { id: id } })
}
// 2. 백엔드의 getClusterInfo를 호출하는 함수
const fetchClusterData = async () => {
  try {
    const res = await axios.get(`${accountStore.API_URL}/이미_설정된_경로/getClusterInfo/`, {
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    if (res.data && res.data.tag) {
      currentCluster.value = res.data // 백엔드에서 준 {tag, title, icon...} 가 저장됨
    }
  } catch (err) {
    console.error('클러스터 정보 로드 실패:', err)
  }
}

onMounted(async () => {
  // 클러스터 정보 가져오기
  await fetchClusterData()
  // 기존 프로필 정보 로드
  await accountStore.getFinancialProfile()
})

// onMounted(async () => {
//   await Promise.all([
//     accountStore.getFinancialProfile()
//   ])
// })

// 추천 신뢰도에 따라 CSS 클래스를 반환하는 함수
const getConfidenceClass = (confidence) => {
  if (confidence >= 0.7) return 'conf-high';
  if (confidence >= 0.4) return 'conf-medium';
  return 'conf-low';
};
</script>

<style scoped>
.analysis-container { background-color: #fff9e6; padding: 20px; font-family: 'Pretendard', sans-serif; }

/* 상단 분석 카드 */
.analysis-summary-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 30px; }
.summary-card { background: #fff; padding: 20px; border-radius: 20px; border: 1px solid #fee500; }
.summary-card h3 { font-size: 16px; margin-bottom: 15px; color: #333; }
.dna-bar-bg { height: 10px; background: #eee; border-radius: 5px; margin: 10px 0; }
.dna-bar-fill { height: 100%; background: #ffcc00; border-radius: 5px; }

/* 랭킹 섹션 */
.ranking-title { text-align: center; font-size: 18px; margin-bottom: 24px; font-weight: 700; }
.blue-text { color: #3182f6; }
.ranking-cards { display: flex; align-items: flex-end; justify-content: center; gap: 10px; margin-bottom: 40px; }

/* 1위 카드 강조 */
.main-card { 
  background: #fff; border: 3px solid #ffcc00; padding: 30px 20px; border-radius: 24px;
  width: 200px; text-align: center; box-shadow: 0 10px 20px rgba(255, 204, 0, 0.2);
  z-index: 2;
}
.big-rate { font-size: 40px; font-weight: 800; color: #ff9900; display: block; }
.apply-btn { background: #332211; color: #fff; border: none; padding: 12px 20px; border-radius: 12px; margin-top: 20px; width: 100%; font-weight: 700; cursor: pointer;}

/* 2, 3위 카드 */
.side-card { 
  background: #fff; border: 1px solid #ddd; padding: 20px 15px; border-radius: 20px;
  width: 150px; text-align: center; height: 220px; opacity: 0.9;
}
.main-rate { font-size: 24px; font-weight: 700; color: #555; margin: 10px 0; }
.small-view-btn { background: #f2f4f6; border: none; padding: 8px 12px; border-radius: 10px; font-size: 12px; width: 100%; }

/* 하단 AI 분석 리포트 */
.ai-deep-analysis { background: #fff; border-radius: 24px; padding: 24px; border: 1px solid #eee; }
.analysis-header { display: flex; align-items: center; gap: 8px; margin-bottom: 20px; }
.analysis-grid { display: grid; grid-template-columns: 1.5fr 1fr; gap: 16px; }
.analysis-box { padding: 20px; border-radius: 18px; }
.reason-box { background: #f0f4ff; }
.group-box { background: #6333ff; color: #fff; }
.point-list { list-style: none; padding: 0; margin-top: 10px; }
.point-list li { margin-bottom: 8px; font-size: 14px; color: #333; }
.yellow-text { color: #ffeb3b; font-weight: 700; }
</style>