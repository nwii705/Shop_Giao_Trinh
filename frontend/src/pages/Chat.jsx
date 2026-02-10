import { useState, useRef, useEffect } from 'react'
import { useAuthStore } from '../stores/authStore'
import { useChatStore } from '../stores/chatStore'
import Sidebar from '../components/Sidebar'
import ChatMessage from '../components/ChatMessage'
import QuickActions from '../components/QuickActions'
import ChatInput from '../components/ChatInput'
import api from '../services/api'
import { HiSparkles } from 'react-icons/hi2'

function Chat() {
  const { user } = useAuthStore()
  const { 
    getMessages,
    getCurrentConversation,
    isGenerating, 
    addMessage, 
    updateLastMessage,
    setGenerating,
    currentConversationId,
    newConversation,
    updateCurrentTitle,
  } = useChatStore()
  
  const messages = getMessages()
  const currentConversation = getCurrentConversation()
  
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const messagesEndRef = useRef(null)

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, currentConversationId])

  // Handle sending message
  const handleSend = async (message, action = null) => {
    if (!message.trim() && !action) return
    
    // Create conversation if not exists
    if (!currentConversation) {
      newConversation()
    }

    // Add user message
    addMessage({
      role: 'user',
      content: message,
      action: action,
    })

    // Add placeholder for AI response
    addMessage({
      role: 'assistant',
      content: '',
      loading: true,
    })

    setGenerating(true)

    try {
      let response

      // Route to appropriate API based on action
      if (action?.type === 'khbd') {
        // Đặt tên conversation theo bài học
        const lessonTitle = `📚 ${action.lessonName}`
        updateCurrentTitle(lessonTitle)
        
        response = await api.generateKHBD({
          subject: action.subject,
          grade: parseInt(action.grade),
          lesson_name: action.lessonName,
          duration: action.duration || 1,
          textbook: action.textbook || 'ctst',
          output_format: 'docx',
        })
        
        updateLastMessage(response.data.markdown_content)
      } else if (action?.type === 'skkn') {
        // Đặt tên conversation theo tên sáng kiến
        const skknTitle = `💡 ${action.topic}`
        updateCurrentTitle(skknTitle)
        
        response = await api.generateSKKNTopics({
          subject: action.subject,
          grade: action.grade,
          problem: action.problem,
        })
        
        // Format topics as markdown
        const topicsText = response.data.topics
          .map((t, i) => `### Đề tài ${i + 1}: ${t.title}\n${t.urgency_analysis}\n`)
          .join('\n')
        
        updateLastMessage(topicsText + '\n\n' + response.data.recommendation)
      } else {
        // Generic chat - gọi API Gemini thực sự
        // Đặt tên conversation theo câu hỏi đầu tiên
        if (!currentConversation || currentConversation.title === 'Cuộc trò chuyện mới') {
          const shortTitle = message.length > 40 ? message.substring(0, 40) + '...' : message
          updateCurrentTitle(`💬 ${shortTitle}`)
        }
        
        const currentMessages = getMessages()
        const history = currentMessages
          .filter(m => !m.loading)
          .map(m => ({
            role: m.role,
            content: m.content,
          }))
        
        response = await api.chat(message, history)
        updateLastMessage(response.data.reply)
      }
    } catch (error) {
      console.error('Error:', error)
      updateLastMessage('❌ Có lỗi xảy ra: ' + (error.response?.data?.detail || error.message))
    } finally {
      setGenerating(false)
    }
  }

  // Handle quick action click
  const handleQuickAction = (actionData) => {
    if (!actionData.data) {
      // Just show a message for unsupported actions
      handleSend(`Tính năng "${actionData.label}" đang được phát triển...`, null)
      return
    }
    
    // Build user message from form data
    let userMessage = ''
    
    if (actionData.type === 'khbd') {
      const d = actionData.data
      // Map tên bộ sách
      const textbookNames = {
        ctst: 'Chân trời sáng tạo',
        kntt: 'Kết nối tri thức với cuộc sống',
        cd: 'Cánh diều',
      }
      const textbookName = textbookNames[d.boSach] || 'Chân trời sáng tạo'
      
      userMessage = `📚 **Soạn Kế hoạch Bài dạy**
- **Bộ sách:** ${textbookName}
- **Bài học:** ${d.baiHoc}
- **Lớp:** ${d.lopHoc}
- **Phân môn:** ${d.linhVuc}
- **Số tiết:** ${d.soTiet}
${d.yeuCauCanDat ? `- **Yêu cầu cần đạt:** ${d.yeuCauCanDat}` : ''}
- **Phương pháp:** ${d.phuongPhap}
${d.thietBi ? `- **Thiết bị:** ${d.thietBi}` : ''}
${d.ghiChu ? `- **Ghi chú:** ${d.ghiChu}` : ''}`
      
      handleSend(userMessage, {
        type: 'khbd',
        subject: actionData.subject,
        lessonName: d.baiHoc,
        grade: d.lopHoc,
        duration: d.soTiet,
        textbook: d.boSach,
        requirements: d.yeuCauCanDat,
        method: d.phuongPhap,
      })
    } else if (actionData.type === 'skkn') {
      const d = actionData.data
      userMessage = `💡 **Viết Sáng kiến Kinh nghiệm**
- **Tên sáng kiến:** ${d.tenSangKien}
- **Lĩnh vực:** ${d.linhVuc}
- **Cấp:** ${d.cap}
${d.monHoc ? `- **Môn học:** ${d.monHoc}` : ''}
${d.vanDe ? `- **Thực trạng:** ${d.vanDe}` : ''}
${d.giaiPhap ? `- **Giải pháp:** ${d.giaiPhap}` : ''}
${d.ketQua ? `- **Kết quả:** ${d.ketQua}` : ''}`
      
      handleSend(userMessage, {
        type: 'skkn',
        topic: d.tenSangKien,
        field: d.linhVuc,
        level: d.cap,
        subject: d.monHoc,
        problem: d.vanDe,
        solution: d.giaiPhap,
        results: d.ketQua,
      })
    }
  }

  return (
    <div className="flex h-screen bg-gemini-bg">
      {/* Sidebar */}
      <Sidebar 
        isOpen={sidebarOpen} 
        onToggle={() => setSidebarOpen(!sidebarOpen)} 
      />

      {/* Main Content */}
      <main className={`flex-1 flex flex-col transition-all duration-300 ${sidebarOpen ? 'ml-72' : 'ml-0'}`}>
        {/* Header */}
        <header className="h-16 flex items-center justify-between px-6 border-b border-gemini-border">
          <div className="flex items-center gap-3">
            {!sidebarOpen && (
              <button 
                onClick={() => setSidebarOpen(true)}
                className="p-2 hover:bg-gemini-hover rounded-lg"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            )}
            <h1 className="text-lg font-semibold flex items-center gap-2">
              <HiSparkles className="text-gemini-blue" />
              GiaoTrinh AI
            </h1>
          </div>
          
          <div className="flex items-center gap-4">
            {/* Quota indicator */}
            <div className="text-sm text-gray-400">
              <span className="text-gemini-blue font-medium">∞</span> giáo án còn lại
            </div>
            
            {/* User avatar */}
            <div className="w-8 h-8 rounded-full bg-gradient-to-r from-gemini-blue to-gemini-purple flex items-center justify-center">
              <span className="text-sm font-medium text-white">
                {user?.full_name?.charAt(0) || 'G'}
              </span>
            </div>
          </div>
        </header>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto">
          {messages.length === 0 ? (
            /* Welcome Screen */
            <div className="h-full flex flex-col items-center justify-center px-4">
              <div className="text-center mb-8">
                <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-gemini-blue to-gemini-purple rounded-3xl mb-6">
                  <HiSparkles className="w-10 h-10 text-white sparkle" />
                </div>
                <h2 className="text-2xl font-bold mb-2">
                  Xin chào {user?.full_name || 'Thầy/Cô'}!
                </h2>
                <p className="text-gray-400 text-lg">
                  Chúng ta nên bắt đầu từ đâu nhỉ?
                </p>
              </div>

              {/* Quick Actions */}
              <QuickActions onAction={handleQuickAction} />
            </div>
          ) : (
            /* Messages */
            <div className="max-w-4xl mx-auto py-6 px-4">
              {messages.map((msg, index) => (
                <ChatMessage 
                  key={msg.id || index} 
                  message={msg}
                  isLast={index === messages.length - 1}
                />
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-gemini-border">
          <div className="max-w-4xl mx-auto">
            <ChatInput 
              onSend={handleSend} 
              disabled={isGenerating}
              placeholder="Hỏi GiaoTrinh AI..."
            />
            
            {/* Quick action buttons below input when in chat */}
            {messages.length > 0 && (
              <div className="flex flex-wrap gap-2 mt-3 justify-center">
                <QuickActions onAction={handleQuickAction} compact />
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

export default Chat
