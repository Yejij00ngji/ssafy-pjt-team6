<template>
  <div class="step-content">
    <h1 class="toss-title">
      나에게 딱 맞는 <br />
      예적금을 찾아볼까요?
    </h1>
    <p class="toss-desc">방식을 선택하면 분석을 시작합니다.</p>

    <div class="card-group">
      <div 
        class="toss-card select-card" 
        :class="isMyData ? 'is-linked' : ''"
        @click="handleMyDataClick"
      >
        <span class="icon">{{ isMyData ? '✅' : '⚡️' }}</span>
        <div class="card-text">
          <strong class="toss-title-sub">
            {{ isMyData ? '마이데이터 분석 시작' : '마이데이터 연결' }}
          </strong>
          <p class="toss-desc-sub">
            {{ isMyData ? '이미 연결된 자산 정보로 진단' : '30초 만에 가장 정확한 추천' }}
          </p>
        </div>
      </div>

      <div class="toss-card select-card" @click="$emit('next', { agreed: false })">
        <span class="icon">📝</span>
        <div class="card-text">
          <strong class="toss-title-sub">직접 입력하기</strong>
          <p class="toss-desc-sub">간단한 질문으로 성향 파악</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  isMyData: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['next'])
const router = useRouter()

const handleMyDataClick = () => {
  if (props.isMyData) {
    // 1. 이미 연동된 경우: LoadingItem -> ResultsStepItem으로 진행
    emit('next', { agreed: true })
  } else {
    // 2. 미연동인 경우: 사용자에게 선택지 제공
    const confirmConnect = window.confirm(
      "현재 마이데이터가 연결되어 있지 않습니다.\n프로필 설정 페이지에서 자산을 연결하시겠습니까?"
    )
    
    if (confirmConnect) {
      // 프로필 수정 페이지(마이데이터 입력란이 있는 곳)로 이동
      router.push({ name: 'ProfileUpdate' }) 
    } else {
      // 연결 안 할 경우 바로 설문 단계로 유도
      emit('next', { agreed: false })
    }
  }
}
</script>

<style scoped>
.step-content {
  animation: fadeIn 0.5s ease-out;
}

.toss-title {
  font-size: 26px;
  font-weight: 700;
  line-height: 1.4;
  color: #191f28;
  margin-bottom: 8px;
}

.toss-desc {
  font-size: 16px;
  color: #4e5968;
}

.card-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 40px;
}

.toss-card {
  background-color: #ffffff;
  border-radius: 20px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.select-card {
  display: flex;
  align-items: center;
  gap: 20px;
  border: 1px solid #f2f4f6;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

.select-card:hover {
  border-color: #3182f6;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(49, 130, 246, 0.08);
}

.select-card.is-linked {
  border-color: #3182f6;
  background-color: #f9fbff;
}

.icon { font-size: 32px; }

.card-text { display: flex; flex-direction: column; }

.toss-title-sub {
  font-size: 18px;
  font-weight: 600;
  color: #191f28;
}

.toss-desc-sub {
  font-size: 14px;
  color: #8b95a1;
  margin-top: 4px;
}

</style>