import { useAuthStore } from '../stores/authStore'
import { useChatStore } from '../stores/chatStore'
import { HiSparkles, HiPlus, HiOutlineTrash } from 'react-icons/hi2'
import { FiSettings, FiHelpCircle, FiLogOut } from 'react-icons/fi'

function Sidebar({ isOpen, onToggle }) {
  const { user, logout } = useAuthStore()
  const { 
    conversations, 
    currentConversationId,
    newConversation,
    selectConversation,
    deleteConversation,
    clearAllConversations,
  } = useChatStore()

  // Format date for display
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24))
    
    if (diffDays === 0) return 'Hôm nay'
    if (diffDays === 1) return 'Hôm qua'
    if (diffDays < 7) return `${diffDays} ngày trước`
    return date.toLocaleDateString('vi-VN')
  }

  // Group conversations by date
  const groupedConversations = conversations.reduce((groups, conv) => {
    const dateLabel = formatDate(conv.createdAt)
    if (!groups[dateLabel]) groups[dateLabel] = []
    groups[dateLabel].push(conv)
    return groups
  }, {})

  return (
    <aside 
      className={`fixed left-0 top-0 h-full bg-gemini-sidebar border-r border-gemini-border
                  transition-all duration-300 z-50 flex flex-col
                  ${isOpen ? 'w-72' : 'w-0 overflow-hidden'}`}
    >
      {/* Header */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-gemini-border">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-gradient-to-r from-gemini-blue to-gemini-purple rounded-lg flex items-center justify-center">
            <HiSparkles className="w-5 h-5 text-white" />
          </div>
          <span className="font-semibold">GiaoTrinh AI</span>
        </div>
        <button 
          onClick={onToggle}
          className="p-2 hover:bg-gemini-hover rounded-lg transition-colors"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
          </svg>
        </button>
      </div>

      {/* New Chat Button */}
      <div className="p-3">
        <button
          onClick={() => newConversation()}
          className="w-full flex items-center gap-3 px-4 py-3 bg-gemini-hover hover:bg-gemini-border
                     rounded-xl transition-colors text-left"
        >
          <HiPlus className="w-5 h-5" />
          <span>Cuộc trò chuyện mới</span>
        </button>
      </div>

      {/* Conversations List */}
      <div className="flex-1 overflow-y-auto px-3">
        {conversations.length === 0 ? (
          <div className="text-gray-500 text-sm px-3 py-8 text-center">
            <HiSparkles className="w-8 h-8 mx-auto mb-2 text-gray-600" />
            <p>Chưa có cuộc trò chuyện nào</p>
            <p className="text-xs mt-1">Bấm nút bên trên để bắt đầu!</p>
          </div>
        ) : (
          <div className="space-y-4">
            {Object.entries(groupedConversations).map(([dateLabel, convs]) => (
              <div key={dateLabel}>
                <div className="text-xs text-gray-500 uppercase tracking-wider px-3 py-2">
                  {dateLabel}
                </div>
                <div className="space-y-1">
                  {convs.map((conv) => (
                    <div
                      key={conv.id}
                      className={`group flex items-center gap-2 px-3 py-2.5 rounded-lg cursor-pointer
                                 transition-colors ${
                                   currentConversationId === conv.id
                                     ? 'bg-gemini-hover border-l-2 border-gemini-blue'
                                     : 'hover:bg-gemini-hover/50'
                                 }`}
                      onClick={() => selectConversation(conv.id)}
                    >
                      <span className="flex-shrink-0">
                        {conv.title?.startsWith('📚') ? '📚' : 
                         conv.title?.startsWith('💡') ? '💡' : 
                         conv.title?.startsWith('💬') ? '💬' : 
                         <HiSparkles className="w-4 h-4 text-gemini-blue" />}
                      </span>
                      <span className="flex-1 truncate text-sm">
                        {conv.title?.replace(/^(📚|💡|💬)\s*/, '') || 'Cuộc trò chuyện'}
                      </span>
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          if (confirm('Xóa cuộc trò chuyện này?')) {
                            deleteConversation(conv.id)
                          }
                        }}
                        className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-500/20 rounded transition-all"
                      >
                        <HiOutlineTrash className="w-4 h-4 text-red-400" />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Quick Links */}
      <div className="border-t border-gemini-border p-3 space-y-1">
        <button className="w-full flex items-center gap-3 px-3 py-2.5 hover:bg-gemini-hover rounded-lg transition-colors text-sm text-gray-400">
          <FiHelpCircle className="w-4 h-4" />
          <span>Hướng dẫn sử dụng</span>
        </button>
        <button className="w-full flex items-center gap-3 px-3 py-2.5 hover:bg-gemini-hover rounded-lg transition-colors text-sm text-gray-400">
          <FiSettings className="w-4 h-4" />
          <span>Cài đặt</span>
        </button>
      </div>

      {/* User Profile */}
      <div className="border-t border-gemini-border p-3">
        <div className="flex items-center gap-3 px-3 py-2">
          <div className="w-10 h-10 rounded-full bg-gradient-to-r from-gemini-blue to-gemini-purple flex items-center justify-center flex-shrink-0">
            <span className="text-sm font-medium text-white">
              {user?.full_name?.charAt(0) || 'G'}
            </span>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">{user?.full_name || 'Giáo viên'}</p>
            <p className="text-xs text-gray-500 truncate">{user?.email}</p>
          </div>
          <button 
            onClick={logout}
            className="p-2 hover:bg-red-500/20 rounded-lg transition-colors"
            title="Đăng xuất"
          >
            <FiLogOut className="w-4 h-4 text-red-400" />
          </button>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
