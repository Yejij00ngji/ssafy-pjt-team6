<template>
  <div class="results-wrap max-w-md mx-auto min-h-screen bg-white shadow-lg overflow-hidden flex flex-col p-6 font-pretendard">
    
    <div class="text-center mb-8 fade-in">
      <div class="inline-block p-5 bg-blue-50 rounded-full mb-4 shadow-sm">
        <span class="text-4xl">{{ personaIcon }}</span>
      </div>
      <h3 class="text-[11px] font-extrabold text-blue-600 uppercase tracking-[0.2em] mb-1">Financial Persona</h3>
      <h1 class="text-3xl font-bold text-slate-900 mb-2">
        {{ accountStore.financial_profile?.cluster_name || '전략적 자산가' }}
      </h1>
      <p class="text-sm text-slate-500 leading-relaxed px-4">
        {{ accountStore.user?.nickname || '고객' }}님은 현재 자산의 
        <span class="font-bold text-slate-700">{{ investmentRatio }}%</span>를 
        투자 자산으로 운용 중인 {{ accountStore.financial_profile?.cluster_name }}입니다.
      </p>
    </div>

    <div class="report-card bg-slate-50 p-6 rounded-[28px] border border-slate-100 mb-8 shadow-sm">
      <div class="flex justify-between items-center mb-6">
        <h4 class="font-bold text-[13px] text-slate-700 flex items-center gap-2">
          <span class="text-blue-500">📊</span> AI 자산 포트폴리오
        </h4>
        <span class="text-[10px] bg-white px-2 py-1 rounded-md text-slate-400 border border-slate-100">MyData 기반</span>
      </div>

      <div class="chart-container relative mb-6" style="height: 220px;">
        <canvas ref="assetChart" />
        <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none" style="padding-bottom: 25px;">
          <span class="text-[10px] text-slate-400 font-semibold">자산 배분</span>
          <span class="text-lg font-bold text-slate-700">TOP 3</span>
        </div>
      </div>

      <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-50">
        <h5 class="font-bold text-sm mb-2 text-slate-800 flex items-center gap-1">
          📝 AI 진단 결과
        </h5>
        <p class="text-[13.5px] text-slate-600 leading-relaxed">
          연간 약 <span class="font-semibold text-slate-900">{{ (accountStore.financial_profile?.annual_income_amt / 10000).toLocaleString() }}만원</span>의 수익 중 
          <span class="text-red-500 font-semibold">{{ (accountStore.financial_profile?.expense_to_income_ratio * 100).toFixed(1) }}%</span>를 소비하고 계시네요. 
          {{ accountStore.financial_profile?.cluster_name }} 성향에 맞춰 자산을 더 효율적으로 불릴 수 있는 상품을 준비했습니다.
        </p>
      </div>
    </div>

    <div class="flex-grow space-y-4 mb-8">
      <div class="flex justify-between items-end mb-2">
        <div>
          <h4 class="font-bold text-slate-900">🏆 머니:비 꿀단지 TOP 3</h4>
          <p class="text-[12px] text-slate-400 mt-1">성향과 자산 데이터를 교차 분석한 결과입니다.</p>
        </div>
      </div>

      <div id="product-list" class="space-y-4">
        <div v-if="main" 
             @click="apply(main.product_option_id || main.product || main.id)"
             class="relative p-6 border-2 border-blue-500 rounded-[24px] bg-white shadow-xl cursor-pointer transform active:scale-95 transition-all">
          <div class="absolute -top-3 left-6 bg-blue-600 text-white text-[10px] px-3 py-1 rounded-full font-bold shadow-md">AI BEST PICK</div>
          
          <div class="flex justify-between items-start mb-3">
            <span class="text-xs font-semibold text-slate-400">{{ main.kor_co_nm || main.bank_name }}</span>
            <div class="text-right">
              <span class="text-[10px] text-blue-500 block font-bold mb-1">최대 금리</span>
              <span class="text-3xl font-black text-blue-600 leading-none">{{ formatRate(main.intr_rate2) }}</span>
            </div>
          </div>
          
          <h5 class="font-bold text-lg text-slate-900 mb-4">{{ main.fin_prdt_nm || main.product_name }}</h5>

          <div class="bg-blue-50 p-4 rounded-xl border border-blue-100 text-[13px] text-blue-800 leading-snug">
            <div class="flex items-center gap-1 mb-1 font-bold">
              <span>🤖</span> <span>AI 분석 리포트</span>
            </div>
            <p class="opacity-90 leading-relaxed">
              {{ main.ai_analysis?.reason || '사용자님의 공격적인 투자 성향을 고려할 때, 이 상품은 안정적인 목돈 마련의 기초가 될 수 있습니다.' }}
            </p>
          </div>
        </div>

        <div v-for="(item, idx) in sideList" :key="idx" 
             @click="apply(item.id)"
             class="p-5 border border-slate-100 rounded-[20px] bg-white flex justify-between items-center shadow-sm hover:border-blue-200 cursor-pointer transition-colors">
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-1">
              <span class="text-[11px] font-bold text-slate-400 italic">0{{ idx + 2 }}</span>
              <span class="text-[11px] text-slate-400">{{ item.kor_co_nm || item.bank_name }}</span>
            </div>
            <h4 class="font-bold text-slate-800 truncate pr-4">{{ item.fin_prdt_nm || item.product_name }}</h4>
          </div>
          <div class="text-xl font-bold text-slate-700">{{ formatRate(item.intr_rate2) }}</div>
        </div>
      </div>
    </div>

    <button @click="$emit('retry')" 
            class="w-full py-4 text-slate-400 font-bold border-2 border-slate-50 rounded-2xl hover:bg-slate-50 hover:text-slate-600 transition-all">
      진단 다시하기
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import Chart from 'chart.js/auto'
import { useAccountStore } from '@/stores/accounts'
import { useRouter } from 'vue-router'

