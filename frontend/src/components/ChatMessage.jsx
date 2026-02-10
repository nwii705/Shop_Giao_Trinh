import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import { HiSparkles, HiUser, HiDocumentArrowDown, HiClipboard, HiArrowPath, HiCheck } from 'react-icons/hi2'
import api from '../services/api'

function ChatMessage({ message, isLast, documentId }) {
  const isUser = message.role === 'user'
  const isLoading = message.loading && !message.content
  const [copied, setCopied] = useState(false)
  const [downloading, setDownloading] = useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message.content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const handleDownloadWord = async () => {
    setDownloading(true)
    try {
      // Gọi API convert-to-word để tạo file Word thực sự
      const response = await api.convertToWord(message.content, 'KHBD')
      const blob = new Blob([response.data], { 
        type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' 
      })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `KHBD_${new Date().toISOString().slice(0,10)}.docx`
      a.click()
      URL.revokeObjectURL(url)
    } catch (err) {
      console.error('Download failed:', err)
      // Fallback: nếu API lỗi thì thử download qua documentId
      if (documentId) {
        try {
          const response = await api.downloadKHBD(documentId)
          const blob = new Blob([response.data], { 
            type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' 
          })
          const url = URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url
          a.download = `KHBD_${documentId}.docx`
          a.click()
          URL.revokeObjectURL(url)
        } catch (err2) {
          console.error('Fallback download also failed:', err2)
          alert('Không thể tải file Word. Vui lòng thử lại sau.')
        }
      } else {
        alert('Không thể tải file Word. Vui lòng thử lại sau.')
      }
    } finally {
      setDownloading(false)
    }
  }

  return (
    <div className={`flex gap-4 mb-6 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {/* AI Avatar */}
      {!isUser && (
        <div className="w-10 h-10 rounded-full bg-gradient-to-r from-gemini-blue to-gemini-purple 
                      flex items-center justify-center flex-shrink-0 sticky top-4">
          <HiSparkles className="w-5 h-5 text-white" />
        </div>
      )}

      {/* Message Content */}
      <div className={`flex-1 max-w-[90%] ${isUser ? 'order-first max-w-[70%]' : ''}`}>
        <div
          className={`rounded-2xl px-6 py-5 ${
            isUser
              ? 'bg-gemini-blue/20 text-white ml-auto'
              : 'bg-gemini-sidebar border border-gemini-border'
          }`}
        >
          {isLoading ? (
            <div className="flex items-center gap-3">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-gemini-blue rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-gemini-purple rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-pink-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
              <span className="text-gray-400 text-sm">Đang soạn giáo án...</span>
            </div>
          ) : isUser ? (
            <p className="text-white whitespace-pre-wrap">{message.content}</p>
          ) : (
            <div className="markdown-content prose prose-invert prose-sm max-w-none">
              <ReactMarkdown
                remarkPlugins={[remarkGfm, remarkMath]}
                rehypePlugins={[rehypeKatex]}
                components={{
                  // Custom table styling
                  table: ({ children }) => (
                    <div className="overflow-x-auto my-4">
                      <table className="min-w-full border-collapse border border-gemini-border">
                        {children}
                      </table>
                    </div>
                  ),
                  th: ({ children }) => (
                    <th className="border border-gemini-border bg-gemini-hover px-3 py-2 text-left font-semibold">
                      {children}
                    </th>
                  ),
                  td: ({ children }) => (
                    <td className="border border-gemini-border px-3 py-2">
                      {children}
                    </td>
                  ),
                  // Custom heading styling
                  h1: ({ children }) => (
                    <h1 className="text-2xl font-bold text-gemini-blue mt-6 mb-4 pb-2 border-b border-gemini-border">
                      {children}
                    </h1>
                  ),
                  h2: ({ children }) => (
                    <h2 className="text-xl font-bold text-gemini-purple mt-5 mb-3">
                      {children}
                    </h2>
                  ),
                  h3: ({ children }) => (
                    <h3 className="text-lg font-semibold text-white mt-4 mb-2">
                      {children}
                    </h3>
                  ),
                  h4: ({ children }) => (
                    <h4 className="text-base font-semibold text-gray-200 mt-3 mb-2">
                      {children}
                    </h4>
                  ),
                  // Code blocks
                  code: ({ inline, children }) => (
                    inline 
                      ? <code className="bg-gemini-hover px-1.5 py-0.5 rounded text-pink-400 text-sm">{children}</code>
                      : <code className="block bg-gemini-dark p-4 rounded-lg overflow-x-auto text-sm">{children}</code>
                  ),
                  // Blockquotes for important notes
                  blockquote: ({ children }) => (
                    <blockquote className="border-l-4 border-gemini-purple bg-gemini-hover/50 pl-4 py-2 my-4 italic">
                      {children}
                    </blockquote>
                  ),
                  // Lists
                  ul: ({ children }) => (
                    <ul className="list-disc list-inside space-y-1 my-3">
                      {children}
                    </ul>
                  ),
                  ol: ({ children }) => (
                    <ol className="list-decimal list-inside space-y-1 my-3">
                      {children}
                    </ol>
                  ),
                  // Horizontal rule
                  hr: () => (
                    <hr className="border-gemini-border my-6" />
                  ),
                  // Strong text
                  strong: ({ children }) => (
                    <strong className="font-bold text-white">{children}</strong>
                  ),
                }}
              >
                {message.content}
              </ReactMarkdown>
            </div>
          )}
        </div>

        {/* Action buttons for AI messages */}
        {!isUser && !isLoading && message.content && (
          <div className="flex items-center gap-3 mt-3 px-2">
            <button 
              onClick={handleDownloadWord}
              disabled={downloading}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-gemini-blue/20 hover:bg-gemini-blue/30 
                       text-gemini-blue rounded-lg transition-colors text-sm font-medium"
              title="Tải file Word"
            >
              <HiDocumentArrowDown className="w-4 h-4" />
              {downloading ? 'Đang tải...' : 'Tải Word'}
            </button>
            
            <button 
              onClick={handleCopy}
              className="flex items-center gap-1.5 px-3 py-1.5 hover:bg-gemini-hover 
                       text-gray-400 hover:text-white rounded-lg transition-colors text-sm"
              title="Sao chép nội dung"
            >
              {copied ? (
                <>
                  <HiCheck className="w-4 h-4 text-green-400" />
                  <span className="text-green-400">Đã sao chép</span>
                </>
              ) : (
                <>
                  <HiClipboard className="w-4 h-4" />
                  Sao chép
                </>
              )}
            </button>
            
            <button 
              className="flex items-center gap-1.5 px-3 py-1.5 hover:bg-gemini-hover 
                       text-gray-400 hover:text-white rounded-lg transition-colors text-sm"
              title="Tạo lại nội dung"
            >
              <HiArrowPath className="w-4 h-4" />
              Tạo lại
            </button>
          </div>
        )}
      </div>

      {/* User Avatar */}
      {isUser && (
        <div className="w-10 h-10 rounded-full bg-gemini-hover flex items-center justify-center flex-shrink-0">
          <HiUser className="w-5 h-5 text-gray-400" />
        </div>
      )}
    </div>
  )
}

export default ChatMessage
