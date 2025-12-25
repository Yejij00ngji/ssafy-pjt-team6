<template>
  <div class="step-content">
    <h1 class="toss-title">
      나에게 딱 맞는 <br />
      예적금을 찾아볼까요?
    </h1>
    <p class="toss-desc">방식을 선택하면 분석을 시작합니다.</p>

    <div class="card-group">
      <div v-if="isMyData">
        <div 
          class="toss-card select-card is-linked" 
          @click="handleMyDataClick"
        >
          <span class="icon">✅</span>
          <div class="card-text">
            <strong class="toss-title-sub">마이데이터 분석 시작</strong>
            <p class="toss-desc-sub">이미 연결된 자산 정보로 진단</p>
          </div>
        </div>
      </div>

      <!-- <div v-else>
        <div class="toss-card select-card" @click="handleMyDataClick">
          <span class="icon">⚡️</span>
          <div class="card-text">
            <strong class="toss-title-sub">마이데이터 연결</strong>
            <p class="toss-desc-sub">30초 만에 가장 정확한 추천</p>
          </div>
        </div>
      </div> -->

      <div v-else>
        <div class="toss-card select-card" @click="$emit('next', { agreed: false })">
          <span class="icon">📝</span>
          <div class="card-text">
            <strong class="toss-title-sub">직접 입력하기</strong>
            <p class="toss-desc-sub">간단한 질문으로 성향 파악</p>
          </div>
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
    emit('next', { agreed: true })
  } else {
    const confirmConnect = window.confirm(
      "현재 마이데이터가 연결되어 있지 않습니다.\n프로필 설정 페이지에서 자산을 연결하시겠습니까?"
    )
    
    if (confirmConnect) {
      router.push({ name: 'Profile' }) 
    } else {
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
  margin-bottom: 12px;
}

.toss-desc {
  font-size: 16px;
  color: #4e5968;
}

.card-group {
  display: flex;
  flex-direction: column;
  gap: 12px; /* 간격을 살짝 좁혀 응집도를 높임 */
  margin-top: 40px;
}

/* 카드 공통 스타일 통합 */
.toss-card {
  background-color: #ffffff;
  border-radius: 22px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); /* 부드러운 토스식 애니메이션 */
  display: flex;
  align-items: center;
  gap: 20px;
  border: 1px solid transparent; /* 기본 보더 투명 처리 */
  background-color: #f9fafb; /* 기본 배경색 */
}

/* 모든 선택 가능한 카드에 동일한 Hover 효과 적용 */
.select-card:hover {
  background-color: #ffffff;
  transform: translateY(-4px); /* 조금 더 들리는 느낌 */
  border-color: rgba(49, 130, 246, 0.1);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.05);
}

/* 클릭 시 슥 눌리는 효과 추가 */
.select-card:active {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.02);
}

/* 마이데이터 연동 완료 시 특수 스타일 (기본 상태) */
.select-card.is-linked {
  background-color: #f2f8ff; /* 연한 파란색 톤 */
  border: 1px solid rgba(49, 130, 246, 0.2);
}

/* 마이데이터 연동 카드가 Hover 되었을 때 강조 */
.select-card.is-linked:hover {
  background-color: #ffffff;
  border-color: #3182f6;
}

.icon { 
  font-size: 32px;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.05));
}

.card-text { display: flex; flex-direction: column; }

.toss-title-sub {
  font-size: 18px;
  font-weight: 700;
  color: #191f28;
}

.toss-desc-sub {
  font-size: 14px;
  color: #6b7684; /* 가독성을 위해 살짝 진하게 조정 */
  margin-top: 4px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>