const props = defineProps({
  recommendations: { type: Array, default: () => [] }
})

const router = useRouter()
const accountStore = useAccountStore()
const assetChart = ref(null)
let chartInstance = null

// --- 계산 로직: 투자 비중 ---
const investmentRatio = computed(() => {
  const profile = accountStore.financial_profile
  if (!profile || !profile.invest_eval_amt) return 0
  const total = profile.invest_eval_amt + profile.balance_amt
  return ((profile.invest_eval_amt / total) * 100).toFixed(1)
})

// --- 페르소나 아이콘 대응 ---
const personaIcon = computed(() => {
  const name = accountStore.financial_profile?.cluster_name || ''
  if (name.includes('공격')) return '🔥'
  if (name.includes('적극')) return '🚀'
  if (name.includes('안정')) return '🛡️'
  return '💰'
})

// --- 상품 노출 제어 ---
const main = computed(() => props.recommendations?.[0] || null)
const sideList = computed(() => props.recommendations?.slice(1, 3) || [])

const formatRate = (r) => (r ? `${Number(r).toFixed(1)}%` : '-')

// --- 실데이터 기반 차트 생성 로직 ---
const buildChartData = () => {
  const profile = accountStore.financial_profile
  
  // 데이터 없을 시 기본값
  if (!profile) return {
    labels: ['데이터 없음'],
    datasets: [{ data: [100], backgroundColor: ['#E2E8F0'] }]
  }

  // 1. 투자자산: invest_eval_amt
  // 2. 저축/예치: balance_amt - withdrawable_amt
  // 3. 비상금(가용): withdrawable_amt
  const invest = profile.invest_eval_amt
  const savings = Math.max(0, profile.balance_amt - profile.withdrawable_amt)
  const emergency = profile.withdrawable_amt
  const total = invest + savings + emergency

  return {
    labels: ['투자자산', '정기저축', '비상금'],
    datasets: [{
      data: [
        ((invest / total) * 100).toFixed(1),
        ((savings / total) * 100).toFixed(1),
        ((emergency / total) * 100).toFixed(1)
      ],
      backgroundColor: ['#3182F6', '#10B981', '#F59E0B'],
      borderWidth: 0,
      hoverOffset: 10
    }]
  }
}

const initChart = () => {
  const el = assetChart.value
  if (!el) return
  const ctx = el.getContext('2d')
  const data = buildChartData()

  if (chartInstance) chartInstance.destroy()

  chartInstance = new Chart(ctx, {
    type: 'doughnut',
    data,
    options: {
      cutout: '72%',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            boxWidth: 10,
            padding: 20,
            font: { size: 12, weight: '600' },
            usePointStyle: true
          }
        },
        tooltip: {
          backgroundColor: '#1E293B',
          titleFont: { size: 13 },
          bodyFont: { size: 13 },
          padding: 12,
          displayColors: false,
          callbacks: {
            label: (ctx) => `비중: ${ctx.raw}%`
          }
        }
      }
    }
  })
}

// 데이터 변경 감지 시 차트 리로드
watch(() => accountStore.financial_profile, initChart, { deep: true })
watch(() => props.recommendations, initChart, { deep: true })

onMounted(() => {
  initChart()
})

const apply = (id) => {
  if (id) router.push({ name: 'Subscribe', params: { id: id } })
}
</script>

<style scoped>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

.font-pretendard {
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
}

.results-wrap {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.fade-in {
  animation: fadeIn 0.6s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.report-card {
  transition: all 0.3s ease;
}

/* 스크롤바 숨기기 */
.results-wrap::-webkit-scrollbar {
  display: none;
}
</style>