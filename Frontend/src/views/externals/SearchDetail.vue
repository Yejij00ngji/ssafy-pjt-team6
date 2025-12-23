<template>
  <div class="toss-container">
    <header class="detail-header">
      <h1 class="toss-title-lg" v-html="$route.query.title"></h1>
      <div class="video-meta-group">
        <span class="channel-name">{{ $route.query.channel }}</span>
        <span class="divider">·</span>
        <span class="meta-item">조회수 {{ formatViewCount($route.query.viewCount) }}회</span>
        <span class="divider">·</span>
        <span class="meta-item">{{ $route.query.date }}</span>
      </div>
    </header>

    <section class="video-wrapper">
      <div class="video-container">
        <iframe 
          :src="`https://www.youtube.com/embed/${$route.params.videoId}?autoplay=1`" 
          title="YouTube video player"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
          allowfullscreen>
        </iframe>
      </div>
    </section>

    <section class="description-section">
      <div class="toss-card description-card">
        <h2 class="section-subtitle">영상 설명</h2>
        <div class="description-content">
          {{ $route.query.description }}
        </div>
      </div>
    </section>

    <div class="action-area">
      <button class="toss-btn-secondary" @click="$router.back()">목록으로 돌아가기</button>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

// 조회수 포맷팅 (숫자)
const formatViewCount = (count) => {
  if (!count) return '0'
  return Number(count).toLocaleString()
}
</script>

<style scoped>
/* 타이포그래피 확장 */
.toss-title-lg {
  font-size: 28px;
  font-weight: 700;
  color: var(--toss-text-main);
  line-height: 1.4;
  margin-bottom: 12px;
}

.video-meta-group {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  color: var(--toss-text-sub);
  margin-bottom: 32px;
}

.channel-name {
  color: var(--toss-blue);
  font-weight: 600;
}

.divider {
  color: var(--toss-border);
}

/* 비디오 컨테이너: 토스 스타일의 32px 라운딩 */
.video-wrapper {
  margin-bottom: 32px;
  border-radius: 32px;
  overflow: hidden;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.04);
}

.video-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 비율 */
  height: 0;
}

.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* 설명 섹션 */
.section-subtitle {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 16px;
  color: var(--toss-text-main);
}

.description-card {
  background-color: var(--toss-gray-bg);
  cursor: default; /* 상세페이지 카드는 클릭 효과 제거 */
}

.description-card:hover {
  transform: none;
  box-shadow: none;
}

.description-content {
  white-space: pre-wrap;
  line-height: 1.6;
  color: var(--toss-text-sub);
  font-size: 16px;
}

/* 하단 버튼 */
.action-area {
  margin-top: 40px;
  display: flex;
  justify-content: center;
}

.toss-btn-secondary {
  padding: 12px 24px;
  border-radius: 12px;
  background-color: var(--toss-gray-bg);
  color: var(--toss-text-sub);
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.toss-btn-secondary:hover {
  background-color: var(--toss-border);
}

@media (max-width: 768px) {
  .toss-title-lg { font-size: 22px; }
  .video-wrapper { border-radius: 16px; } /* 모바일에서는 라운딩 축소 */
}
</style>