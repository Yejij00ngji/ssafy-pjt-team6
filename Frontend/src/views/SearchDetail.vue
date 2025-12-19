<template>
  <div class="detail-page">
    <div class="video-section bg-black">
      <div class="container-fluid px-0">
        <div class="ratio ratio-21x9">
          <iframe 
            :src="`https://www.youtube.com/embed/${$route.params.videoId}?autoplay=1`" 
            title="YouTube video player"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
          </iframe>
        </div>
      </div>
    </div>

    <div class="container mt-4 pb-5">
      <div class="row justify-content-center">
        <div class="col-lg-11">
          
          <div class="d-flex justify-content-between align-items-start mb-2">
            <h1 class="video-title fw-bold" v-html="$route.query.title"></h1>
            <div class="text-end text-muted small mt-2 ps-3">
              <p class="mb-0">게시일: {{ $route.query.date }}</p>
              <p class="mb-0">조회수: {{ formatViewCount($route.query.viewCount) }}회</p>
            </div>
          </div>

          <div class="channel-info mb-4">
            <h4 class="text-primary fw-normal h5">{{ $route.query.channel }}</h4>
          </div>

          <div class="description-container p-4 rounded-3 border bg-white">
            <h6 class="fw-bold mb-4 border-bottom pb-2 text-secondary">영상 설명</h6>
            <div class="description-content">
              {{ $route.query.description }}
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

// 조회수 포맷팅 (예: 1234567 -> 1,234,567)
const formatViewCount = (count) => {
  if (!count) return '0'
  return Number(count).toLocaleString()
}
</script>

<style scoped>
.detail-page {
  background-color: #ffffff;
  min-height: 100vh;
}

.video-section {
  border-bottom: 1px solid #eee;
}

.video-title {
  font-size: 2rem;
  line-height: 1.3;
  color: #1a1a1a;
  max-width: 85%;
}

.channel-info h4 {
  color: #3b82f6 !important; /* 이미지의 밝은 파란색 */
}

.description-container {
  border: 1px solid #e5e7eb !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.description-content {
  white-space: pre-wrap; /* 줄바꿈 유지 */
  line-height: 1.8;
  color: #4b5563;
  font-size: 0.95rem;
  word-break: break-all;
}

/* 이미지와 동일한 느낌을 위한 여백 조정 */
@media (max-width: 768px) {
  .video-title {
    font-size: 1.4rem;
    max-width: 100%;
  }
  .ratio-21x9 {
    --bs-aspect-ratio: 56.25%; /* 모바일에서는 16:9로 변경 */
  }
}
</style>