<template>
  <div class="map-page-wrapper">
    <div class="content-container">
      
      <header class="map-header">
        <h2 class="title">은행 찾기</h2>
        <p class="subtitle">가장 가까운 영업점을 확인하고 경로를 탐색해 보세요.</p>
      </header>

      <div class="main-grid">
        <aside class="search-section">
          <div class="filter-card">
            <div class="select-group">
              <label>지역 선택</label>
              <select v-model="searchFields.city" @change="handleCityChange" class="toss-select mb-2">
                <option v-for="(districts, city) in regionData" :key="city" :value="city">{{ city }}</option>
              </select>
              <select v-model="searchFields.district" class="toss-select" :disabled="!availableDistricts.length">
                <!-- <option value="">전체</option> -->
                <option v-for="dist in availableDistricts" :key="dist" :value="dist">{{ dist }}</option>
              </select>
            </div>

            <div class="select-group mt-4">
              <label>은행</label>
              <select v-model="searchFields.bank" class="toss-select">
                <option v-for="bank in bankList" :key="bank" :value="bank">{{ bank }}</option>
              </select>
            </div>

            <div class="button-group mt-5">
              <button @click="searchByFields" class="btn-main">검색하기</button>
              <button @click="getCurrentLocation" class="btn-sub">내 주변 검색</button>
            </div>
          </div>

          <div v-if="banks.length" class="result-section mt-4">
            <div class="result-header">
              <span class="result-count">검색 결과 <strong>{{ banks.length }}</strong>건</span>
            </div>
            <div class="bank-scroll-list">
              <div v-for="bank in banks" :key="bank.id" 
                  class="bank-card" :class="{ 'is-selected': selectedBankId === bank.id }"
                  @click="onBankClick(bank)">
                <div class="bank-status-dot"></div>
                <div class="bank-info">
                  <h6 class="bank-name">{{ bank.place_name }}</h6>
                  <p class="bank-addr">{{ bank.address_name }}</p>
                </div>
              </div>
            </div>
          </div>
        </aside>

        <main class="map-section">
          <div id="map" class="kakao-map-canvas"></div>
          
          <transition name="fade-slide">
            <div v-if="routeInfo" class="route-floating-wrapper">
              <div class="route-content">
                <div class="icon-circle"><i class="bi bi-cursor-fill"></i></div>
                <div class="text-info">
                  <p class="route-summary">
                    <span class="target-name">{{ routeInfo.targetName }}</span>까지 
                    약 <strong>{{ routeInfo.duration }}분</strong> 걸립니다
                  </p>
                  <p class="route-detail">거리 {{ routeInfo.distance }}km ({{ routeInfo.originName }} 출발)</p>
                </div>
                <button @click="routeInfo = null" class="btn-close-route">✕</button>
              </div>
            </div>
          </transition>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, reactive, computed } from 'vue'
import axios from 'axios'

// --- 데이터 정의 ---
const regionData = {
  '서울특별시': ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구'],
  '경기도': ['수원시', '성남시', '고양시', '용인시', '부천시', '안산시', '안양시', '남양주시', '화성시', '평택시'],
  '인천광역시': ['계양구', '미추홀구', '남동구', '동구', '부평구', '서구', '연수구', '중구'],
  '부산광역시': ['강서구', '금정구', '남구', '동구', '동래구', '부산진구', '북구', '사상구', '사하구'],
  '대구광역시': ['남구', '달서구', '동구', '북구', '서구', '수성구', '중구']
}
const bankList = ['우리은행', '국민은행', '신한은행', '하나은행', '기업은행', 'NH농협은행']


const map = ref(null); const banks = ref([]); const markers = ref([]);
const infowindow = ref(null); const routeLine = ref(null); const routeInfo = ref(null);
const selectedBankId = ref(null);
const searchFields = reactive({ city: '서울특별시', district: '강남구', bank: '국민은행' });
const availableDistricts = computed(() => {
  const districts = regionData[searchFields.city] || [];
  return [...districts].sort(); // 가나다순 정렬
});
onMounted(() => {
  if (window.kakao?.maps?.load) {
    window.kakao.maps.load(initMap);
    return;
  }

  // If SDK not yet available, poll briefly until it is then initialize
  const poll = setInterval(() => {
    if (window.kakao?.maps?.load) {
      clearInterval(poll);
      window.kakao.maps.load(initMap);
    }
  }, 200);
});

