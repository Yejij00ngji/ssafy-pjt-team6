<template>
  <div class="toss-container">
    <header class="asset-header">
      <h1 class="toss-title">실시간 시세 조회</h1>
      <p class="toss-desc">금과 은의 글로벌 시세 변동을 한눈에 확인하세요.</p>

      <div class="data-info-badge">
        <span class="info-icon">i</span>
        현재 <strong>2023.01 ~ 2024.12</strong> 기간의 데이터가 제공됩니다.
      </div>
    </header>

    <div class="toss-card control-card">
      <div class="filter-row">
        <div class="toss-tabs">
          <button 
            @click="assetType = 'gold'" 
            :class="['tab-item', { active: assetType === 'gold' }]"
          >금</button>
          <button 
            @click="assetType = 'silver'" 
            :class="['tab-item', { active: assetType === 'silver' }]"
          >은</button>
        </div>

        <div class="date-picker-group">
          <div class="select-wrapper">
            <select v-model="startYear" class="toss-select-s">
              <option value="2023">2023년</option>
              <option value="2024">2024년</option>
            </select>
            <select v-model="startMonth" class="toss-select-s">
              <option v-for="m in monthOptions" :key="m" :value="m">{{ m }}월</option>
            </select>
          </div>

          <span class="date-divider">~</span>

          <div class="select-wrapper">
            <select v-model="endYear" class="toss-select-s">
              <option value="2023">2023년</option>
              <option value="2024">2024년</option>
            </select>
            <select v-model="endMonth" class="toss-select-s">
              <option v-for="m in monthOptions" :key="m" :value="m">{{ m }}월</option>
            </select>
          </div>

          <button @click="fetchData" class="toss-btn-search-s">조회</button>
        </div>
      </div>
    </div>

    <div class="toss-card chart-card">
      <div class="chart-header">
        <h3 class="chart-title">
          <span :class="['dot', assetType]"></span>
          {{ assetType === 'gold' ? '금(Gold)' : '은(Silver)' }} 시세 추이
        </h3>
      </div>
      
      <div class="chart-body">
        <canvas v-show="hasData" id="assetChart"></canvas>
        
        <div v-if="!hasData" class="empty-chart">
          <div class="empty-icon">⚠️</div>
          <p class="empty-text">해당 기간의 데이터가 없습니다.</p>
          <span class="empty-subtext">날짜 범위를 다시 설정해 주세요.</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'
import Chart from 'chart.js/auto'

// --- State 및 초기값 설정 ---
const accountStore = useAccountStore()
const assetType = ref('gold')
const hasData = ref(true)
let chartInstance = null

const startYear = ref('2023')
const startMonth = ref('01')
const endYear = ref('2024')
const endMonth = ref('12')
const monthOptions = Array.from({ length: 12 }, (_, i) => String(i + 1).padStart(2, '0'))

