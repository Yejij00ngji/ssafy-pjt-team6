<template>
  <div class="step-container center">
    <div class="loader-wrapper">
      <div class="scanner-box">
        <div class="moving-bar"></div>
        <div class="logo-track">
          <span v-for="icon in bankIcons" :key="icon" class="bank-icon">{{ icon }}</span>
        </div>
      </div>
      
      <h2 class="loading-title">{{ displayTitle }}</h2>
      <p class="loading-sub">{{ displaySub }}</p>
    </div>

    <div class="progress-container">
      <div class="progress-bar" :style="{ width: progress + '%' }"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const props = defineProps({
  isMyData: Boolean // 부모로부터 동의 여부를 전달받음
})

const emit = defineEmits(['next'])
const progress = ref(0)
const bankIcons = ['🏦', '💳', '💰', '📉', '💵', '🏛️', '💎']

const displayTitle = computed(() => 
  props.isMyData ? '금융 정보를 불러오고 있어요' : '성향 분석을 시작합니다'
)

const displaySub = computed(() => 
  props.isMyData 
    ? '연결된 기관에서 자산 데이터를 안전하게 가져오는 중입니다.' 
    : '입력하신 정보를 바탕으로 가장 유사한 그룹을 찾는 중이에요.'
)

onMounted(() => {
  // 3초간 프로그레스 바가 차오른 뒤 결과 페이지로 이동
  const interval = setInterval(() => {
    progress.value += 1
    if (progress.value >= 100) {
      clearInterval(interval)
      setTimeout(() => emit('next'), 500) // 100% 도달 후 살짝 대기했다가 이동
    }
  }, 30)
})
</script>

<style scoped>
.step-container.center {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px;
  height: 100vh;
  text-align: center;
}

/* 스캐너 애니메이션 */
.scanner-box {
  position: relative;
  width: 100px;
  height: 120px;
  background: #f9fafb;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 32px;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid #e5e8eb;
}

.moving-bar {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: #00ad7c;
  box-shadow: 0 0 10px #00ad7c;
  animation: scan 2s infinite ease-in-out;
  z-index: 2;
}

.logo-track {
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: scrollLogos 5s infinite linear;
}

.bank-icon { font-size: 30px; }

/* 텍스트 스타일 */
.loading-title { font-size: 22px; font-weight: 700; color: #191f28; margin-bottom: 12px; }
.loading-sub { font-size: 15px; color: #8b95a1; line-height: 1.5; }

/* 하단 바 */
.progress-container {
  position: absolute;
  bottom: 80px;
  width: calc(100% - 80px);
  height: 4px;
  background: #f2f4f6;
  border-radius: 2px;
}
.progress-bar {
  height: 100%;
  background: #00ad7c;
  border-radius: 2px;
  transition: width 0.1s linear;
}

@keyframes scan {
  0% { top: 0; }
  50% { top: 100%; }
  100% { top: 0; }
}

@keyframes scrollLogos {
  0% { transform: translateY(50px); }
  100% { transform: translateY(-150px); }
}
</style>