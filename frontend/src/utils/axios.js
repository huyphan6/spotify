import axios from 'axios';

// axios instance for making requests
const axiosInstance = axios.create();

axiosInstance.interceptors.request.use((config) => {
  config.baseURL = 'http://localhost:5000';
  return config;
})

export default axiosInstance;