// --- 데이터 통신 로직 ---
const fetchData = async () => {
  // 날짜 유효성 체크
  if (Number(startYear.value + startMonth.value) > Number(endYear.value + endMonth.value)) {
    alert('시작 기간이 종료 기간보다 늦을 수 없습니다.')
    return
  }

  try {
    const params = {
      type: assetType.value,
      start: `${startYear.value}-${startMonth.value}`,
      end: `${endYear.value}-${endMonth.value}`
    }
    
    const { data } = await axios.get(`${accountStore.API_URL}/externals/asset-prices/`, { params })

    if (data && data.length > 0) {
      data.sort((a, b) => new Date(a.date) - new Date(b.date))
      hasData.value = true
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
    hasData.value = false
  }
}

// --- 차트 렌더링 로직 ---
const renderChart = (data) => {
  const ctx = document.getElementById('assetChart').getContext('2d')
  if (chartInstance) chartInstance.destroy()

  const isGold = assetType.value === 'gold'
  const accentColor = isGold ? '#FFD700' : '#8B95A1'

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.map(item => item.date),
      datasets: [{
        label: `${assetType.value.toUpperCase()} ($)`,
        data: data.map(item => item.price),
        borderColor: accentColor,
        backgroundColor: isGold ? 'rgba(255, 215, 0, 0.1)' : 'rgba(139, 149, 161, 0.1)',
        borderWidth: 3,
        fill: true,
        pointRadius: 0,
        pointHoverRadius: 5,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { 
          grid: { display: false }, 
          ticks: { color: '#8B95A1', font: { size: 12 } } 
        },
        y: { 
          position: 'right', // 금융 앱 스타일로 우측 배치
          beginAtZero: false, 
          grid: { color: '#F2F4F6' },
          ticks: { color: '#8B95A1', font: { size: 12 } },
          // --- Y축 설명(Title) 추가 부분 ---
          title: {
            display: true,
            text: '가격 (USD)', // 표시될 문구
            color: '#8B95A1',  // 보조 텍스트 색상
            font: {
              size: 13,
              weight: '600',
              family: 'Pretendard'
            },
            padding: { bottom: 10 }
          }
        }
      }
    }
  })
}

// --- Watchers & Lifecycle ---
watch(assetType, () => fetchData())
onMounted(() => fetchData())
</script>

<style scoped>
/* 1. Header & Badge */
.data-info-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: #f2f4f6;
  padding: 10px 16px;
  border-radius: 12px;
  font-size: 14px;
  color: #4e5968;
  margin-bottom: 24px;
}
.info-icon {
  display: flex;
  align-items: center; justify-content: center;
  width: 18px; height: 18px;
  background-color: #8b95a1;
  color: #fff; border-radius: 50%;
  font-size: 11px; font-weight: bold;
}
.data-info-badge strong { color: var(--toss-blue); }

/* 2. Control Card */
.control-card { margin-bottom: 24px; padding: 16px 24px; }
.filter-row {
  display: flex; justify-content: space-between;
  align-items: center; flex-wrap: wrap; gap: 16px;
}

/* Tabs */
.toss-tabs { background-color: #EEEFEE; padding: 4px; border-radius: 12px; display: flex; }
.tab-item {
  border: none; background: none; padding: 8px 24px;
  border-radius: 10px; font-weight: 600; color: #4e5968;
  cursor: pointer; transition: all 0.2s;
}
.tab-item.active {
  background-color: #fff; color: #191f28;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Selects */
.date-picker-group { display: flex; align-items: center; gap: 8px; }
.select-wrapper { display: flex; gap: 4px; }
.toss-select-s {
  border: 1px solid var(--toss-border);
  background-color: #fff; padding: 8px 12px;
  border-radius: 10px; font-size: 14px;
  color: #191f28; outline: none; cursor: pointer;
}
.date-divider { color: #8b95a1; font-weight: 600; }
.toss-btn-search-s {
  background-color: #e8f3ff; color: var(--toss-blue);
  border: none; padding: 8px 16px; border-radius: 10px;
  font-weight: 700; cursor: pointer;
}

/* 3. Chart Card */
.chart-card { background-color: #fff; min-height: 480px; display: flex; flex-direction: column; }
.chart-header { margin-bottom: 30px; }
.chart-title { display: flex; align-items: center; gap: 8px; font-size: 18px; font-weight: 700; }
.dot { width: 10px; height: 10px; border-radius: 50%; }
.dot.gold { background-color: #FFD700; }
.dot.silver { background-color: #8B95A1; }

.chart-body { flex-grow: 1; position: relative; }
.empty-chart {
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%); text-align: center;
}
.empty-icon { font-size: 40px; margin-bottom: 12px; }
.empty-text { font-weight: 600; color: #191f28; }
.empty-subtext { font-size: 14px; color: #8b95a1; }

@media (max-width: 768px) {
  .filter-row { flex-direction: column; align-items: stretch; }
  .toss-tabs { width: 100%; }
  .tab-item { flex: 1; }
}
</style>