<template>
  <div class="profile-container">
    <h1>내 프로필</h1>
    
    <div v-if="accountStore.user" class="user-info">
      <p><strong>사용자명:</strong> {{ accountStore.user.username }}</p>
      <p><strong>내 데이터 동의 여부:</strong> {{ accountStore.isMyData ? '동의' : '미동의' }}</p>
    </div>

    <hr>

    <h2>가입한 상품 내역</h2>
    <div v-if="accountStore.subscriptions && accountStore.subscriptions.length > 0" class="table-container">
      <table>
        <thead>
          <tr>
            <th>가입일</th>
            <th>은행명</th>
            <th>상품명</th>
            <th>저축 기간</th>
            <th>가입 금액</th>
            <th>금리</th>
            <th>만기 예정일</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sub in accountStore.subscriptions" :key="sub.id">
            <td>{{ sub.subscribed_at }}</td>
            <td>{{ sub.bank_name }}</td>
            <td class="product-name">{{ sub.product_name }}</td>
            <td>{{ sub.save_trm }}개월</td>
            <td>{{ sub.amounts.toLocaleString() }}원</td>
            <td class="rate">{{ sub.intr_rate2 }}%</td>
            <td>{{ sub.expired_at || '정보 없음' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="no-data">
      <p>가입한 상품 내역이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const accountStore = useAccountStore()

onMounted(async () => {
  // 컴포넌트가 로드될 때 가입 내역을 가져옵니다.
  await accountStore.getSubscriptions()
})
</script>

<style scoped>

</style>