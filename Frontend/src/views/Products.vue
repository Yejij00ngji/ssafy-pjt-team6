<template>
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
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useProductStore } from '@/stores/products'

const router = useRouter();

const productStore = useProductStore()

const products = ref([]);
const filters = reactive({
  bank: '',
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

<style scoped>

</style>