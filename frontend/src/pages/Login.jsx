import { useState } from 'react'
import { useAuthStore } from '../stores/authStore'
import { FcGoogle } from 'react-icons/fc'
import { HiSparkles } from 'react-icons/hi2'
import { FiMail, FiLock, FiEye, FiEyeOff } from 'react-icons/fi'

function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const { login, loading, error, clearError } = useAuthStore()

  const handleSubmit = async (e) => {
    e.preventDefault()
    await login(email, password)
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      {/* Background effects */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gemini-blue/20 rounded-full blur-3xl"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gemini-purple/20 rounded-full blur-3xl"></div>
      </div>

      <div className="relative w-full max-w-md">
        {/* Logo & Title */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-gemini-blue to-gemini-purple rounded-2xl mb-4">
            <HiSparkles className="w-8 h-8 text-white sparkle" />
          </div>
          <h1 className="text-3xl font-bold gradient-text mb-2">GiaoTrinh AI</h1>
          <p className="text-gray-400">Hỗ trợ Giáo viên soạn giáo án</p>
        </div>

        {/* Login Card */}
        <div className="bg-gemini-sidebar/80 backdrop-blur-xl rounded-3xl p-8 shadow-2xl border border-gemini-border">
          <h2 className="text-xl font-semibold text-center mb-6">Đăng nhập</h2>

          {error && (
            <div className="bg-red-500/10 border border-red-500/30 text-red-400 px-4 py-3 rounded-xl mb-4 text-sm">
              {error}
              <button 
                onClick={clearError}
                className="float-right text-red-400 hover:text-red-300"
              >
                ✕
              </button>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email */}
            <div>
              <label className="block text-sm text-gray-400 mb-2">Email</label>
              <div className="relative">
                <FiMail className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="giaovien@truong.edu.vn"
                  className="w-full bg-gemini-bg border border-gemini-border rounded-xl py-3 pl-12 pr-4 
                           text-white placeholder-gray-500 input-focus"
                  required
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm text-gray-400 mb-2">Mật khẩu</label>
              <div className="relative">
                <FiLock className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full bg-gemini-bg border border-gemini-border rounded-xl py-3 pl-12 pr-12 
                           text-white placeholder-gray-500 input-focus"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300"
                >
                  {showPassword ? <FiEyeOff /> : <FiEye />}
                </button>
              </div>
            </div>

            {/* Remember me & Forgot */}
            <div className="flex items-center justify-between text-sm">
              <label className="flex items-center gap-2 text-gray-400 cursor-pointer">
                <input type="checkbox" className="rounded border-gemini-border bg-gemini-bg" />
                Ghi nhớ đăng nhập
              </label>
              <a href="#" className="text-gemini-blue hover:text-gemini-purple">
                Quên mật khẩu?
              </a>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-gemini-blue to-gemini-purple 
                       text-white font-semibold py-3 rounded-xl 
                       hover:opacity-90 transition-opacity
                       disabled:opacity-50 disabled:cursor-not-allowed
                       flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  Đang đăng nhập...
                </>
              ) : (
                'Đăng nhập'
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gemini-border"></div>
            </div>
            <div className="relative flex justify-center">
              <span className="px-4 bg-gemini-sidebar text-sm text-gray-500">hoặc</span>
            </div>
          </div>

          {/* Google Login */}
          <button
            type="button"
            className="w-full bg-white text-gray-800 font-medium py-3 rounded-xl 
                     hover:bg-gray-100 transition-colors
                     flex items-center justify-center gap-3"
          >
            <FcGoogle className="w-5 h-5" />
            Đăng nhập bằng Google
          </button>

          {/* Help text */}
          <p className="text-center text-sm text-gray-500 mt-6">
            Chưa có tài khoản?{' '}
            <a href="#" className="text-gemini-blue hover:text-gemini-purple">
              Liên hệ Nhà trường
            </a>
          </p>
        </div>

        {/* Footer */}
        <p className="text-center text-xs text-gray-600 mt-6">
          © 2026 GiaoTrinh AI. Phát triển bởi Nhat Huy
        </p>
      </div>
    </div>
  )
}

export default Login
