<template>
  <div class="container-fluid py-4 bg-light min-vh-100">
    <div class="row g-4">
      <div class="col-md-3">
        <div class="card border-0 shadow-sm p-4">
          <h4 class="fw-bold mb-4 text-primary">은행 찾기</h4>
          
          <div class="mb-3">
            <label class="form-label small fw-bold text-secondary">광역시 / 도</label>
            <select v-model="searchFields.city" class="form-select border-2">
              <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label small fw-bold text-secondary">시 / 군 / 구</label>
            <input v-model="searchFields.district" type="text" class="form-control border-2" placeholder="예: 강남구">
          </div>

          <div class="mb-4">
            <label class="form-label small fw-bold text-secondary">은행 선택</label>
            <select v-model="searchFields.bank" class="form-select border-2">
              <option v-for="bank in bankList" :key="bank" :value="bank">{{ bank }}</option>
            </select>
          </div>

          <button @click="searchByFields" class="btn btn-primary w-100 py-2 mb-2 fw-bold shadow-sm">
            검색하기
          </button>
          <button @click="getCurrentLocation" class="btn btn-outline-primary w-100 py-2 fw-bold">
            내 주변 검색
          </button>
        </div>
      </div>

      <div class="col-md-9 position-relative">
        <div id="map" class="kakao-map shadow-sm rounded-4 border-0"></div>
        
        <div v-if="banks.length" class="bank-summary-list shadow-lg border-0 rounded-3">
          <div class="p-3 bg-primary text-white rounded-top-3">
            <span class="small">검색 결과 {{ banks.length }}건</span>
          </div>
          <div v-for="bank in banks" :key="bank.id" class="summary-item" @click="moveMap(bank.y, bank.x)">
            <p class="mb-1 fw-bold text-dark">{{ bank.place_name }}</p>
            <p class="mb-0 x-small text-muted">{{ bank.distance }}m | {{ bank.address_name }}</p>
          </div>
        </div>

        <!-- 예상 소요시간 -->
        <div v-if="routeInfo" class="route-info-card shadow-lg animate__animated animate__fadeInUp">
          <div class="d-flex align-items-center justify-content-between">
            <div>
              <span class="badge bg-primary mb-1">추천 경로</span>
              <h5 class="mb-0 fw-bold text-dark">
                예상 소요 시간: <span class="text-primary">{{ routeInfo.duration }}분</span>
              </h5>
              <p class="mb-0 small text-muted">총 거리: {{ routeInfo.distance }}km</p>
            </div>
            <button @click="routeInfo = null" class="btn-close"></button>
          </div>
        </div>
        
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, reactive } from 'vue'
import axios from 'axios'

// --- 상태 관리 ---
const map = ref(null)
const banks = ref([])
const markers = ref([]) // 마커 관리를 위한 리스트
const infowindow = ref(null)
const routeLine = ref(null)

const cities = ['서울특별시', '경기도', '부산광역시', '인천광역시', '대구광역시']
const bankList = ['우리은행', '국민은행', '신한은행', '하나은행', '기업은행', 'NH농협은행']
const searchFields = reactive({ city: '서울특별시', district: '', bank: '국민은행' })

// --- 초기화 ---
onMounted(() => {
  if (window.kakao?.maps) {
    window.kakao.maps.load(initMap)
  }
})

const initMap = () => {
  const container = document.getElementById('map')
  map.value = new window.kakao.maps.Map(container, {
    center: new window.kakao.maps.LatLng(37.5668, 126.9786),
    level: 3
  })
  infowindow.value = new window.kakao.maps.InfoWindow({ zIndex: 1 })
  getCurrentLocation()
}

// --- 마커 및 경로 초기화 로직 ---
const clearMapObjects = () => {
  markers.value.forEach(m => m.setMap(null))
  markers.value = []
  if (routeLine.value) routeLine.value.setMap(null)
}

// --- 기능 함수 ---
// 내 현재 위치 찾기
const getCurrentLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const loc = new window.kakao.maps.LatLng(pos.coords.latitude, pos.coords.longitude)
        map.value.setCenter(loc)
        searchBanksByKeyword('은행', loc)
      },
      () => searchBanksByKeyword('은행', map.value.getCenter())
    )
  }
}

