import axios from 'axios'

const apiBaseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const instance = axios.create({
    baseURL: apiBaseURL
})

export default instance
