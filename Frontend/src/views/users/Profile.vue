<template>
  <div class="profile-container">
    <h1>내 프로필</h1>
    
    <div v-if="accountStore.user" class="user-info">
      <p><strong>사용자명:</strong> {{ accountStore.user.username }}</p>
      <p><strong>내 데이터 동의 여부:</strong> {{ accountStore.isMyData ? '동의' : '미동의' }}</p>
    </div>

    <hr>

    <h2>상품별 금리 비교</h2>
    <div v-if="productStore.subscriptions && productStore.subscriptions.length > 0" class="chart-wrapper">
      <canvas id="rateChart"></canvas>
    </div>

    <hr>

    <h2>가입한 상품 내역</h2>
    <div v-if="productStore.subscriptions && productStore.subscriptions.length > 0" class="table-container">
      <table>
        <thead>
          <tr>
            <th>가입일</th>
            <th>은행명</th>
            <th>상품명</th>
            <th>저축 기간</th>
            <th>가입 금액</th>
            <th>기본 금리</th>
            <th>우대 금리</th>
            <th>만기 예정일</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sub in productStore.subscriptions" :key="sub.id">
            <td>{{ sub.subscribed_at }}</td>
            <td>{{ sub.bank_name }}</td>
            <td class="product-name">{{ sub.product_name }}</td>
            <td>{{ sub.save_trm }}개월</td>
            <td>{{ sub.amount.toLocaleString() }}원</td>
            <td class="rate">{{ sub.intr_rate }}%</td>
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
import { onMounted, watch, ref } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import Chart from 'chart.js/auto'
import { useProductStore } from '@/stores/products'

const accountStore = useAccountStore()
const productStore = useProductStore()
let rateChart = null

// 차트를 그리는 함수
const renderChart = () => {
  const ctx = document.getElementById('rateChart')
  if (!ctx) return
  
  // 기존 차트가 있으면 파괴 (재랜더링 시 충돌 방지)
  if (rateChart) {
    rateChart.destroy()
  }

  const subscriptions = productStore.subscriptions
  
  // 차트 데이터 가공 (상품명 + 기간을 라벨로 사용)
  const labels = subscriptions.map(sub => `${sub.product_name}(${sub.save_trm}M)`)
  const baseRates = subscriptions.map(sub => sub.intr_rate)
  const maxRates = subscriptions.map(sub => sub.intr_rate2)

  rateChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: '기본 금리 (%)',
          data: baseRates,
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        },
        {
          label: '우대 금리 (%)',
          data: maxRates,
          backgroundColor: 'rgba(255, 99, 132, 0.5)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: '금리 (%)'
          }
        }
      },
      plugins: {
        legend: {
          position: 'top',
        },
        tooltip: {
          mode: 'index',
          intersect: false
        }
      }
    }
  })
}

onMounted(async () => {
  // 컴포넌트가 로드될 때 가입 내역을 가져옵니다.
  await productStore.getSubscriptions()
  renderChart()
})

// 데이터가 비동기로 로드될 경우를 대비해 watch 추가
watch(() => productStore.subscriptions, () => {
  renderChart()
}, { deep: true })
</script>

<style scoped>

</style>