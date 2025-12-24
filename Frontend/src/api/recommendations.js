import axios from "axios"

const API_URL = "http://localhost:8000"

export const fetchRecommendations = async () => {
  const token = localStorage.getItem("token")
  console.log("ACCESS TOKEN:", token)

   // 요청 전에 로그 찍기
  console.log("추천 API 호출 중...");


  return axios.get(`${API_URL}/recommendations/`, {
    headers: {
      Authorization: `Token ${token}`
    },
    // 1. 타임아웃을 30초로 넉넉하게 설정 (OpenAI 응답 대기용)
    timeout: 30000
  })
  .then(response => {
    console.log("추천 받은 데이터:", response.data);  // 응답 내용 로그
    return response;
  })
  .catch(error => {
    console.error("추천 API 호출 오류:", error);  // 에러 내용 로그
    throw error; // 오류를 throw해서 catch 블록에서 처리
  });
}
