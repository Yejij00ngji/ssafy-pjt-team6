<template>
  <div class="toss-container-narrow center">
    <div class="loader-visual">
      <div v-if="isMyData" class="scanner-box">
        <div class="moving-bar"></div>
        <div class="logo-track">
          <span v-for="icon in bankIcons" :key="icon" class="bank-icon">{{ icon }}</span>
        </div>
      </div>

      <div v-else class="pulse-wrapper">
        <div class="pulse-ring"></div>
        <div class="ai-icon">🤖</div>
      </div>
    </div>
    
    <div class="text-group">
      <h2 class="toss-title">{{ displayTitle }}</h2>
      <p class="toss-desc">{{ displaySub }}</p>
    </div>

    <div class="progress-container">
      <div class="progress-bar" :style="{ width: progress + '%' }"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const props = defineProps({ isMyData: Boolean })
const emit = defineEmits(['next'])

const progress = ref(0)
const bankIcons = ['🏦', '💳', '💰', '💵', '🏛️']

const displayTitle = computed(() => 
  props.isMyData ? '금융 정보를 불러오고 있어요' : '성향 분석을 시작합니다'
)

const displaySub = computed(() => 
  props.isMyData 
    ? '기관에서 데이터를 안전하게 가져오는 중입니다.' 
    : '입력하신 정보를 바탕으로 그룹을 찾는 중이에요.'
)

onMounted(() => {
  const interval = setInterval(() => {
    progress.value += 2
    if (progress.value >= 100) {
      clearInterval(interval)
      setTimeout(() => emit('next'), 500)
    }
  }, 40)
})
</script>

<style scoped>
/* 레이아웃 간략화 */
.center {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  height: 80vh; text-align: center;
}

.loader-visual { margin-bottom: 40px; position: relative; width: 120px; height: 120px; display: flex; align-items: center; justify-content: center; }

/* A. 마이데이터 스캐너 (기존 로직 유지 + 변수 적용) */
.scanner-box {
  width: 100px; height: 120px; background: var(--toss-gray-bg);
  border-radius: 16px; overflow: hidden; border: 1px solid var(--toss-border);
}
.moving-bar {
  position: absolute; top: 0; left: 0; width: 100%; height: 4px;
  background: var(--toss-blue); box-shadow: 0 0 10px var(--toss-blue);
  animation: scan 2s infinite ease-in-out; z-index: 2;
}
.logo-track { display: flex; flex-direction: column; gap: 20px; animation: scrollLogos 5s infinite linear; opacity: 0.5; }
.bank-icon { font-size: 30px; }

/* B. 미동의자 펄스 링 (추가) */
.pulse-wrapper { position: relative; display: flex; align-items: center; justify-content: center; }
.ai-icon { font-size: 40px; z-index: 2; }
.pulse-ring {
  position: absolute; width: 60px; height: 60px;
  border: 4px solid var(--toss-blue); border-radius: 50%;
  animation: pulse-ani 2s infinite;
}

/* 하단 프로그레스 바 (간략화) */
.progress-container {
  position: absolute; bottom: 80px; width: 240px; height: 4px;
  background: var(--toss-gray-bg); border-radius: 2px;
}
.progress-bar {
  height: 100%; background: var(--toss-blue);
  border-radius: 2px; transition: width 0.1s linear;
}

/* 애니메이션 */
@keyframes scan { 0%, 100% { top: 0; } 50% { top: 100%; } }
@keyframes scrollLogos { 0% { transform: translateY(50px); } 100% { transform: translateY(-150px); } }
@keyframes pulse-ani { 0% { transform: scale(0.8); opacity: 0.8; } 100% { transform: scale(1.8); opacity: 0; } }
</style>