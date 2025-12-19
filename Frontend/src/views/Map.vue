<template>
  <div class="container-fluid py-4">
    <div class="row">
      <div class="col-md-3 bg-light p-4 border rounded shadow-sm">
        <h4 class="fw-bold mb-4">은행 찾기</h4>
        
        <div class="mb-3">
          <label class="form-label small text-muted">광역시 / 도</label>
          <select v-model="searchFields.city" class="form-select">
            <option value="서울특별시">서울특별시</option>
            <option value="경기도">경기도</option>
            <option value="부산광역시">부산광역시</option>
          </select>
        </div>

        <div class="mb-3">
          <label class="form-label small text-muted">시 / 군 / 구</label>
          <input v-model="searchFields.district" type="text" class="form-control" placeholder="예: 강남구">
        </div>

        <div class="mb-4">
          <label class="form-label small text-muted">은행</label>
          <select v-model="searchFields.bank" class="form-select">
            <option value="우리은행">우리은행</option>
            <option value="국민은행">국민은행</option>
            <option value="신한은행">신한은행</option>
            <option value="하나은행">하나은행</option>
          </select>
        </div>

        <button @click="searchByFields" class="btn btn-primary w-100 py-2 shadow-sm">찾기</button>
        <button @click="getCurrentLocation" class="btn btn-outline-secondary w-100 mt-2 py-2">내 위치 기반 검색</button>
      </div>

      <div class="col-md-9 position-relative">
        <div id="map" class="kakao-map shadow-sm rounded border"></div>
        
        <div v-if="banks.length" class="bank-summary-list shadow">
          <div v-for="bank in banks" :key="bank.id" class="summary-item" @click="moveMap(bank.y, bank.x)">
            <p class="mb-1 fw-bold">{{ bank.place_name }}</p>
            <p class="mb-0 x-small text-muted">{{ bank.distance }}m | {{ bank.address_name }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, reactive } from 'vue'

const map = ref(null)
const banks = ref([])
const infowindow = ref(null)
const searchFields = reactive({
  city: '서울특별시',
  district: '',
  bank: '국민은행'
})

onMounted(() => {
  if (window.kakao && window.kakao.maps) {
    window.kakao.maps.load(initMap)
  }
})

const initMap = () => {
  const container = document.getElementById('map')
  const options = {
    center: new window.kakao.maps.LatLng(37.5668, 126.9786), // 초기값 서울시청
    level: 4
  }
  map.value = new window.kakao.maps.Map(container, options)
  infowindow.value = new window.kakao.maps.InfoWindow({ zIndex: 1 })
  
  // 시작하자마자 내 위치 잡기
  getCurrentLocation()
}

// 1. 내 위치 기반 검색 (F06-1)
const getCurrentLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      const lat = position.coords.latitude
      const lng = position.coords.longitude
      const locPosition = new window.kakao.maps.LatLng(lat, lng)
      
      map.value.setCenter(locPosition)
      searchBanksByKeyword('은행', locPosition)
    }, (err) => {
      alert('위치 정보를 가져올 수 없습니다. 기본 위치로 검색합니다.')
      searchBanksByKeyword('은행', map.value.getCenter())
    })
  }
}

// 2. 입력 필드 기반 검색 (F06-1)
const searchByFields = () => {
  const keyword = `${searchFields.city} ${searchFields.district} ${searchFields.bank}`
  searchBanksByKeyword(keyword, map.value.getCenter())
}

const searchBanksByKeyword = (keyword, position) => {
  const ps = new window.kakao.maps.services.Places()
  
  ps.keywordSearch(keyword, (data, status) => {
    if (status === window.kakao.maps.services.Status.OK) {
      banks.value = data
      displayMarkers(data)
    } else {
      banks.value = []
      alert('검색 결과가 없습니다.')
    }
  }, { location: position, radius: 5000 })
}

// 3. 마커 및 요약 정보 표시 (F06-2)
const displayMarkers = (places) => {
  const bounds = new window.kakao.maps.LatLngBounds()
  
  // 기존 마커 제거 로직 (생략 가능하나 권장)
  // ...

  places.forEach((place) => {
    const markerPosition = new window.kakao.maps.LatLng(place.y, place.x)
    const marker = new window.kakao.maps.Marker({
      map: map.value,
      position: markerPosition
    })

    const content = `
      <div class="p-2" style="font-size:12px; min-width:150px;">
        <div class="fw-bold text-primary">${place.place_name}</div>
        <div class="text-muted small">${place.address_name}</div>
        <div class="mt-1"><a href="https://map.kakao.com/link/to/${place.place_name},${place.y},${place.x}" target="_blank" style="color:blue">길찾기 🚀</a></div>
      </div>
    `

    window.kakao.maps.event.addListener(marker, 'click', () => {
      infowindow.value.setContent(content)
      infowindow.value.open(map.value, marker)
    })

    bounds.extend(markerPosition)
  })

  // 검색 결과가 모두 보이도록 지도 범위 조정
  map.value.setBounds(bounds)
}

const moveMap = (y, x) => {
  map.value.panTo(new window.kakao.maps.LatLng(y, x))
}
</script>

<style scoped>
.kakao-map {
  width: 100%;
  height: 600px;
}
.bank-summary-list {
  position: absolute;
  top: 10px;
  right: 25px;
  width: 250px;
  max-height: 580px;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.9);
  z-index: 10;
  border-radius: 8px;
}
.summary-item {
  padding: 12px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: 0.2s;
}
.summary-item:hover { background: #f0f7ff; }
.x-small { font-size: 0.75rem; }
</style>