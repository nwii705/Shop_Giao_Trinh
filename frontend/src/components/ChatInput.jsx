import { useState, useRef, useEffect } from 'react'
import { HiPaperAirplane, HiMicrophone, HiPlus } from 'react-icons/hi2'

function ChatInput({ onSend, disabled, placeholder }) {
  const [message, setMessage] = useState('')
  const textareaRef = useRef(null)

  // Auto-resize textarea
  useEffect(() => {
    const textarea = textareaRef.current
    if (textarea) {
      textarea.style.height = 'auto'
      textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px'
    }
  }, [message])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim() && !disabled) {
      onSend(message)
      setMessage('')
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="relative">
      <div className="flex items-end gap-3 bg-gemini-sidebar border border-gemini-border rounded-2xl p-3">
        {/* Add attachment button */}
        <button
          type="button"
          className="p-2 hover:bg-gemini-hover rounded-xl transition-colors flex-shrink-0"
          title="Đính kèm file"
        >
          <HiPlus className="w-5 h-5 text-gray-400" />
        </button>

        {/* Text input */}
        <div className="flex-1">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            disabled={disabled}
            rows={1}
            className="w-full bg-transparent text-white placeholder-gray-500 resize-none 
                     focus:outline-none disabled:opacity-50"
            style={{ maxHeight: '200px' }}
          />
        </div>

        {/* Action buttons */}
        <div className="flex items-center gap-2 flex-shrink-0">
          {/* Voice input */}
          <button
            type="button"
            className="p-2 hover:bg-gemini-hover rounded-xl transition-colors"
            title="Nhập bằng giọng nói"
          >
            <HiMicrophone className="w-5 h-5 text-gray-400" />
          </button>

          {/* Send button */}
          <button
            type="submit"
            disabled={!message.trim() || disabled}
            className="p-2 bg-gradient-to-r from-gemini-blue to-gemini-purple rounded-xl
                     disabled:opacity-50 disabled:cursor-not-allowed
                     hover:opacity-90 transition-opacity"
          >
            <HiPaperAirplane className="w-5 h-5 text-white" />
          </button>
        </div>
      </div>

      {/* Helper text */}
      <p className="text-center text-xs text-gray-500 mt-2">
        GiaoTrinh AI có thể mắc lỗi. Vui lòng kiểm tra lại nội dung trước khi sử dụng.
      </p>
    </form>
  )
}

export default ChatInput
