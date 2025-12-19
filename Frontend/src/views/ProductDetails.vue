<template>
  <div v-if="product" class="detail-container">
    <h1>{{ product.fin_prdt_nm }}</h1>
    <hr>
    <button @click="$router.back()">뒤로가기</button>
    <div class="info-card">
      <p><strong>금융회사:</strong> {{ product.kor_co_nm }}</p>
      <p><strong>공시 시작일:</strong> {{ product.dcls_strt_day }}</p>
      <p><strong>가입 방법:</strong> {{ product.join_way }}</p>
      <p><strong>우대 조건:</strong> {{ product.spcl_cnd }}</p>
    </div>
  </div>

<h2 class="option-title">금리 옵션 안내</h2>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>저축 기간</th>
            <th>금리 유형</th>
            <th>저축 금리</th>
            <th>최고 우대금리</th>
            <th>가입</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="option in product.options" 
            :key="option.id" 
            @click="goOptionApply(option.id)"
            class="option-row"
          >
            <td>{{ option.save_trm }}개월</td>
            <td>{{ option.intr_rate_type_nm }}</td>
            <td class="rate">{{ option.intr_rate }}%</td>
            <td class="rate2">{{ option.intr_rate2 }}%</td>
            <td><button class="apply-btn">O</button></td>
          </tr>
        </tbody>
      </table>
    </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useProductStore } from '@/stores/products'
import { ref, onMounted } from 'vue'

const route = useRoute()
const router = useRouter();
const productStore = useProductStore()

const product = ref([])

const goOptionApply = (id) => {
    router.push({ name: 'Subscribe', params: { id: id } })
}

onMounted(async () => {
  product.value = await productStore.getProductDetails(route.params.id)
})
</script>

<style scoped>

</style>