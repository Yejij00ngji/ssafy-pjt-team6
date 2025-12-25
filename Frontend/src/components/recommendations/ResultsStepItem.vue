<template>
  <div class="results-wrap max-w-md mx-auto min-h-screen bg-white shadow-lg overflow-hidden flex flex-col p-6">
    <!-- Persona -->
    <div class="text-center mb-6">
      <div class="inline-block p-5 bg-blue-50 rounded-full mb-4">
        <span class="text-4xl" v-html="persona.icon || '✈️'"></span>
      </div>
      <h3 class="text-[10px] font-bold text-blue-600 uppercase tracking-[0.2em] mb-1">Financial Persona</h3>
      <h1 class="text-3xl font-bold text-slate-900" id="persona-name">{{ persona.name || '분석가형' }}</h1>
      <p class="text-sm text-slate-500 mt-2">{{ persona.description }}</p>
    </div>

    <!-- AI Report + Chart -->
    <div class="report-card bg-slate-50 p-6 rounded-[24px] border border-slate-100 mb-6">
      <h4 class="font-bold mb-4 text-xs text-slate-400 uppercase tracking-tight">📊 AI 자산 분석 리포트</h4>
      <div class="chart-wrap mb-4 px-2">
        <canvas ref="assetChart" />
      </div>

      <!-- 금융 리포트 (차트 아래) -->
      <div class="bg-white p-4 rounded-2xl text-sm text-slate-600 leading-relaxed shadow-sm mt-3">
        <h5 class="font-semibold text-sm mb-2">금융 리포트</h5>
        <p id="report-text" class="text-[14px]">{{ reportText }}</p>
      </div>
    </div>

    <!-- TOP 3 상품 -->
    <div class="space-y-4 mb-6 flex-grow">
      <div class="flex justify-between items-center mb-2">
        <div>
          <h4 class="font-bold text-sm">🏆 맞춤 추천 상품</h4>
          <p class="text-[12px] text-slate-400 mt-1">데이터 기반으로 엄선된 상위 3개 상품입니다.</p>
        </div>
        <span class="text-[10px] text-slate-400">데이터 업데이트: 오늘</span>
      </div>

      <!-- 넛지 배너: 상위 상품의 nudge를 강조 -->
      <div v-if="main && (main.ai_analysis?.nudge || main.nudge)" class="nudge-banner p-3 rounded-xl bg-yellow-50 border border-yellow-100 text-sm text-yellow-800 mb-3">
        💡 {{ main.ai_analysis?.nudge || main.nudge }}
      </div>

      <div id="product-list" class="space-y-3 pb-6">
        <div v-if="main" class="relative p-6 border-2 border-blue-500 rounded-[20px] bg-white shadow-xl">
          <div class="absolute -top-3 left-6 bg-blue-600 text-white text-[10px] px-3 py-1 rounded-full font-bold">AI BEST PICK</div>
          <div class="flex justify-between items-start mb-4">
            <span class="text-xs text-slate-400">{{ main.bank_name || main.kor_co_nm }}</span>
            <span class="text-3xl font-black text-blue-600">{{ formatRate(main.intr_rate2) }}</span>
          </div>
          <h5 class="font-bold text-lg mb-3">{{ main.product_name || main.fin_prdt_nm }}</h5>

          <!-- 1위에만 AI 리포트/사유 표시 -->
          <div class="bg-blue-50 p-4 rounded-2xl border border-blue-100 text-[13px] text-blue-900 leading-snug mb-4">
            <strong>🤖 AI 가이드:</strong>
            <p class="mt-1 opacity-90">{{ main.ai_analysis?.report || main.reason || '데이터 기반 추천입니다.' }}</p>
            <p v-if="main.ai_analysis?.reason || main.reason" class="mt-2 text-sm text-slate-600">추천 이유: {{ main.ai_analysis?.reason || main.reason }}</p>
          </div>

          <!-- CTA with nudge -->
          <div class="flex gap-3">
            <button class="flex-1 py-3 bg-blue-600 text-white rounded-xl font-bold" @click="apply(main.product_option_id || main.product_option?.id)">
              가입하러 가기
            </button>
            <button v-if="main.ai_analysis?.nudge || main.nudge" class="py-3 px-3 bg-yellow-50 text-yellow-800 rounded-xl border border-yellow-100 text-sm" @click="showNudgeInfo(main)">
              넛지 보기
            </button>
          </div>
        </div>

        <div v-if="side(1)" class="p-4 border rounded-xl bg-white flex justify-between items-center">
          <div>
            <p class="text-xs text-slate-400">{{ side(1).bank_name || side(1).kor_co_nm }}</p>
            <h4 class="font-semibold">{{ side(1).product_name || side(1).fin_prdt_nm }}</h4>
            <p class="text-xs text-slate-400 mt-1">{{ side(1).reason || '데이터 기반 추천' }}</p>
          </div>
          <div class="text-xl font-bold text-slate-700">{{ formatRate(side(1).intr_rate2) }}</div>
        </div>

        <div v-if="side(2)" class="p-4 border rounded-xl bg-white flex justify-between items-center">
          <div>
            <p class="text-xs text-slate-400">{{ side(2).bank_name || side(2).kor_co_nm }}</p>
            <h4 class="font-semibold">{{ side(2).product_name || side(2).fin_prdt_nm }}</h4>
            <p class="text-xs text-slate-400 mt-1">{{ side(2).reason || '데이터 기반 추천' }}</p>
          </div>
          <div class="text-xl font-bold text-slate-700">{{ formatRate(side(2).intr_rate2) }}</div>
        </div>
      </div>
    </div>

    <button @click="$emit('retry')" class="w-full py-4 text-slate-500 font-bold border-2 border-slate-50 rounded-2xl hover:text-slate-700 transition-colors">
      다시 진단하기
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import Chart from 'chart.js/auto'
import { useAccountStore } from '@/stores/accounts'
import { useRouter } from 'vue-router'

