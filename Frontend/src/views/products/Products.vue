<template>
  <div class="products-container">
    <header class="page-header">
      <div class="header-content">
        <h2 class="title">예금/적금 상품</h2>
        <p class="subtitle">안정적인 자산 증식을 위한 최적의 금리 상품을 만나보세요.</p>
      </div>
      
      <div class="header-actions">
        <div class="select-group">
          <!-- <span class="search-icon">🔍</span> -->
          <input 
            v-model="filters.bank" 
            type="text" 
            placeholder="은행명을 입력하세요" 
            class="custom-input"
          />
          <span>  </span>

          <select v-model="filters.term" class="custom-select">
            <option value="">전체 기간</option>
            <option v-for="m in [1, 3, 6, 12, 24, 36]" :key="m" :value="m">
              {{ m }}개월
            </option>
          </select>
        </div>
      </div>
    </header>

    <section class="tab-section">
      <div class="tab-filters">
        <button 
          v-for="type in [
            { label: '전체', value: '' }, 
            { label: '정기예금', value: 'DEPOSIT' }, 
            { label: '정기적금', value: 'SAVING' },
          ]" 
          :key="type.value"
          :class="['filter-tab', { active: filters.product_type === type.value }]"
          @click="filters.product_type = type.value"
        >
          {{ type.label }}
        </button>
      </div>
    </section>

    <section class="list-section">
      <div class="list-table">
        <div class="list-thead">
          <span class="th">상품유형</span>
          <span class="th">상품정보</span>
          <span class="th text-center">금리 (연)</span>
          <span class="th text-center">기간</span>
          <span class="th mobile-hidden">우대조건 / 특징</span>
          <!-- <span class="th"></span> -->
        </div>

        <div class="list-tbody">
          <div v-if="products.length === 0" class="empty-state">
            찾으시는 상품이 없습니다. 다른 조건으로 검색해보세요.
          </div>

          <div 
            v-for="product in products" 
            :key="product.id" 
            class="product-row"
            @click="goDetail(product.id)"
          >
            <div class="td type">
              <span :class="['type-badge', product.product_type?.toLowerCase()]">
                {{ product.product_type_display || '정기예금' }}
              </span>
            </div>

            <div class="td info">
              <div class="bank-avatar">
                <span class="avatar-text">{{ product.kor_co_nm[0] }}</span>
              </div>
              <div class="name-group">
                <span class="bank-name">{{ product.kor_co_nm }}</span>
                <strong class="product-name">{{ product.fin_prdt_nm }}</strong>
              </div>
            </div>

            <div class="td rate text-center">
              <template v-if="getDisplayOption(product)">
                <span class="rate-value">{{ getDisplayOption(product).intr_rate }}%</span>
                <span v-if="getDisplayOption(product).intr_rate2 > getDisplayOption(product).intr_rate" class="rate-tag">
                  최고
                </span>
              </template>
            </div>

            <div class="td term text-center">
              {{ getDisplayOption(product) ? getDisplayOption(product).save_trm : '-' }}개월
            </div>

            <div class="td feature mobile-hidden">
              {{ product.spcl_cnd || '조건 없이 누구에게나 높은 금리 제공' }}
            </div>

            <!-- <div class="td action">
              <button class="sub-btn">상세보기</button>
            </div> -->
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Toss Style Guide Implementation */
.products-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 48px 24px;
  font-family: 'Pretendard', sans-serif;
  color: #191F28;
}

