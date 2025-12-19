<template>
  <div>
<div class="product-card">
    <h3>{{ product.fin_prdt_nm }}</h3>
    <p>은행명: {{ product.kor_co_nm }}</p>
    <p>저축 기간: {{ product.save_trm.join(', ') }}개월</p>
    <p>공시일: {{ product.dcls_strt_day }}</p>
  </div>
  </div>
</template>

<script setup>
const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>

</style>