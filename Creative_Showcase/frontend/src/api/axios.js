import axios from "axios";

const api = axios.create({
  baseURL: "https://internal-technical-assessment.onrender.com/api/v1",
  withCredentials: true, // IMPORTANT for JWT cookies
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
