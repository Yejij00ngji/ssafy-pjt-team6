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
  if (routeLine.value) { routeLine.value.setMap(null); routeLine.value = null; }

  // 멀티캠퍼스 역삼을 항상 출발지로 사용
  const multicampus = { lat: 37.5012767, lng: 127.0396002, name: "멀티캠퍼스 역삼" };
  const originLngLat = `${multicampus.lng},${multicampus.lat}`;

  // 시도할 priority 목록: 도보 기준 FASTEST 우선, 실패 시 RECOMMEND 폴백
  const priorities = ['FASTEST', 'RECOMMEND'];
  let finalResponse = null;

  for (const pr of priorities) {
    try {
      const response = await axios.get('http://127.0.0.1:8000/externals/map/route/', {
        params: {
          origin: originLngLat,
          destination: `${dest.lng},${dest.lat}`,
          priority: pr
        }
      });

      console.log('route API response', response.data);

      if (response.data && typeof response.data.code === 'number' && response.data.code < 0) {
        const msg = String(response.data.msg || '').toLowerCase();
        console.warn('route API error code:', response.data.code, response.data.msg);
        if (msg.includes('invalid priority') || response.data.code === -2) continue;
        finalResponse = response; break;
      }

      if (response.data && response.data.routes && response.data.routes.length > 0) {
        finalResponse = response; break;
      }
    } catch (err) {
      console.error('route API call failed for priority', pr, err?.response?.data || err.message || err);
      continue;
    }
  }

  if (!finalResponse) {
    console.warn('No valid route response after trying priorities');
    return;
  }

  const route = finalResponse.data?.routes?.[0];
  if (route && route.summary) {
    const summary = route.summary;
    routeInfo.value = {
      targetName: dest.name,
      originName: multicampus.name,
      distance: (summary.distance / 1000).toFixed(1),
      duration: Math.ceil(summary.duration / 60)
    };
    drawRoute(route);
  } else {
    console.warn('No route found in response', finalResponse.data);
  }
};

// drawRoute: vertexes 순서(lon/lat vs lat/lon) 자동 감지해서 polyline 생성
const drawRoute = (routeData) => {
  if (!routeData || !routeData.sections) return;
  const linePath = [];

  // sections -> roads -> vertexes (vertexes: flat array [lng, lat, lng, lat,...] 혹은 [lat, lng,...])
  routeData.sections.forEach(section => {
    (section.roads || []).forEach(road => {
      const verts = road.vertexes || [];
      for (let i = 0; i + 1 < verts.length; i += 2) {
        const a = Number(verts[i]);
        const b = Number(verts[i + 1]);
        // 자동 판별: 위도(lat)는 -90..90 범위, 경도(lng)는 -180..180 범위
        // 만약 a가 경도 범위(-180..180)이고 b가 위도 범위(-90..90)라면 verts = [lng, lat]
        let lat, lng;
        if (a >= -180 && a <= 180 && b >= -90 && b <= 90) {
          // assume [lng, lat]
          lng = a; lat = b;
        } else if (a >= -90 && a <= 90 && b >= -180 && b <= 180) {
          // assume [lat, lng]
          lat = a; lng = b;
        } else {
          // fallback: try swapping
          lat = verts[i + 1]; lng = verts[i];
        }
        linePath.push(new window.kakao.maps.LatLng(Number(lat), Number(lng)));
      }
    });
  });

  if (linePath.length === 0) {
    console.warn('라인 패스가 비어있습니다. routeData 확인 필요.', routeData);
    return;
  }

  // 기존 라인 지우기
  if (routeLine.value) {
    routeLine.value.setMap(null);
    routeLine.value = null;
  }

  routeLine.value = new window.kakao.maps.Polyline({
    path: linePath,
    strokeWeight: 6,
    strokeColor: '#3182F6',
    strokeOpacity: 0.9
  });
  routeLine.value.setMap(map.value);

  // 지도 영역에 맞춰 중심/줌 조정
  const bounds = new window.kakao.maps.LatLngBounds();
  linePath.forEach(p => bounds.extend(p));
  map.value.setBounds(bounds);
};
</script>

