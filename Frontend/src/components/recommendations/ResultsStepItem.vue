<template>
  <div class="result-container">
    <header class="result-header">
      <div class="analysis-tag">
        {{ isMyData ? '✅ 마이데이터 분석 완료' : '📝 설문 기반 분석 완료' }}
      </div>
      <h1 class="user-analysis">
        <span>{{ userName }}</span>님은 <br/>
        <span class="highlight">#{{ clusterName }}</span> 성향이시네요!
      </h1>
    </header>

    <section class="best-match-section">
      <h3 class="section-label">가장 추천하는 상품</h3>
      <div class="product-card-premium">
        <div class="match-score">매칭률 {{ bestProduct.matchRate }}%</div>
        <div class="product-brand">{{ bestProduct.bankName }}</div>
        <h2 class="product-title">{{ bestProduct.title }}</h2>
        
        <div class="benefit-box">
          <div class="benefit-item">
            <span class="label">최대 금리</span>
            <span class="value main-green">{{ bestProduct.maxRate }}%</span>
          </div>
          <div class="benefit-item">
            <span class="label">가입 기간</span>
            <span class="value">{{ bestProduct.period }}개월</span>
          </div>
        </div>

        <div class="reason-tag">
          💡 {{ bestProduct.reason }}
        </div>

        <button class="apply-btn">상품 자세히 보기</button>
      </div>
    </section>

    <div v-if="!isMyData" class="upsell-banner" @click="reAuth">
      <div class="upsell-text">
        <strong>더 정확한 금리를 알고 싶다면?</strong>
        <span>마이데이터 연결하고 0.5% 우대금리 찾기</span>
      </div>
      <span class="arrow">→</span>
    </div>

    <button class="retry-btn" @click="$emit('retry')">처음부터 다시하기</button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  isMyData: Boolean,
  userName: { type: String, default: '똑똑한 저축가' }
})

// 가상의 추천 결과 데이터 (실제로는 API에서 가져온 벡터 유사도 기반 데이터)
const clusterName = computed(() => props.isMyData ? '공격적인 자산가' : '실속파 목돈마련형')

const bestProduct = {
  bankName: '머니비 은행',
  title: '청년 도약 플러스 적금',
  maxRate: '6.5',
  period: '24',
  matchRate: 98,
  reason: '선호하시는 단기 목돈 마련에 가장 유리한 금리에요.'
}

const reAuth = () => {
  alert('마이데이터 연동 페이지로 이동합니다.')
}
</script>

<style scoped>
.result-container { padding: 40px 24px; background-color: #f9fafb; min-height: 100vh; }

.result-header { margin-bottom: 32px; }
.analysis-tag { 
  display: inline-block; padding: 6px 12px; background: #fff; border: 1px solid #e5e8eb;
  border-radius: 30px; font-size: 13px; color: #4e5968; margin-bottom: 16px; font-weight: 600;
}
.user-analysis { font-size: 24px; font-weight: 700; color: #191f28; line-height: 1.4; }
.highlight { color: #00ad7c; }

/* 프리미엄 카드 디자인 */
.product-card-premium {
  background: #fff; border-radius: 24px; padding: 28px;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.05); position: relative;
}
.match-score {
  position: absolute; top: 28px; right: 28px;
  background: #f2fcf9; color: #00ad7c; font-weight: 700; font-size: 14px;
  padding: 4px 10px; border-radius: 8px;
}
.product-brand { font-size: 14px; color: #8b95a1; margin-bottom: 8px; }
.product-title { font-size: 20px; font-weight: 700; color: #191f28; margin-bottom: 24px; }

.benefit-box { display: flex; gap: 32px; margin-bottom: 24px; }
.benefit-item { display: flex; flex-direction: column; gap: 4px; }
.benefit-item .label { font-size: 13px; color: #8b95a1; }
.benefit-item .value { font-size: 18px; font-weight: 700; color: #333d4b; }
.main-green { color: #00ad7c !important; }

.reason-tag {
  background: #f2f4f6; padding: 14px; border-radius: 12px;
  font-size: 14px; color: #4e5968; margin-bottom: 24px; line-height: 1.5;
}

.apply-btn {
  width: 100%; padding: 16px; background: #191f28; color: #fff;
  border: none; border-radius: 14px; font-size: 16px; font-weight: 700; cursor: pointer;
}

/* 업셀링 배너 */
.upsell-banner {
  margin-top: 24px; background: #fff; border: 1px solid #e5e8eb;
  padding: 20px; border-radius: 20px; display: flex; justify-content: space-between;
  align-items: center; cursor: pointer;
}
.upsell-text { display: flex; flex-direction: column; gap: 4px; }
.upsell-text strong { font-size: 15px; color: #191f28; }
.upsell-text span { font-size: 13px; color: #00ad7c; font-weight: 600; }

.retry-btn {
  width: 100%; margin-top: 40px; background: none; border: none;
  color: #8b95a1; text-decoration: underline; cursor: pointer; font-size: 14px;
}
</style>