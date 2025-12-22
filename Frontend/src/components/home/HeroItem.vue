<template>
  <section class="hero-section">
    <div class="content-wrapper">
      <h1 class="hero-title">
        금융의 모든 것<br />
        <span class="text-blue">Money:B</span>에서 쉽고 간편하게
      </h1>
      <p class="hero-subtitle">
        나보다 나를 더 잘 아는 인공지능이<br />
        당신의 자산 페르소나에 딱 맞는 금융 전략을 제안합니다.
      </p>
      
      <router-link :to="{ name: 'Recommendations' }" class="cta-button">
        내 맞춤 상품 추천받기
        <span class="material-symbols-outlined">arrow_forward</span>
      </router-link>
    </div>
    
    <div class="hero-bg-graphic">
      <div class="floating-hexagon"></div>
    </div>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'
// 스크립트 로직은 현재 필요 없음
</script>

<style scoped>
/* 히어로 섹션 스타일 */
.hero-section {
  padding: 120px 20px;
  background: linear-gradient(to bottom, #f9fafb, #ffffff);
  text-align: center;
  position: relative;
  overflow: hidden; /* 배경 요소가 밖으로 나가지 않도록 */
}

.content-wrapper {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
  z-index: 10; /* 배경 그래픽 위에 오도록 */
}

.hero-title {
  font-size: 56px;
  font-weight: 800;
  line-height: 1.3;
  color: #191f28;
  margin-bottom: 24px;
}

.text-blue { color: #3182f6; }

.hero-subtitle {
  font-size: 18px;
  color: #4e5968;
  line-height: 1.6;
  margin-bottom: 48px;
}

/* CTA 버튼 (토스 블루 버튼) */
.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: #3182f6;
  color: white;
  padding: 18px 32px;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 700;
  text-decoration: none;
  transition: transform 0.2s, background-color 0.2s;
  cursor: pointer;
}

.cta-button:hover {
  background-color: #1b64da;
  transform: translateY(-2px);
}

/* 배경 그래픽 (추후 Toss처럼 3D 이미지로 대체 예정) */
.hero-bg-graphic {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 1200px; /* 배경 그래픽 최대 너비 */
  height: 300px; /* 임시 높이, 실제 이미지에 맞춰 조절 */
  background: transparent; /* 임시 */
  z-index: 5;
  pointer-events: none; /* 클릭 방지 */
  /* 여기에 Toss 이미지 같은 배경을 넣을 수 있습니다. */
  /* background-image: url('/assets/toss_hero_graphic.png'); */
  /* background-size: contain; */
  /* background-repeat: no-repeat; */
  /* background-position: center bottom; */
}

.floating-hexagon {
    /* 임시 육각형 데코레이션 */
    width: 100px;
    height: 100px;
    background-color: #e8f3ff;
    clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
    position: absolute;
    bottom: 50px;
    left: 10%;
    opacity: 0.3;
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-15px); }
    100% { transform: translateY(0px); }
}


/* 반응형 처리 */
@media (max-width: 768px) {
  .hero-title { font-size: 36px; }
  .hero-subtitle { font-size: 16px; }
  .cta-button { padding: 14px 24px; font-size: 16px; }
  .hero-section { padding: 80px 20px 60px; }
}
</style>