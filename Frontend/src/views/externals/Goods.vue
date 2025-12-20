<template>
  <div>
    <h1>
      현물 상품 시각화
    </h1>
  </div>
  <hr>
  <div class="asset-container">
    <h2>금/은 시세 변동 그래프</h2>

    <div class="filter-controls">
      <div class="asset-buttons">
        <a href="#" @click.prevent="assetType = 'gold'" :class="{ active: assetType === 'gold' }">금(Gold)</a>
        <span> | </span>
        <a href="#" @click.prevent="assetType = 'silver'" :class="{ active: assetType === 'silver' }">은(Silver)</a>
      </div>
      
      <div class="date-picker">
        <input type="date" v-model="startDate"> ~
        <input type="date" v-model="endDate">
        <button @click="fetchData" class="search-btn">조회</button>
      </div>
    </div>

    <hr>

    <div class="chart-wrapper">
      <canvas v-show="hasData" id="assetChart"></canvas>
      
      <div v-if="!hasData" class="no-data-overlay">
        <p>⚠️ 선택하신 기간 및 조건에 해당하는 데이터가 없습니다.</p>
        <span>날짜 범위를 다시 설정해 주세요.</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'
import Chart from 'chart.js/auto'

const accountStore = useAccountStore()

const assetType = ref('gold')
const startDate = ref('')
const endDate = ref('')
const hasData = ref(true)
let chartInstance = null

const fetchData = async () => {
  try {
    const params = {
      type: assetType.value,
      start: startDate.value,
      end: endDate.value
    }
    
    const response = await axios.get(`${accountStore.API_URL}/externals/asset-prices/`, { params })
    const data = response.data

    if (data && data.length > 0) {
      hasData.ref = true
      await nextTick()
      renderChart(data)
    } else {
      hasData.value = false
      if (chartInstance) {
        chartInstance.destroy()
        chartInstance = null
      }
    }
  } catch (error) {
    console.error('데이터 로드 실패:', error)
    alert('데이터를 불러오는 중 오류가 발생했습니다.')
  }
}

// Chart.js를 그리는 함수
const renderChart = (data) => {
  const ctx = document.getElementById('assetChart').getContext('2d')
  
  if (chartInstance) {
    chartInstance.destroy()
  }

  const labels = data.map(item => item.date)
  const prices = data.map(item => item.price)

  chartInstance = new Chart(ctx, {
    type: 'line', // 변동 그래프는 선 그래프(line)가 적합합니다.
    data: {
      labels: labels,
      datasets: [{
        label: `${assetType.value.toUpperCase()} 가격 (USD)`,
        data: prices,
        borderColor: assetType.value === 'gold' ? '#f1c40f' : '#bdc3c7',
        backgroundColor: assetType.value === 'gold' ? 'rgba(241, 196, 15, 0.2)' : 'rgba(189, 195, 199, 0.2)',
        borderWidth: 2,
        fill: true,
        pointRadius: 1,
        tension: 0.1 // 선의 곡률
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          grid: { display: false }
        },
        y: {
          beginAtZero: false, // 시세 데이터이므로 0부터 시작할 필요 없음
          title: { display: true, text: '가격 ($)' }
        }
      }
    }
  })
}

// 자산 타입이 바뀌면 자동으로 다시 조회
watch(assetType, () => {
  fetchData()
})

onMounted(() => {
  fetchData()
})
</script>

<style scoped>

</style>