<template>
<div class="subscription-container">
    <h1>상품 가입하기</h1>
    <hr>
    
    <div class="input-group">
      <label for="amounts">가입 금액 (원)</label>
      <input 
        id="amounts"
        v-model.number="payload.amounts" 
        type="number" 
        placeholder="가입하실 금액을 입력하세요"
      >
    </div>

    <div class="info-text">
      <p>선택하신 옵션 번호: <strong>{{ payload.product_option }}</strong></p>
      <p>최종 가입 금액: <strong>{{ payload.amounts.toLocaleString() }}</strong> 원</p>
    </div>

    <div class="button-group">
      <button @click="onSubscribe" class="subscribe-btn">가입 완료</button>
      <button @click="$router.back()" class="cancel-btn">취소</button>
    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useProductStore } from '@/stores/products'
import { ref } from 'vue'

const route = useRoute()
const router = useRouter()
const productStore = useProductStore()

const payload = ref({
  product_option: route.params.id,
  amounts: 0,
})

const onSubscribe = async () => {
  if (payload.value.amounts <= 0) {
    alert('가입 금액을 0원 이상 입력해 주세요.')
    return
  }

  if (confirm('정말로 이 상품에 가입하시겠습니까?')) {
    try {
      // Store의 subscribeProduct 호출
      await productStore.subscribeProduct({
        product_option: payload.value.product_option,
        amounts: payload.value.amounts
      })
      
      alert('가입이 완료되었습니다!')
      router.push({ name: 'Profile' }) // 가입 후 프로필 페이지 등으로 이동
    } catch (err) {
      console.error(err)
      alert('가입 처리 중 오류가 발생했습니다.')
    }
  }
}
</script>

<style scoped>

</style>