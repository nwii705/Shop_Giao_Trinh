import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import api from '../services/api'

export const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      loading: false,
      error: null,

      login: async (email, password) => {
        set({ loading: true, error: null })
        try {
          const response = await api.login(email, password)
          const { access_token } = response.data
          
          // Get user info
          api.setToken(access_token)
          const userResponse = await api.getMe()
          
          set({
            token: access_token,
            user: userResponse.data,
            isAuthenticated: true,
            loading: false,
          })
          
          return true
        } catch (error) {
          set({
            error: error.response?.data?.detail || 'Đăng nhập thất bại',
            loading: false,
          })
          return false
        }
      },

      logout: () => {
        api.setToken(null)
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        })
      },

      clearError: () => set({ error: null }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