const initMap = () => {
  const mapContainer = document.getElementById('map');
  const mapOption = {
    center: new window.kakao.maps.LatLng(37.5667, 126.9783), // 서울시청 좌표
    level: 3
  };
  map.value = new window.kakao.maps.Map(mapContainer, mapOption);
  infowindow.value = new window.kakao.maps.InfoWindow({ zIndex: 1 });

  // 내 위치를 찾는 동안 서울시청이 먼저 보이고, 위치 허용 시 내 위치로 이동합니다.
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((pos) => {
      const moveLatLon = new window.kakao.maps.LatLng(pos.coords.latitude, pos.coords.longitude);
      map.value.setCenter(moveLatLon);
    });
  }
};

const displayMarkers = (places, shouldMoveCenter = true) => {
  markers.value.forEach(m => m.setMap(null));
  markers.value = [];

  const bounds = new window.kakao.maps.LatLngBounds();

  places.forEach((place) => {
    const markerPosition = new window.kakao.maps.LatLng(place.y, place.x);
    const marker = new window.kakao.maps.Marker({
      map: map.value,
      position: markerPosition
    });
    window.kakao.maps.event.addListener(marker, 'click', () => onBankClick(place, marker));
    markers.value.push(marker);
    bounds.extend(markerPosition);
  });

  // '내 주변 검색'이 아닐 때(shouldMoveCenter가 true일 때)만 중심 이동
  if (places.length > 0 && shouldMoveCenter) {
    const firstPlace = new window.kakao.maps.LatLng(places[0].y, places[0].x);
    map.value.setCenter(firstPlace);
    map.value.setLevel(4);
  }
};

const handleCityChange = () => {
  const districts = regionData[searchFields.city];
  if (districts && districts.length > 0) {
    // 가나다순 정렬 후 첫 번째 값 선택
    const sortedDistricts = [...districts].sort();
    searchFields.district = sortedDistricts[0];
  } else {
    searchFields.district = '';
  }
};

const searchByFields = () => {
  const city = searchFields.city || '';
  const district = (searchFields.district === '전체' || !searchFields.district) ? '' : searchFields.district;
  const bank = searchFields.bank || '';
  
  // 1. 키워드 조합 (예: "인천광역시 남동구 국민은행")
  const keyword = `${city} ${district} ${bank}`.trim();
  
  if (!keyword) {
    alert("지역과 은행을 선택해주세요.");
    return;
  }

  const ps = new window.kakao.maps.services.Places();
  
  // 2. 검색 옵션: size를 15로 고정하여 규격 준수
  const options = {
    size: 15 
  };

  ps.keywordSearch(keyword, (data, status) => {
    if (status === window.kakao.maps.services.Status.OK) {
      
      // [이 부분을 추가/수정하세요]
      // 검색 결과(data) 중에서 사용자가 선택한 '구(district)'가 주소에 포함된 것만 골라냅니다.
      const filteredData = data.filter(item => 
        item.address_name.includes(searchFields.district) || 
        item.road_address_name.includes(searchFields.district)
      );

      // 필터링된 데이터만 화면과 지도에 표시
      banks.value = filteredData; 
      displayMarkers(filteredData); 

      // 만약 필터링했더니 아무것도 없다면 안내
      if (filteredData.length === 0) {
        alert(`${searchFields.district} 내에 검색 결과가 없습니다.`);
      }

    } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
      alert(`'${keyword}' 검색 결과가 없습니다.`);
      banks.value = [];
    } else {
      alert("검색 중 오류가 발생했습니다.");
    }
  }, { size: 15 });
};

const getCurrentLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((pos) => {
      const lat = pos.coords.latitude;
      const lng = pos.coords.longitude;
      const locPosition = new window.kakao.maps.LatLng(lat, lng);
      
      // 1. 지도의 중심을 내 현재 위치로 즉시 이동
      map.value.setCenter(locPosition);
      map.value.setLevel(3); // 주변 검색이므로 더 자세히 보기 위해 레벨 조정
      
      const ps = new window.kakao.maps.services.Places();
      ps.keywordSearch('은행', (data, status) => {
        if (status === window.kakao.maps.services.Status.OK) {
           banks.value = data;
           // 2. 마커는 그리되, 지도의 중심이 바뀌지 않도록 처리
           displayMarkers(data, false); // 두 번째 인자로 중심 이동 여부 제어
        }
      }, { location: locPosition, radius: 2000 });
    });
  }
};

