<template>
  <div class="toss-container-narrow result-step">
    <header class="result-header">
      <div class="status-badge" :class="{ 'is-my-data': isMyData }">
        {{ isMyData ? '✅ 자산 분석 완료' : '📝 성향 분석 완료' }}
      </div>
      <h1 class="toss-title main-title">
        {{ userName }}님에게 <br />
        가장 유리한 상품을 찾았어요
      </h1>
      <p class="toss-desc">
        {{ analysisSummary }}
      </p>
    </header>

    <section class="best-product-section">
      <div class="toss-card premium-card">
        <div class="match-badge">추천도 {{ bestProduct.matchRate }}%</div>
        
        <div class="bank-info">
          <span class="bank-logo">🏦</span>
          <span class="bank-name">{{ bestProduct.bankName }}</span>
        </div>
        
        <h2 class="product-name">{{ bestProduct.title }}</h2>
        
        <div class="benefit-grid">
          <div class="benefit-item">
            <span class="label">최대 금리</span>
            <span class="value accent">연 {{ bestProduct.maxRate }}%</span>
          </div>
          <div class="benefit-item">
            <span class="label">가입 기간</span>
            <span class="value">{{ bestProduct.period }}개월</span>
          </div>
        </div>

        <div class="recommend-reason">
          <span class="light-bulb">💡</span>
          <p>{{ bestProduct.reason }}</p>
        </div>

        <button class="toss-btn-main full-width">상품 자세히 보기</button>
      </div>
    </section>

    <footer class="result-footer">
      <div v-if="!isMyData" class="upsell-card" @click="handleReAuth">
        <div class="upsell-content">
          <strong>내 진짜 자산 연결하기</strong>
          <span>마이데이터를 연결하면 정확한 우대금리를 확인해요</span>
        </div>
        <span class="arrow">→</span>
      </div>

      <button class="retry-link" @click="$emit('retry')">
        다시 분석하기
      </button>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  isMyData: Boolean,
  userName: { type: String, default: '사용자' }
})

const analysisSummary = computed(() => {
  return props.isMyData 
    ? '현재 보유하신 자산 현황과 지출 패턴을 고려하여 선정했습니다.'
    : '답변하신 가입 목적과 선호 기간을 바탕으로 선정했습니다.'
})

// 실제로는 API에서 받아올 데이터 예시
const bestProduct = {
  bankName: '토스뱅크',
  title: '굴리기 적금 (최고 우대형)',
  maxRate: '5.5',
  period: '12',
  matchRate: 98,
  reason: props.isMyData 
    ? '보유하신 여유 자금 500만원을 1년간 굴렸을 때 가장 수익이 높아요.'
    : '안정적인 목돈 마련을 선호하시는 성향에 딱 맞는 금리 조건이에요.'
}

const handleReAuth = () => {
  // 마이데이터 연동 로직
  console.log('Redirecting to MyData Auth...')
}
</script>

<style scoped>
.result-step { padding-bottom: 80px; }

/* 헤더 스타일 */
.result-header { margin-bottom: 40px; text-align: center; }
.status-badge {
  display: inline-block; padding: 6px 16px; border-radius: 50px;
  background: var(--toss-gray-bg); color: var(--toss-text-sub);
  font-size: 13px; font-weight: 600; margin-bottom: 20px;
}
.status-badge.is-my-data { background: #e8f3ff; color: var(--toss-blue); }
.main-title { font-size: 28px; line-height: 1.4; }

/* 프리미엄 추천 카드 */
.premium-card {
  padding: 32px !important; border: 1px solid var(--toss-border);
  position: relative; overflow: hidden; background: #fff !important;
}
.match-badge {
  position: absolute; top: 0; right: 0; padding: 8px 16px;
  background: var(--toss-blue); color: #fff; font-size: 13px;
  font-weight: 700; border-bottom-left-radius: 20px;
}
.bank-info { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
.bank-name { color: var(--toss-text-sub); font-size: 15px; }
.product-name { font-size: 22px; font-weight: 700; margin-bottom: 30px; }

.benefit-grid { display: flex; gap: 40px; margin-bottom: 30px; }
.benefit-item { display: flex; flex-direction: column; gap: 6px; }
.benefit-item .label { font-size: 13px; color: var(--toss-text-tertiary); }
.benefit-item .value { font-size: 20px; font-weight: 700; }
.value.accent { color: var(--toss-blue); }

.recommend-reason {
  display: flex; gap: 10px; background: var(--toss-gray-bg);
  padding: 16px; border-radius: 14px; margin-bottom: 30px;
}
.recommend-reason p { font-size: 14px; color: var(--toss-text-sub); line-height: 1.5; margin: 0; }

.full-width { width: 100%; padding: 18px; }

/* 하단 업셀링 & 리트라이 */
.result-footer { margin-top: 30px; }
.upsell-card {
  display: flex; justify-content: space-between; align-items: center;
  padding: 20px; border-radius: 20px; background: #fff;
  border: 1px solid var(--toss-border); cursor: pointer; transition: 0.2s;
}
.upsell-card:hover { border-color: var(--toss-blue); }
.upsell-content { display: flex; flex-direction: column; gap: 4px; }
.upsell-content strong { font-size: 15px; color: var(--toss-text-main); }
.upsell-content span { font-size: 13px; color: var(--toss-blue); font-weight: 600; }

.retry-link {
  display: block; width: 100%; background: none; border: none;
  margin-top: 30px; color: var(--toss-text-tertiary); text-decoration: underline;
  cursor: pointer; font-size: 14px;
}
</style>