const props = defineProps({
  isMyData: Boolean,
  userName: { type: String, default: '사용자' },
  cluster: { type: [Number, String, Object], default: 0 },
  recommendations: { type: Array, default: () => [] }
})

const router = useRouter()
const accountStore = useAccountStore()
const assetChart = ref(null)
let chartInstance = null

const persona = computed(() => {
  if (props.cluster && typeof props.cluster === 'object') return props.cluster
  return {
    name: accountStore.user?.nickname || '분석가형',
    icon: '💰',
    description: `${accountStore.user?.nickname || '고객'}님의 금융 성향을 바탕으로 분석했습니다.`
  }
})

const reportText = computed(() => {
  const main = props.recommendations?.[0]
  if (main?.ai_analysis?.report) return main.ai_analysis.report
  if (main?.report) return main.report
  if (main?.reason) return main.reason
  return '현재 수입 대비 지출 비중이 높습니다. 비상금 마련을 권장합니다.'
})

const main = computed(() => props.recommendations?.[0] || null)
const side = (i) => props.recommendations?.[i] || null

const formatRate = (r) => {
  if (r === undefined || r === null) return '-'
  return `${Number(r).toFixed(1)}%`
}

const buildChartData = () => {
  const data = {
    labels: ['소비', '저축', '투자'],
    datasets: [{
      data: [70, 20, 10],
      backgroundColor: ['#3b82f6', '#94a3b8', '#f1f5f9'],
      hoverOffset: 4,
      borderWidth: 0
    }]
  }
  return data
}

const initChart = () => {
  const el = assetChart.value
  if (!el) return
  const ctx = el.getContext('2d')
  if (chartInstance) chartInstance.destroy()
  chartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: buildChartData(),
    options: {
      cutout: '70%',
      responsive: true,
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 8, font: { size: 10, weight: '600' }, padding: 16 } }
      }
    }
  })
}

onMounted(() => {
  initChart()
})

watch(() => props.recommendations, () => {
  initChart()
}, { deep: true })

// CTA helpers
const apply = (optionId) => {
  if (!optionId) {
    alert('상품 정보가 준비되지 않았습니다.')
    return
  }
  router.push({ name: 'Subscribe', params: { id: optionId } })
}

const showNudgeInfo = (item) => {
  const n = item.ai_analysis?.nudge || item.nudge || '지금 가입하시면 추가 혜택을 받을 수 있습니다.'
  alert(n)
}
</script>

<style scoped>
.results-wrap { font-family: 'Pretendard', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; background:#fff; color:#0f172a; }
.report-card { background: #f8fafc; }
.nudge-banner { font-size: 13px; }
@media (max-width: 420px){ .results-wrap { padding: 16px; } }
.fade-in { animation: fadeIn 0.45s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
</style>