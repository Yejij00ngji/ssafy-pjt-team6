<template>
  <div class="detail-container" v-if="product">
    <button class="back-btn" @click="router.back()">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      돌아가기
    </button>

    <header class="product-header-card">
      <div class="header-top">
        <div class="bank-info">
          <div class="bank-logo-circle">
            <span class="avatar-text">{{ product.kor_co_nm?.[0] }}</span>
          </div>
          <span class="bank-name">{{ product.kor_co_nm }}</span>
        </div>
        <div class="rate-summary">
          <span class="rate-label">최고 금리 (연, 세전)</span>
          <h1 class="main-rate">{{ product.max_intr_rate }}%</h1>
          <p class="rate-sub">기본 {{ product.options?.[0]?.intr_rate }}% ~ 우대금리 포함</p>
        </div>
      </div>
      
      <h2 class="product-title">{{ product.fin_prdt_nm }}</h2>
      
      <div class="badge-group">
        <span 
          v-for="(badge, index) in productBadges" 
          :key="index" 
          class="type-badge" 
          :class="[badge.isBlue ? 'deposit' : 'saving']"
        >
          {{ badge.text }}
        </span>
      </div>
    </header>

    <section class="info-grid">
      <div class="info-card">
        <span class="info-label">가입 기간</span>
        <strong class="info-value">{{ saveTrmRange }}</strong>
      </div>
      <div class="info-card">
        <span class="info-label">이자 계산</span>
        <strong class="info-value">{{ interestType }}</strong>
      </div>
      <div class="info-card">
        <span class="info-label">우대 금리</span>
        <strong class="info-value">최대 {{ maxSpclRate }}</strong>
      </div>
      <div class="info-card">
        <span class="info-label">가입 대상</span>
        <strong class="info-value">{{ product.join_member }}</strong>
      </div>
    </section>

    <div class="detail-content-layout">
      <div class="main-content">
        <nav class="content-tabs">
          <button 
            class="tab-item" 
            :class="{ active: activeTab === 'guide' }" 
            @click="activeTab = 'guide'"
          >상품 안내</button>
          <button 
            class="tab-item" 
            :class="{ active: activeTab === 'rates' }" 
            @click="activeTab = 'rates'"
          >금리 정보</button>
          <button 
            class="tab-item" 
            :class="{ active: activeTab === 'notice' }" 
            @click="activeTab = 'notice'"
          >유의 사항</button>
        </nav>

        <div class="tab-pane">
          <div v-if="activeTab === 'guide'" class="detail-section">
            <h3 class="section-title">가입 조건 및 혜택 상세</h3>
            <ul class="benefit-list">
              <li>
                <span class="check-icon">✓</span>
                <p><strong>가입 방법:</strong> {{ product.join_way }}</p>
              </li>
              <li>
                <span class="check-icon">✓</span>
                <p><strong>우대 조건:</strong> {{ product.spcl_cnd === '해당사항 없음' ? '특별한 조건 없이 누구나 기본 금리 혜택을 받을 수 있습니다.' : product.spcl_cnd }}</p>
              </li>
              <li>
                <span class="check-icon">✓</span>
                <p><strong>가입 대상:</strong> {{ product.join_member }}</p>
              </li>
            </ul>
          </div>

          <div v-if="activeTab === 'rates'" class="detail-section">
            <h3 class="section-title">만기 후 이율 안내</h3>
            <p class="etc-text">{{ product.mtrt_int }}</p>
            <h3 class="section-title" style="margin-top: 32px;">중도해지 이율</h3>
            <p class="etc-text">본 상품의 중도해지 이율은 가입 당시 고시된 기간별 중도해지 이율을 따릅니다.</p>
          </div>

          <div v-if="activeTab === 'notice'" class="detail-section">
            <h3 class="section-title">기타 안내 및 유의사항</h3>
            <p class="etc-text">{{ product.etc_note }}</p>
          </div>
        </div>
      </div>

      <aside class="side-rate-card">
        <div class="card-header">
          <div class="bank-avatar">
            <span class="avatar-text">%</span>
          </div>
          <h3 class="card-title">기간별 금리</h3>
        </div>
        <table class="rate-table">
          <thead>
            <tr>
              <th>기간</th>
              <th>기본</th>
              <th>최고</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="opt in product.options" :key="opt.id" class="rate-row-clickable" @click="goOptionApply(opt.id)">
              <td>{{ opt.save_trm }}개월</td>
              <td>{{ opt.intr_rate }}%</td>
              <td class="rate-value highlight">{{ opt.intr_rate2 }}%</td>
            </tr>
          </tbody>
        </table>
        <p class="rate-notice">* 최고 금리는 모든 우대 조건을 충족했을 때 적용됩니다.</p>
        <p class="rate-notice">* 시장 상황에 따라 금리가 변동될 수 있습니다.</p>
      </aside>
    </div>
  </div>
