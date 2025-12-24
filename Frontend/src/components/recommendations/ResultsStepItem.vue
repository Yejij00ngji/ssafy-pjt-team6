<template>
  <div class="toss-detail-container">
    <!-- 페르소나 정의 -->
    <section class="user-persona-card">
      <div class="persona-icon">{{ accountStore.financial_profile.icon }}</div>
      <div class="persona-info">
        <span class="persona-tag">{{ accountStore.financial_profile.tag }}</span>
        <h2 class="persona-title">{{ userName }}님은 <br/>{{ accountStore.financial_profile.title }}</h2>
        <p class="persona-desc">{{ accountStore.financial_profile.description }}</p>
      </div>
    </section>

    <div v-for="(rec, index) in recommendations" :key="index" class="product-full-section">
      
      <header class="product-header">
        <p class="bank-label">{{ rec.bank_name }} 〉</p>
        <h2 class="product-title">{{ rec.product_name }}</h2>
        
        <div class="rate-highlight-box">
          <span class="rate-label">최대 금리</span>
          <span class="rate-value">연 {{ rec.intr_rate2 }}%</span>
        </div>
      </header>

      <div class="summary-info-bar">
        <div class="info-item">
          <span class="label">가입 기간</span>
          <span class="value">{{ rec.save_trm }}개월</span>
        </div>
        <div class="info-item">
          <span class="label">적합도</span>
          <span class="value accent">{{ (rec.score * 100).toFixed(0) }}점</span>
        </div>
      </div>

      <div class="button-group">
        <button class="toss-btn-blue" @click="goOptionApply(rec.product_option_id)">신청하기</button>
      </div>

      <hr class="toss-divider" />

      <section class="ai-analysis-section">
        <h3 class="section-title">AI가 분석한 추천 이유</h3>
        
        <div class="analysis-list">
          <div class="analysis-item">
            <div class="icon">✨</div>
            <div class="item-text">
              <strong>맞춤형 혜택 분석</strong>
              <p>{{ rec.reason }}</p>
            </div>
          </div>

          <div class="analysis-item">
            <div class="icon">📊</div>
            <div class="item-text">
              <strong>유사 그룹 선호도</strong>
              <p>사용자님과 유사한 금융 성향을 가진 분들이 가장 많이 가입한 상품이에요.</p>
            </div>
          </div>

          <div class="analysis-item">
            <div class="icon">🔒</div>
            <div class="item-text">
              <strong>안정성 및 신뢰도</strong>
              <p>원금 보장이 확실하고 신뢰도 지표가 매우 우수한 상품입니다.</p>
            </div>
          </div>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts';

const router = useRouter()
const accountStore = useAccountStore()

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

onMounted(async () => {
  await Promise.all([
    accountStore.getFinancialProfile()
  ])
})
</script>

<style scoped>
.toss-detail-container { background-color: #fff; padding-bottom: 40px; }
.product-full-section { padding: 48px 24px; border-bottom: 10px solid #f2f4f6; }

/* 헤더: 텍스트 위계 강조 */
.product-header { margin-bottom: 32px; }
.bank-label { font-size: 15px; color: #6b7684; margin-bottom: 8px; font-weight: 500; }
.product-title { font-size: 28px; font-weight: 700; color: #191f28; margin-bottom: 16px; line-height: 1.3; }

/* 금리 표시: 상품명 아래 단에 색상 차별화 */
.rate-highlight-box { display: flex; align-items: baseline; gap: 8px; }
.rate-label { font-size: 17px; color: #4e5968; font-weight: 500; }
.rate-value { font-size: 24px; font-weight: 700; color: #3182f6; } /* 토스 블루 컬러 적용 */

/* 요약 바 */
.summary-info-bar { display: flex; gap: 32px; margin-bottom: 32px; padding: 4px 0; }
.info-item { display: flex; flex-direction: column; gap: 4px; }
.info-item .label { font-size: 14px; color: #8b95a1; }
.info-item .value { font-size: 16px; font-weight: 600; color: #333d4b; }
.value.accent { color: #191f28; }

/* 버튼 */
.button-group { margin-bottom: 10px; }
.toss-btn-blue { 
  width: 100%; padding: 18px; background: #3182f6; color: #fff; 
  border-radius: 14px; border: none; font-weight: 600; font-size: 17px; 
  cursor: pointer;
}

.toss-divider { border: 0; height: 1px; background: #f2f4f6; margin: 48px 0; }

/* 🟢 추가된 페르소나 카드 스타일 (토스 스타일) */
.user-persona-card {
  padding: 40px 24px;
  background: linear-gradient(135deg, #f9fafb 0%, #f2f4f6 100%);
  border-radius: 0 0 24px 24px;
  display: flex;
  align-items: center;
  gap: 20px;
}
.persona-icon { font-size: 48px; }
.persona-tag { 
  display: inline-block; padding: 4px 8px; background: #fff; 
  color: #3182f6; border-radius: 6px; font-size: 12px; font-weight: 700; margin-bottom: 8px;
}
.persona-title { font-size: 22px; font-weight: 700; color: #191f28; line-height: 1.4; margin: 0; }
.persona-desc { font-size: 15px; color: #4e5968; margin-top: 8px; line-height: 1.5; }

/* AI 분석 리스트 */
.section-title { font-size: 20px; font-weight: 700; color: #191f28; margin-bottom: 28px; }
.analysis-list { display: flex; flex-direction: column; gap: 32px; }
.analysis-item { display: flex; gap: 16px; }
.icon { font-size: 24px; }
.item-text strong { display: block; font-size: 16px; color: #333d4b; margin-bottom: 6px; font-weight: 600; }
.item-text p { font-size: 15px; color: #4e5968; line-height: 1.6; margin: 0; word-break: keep-all; }
</style>