<template>
  <div class="detail-page">
    <div class="detail-container">
      <button class="back-link-btn" @click="router.back()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        돌아가기
      </button>

      <header class="detail-header">
        <h1 class="detail-title">상품 상세 정보</h1>
        <p class="detail-description">가입하신 금융 상품의 상세 내역과 금리 조건을 확인하세요.</p>
      </header>

      <div v-if="subscribedOption" class="detail-content">
        <section class="card summary-card">
          <div class="product-badge">{{ subscribedOption.bank_name }}</div>
          <h2 class="product-name">{{ subscribedOption.product_name }}</h2>
          <div class="amount-display">
            <span class="label">현재 잔액</span>
            <span class="value">₩ {{ subscribedOption.amount?.toLocaleString() }}</span>
          </div>
          
          <div class="status-tags">
            <span class="tag">D-{{ calculateDDay(subscribedOption.expired_at) }}</span>
            <span class="tag blue">{{ subscribedOption.init_intr_rate_type_nm }}</span>
          </div>
        </section>

        <div class="info-grid">
          <div class="card info-card">
            <h3 class="card-subtitle">금리 정보</h3>
            <div class="info-list">
              <div class="info-row">
                <span class="info-label">기본 금리</span>
                <span class="info-value">{{ subscribedOption.intr_rate }}%</span>
              </div>
              <div class="info-row">
                <span class="info-label">우대 금리 (최대)</span>
                <span class="info-value highlight">{{ subscribedOption.intr_rate2 }}%</span>
              </div>
              <div class="info-row">
                <span class="info-label">가입 시점 금리</span>
                <span class="info-value">{{ subscribedOption.init_intr_rate }}%</span>
              </div>
            </div>
          </div>

          <div class="card info-card">
            <h3 class="card-subtitle">기간 및 날짜</h3>
            <div class="info-list">
              <div class="info-row">
                <span class="info-label">가입 기간</span>
                <span class="info-value">{{ subscribedOption.save_trm }}개월</span>
              </div>
              <div class="info-row">
                <span class="info-label">가입일</span>
                <span class="info-value">{{ subscribedOption.subscribed_at }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">만기 예정일</span>
                <span class="info-value">{{ subscribedOption.expired_at }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="action-footer">
          <button class="btn-danger" @click="handleUnsubscribe">상품 가입 해지하기</button>
        </div>
      </div>

      <div v-else class="loading-state">
        <p>상품 정보를 불러오고 있습니다...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useProductStore } from '@/stores/products'
import { ref, onMounted } from 'vue'

const route = useRoute()
const router = useRouter()
const productStore = useProductStore()

const subscribedOption = ref(null)

// D-Day 계산 함수
const calculateDDay = (expiryDate) => {
  if (!expiryDate) return '0'
  const today = new Date()
  const expired = new Date(expiryDate)
  const diffTime = expired - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays > 0 ? diffDays : '만기'
}

// 해지 처리 함수
const handleUnsubscribe = async () => {
  if (confirm('정말로 이 상품을 해지하시겠습니까? 해지 후에는 복구가 불가능합니다.')) {
    try {
      const success = await productStore.delSubscription(subscribedOption.value.id)
      if (success) {
        alert('상품 해지가 완료되었습니다.')
        router.push({ name: 'Profile' }) // 마이페이지로 리다이렉트
      }
    } catch (error) {
      console.error('해지 중 오류 발생:', error)
      alert('해지 처리 중 오류가 발생했습니다.')
    }
  }
}

onMounted(async () => {
  if (productStore.subscriptions.length === 0) {
    await productStore.getSubscriptions()
  }

  const found = productStore.subscriptions.find(
    (item) => item.id === Number(route.params.id)
  )

  if (found) {
    subscribedOption.value = found
  } else {
    console.error('해당 구독 정보를 찾을 수 없습니다.')
  }
})
</script>

<style scoped>
.detail-page {
  min-height: 100vh;
  background-color: #F9FAFB;
  padding: 40px 20px;
  font-family: 'Pretendard', sans-serif;
}

.detail-container {
  max-width: 1000px;
  margin: 0 auto;
}

/* 상단 뒤로가기 */
.back-link-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  color: #8B95A1;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 24px;
  transition: color 0.2s;
}

.back-link-btn:hover { color: #4E5968; }

/* 헤더 */
.detail-header { margin-bottom: 32px; }
.detail-title { font-size: 28px; font-weight: 700; color: #191F28; margin-bottom: 8px; }
.detail-description { color: #4E5968; font-size: 16px; }

/* 공통 카드 스타일 */
.card {
  background: #FFFFFF;
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(0, 0, 0, 0.02);
}

/* 메인 요약 카드 */
.summary-card {
  margin-bottom: 24px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.product-badge {
  background: #F2F4F6;
  color: #4E5968;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 16px;
}

.product-name { font-size: 24px; font-weight: 700; color: #191F28; margin-bottom: 24px; }

.amount-display {
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.amount-display .label { color: #8B95A1; font-size: 15px; }
.amount-display .value { font-size: 36px; font-weight: 800; color: #191F28; }

.status-tags { display: flex; gap: 8px; }
.tag {
  background: #F2F4F6;
  color: #4E5968;
  padding: 6px 14px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 700;
}
.tag.blue { background: #E8F3FF; color: #3182F6; }

/* 그리드 레이아웃 */
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 32px;
}

.card-subtitle {
  font-size: 18px;
  font-weight: 700;
  color: #191F28;
  margin-bottom: 20px;
}

.info-list { display: flex; flex-direction: column; gap: 16px; }
.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-label { color: #8B95A1; font-size: 15px; }
.info-value { color: #191F28; font-weight: 600; font-size: 15px; }
.info-value.highlight { color: #3182F6; font-weight: 700; }

/* 푸터 액션 */
.action-footer {
  display: flex;
  justify-content: center;
  padding-top: 20px;
}

/* 강조된 해지 버튼 */
.btn-danger {
  width: 100%;
  max-width: 400px;
  padding: 18px;
  background-color: #F04452;
  color: white;
  border: none;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-danger:hover {
  background-color: #D93D4A;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(240, 68, 82, 0.2);
}

/* 로딩 상태 */
.loading-state {
  text-align: center;
  padding: 100px 0;
  color: #8B95A1;
}

@media (max-width: 768px) {
  .info-grid { grid-template-columns: 1fr; }
}
</style>