const onBankClick = (place, marker = null) => {
  selectedBankId.value = place.id;
  map.value.panTo(new window.kakao.maps.LatLng(place.y, place.x));
  const content = `
    <div style="padding:16px; min-width:200px; font-family: 'Pretendard';">
      <div style="font-weight:700; color:#191f28; margin-bottom:4px;">${place.place_name}</div>
      <div style="font-size:12px; color:#6b7684; margin-bottom:12px;">${place.address_name}</div>
      <a href="https://map.kakao.com/link/to/${place.id}" target="_blank" 
         style="display:block; text-align:center; background:#3182f6; color:#fff; text-decoration:none; 
                padding:10px; border-radius:10px; font-size:13px; font-weight:600;">카카오맵 상세정보</a>
    </div>`;
  const targetMarker = marker || markers.value.find(m => m.getPosition().getLat() == place.y);
  infowindow.value.setContent(content);
  infowindow.value.open(map.value, targetMarker);
  getRoute({ lat: place.y, lng: place.x, name: place.place_name });
};

const getRoute = async (dest) => {
  if (routeLine.value) routeLine.value.setMap(null);
  
  // 1. 출발지를 멀티캠퍼스 역삼 좌표로 고정
  const multicampus = {
    lat: 37.5012767,
    lng: 127.0396002,
    name: "멀티캠퍼스 역삼"
  };

  try {
    const response = await axios.get('http://127.0.0.1:8000/externals/map/route/', {
      params: { 
        // 고정된 멀티캠퍼스 좌표 사용
        origin: `${multicampus.lng},${multicampus.lat}`, 
        destination: `${dest.lng},${dest.lat}` 
      }
    });
    
    if (response.data.routes?.[0]) {
      const summary = response.data.routes[0].summary;
      routeInfo.value = { 
        targetName: dest.name, 
        originName: multicampus.name, // 출발지 이름 추가
        distance: (summary.distance / 1000).toFixed(1), 
        duration: Math.ceil(summary.duration / 60) 
      };
      drawRoute(response.data.routes[0]);
    }
  } catch (e) {
    console.error("경로 탐색 실패:", e.response?.data || e.message);
  }
};

const drawRoute = (routeData) => {
  const linePath = [];
  routeData.sections.forEach(s => s.roads.forEach(r => r.vertexes.forEach((v, i) => { if (i % 2 === 0) linePath.push(new window.kakao.maps.LatLng(r.vertexes[i+1], r.vertexes[i])) })));
  routeLine.value = new window.kakao.maps.Polyline({ path: linePath, strokeWeight: 6, strokeColor: '#3182F6', strokeOpacity: 0.9 });
  routeLine.value.setMap(map.value);
};
</script>

