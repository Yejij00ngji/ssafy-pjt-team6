<template>
  <div class="search-view container-fluid py-4">
    <h1 class="text-center mb-4 display-5 fw-bold">비디오 검색</h1>
    
    <div class="row justify-content-center mb-5">
      <div class="col-12 col-md-6 d-flex gap-2">
        <input 
          v-model="searchQuery" 
          type="text" 
          class="form-control border-2" 
          placeholder="검색어를 입력하세요"
          @keyup.enter="fetchVideos"
        >
        <button class="btn btn-primary px-4 shadow-sm" @click="fetchVideos">검색</button>
      </div>
    </div>

    <div v-if="videos.length" class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 px-lg-5">
      <div v-for="video in videos" :key="video.videoId" class="col">
        <div class="card h-100 border-0 shadow-sm video-card" @click="goToDetail(video)">
          <div class="card-img-wrapper">
            <img :src="video.thumbnail" class="card-img-top" alt="thumbnail">
          </div>
          <div class="card-body p-3">
            <h5 class="card-title text-truncate mb-2" v-html="video.title"></h5>
            <p class="card-text text-muted small mb-0">{{ video.channelName }}</p>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="isSearched" class="text-center py-5">
      <p class="text-muted h5">검색 결과가 없습니다.</p>
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
      channel: video.channelName,
      description: video.description,
      date: new Date(video.publishedAt).toLocaleDateString('ko-KR'),
      viewCount: video.viewCount,
    }
  })
}

fetchVideos()
</script>

<style scoped>
.search-view { background-color: #f9f9f9; min-height: 100vh; }
.video-card { cursor: pointer; transition: transform 0.2s ease-in-out; border-radius: 8px; overflow: hidden; }
.video-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important; }
.card-img-wrapper { position: relative; padding-top: 56.25%; overflow: hidden; }
.card-img-wrapper img { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; }
.card-title { font-size: 1.1rem; font-weight: 500; }
</style>