<style scoped>
.map-page-wrapper { background: #fff; min-height: 100vh; padding: 24px 0; font-family: 'Pretendard', sans-serif; }
.content-container { max-width: 1000px; margin: 0 auto; padding: 0 16px; }
.map-header { margin-bottom: 18px; }
.map-header .title { font-size: 24px; font-weight: 800; color: #191f28; }
.map-header .subtitle { font-size: 14px; color: #4e5968; margin-top: 6px; }

.main-grid { display: grid; grid-template-columns: 300px 1fr; gap: 20px; }

/* 필터 카드 컴팩트화 */
.filter-card {
  background-color: #f9fafb;
  border-radius: 20px;
  padding: 18px 16px;
}

.select-group label {
  display: block; font-size: 13px; font-weight: 600; color: #4e5968; margin-bottom: 8px;
}

.toss-select {
  width: 100%; padding: 10px;
  border: 1px solid #e5e8eb; background: #fff;
  border-radius: 10px; font-size: 14px; color: #191f28;
  appearance: none; outline: none; margin-bottom: 8px;
}

/* 버튼 크기 축소 */
.btn-main {
  width: 100%; background-color: #3182f6; color: #fff;
  border: none; padding: 10px; border-radius: 10px;
  font-weight: 700; font-size: 14px; cursor: pointer; margin-bottom: 8px;
}

.btn-sub {
  width: 100%; background-color: #fff; color: #3182f6;
  border: 1px solid #e5e8eb; padding: 10px; border-radius: 10px;
  font-weight: 700; font-size: 14px; cursor: pointer;
}

/* 지도 및 경로 카드 스타일 (높이 축소) */
.kakao-map-canvas { width: 100%; height: 600px; border-radius: 20px; border: 1px solid #f2f4f6; }

.route-floating-card { position: absolute; top: 12px; left: 12px; z-index: 10; width: 240px; }
.route-content {
  background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(8px);
  padding: 12px; border-radius: 12px; display: flex; align-items: center;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
}
.destination-tag { background: #e8f3ff; color: #3182f6; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 6px; margin-bottom: 4px; display: inline-block; }
.icon-circle { width: 34px; height: 34px; background: #3182f6; color: #fff; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 12px; }

/* 헬퍼 클래스 */
.mt-2 { margin-top: 8px; } .mt-3 { margin-top: 12px; } .mt-4 { margin-top: 16px; } .mt-5 { margin-top: 18px; } .mb-2 { margin-bottom: 8px; }

/* 검색 결과 섹션 전체 (컴팩트) */
.result-section { border-top: 1px solid #f2f4f6; padding-top: 16px; }
.result-header { margin-bottom: 10px; padding: 0 4px; }
.result-count { font-size: 14px; color: #4e5968; }
.result-count strong { color: #3182f6; }

.bank-scroll-list { 
  max-height: 320px; overflow-y: auto; padding-right: 4px;
}

/* 개별 은행 카드 (작게) */
.bank-card {
  display: flex; align-items: flex-start;
  padding: 12px; margin-bottom: 10px;
  background: #ffffff; border: 1px solid #f2f4f6;
  border-radius: 12px; cursor: pointer;
  transition: all 0.15s ease;
  position: relative;
}

.bank-card:hover { transform: translateY(-1px); box-shadow: 0 6px 12px rgba(0,0,0,0.03); border-color: #3182f6; }
.bank-card.is-selected { background: #f2f8ff; border-color: #3182f6; }

.bank-status-dot { 
  width: 8px; height: 8px; background: #3182f6; border-radius: 50%; 
  margin-top: 6px; margin-right: 10px; flex-shrink: 0;
}

.bank-info { flex-grow: 1; }
.bank-name { font-size: 14px; font-weight: 700; color: #191f28; margin: 0 0 6px 0; }
.bank-addr { font-size: 12px; color: #6b7684; margin: 0 0 6px 0; line-height: 1.3; }

/* 스크롤바 커스텀 */
.bank-scroll-list::-webkit-scrollbar { width: 6px; }
.bank-scroll-list::-webkit-scrollbar-thumb { background: #e5e8eb; border-radius: 4px; }

/* 소요 시간 카드 위치를 지도 하단 중앙으로 (크기 축소) */
.route-floating-wrapper {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  width: auto;
  min-width: 260px;
}

.route-content {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(8px);
  padding: 10px 14px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e5e8eb;
}

.icon-circle {
  width: 34px;
  height: 34px;
  background: #3182f6;
  color: #fff;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  flex-shrink: 0;
}

.text-info { flex-grow: 1; }

.route-summary {
  font-size: 14px;
  color: #191f28;
  margin: 0;
  font-weight: 500;
}

.target-name {
  color: #3182f6;
  font-weight: 700;
}

.route-summary strong {
  font-size: 16px;
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
  font-size: 16px;
  cursor: pointer;
  margin-left: 8px;
  padding: 4px;
}

.map-section { position: relative; }

.route-floating-wrapper {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  width: auto;
  min-width: 260px;
  pointer-events: auto;
}

/* 애니메이션 효과 */
.fade-slide-enter-from, .fade-slide-leave-to { opacity: 0; transform: translateY(-12px); }
.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.25s ease; }
.fade-slide-enter-from { opacity: 0; transform: translate(-50%, 12px); }
.fade-slide-leave-to { opacity: 0; transform: translate(-50%, 12px); }
.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1); }
</style>