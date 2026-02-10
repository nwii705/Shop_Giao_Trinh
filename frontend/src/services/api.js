import axios from 'axios'

const axiosInstance = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth-token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

const api = {
  // Set token
  setToken: (token) => {
    if (token) {
      localStorage.setItem('auth-token', token)
    } else {
      localStorage.removeItem('auth-token')
    }
  },

  // Auth
  login: (email, password) => {
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)
    return axiosInstance.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
  },

  getMe: () => axiosInstance.get('/auth/me'),

  // KHBD - Kế hoạch bài dạy
  generateKHBD: (data) => axiosInstance.post('/khbd/generate', data),
  
  downloadKHBD: (id) => axiosInstance.get(`/khbd/${id}/download`, {
    responseType: 'blob',
  }),

  // Convert markdown to Word
  convertToWord: (markdownContent, filename = 'document') => 
    axiosInstance.post('/khbd/convert-to-word', {
      markdown_content: markdownContent,
      filename: filename,
    }, {
      responseType: 'blob',
    }),

  getKHBDHistory: () => axiosInstance.get('/khbd/history'),

  // SKKN - Sáng kiến kinh nghiệm
  generateSKKNTopics: (data) => axiosInstance.post('/skkn/ideation', data),
  generateSKKNOutline: (data) => axiosInstance.post('/skkn/outline', data),
  generateSKKNSection: (data) => axiosInstance.post('/skkn/section', data),
  generateSKKNFull: (data) => axiosInstance.post('/skkn/full', data),

  // Quota
  getQuotaStatus: () => axiosInstance.get('/organizations/me/quota'),

  // Chat AI - Gọi Gemini API
  chat: (message, history = [], context = null) => 
    axiosInstance.post('/chat/send', { 
      message, 
      history,
      context 
    }),
  
  // Quick answer (không cần history)
  quickAnswer: (question) => 
    axiosInstance.post('/chat/quick-answer', null, {
      params: { question }
    }),
}

export default api
