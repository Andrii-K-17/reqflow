import axios, { type AxiosInstance, type InternalAxiosRequestConfig } from 'axios'
import { useAuthStore } from '@/stores/auth'

const api: AxiosInstance = axios.create({ baseURL: '/api' })

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const auth = useAuthStore()
  if (auth.accessToken) {
    config.headers.Authorization = `Bearer ${auth.accessToken}`
  }
  return config
})

let isRefreshing = false
let pendingQueue: Array<() => void> = []

api.interceptors.response.use(
  response => response,
  async error => {
    const auth = useAuthStore()
    const originalRequest = error.config

    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error)
    }

    if (isRefreshing) {
      return new Promise(resolve => {
        pendingQueue.push(() => resolve(api(originalRequest)))
      })
    }

    originalRequest._retry = true
    isRefreshing = true

    try {
      await auth.refreshTokens()
      pendingQueue.forEach(resolve => resolve())
      pendingQueue = []
      return api(originalRequest)
    } catch (refreshError) {
      auth.logout()
      return Promise.reject(refreshError)
    } finally {
      isRefreshing = false
    }
  },
)

export default api
