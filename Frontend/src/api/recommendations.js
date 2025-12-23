import axios from "axios"

const API_URL = "http://localhost:8000"

export const fetchRecommendations = async () => {
  const token = localStorage.getItem("token")
  console.log("ACCESS TOKEN:", token)

  return axios.get(`${API_URL}/recommendations/test/`, {
    headers: {
      Authorization: `Token ${token}`
    }
  })
}
