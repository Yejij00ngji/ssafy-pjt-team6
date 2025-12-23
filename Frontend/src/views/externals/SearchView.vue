<template>
  <div class="toss-container">
    <header class="search-header">
      <h1 class="toss-title">관심 종목 동영상 검색</h1>
      <p class="toss-desc">금융 전문가들의 분석 영상을 확인해보세요.</p>
    </header>

    <div class="toss-input-group">
      <input 
        v-model="searchQuery" 
        type="text" 
        class="toss-input" 
        placeholder="궁금한 종목이나 키워드를 입력하세요"
        @keyup.enter="fetchVideos"
      />
      <button class="toss-btn-search" @click="fetchVideos">
        검색
      </button>
    </div>

    <div class="search-results">
      <div v-if="loading" class="loading-spinner">영상을 불러오는 중입니다...</div>

      <div 
        v-for="video in videos" 
        :key="video.id" 
        class="toss-card video-card"
        @click="goToDetail(video)"
      >
        <div class="thumbnail-wrapper">
          <img :src="video.thumbnail" alt="thumbnail" class="video-thumbnail" />
        </div>
        <div class="video-info">
          <h3 class="video-title">{{ video.title }}</h3>
          <div class="video-meta">
            <span class="channel-name">{{ video.channelTitle }}</span>
            <span class="divider">·</span>
            <span class="publish-date">{{ video.publishedAt }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const searchQuery = ref('') // 초기값 설정
const videos = ref([])
const isSearched = ref(false)

const fetchVideos = async () => {
  if (!searchQuery.value.trim()) return
  try {
    const response = await axios.get('http://127.0.0.1:8000/externals/search/', {
      params: { q: searchQuery.value }
    })
    videos.value = response.data
    isSearched.value = true
  } catch (err) {
    console.error(err)
  }
}

const goToDetail = (video) => {
  router.push({
    name: 'SearchDetail',
    params: { videoId: video.videoId },
    query: { 
      title: video.title, 
      channel: video.channelTitle,
      description: video.description,
      date: new Date(video.publishedAt).toLocaleDateString('ko-KR'),
      viewCount: video.viewCount,
    }
  })
}

fetchVideos()
</script>

<style scoped>
.search-header {
  margin-bottom: 32px;
}

.video-card {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 16px;
}

.thumbnail-wrapper {
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  border-radius: 16px;
}

.video-thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--toss-text-main);
  margin: 0 0 8px 0;
  /* 말줄임 처리 (2줄) */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.video-meta {
  font-size: 14px;
  color: var(--toss-text-tertiary);
  display: flex;
  align-items: center;
  gap: 6px;
}

.empty-state {
  text-align: center;
  padding: 80px 0;
  color: var(--toss-text-tertiary);
  font-size: 16px;
}

.loading-spinner {
  text-align: center;
  padding: 40px;
  color: var(--toss-blue);
  font-weight: 600;
}
</style>