/* Header Styling */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 40px;
}
.title { font-size: 28px; font-weight: 700; margin-bottom: 12px; }
.subtitle { color: #4E5968; font-size: 16px; }

.header-actions { display: flex; gap: 12px; align-items: center; }

/* 검색창 & 셀렉트 박스 커스텀 */
.custom-input, .custom-select {
  padding: 10px 16px;
  border-radius: 12px;
  border: 1px solid #E5E8EB;
  background-color: #F9FAFB;
  color: #4E5968;
  font-size: 14px;
  outline: none;
}

/* Tab Filter Styling */
.tab-section { margin-bottom: 32px; }
.tab-filters { display: flex; gap: 10px; }
.filter-tab {
  padding: 12px 20px;
  border-radius: 32px;
  border: none;
  background-color: #F2F4F6;
  color: #4E5968;
  font-weight: 600;
  transition: all 0.2s ease;
  cursor: pointer;
}
.filter-tab.active { background-color: #3182F6; color: #FFFFFF; }
.filter-tab:hover:not(.active) { background-color: #E5E8EB; }

/* Table Styling - Grid 가이드 적용 */
.list-table { background: #FFFFFF; border-radius: 32px; }

/* 헤더와 행의 그리드 비율 통일 */
.list-thead, .product-row {
  display: grid;
  /* 유형(100px), 정보(1.2fr), 금리(1fr), 기간(1fr), 특징(1.5fr) */
  grid-template-columns: 100px 1.2fr 1fr 1fr 1.5fr;
  align-items: center;
  padding: 20px 24px;
  gap: 10px;
}

.list-thead {
  border-bottom: 1px solid #E5E8EB;
}

/* 공통 텍스트/셀 정렬 */
.th { 
  font-size: 14px; 
  color: #8B95A1; 
  font-weight: 500; 
  text-align: center; /* 헤더 중앙 정렬 */
}

.td {
  display: flex;
  align-items: center;
  justify-content: center; /* 수평 가운데 정렬 */
  width: 100%;
}

/* Product Row Styling */
.product-row {
  margin: 8px 0;
  border-radius: 20px;
  transition: all 0.2s ease;
  cursor: pointer;
}
.product-row:hover {
  transform: translateY(-2px);
  background-color: #F9FAFB;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.04);
}

/* Bank Avatar */
.bank-avatar {
  width: 44px;
  height: 44px;
  background-color: #F2F4F6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  flex-shrink: 0;
}
.avatar-text { font-weight: 700; color: #3182F6; }

/* 상품 정보(은행, 상품명)는 가독성을 위해 왼쪽 정렬 유지 */
.td.info {
  justify-content: flex-start;
  text-align: left;
}
.name-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.bank-name { font-size: 13px; color: #8B95A1; margin-bottom: 2px; }
.product-name { font-size: 16px; font-weight: 700; color: #191F28; }

/* 금리 영역 */
.td.rate {
  flex-direction: column;
  gap: 4px;
}
.rate-value { font-size: 18px; font-weight: 700; color: #3182F6; }
.rate-tag {
  font-size: 11px;
  color: #FF4D4F;
  background: #FFF1F0;
  padding: 2px 6px;
  border-radius: 4px;
}

/* 기간 및 특징 */
.td.term { font-weight: 500; color: #4E5968; }
.td.feature { 
  color: #8B95A1; 
  font-size: 14px;
  justify-content: center;
  text-align: center;
}

/* Badges */
.type-badge {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}
.type-badge.deposit { background: #E7F3FF; color: #3182F6; }
.type-badge.saving { background: #FFF5E7; color: #FF9500; }

.text-center { text-align: center; }
.mobile-hidden { display: block; }

/* 모바일 대응 */
@media (max-width: 900px) {
  .mobile-hidden { display: none; }
  .list-thead, .product-row {
    grid-template-columns: 80px 1.2fr 1fr 1fr; /* 특징 제외 */
    padding: 16px;
  }
}
</style>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useProductStore } from '@/stores/products'

const router = useRouter();
const productStore = useProductStore()

const products = ref([]);
const filters = reactive({
  bank: '',
  product_type: '',
  term: ''
});

// [추가] 템플릿에서 사용할 최적 옵션 추출 함수
const getDisplayOption = (product) => {
  if (!product.options || product.options.length === 0) return null;

  // 1. 특정 기간(term)이 선택된 경우 해당 기간 옵션 찾기
  if (filters.term) {
    return product.options.find(opt => Number(opt.save_trm) === Number(filters.term)) || product.options[0];
  }

  // 2. 전체 기간일 경우 기본 금리(intr_rate)가 가장 높은 옵션 반환
  // slice()를 사용하여 원본 배열 보존
  return [...product.options].sort((a, b) => b.intr_rate - a.intr_rate)[0];
};

const onSearch = async () => {
  products.value = await productStore.getProducts(filters)
}

const goDetail = (id) => {
  router.push({ name: 'ProductDetails', params: { id: id } })
}

watch(filters, () => {
  console.log(filters)
  onSearch();
}, { deep: true });

onMounted(() => {
  onSearch()
})
</script>

<!-- <style scoped>

</style> -->