// 맞춤형 검색어 조합
const searchByFields = () => {
  const keyword = `${searchFields.city} ${searchFields.district} ${searchFields.bank}`
  searchBanksByKeyword(keyword, map.value.getCenter())
}

// 카카오 장소 API 호출
const searchBanksByKeyword = (keyword, position) => {
  const ps = new window.kakao.maps.services.Places()
  ps.keywordSearch(keyword, (data, status) => {
    if (status === window.kakao.maps.services.Status.OK) {
      banks.value = data
      displayMarkers(data)
    }
  }, { location: position, radius: 5000 })
}

const displayMarkers = (places) => {
  clearMapObjects()
  places.forEach((place) => {
    const marker = new window.kakao.maps.Marker({
      map: map.value,
      position: new window.kakao.maps.LatLng(place.y, place.x)
    })
    markers.value.push(marker)
    window.kakao.maps.event.addListener(marker, 'click', () => {
      displayInfoWindow(place, marker)
      getRoute({ lat: place.y, lng: place.x })
    })
  })
}

// 마커를 클릭했을 때 나타나는 하얀색 말풍선
const displayInfoWindow = (place, marker) => {
  const content = `
    <div class="p-2" style="min-width:150px;">
      <div class="fw-bold text-primary mb-1">${place.place_name}</div>
      <div class="x-small text-muted mb-2">${place.address_name}</div>
      <a href="https://map.kakao.com/link/to/${place.id}" target="_blank" class="btn btn-sm btn-outline-primary py-0 px-2 x-small">상세보기</a>
    </div>`
  infowindow.value.setContent(content)
  infowindow.value.open(map.value, marker)
}

// 상태 관리 변수 (소요 시간)
const routeInfo = ref(null); // { distance: 0, duration: 0 }

const getRoute = async (dest) => {
  if (routeLine.value) routeLine.value.setMap(null)
  const origin = "127.039585,37.5012743" // 멀캠 역삼 고정
  
  try {
    const response = await axios.get('http://127.0.0.1:8000/externals/map/route/', {
      params: { origin, destination: `${dest.lng},${dest.lat}` }
    })
    const data = response.data;
    if (data.routes?.[0]) {
      // 요약 정보 추출 (distance: 미터, duration: 초)
      const summary = data.routes[0].summary;
      routeInfo.value = {
        distance: (summary.distance / 1000).toFixed(1), // km로 변환
        duration: Math.ceil(summary.duration / 60)      // 분으로 변환
      };
      
      drawRoute(data.routes[0]);
    }
  } catch (e) {
    console.error("Route Error:", e)
  }
}

const drawRoute = (routeData) => {
  const linePath = []
  routeData.sections.forEach(s => {
    s.roads.forEach(r => {
      r.vertexes.forEach((v, i) => {
        if (i % 2 === 0) linePath.push(new window.kakao.maps.LatLng(r.vertexes[i+1], r.vertexes[i]))
      })
    })
  })

  routeLine.value = new window.kakao.maps.Polyline({
    path: linePath,
    strokeWeight: 6,
    strokeColor: '#3366FF',
    strokeOpacity: 0.8
  })
  routeLine.value.setMap(map.value)
  
  const bounds = new window.kakao.maps.LatLngBounds()
  linePath.forEach(p => bounds.extend(p))
  map.value.setBounds(bounds)
}

const moveMap = (y, x) => map.value.panTo(new window.kakao.maps.LatLng(y, x))
</script>

<style scoped>
.kakao-map { width: 100%; height: 700px; }
.bank-summary-list {
  position: absolute; top: 20px; right: 20px;
  width: 280px; max-height: 600px;
  overflow-y: auto; background: white; z-index: 10;
}
.summary-item {
  padding: 15px; border-bottom: 1px solid #f0f0f0;
  cursor: pointer; transition: background 0.2s;
}
.summary-item:hover { background: #f8fbff; }
.x-small { font-size: 0.7rem; }

/* Map.vue <style> */
.route-info-card {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 20;
  background: white;
  padding: 20px;
  border-radius: 15px;
  width: 320px;
  border-left: 5px solid #3366FF; /* 포인트 컬러 */
}

/* 부드러운 등장 애니메이션 (선택사항) */
.animate__fadeInUp {
  animation: fadeInUp 0.4s ease-out;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translate(-50%, 20px); }
  to { opacity: 1; transform: translate(-50%, 0); }
}
</style>