</template>

<style scoped>
/* Toss Style Detail Integration */
.detail-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 48px 24px 140px;
  font-family: 'Pretendard', sans-serif;
  color: #191F28;
  background-color: #F9FAFB;
}

/* 0. 뒤로가기 */
.back-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  color: #8B95A1;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 24px;
  transition: color 0.2s;
}
.back-btn:hover { color: #4E5968; }

/* 1. 제품 헤더 카드 */
.product-header-card {
  background: #FFFFFF;
  border-radius: 32px;
  padding: 40px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.04);
  margin-bottom: 32px;
}
.header-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.bank-info { display: flex; align-items: center; gap: 16px; }
.bank-logo-circle {
  width: 48px; height: 48px;
  background-color: #F2F4F6;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
}
.avatar-text { font-weight: 700; color: #3182F6; }
.bank-name { color: #8B95A1; font-weight: 600; font-size: 17px; }

.rate-summary { text-align: right; }
.rate-label { font-size: 14px; color: #8B95A1; font-weight: 500; }
.main-rate { font-size: 42px; font-weight: 800; color: #3182F6; margin: 4px 0; }
.rate-sub { font-size: 14px; color: #B0B8C1; }

.product-title { font-size: 32px; font-weight: 700; margin-bottom: 24px; letter-spacing: -0.5px; }

/* 리스트 페이지의 Badge 스타일 적용 */
.type-badge {
  padding: 8px 16px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  display: inline-block;
  margin-right: 8px;
}
.type-badge.deposit { background: #E7F3FF; color: #3182F6; }
.type-badge.saving { background: #FFF5E7; color: #FF9500; }

/* 2. 정보 그리드 */
.info-grid { 
  display: grid; 
  grid-template-columns: repeat(4, 1fr); 
  gap: 20px; 
  margin-bottom: 32px; 
}
.info-card {
  background: #FFFFFF; 
  padding: 24px;
  border-radius: 24px; 
  display: flex; flex-direction: column; gap: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
}
.info-label { font-size: 14px; color: #8B95A1; font-weight: 500; }
.info-value { font-size: 18px; font-weight: 700; color: #191F28; }

/* 3. 탭 & 상세 내용 */
.detail-content-layout { display: flex; gap: 32px; align-items: flex-start; }
.main-content { 
  flex: 2; 
  background: #FFFFFF; 
  border-radius: 32px; 
  padding: 40px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.04);
}
.content-tabs { display: flex; border-bottom: 1px solid #F2F4F6; margin-bottom: 32px; }
.tab-item {
  padding: 16px 24px; border: none; background: none;
  font-size: 17px; font-weight: 600; color: #8B95A1; cursor: pointer;
  position: relative; transition: color 0.2s;
}
.tab-item.active { color: #3182F6; }
.tab-item.active::after {
  content: ""; position: absolute; bottom: 0; left: 0; right: 0;
  height: 3px; background-color: #3182F6; border-radius: 3px 3px 0 0;
}

.section-title { font-size: 20px; font-weight: 700; margin-bottom: 24px; }
.benefit-list { list-style: none; padding: 0; }
.benefit-list li { display: flex; gap: 12px; margin-bottom: 20px; color: #4E5968; line-height: 1.6; }
.check-icon { color: #3182F6; font-weight: 800; }
.etc-text { 
  white-space: pre-wrap; color: #4E5968; line-height: 1.8; 
  background: #F9FAFB; padding: 24px; border-radius: 20px; font-size: 15px;
}

/* 4. 사이드 카드 (금리표) */
.side-rate-card {
  flex: 1; 
  background: #FFFFFF; border-radius: 32px; padding: 32px;
  border: 1px solid #F2F4F6; position: sticky; top: 40px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.04);
}
.card-header { display: flex; align-items: center; gap: 12px; margin-bottom: 24px; }
.card-title { font-size: 19px; font-weight: 700; }

.rate-table { width: 100%; border-collapse: separate; border-spacing: 0; margin-bottom: 24px; }
.rate-table th { text-align: left; padding: 12px 8px; color: #8B95A1; font-size: 14px; border-bottom: 1px solid #F2F4F6; }
.rate-table td { padding: 16px 8px; border-top: 1px solid #F2F4F6; font-size: 15px; }

/* 리스트 페이지와 동일한 Hover 효과 */
.rate-row-clickable { cursor: pointer; transition: all 0.2s; }
.rate-row-clickable:hover {
  background-color: #F9FAFB;
  transform: scale(1.02);
}
.rate-row-clickable:hover td:first-child { border-top-left-radius: 12px; border-bottom-left-radius: 12px; }
.rate-row-clickable:hover td:last-child { border-top-right-radius: 12px; border-bottom-right-radius: 12px; }

.highlight { color: #3182F6; font-weight: 700; }
.rate-notice { font-size: 12px; color: #B0B8C1; margin-top: 8px; line-height: 1.5; }

/* 모바일 대응 */
@media (max-width: 900px) {
  .detail-content-layout { flex-direction: column; }
  .info-grid { grid-template-columns: repeat(2, 1fr); }
  .side-rate-card { position: static; width: 100%; box-sizing: border-box; }
}
</style>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useProductStore } from '@/stores/products'
import { useAccountStore } from '@/stores/accounts'
import { ref, onMounted, computed } from 'vue'

const route = useRoute()
const router = useRouter();
const productStore = useProductStore()
const accountStore = useAccountStore()

const product = ref(null) // null로 초기화하여 데이터 로딩 전 체크

const activeTab = ref('guide')

const saveTrmRange = computed(() => {
  if (!product.value || !product.value.options || product.value.options.length === 0) {
    return '정보 없음'
  }
  
  // save_trm 값들만 모아서 정렬
  const terms = product.value.options.map(opt => opt.save_trm).sort((a, b) => a - b)
  const minTerm = terms[0]
  const maxTerm = terms[terms.length - 1]
  
  return minTerm === maxTerm ? `${minTerm}개월` : `${minTerm}개월 ~ ${maxTerm}개월`
})

const productBadges = computed(() => {
  if (!product.value) return []
  
  const badges = []
  
  // 1. 상품 유형에 따른 뱃지 (DEPOSIT면 정기예금, SAVING이면 자유적립식 등)
  if (product.value.product_type === 'DEPOSIT') {
    badges.push({ text: '거치식예금', isBlue: false })
  } else {
    badges.push({ text: '자유적립식', isBlue: false })
  }

  // 2. 가입 방법에 따른 뱃지
  if (product.value.join_way.includes('스마트폰')) {
    badges.push({ text: '스마트폰 가입', isBlue: true })
  }
  
  // 3. 기타 조건 (데이터에 '비과세' 키워드가 있다면 추가)
  if (product.value.etc_note?.includes('비과세')) {
    badges.push({ text: '비과세 혜택', isBlue: false })
  }

  // 4. 우대 조건이 없을 때 깔끔함을 주는 뱃지
  if (product.value.spcl_cnd.includes('없음')) {
    badges.push({ text: '조건없는 우대', isBlue: false })
  } 
  
  return badges
})


// 우대 금리 폭 계산 (최고 금리 - 기본 금리)
const maxSpclRate = computed(() => {
  if (!product.value || !product.value.options) return '0.00'
  
  const baseRate = product.value.options[0].intr_rate // 기본 금리
  const maxRate = product.value.max_intr_rate // 최고 금리
  
  // 소수점 2자리까지 계산
  const diff = (maxRate - baseRate).toFixed(2)
  return diff > 0 ? `${diff}%p` : '없음'
})

// 이자 계산 방식 (단리/복리)
const interestType = computed(() => {
  return product.value?.options?.[0]?.intr_rate_type_nm || '단리'
})
const goOptionApply = (id) => {
    router.push({ name: 'Subscribe', params: { id: id } })
}

onMounted(async () => {
  // 실제 API 호출을 통해 데이터 저장
  product.value = await productStore.getProductDetails(route.params.id)
})
</script>