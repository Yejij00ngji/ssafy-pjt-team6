<template>
  <div class="step-content">
    <h1 class="toss-title">나에게 딱 맞는 <br/>예적금을 찾아볼까요?</h1>
    <p class="toss-desc">방식을 선택하면 분석을 시작합니다.</p>

    <div class="card-group">
      <div class="toss-card select-card" @click="$emit('next', { agreed: true })">
        <span class="icon">⚡️</span>
        <div class="card-text">
          <strong class="toss-title" style="font-size: 18px;">마이데이터 연결</strong>
          <p class="toss-desc" style="margin:0;">30초 만에 가장 정확한 추천</p>
        </div>
      </div>

      <div class="toss-card select-card" @click="$emit('next', { agreed: false })">
        <span class="icon">📝</span>
        <div class="card-text">
          <strong class="toss-title" style="font-size: 18px;">직접 입력하기</strong>
          <p class="toss-desc" style="margin:0;">간단한 질문으로 성향 파악</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card-group { display: flex; flex-direction: column; gap: 16px; margin-top: 40px; }
.select-card { display: flex; align-items: center; gap: 20px; border: 1px solid var(--toss-border); }
.select-card:hover { border-color: var(--toss-blue); }
.icon { font-size: 32px; }
</style>