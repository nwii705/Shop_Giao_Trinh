import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useChatStore = create(
  persist(
    (set, get) => ({
      conversations: [],
      currentConversationId: null,
      isGenerating: false,

      // Lấy current conversation
      getCurrentConversation: () => {
        const { conversations, currentConversationId } = get()
        return conversations.find(c => c.id === currentConversationId) || null
      },

      // Lấy messages của current conversation
      getMessages: () => {
        const conversation = get().getCurrentConversation()
        return conversation?.messages || []
      },

      // Tạo cuộc trò chuyện mới
      newConversation: (title = null) => {
        // Lưu messages hiện tại vào conversation cũ trước
        const { currentConversationId, conversations } = get()
        
        const id = Date.now().toString()
        const conversation = {
          id,
          title: title || 'Cuộc trò chuyện mới',
          createdAt: new Date().toISOString(),
          messages: [],
        }
        
        set({
          conversations: [conversation, ...conversations],
          currentConversationId: id,
        })
        
        return conversation
      },

      // Chọn cuộc trò chuyện
      selectConversation: (id) => {
        const conversation = get().conversations.find(c => c.id === id)
        if (conversation) {
          set({ currentConversationId: id })
        }
      },

      // Thêm tin nhắn vào conversation hiện tại
      addMessage: (message) => {
        const { currentConversationId, conversations } = get()
        
        if (!currentConversationId) {
          // Tạo conversation mới nếu chưa có
          get().newConversation()
        }
        
        const newMessage = {
          id: Date.now().toString(),
          ...message,
          createdAt: new Date().toISOString(),
        }
        
        set((state) => ({
          conversations: state.conversations.map(conv => 
            conv.id === state.currentConversationId
              ? { ...conv, messages: [...(conv.messages || []), newMessage] }
              : conv
          ),
        }))
      },

      // Cập nhật tin nhắn cuối (cho streaming/loading)
      updateLastMessage: (content) => {
        set((state) => ({
          conversations: state.conversations.map(conv => {
            if (conv.id === state.currentConversationId) {
              const messages = [...(conv.messages || [])]
              if (messages.length > 0) {
                messages[messages.length - 1] = {
                  ...messages[messages.length - 1],
                  content,
                  loading: false,
                }
              }
              return { ...conv, messages }
            }
            return conv
          }),
        }))
      },

      // Set trạng thái generating
      setGenerating: (value) => set({ isGenerating: value }),

      // Cập nhật title cuộc trò chuyện
      updateConversationTitle: (id, title) => {
        set((state) => ({
          conversations: state.conversations.map(c =>
            c.id === id ? { ...c, title } : c
          ),
        }))
      },

      // Cập nhật title của conversation hiện tại
      updateCurrentTitle: (title) => {
        const { currentConversationId } = get()
        if (currentConversationId && title) {
          get().updateConversationTitle(currentConversationId, title)
        }
      },

      // Xóa cuộc trò chuyện
      deleteConversation: (id) => {
        set((state) => {
          const newConversations = state.conversations.filter(c => c.id !== id)
          const wasCurrentDeleted = state.currentConversationId === id
          
          return {
            conversations: newConversations,
            currentConversationId: wasCurrentDeleted 
              ? (newConversations[0]?.id || null)
              : state.currentConversationId,
          }
        })
      },

      // Xóa tất cả conversations
      clearAllConversations: () => {
        set({
          conversations: [],
          currentConversationId: null,
        })
      },
    }),
    {
      name: 'giaotrinh-chat-storage', // Key trong localStorage
      partialize: (state) => ({
        conversations: state.conversations,
        currentConversationId: state.currentConversationId,
      }),
    }
  )
)