<style scoped>
/* 이미지 속 디자인 완벽 복구 스타일 */
.map-page-wrapper { background: #fff; min-height: 100vh; padding: 40px 0; font-family: 'Pretendard', sans-serif; }
.content-container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.map-header { margin-bottom: 30px; }
.map-header .title { font-size: 32px; font-weight: 800; color: #191f28; }
.map-header .subtitle { font-size: 16px; color: #4e5968; margin-top: 8px; }

.main-grid { display: grid; grid-template-columns: 340px 1fr; gap: 40px; }

/* 이미지 속 필터 카드 디자인 */
.filter-card {
  background-color: #f9fafb; /* 이미지의 아주 연한 회색 배경 */
  border-radius: 28px;      /* 이미지처럼 아주 둥근 모서리 */
  padding: 32px 24px;
}

.select-group label {
  display: block; font-size: 14px; font-weight: 600; color: #4e5968; margin-bottom: 12px;
}

.toss-select {
  width: 100%; padding: 16px;
  border: 1px solid #e5e8eb; background: #fff;
  border-radius: 12px; font-size: 16px; color: #191f28;
  appearance: none; outline: none; margin-bottom: 8px;
}

/* 이미지 속 버튼 디자인 */
.btn-main {
  width: 100%; background-color: #3182f6; color: #fff;
  border: none; padding: 18px; border-radius: 16px;
  font-weight: 700; font-size: 16px; cursor: pointer; margin-bottom: 12px;
}

.btn-sub {
  width: 100%; background-color: #fff; color: #3182f6;
  border: 1px solid #e5e8eb; padding: 18px; border-radius: 16px;
  font-weight: 700; font-size: 16px; cursor: pointer;
}

/* 지도 및 경로 카드 스타일 */
.kakao-map-canvas { width: 100%; height: 750px; border-radius: 32px; border: 1px solid #f2f4f6; }
.route-floating-card { position: absolute; top: 24px; left: 24px; z-index: 10; width: 280px; }
.route-content {
  background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px);
  padding: 20px; border-radius: 24px; display: flex; align-items: center;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}
.destination-tag { background: #e8f3ff; color: #3182f6; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 6px; margin-bottom: 4px; display: inline-block; }
.time strong { color: #3182f6; font-size: 20px; }
.icon-circle { width: 44px; height: 44px; background: #3182f6; color: #fff; border-radius: 14px; display: flex; align-items: center; justify-content: center; margin-right: 14px; }

/* 헬퍼 클래스 */
.mt-2 { margin-top: 8px; } .mt-3 { margin-top: 12px; } .mt-4 { margin-top: 16px; } .mt-5 { margin-top: 20px; } .mb-2 { margin-bottom: 8px; }

/* 경로 애니메이션 */
.fade-slide-enter-from, .fade-slide-leave-to { opacity: 0; transform: translateY(-20px); }
.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.3s ease; }

/* 검색 결과 섹션 전체 */
.result-section { border-top: 1px solid #f2f4f6; padding-top: 24px; }
.result-header { margin-bottom: 16px; padding: 0 4px; }
.result-count { font-size: 15px; color: #4e5968; }
.result-count strong { color: #3182f6; }

.bank-scroll-list { 
  max-height: 400px; overflow-y: auto; padding-right: 4px;
}

/* 개별 은행 카드 */
.bank-card {
  display: flex; align-items: flex-start;
  padding: 20px; margin-bottom: 12px;
  background: #ffffff; border: 1px solid #f2f4f6;
  border-radius: 20px; cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.bank-card:hover { transform: translateY(-2px); box-shadow: 0 8px 16px rgba(0,0,0,0.04); border-color: #3182f6; }
.bank-card.is-selected { background: #f2f8ff; border-color: #3182f6; }

.bank-status-dot { 
  width: 8px; height: 8px; background: #3182f6; border-radius: 50%; 
  margin-top: 6px; margin-right: 12px; flex-shrink: 0;
}

.bank-info { flex-grow: 1; }
.bank-name { font-size: 16px; font-weight: 700; color: #191f28; margin: 0 0 6px 0; }
.bank-addr { font-size: 13px; color: #6b7684; margin: 0 0 10px 0; line-height: 1.4; }

/* 스크롤바 커스텀 */
.bank-scroll-list::-webkit-scrollbar { width: 4px; }
.bank-scroll-list::-webkit-scrollbar-thumb { background: #e5e8eb; border-radius: 4px; }

/* 소요 시간 카드 위치를 지도 하단 중앙으로 */
.route-floating-wrapper {
  position: absolute;
  bottom: 24px;   /* 지도 바닥에서 24px 띄움 */
  left: 50%;      /* 왼쪽에서 50% 이동 */
  transform: translateX(-50%); /* 정확히 중앙 정렬 */
  z-index: 10;
  width: auto;
  min-width: 320px;
}

.route-content {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  padding: 16px 20px;
  border-radius: 20px; /* 토스풍 둥근 모서리 */
  display: flex;
  align-items: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e8eb;
}

.icon-circle {
  width: 40px;
  height: 40px;
  background: #3182f6;
  color: #fff;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 14px;
  flex-shrink: 0;
}

.text-info { flex-grow: 1; }

.route-summary {
  font-size: 15px;
  color: #191f28;
  margin: 0;
  font-weight: 500;
}

.target-name {
  color: #3182f6;
  font-weight: 700;
}

.route-summary strong {
  font-size: 18px;
  color: #3182f6;
}

.route-detail {
  font-size: 12px;
  color: #8b95a1;
  margin: 2px 0 0 0;
}

.btn-close-route {
  background: none;
  border: none;
  color: #b0b8c1;
  font-size: 18px;
  cursor: pointer;
  margin-left: 10px;
  padding: 4px;
}

/* 애니메이션 효과: 아래에서 위로 슥 올라오게 */
.fade-slide-enter-from { opacity: 0; transform: translate(-50%, 20px); }
.fade-slide-leave-to { opacity: 0; transform: translate(-50%, 20px); }
.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
</style>