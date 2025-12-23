<!-- <template>
  <div class="product-container">
    <h1>금융 상품 금리 비교</h1>

    <hr>

    <h2>상품 검색 필터</h2>
      
    <div class="filter-box">

      <select v-model="filters.bank">
          <option value="">모든 은행</option>
          <option value="우리은행">우리은행</option>
          <option value="국민은행">국민은행</option>
          <option value="신한은행">신한은행</option>
          <option value="농협은행주식회사">농협은행</option>
        </select>

      <select v-model="filters.term">
        <option value="">모든 기간</option>
        <option :value="1">1개월</option>
        <option :value="3">3개월</option>
        <option :value="6">6개월</option>
        <option :value="12">12개월</option>
        <option :value="24">24개월</option>
        <option :value="36">36개월</option>
        </select>

      <button @click="onSearch">검색하기</button>
      </div>

    <hr />

    <div class="result-info">

      <p>현재 검색 조건: {{ filters.bank || '전체' }} / {{ filters.term || '전체' }}</p>

      <p>결과는 브라우저 콘솔(F12)을 확인하세요.</p>

    </div>



    <hr>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>공시 제출월</th>
            <th>금융회사명</th>
            <th>상품명</th>
            <th>1개월</th>
            <th>3개월</th>
            <th>6개월</th>
            <th>12개월</th>
            <th>24개월</th>
            <th>36개월</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="product in products" 
            :key="product.id" 
            @click="goDetail(product.id)"
            class="product-row"
          >
            <td>{{ product.dcls_month || '-' }}</td>
            <td>{{ product.kor_co_nm }}</td>
            <td class="product-name">{{ product.fin_prdt_nm }}</td>
            <td>{{ getRate(product, 1) }}</td>
            <td>{{ getRate(product, 3) }}</td>
            <td>{{ getRate(product, 6) }}</td>
            <td>{{ getRate(product, 12) }}</td>
            <td>{{ getRate(product, 24) }}</td>
            <td>{{ getRate(product, 36) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template> -->

<template>
  <div class="product-page">
    <header class="page-header">
      <h1 class="title">금융 상품 탐색</h1>
      <p class="subtitle">나에게 딱 맞는 예적금 상품을 찾아보세요.</p>
    </header>

    <section class="filter-card">
      <div class="filter-group">
        <div class="filter-item">
          <label>은행</label>
          <input 
            v-model="filters.bank" 
            type="text" 
            placeholder="은행명 입력" 
            @input="onSearch"
          />
        </div>
        
        <div class="filter-item">
          <label>상품 종류</label>
          <select v-model="filters.product_type" @change="onSearch">
            <option value="">전체</option>
            <option value="DEPOSIT">정기예금</option>
            <option value="SAVING">적금</option>
          </select>
        </div>

        <div class="filter-item">
          <label>가입 기간</label>
          <select v-model="filters.term" @change="onSearch">
            <option value="">전체</option>
            <option value="6">6개월</option>
            <option value="12">12개월</option>
            <option value="24">24개월</option>
            <option value="36">36개월</option>
          </select>
        </div>
      </div>
    </section>

    <section class="product-list">
      <div v-if="products.length > 0" class="list-container">
        <div 
          v-for="product in products" 
          :key="product.id" 
          class="product-card"
          @click="goDetail(product.id)"
        >
          <div class="card-content">
            <div class="bank-info">
              <span class="bank-name">{{ product.kor_co_nm }}</span>
              <span :class="['product-badge', product.product_type]">
                {{ product.product_type === 'DEPOSIT' ? '예금' : '적금' }}
              </span>
            </div>
            <h3 class="product-name">{{ product.fin_prdt_nm }}</h3>
            
            <div class="rate-info">
              <div class="rate-item">
                <span class="rate-label">6개월</span>
                <span class="rate-value">{{ getRate(product, 6) }}</span>
              </div>
              <div class="rate-item">
                <span class="rate-label">12개월</span>
                <span class="rate-value highlight">O</span>
              </div>
              <div class="rate-item">
                <span class="rate-label">24개월</span>
                <span class="rate-value">{{ getRate(product, 24) }}</span>
              </div>
            </div>
          </div>
          <div class="chevron">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M7 4L13 10L7 16" stroke="#8B95A1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <p>검색 결과가 없습니다.</p>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Base Styles */
.product-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: #ffffff;
  font-family: 'Pretendard', sans-serif;
  color: #191f28;
}

/* Header */
.page-header {
  margin-bottom: 32px;
}
.title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
}
.subtitle {
  color: #4e5968;
  font-size: 16px;
}

/* Filter Card */
.filter-card {
  background-color: #f9fafb;
  border-radius: 24px;
  padding: 24px;
  margin-bottom: 32px;
}
.filter-group {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
.filter-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
  min-width: 150px;
}
.filter-item label {
  font-size: 13px;
  font-weight: 600;
  color: #8b95a1;
  padding-left: 4px;
}
.filter-item input, .filter-item select {
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid #e5e8eb;
  background-color: #ffffff;
  font-size: 15px;
  transition: border-color 0.2s;
}
.filter-item input:focus {
  outline: none;
  border-color: #3182f6;
}

/* Product Card */
.list-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.product-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  background-color: #ffffff;
  border-radius: 24px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.04);
}
.product-card:hover {
  transform: translateY(-2px);
  background-color: #f9fafb;
}

.bank-info {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}
.bank-name {
  font-size: 14px;
  color: #4e5968;
}
.product-badge {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 600;
}
.product-badge.DEPOSIT { background: #e8f3ff; color: #3182f6; }
.product-badge.SAVING { background: #fff0f0; color: #ff4d4f; }

.product-name {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 16px;
}

/* Rate Info Row */
.rate-info {
  display: flex;
  gap: 24px;
}
.rate-item {
  display: flex;
  flex-direction: column;
}
.rate-label {
  font-size: 12px;
  color: #8b95a1;
}
.rate-value {
  font-size: 15px;
  font-weight: 600;
  color: #4e5968;
}
.rate-value.highlight {
  color: #3182f6;
}

.empty-state {
  text-align: center;
  padding: 60px;
  color: #8b95a1;
}
</style>

<script setup>
import { ref, reactive, onMounted } from 'vue';
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

const onSearch = async () => {
  products.value = await productStore.getProducts(filters)

  console.log(products.value)
}

const goDetail = (id) => {
  router.push({ name: 'ProductDetails', params: { id: id } })
}

const getRate = (product, month) => {
  // 현재 데이터 구조에서 save_trm 리스트에 해당 개월이 있는지 확인
  return product.save_trm.includes(month) ? 'O' : '-'
}

onMounted(() => {
  onSearch()
})
</script>

<!-- <style scoped>

</style> -->