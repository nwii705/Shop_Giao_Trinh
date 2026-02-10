import { useState } from 'react'
import { 
  HiBookOpen, 
  HiBeaker, 
  HiLightBulb, 
  HiClipboardDocumentList,
  HiAcademicCap,
  HiDocumentText,
  HiPencilSquare,
  HiChatBubbleLeftRight
} from 'react-icons/hi2'
import KHBDModal from './modals/KHBDModal'
import SKKNModal from './modals/SKKNModal'

// Các action buttons cho giáo viên - KHÔNG chung chung như Gemini gốc
const QUICK_ACTIONS = [
  {
    id: 'khbd_khtn',
    label: 'Soạn KHBD KHTN',
    description: 'Khoa học Tự nhiên (Lý, Hóa, Sinh)',
    icon: HiBeaker,
    color: 'from-green-500 to-emerald-600',
    type: 'khbd',
    subject: 'khtn',
  },
  {
    id: 'khbd_nguvan',
    label: 'Soạn KHBD Ngữ Văn',
    description: 'Đọc hiểu, Viết, Nói và Nghe',
    icon: HiBookOpen,
    color: 'from-purple-500 to-violet-600',
    type: 'khbd',
    subject: 'nguvan',
  },
  {
    id: 'khbd_toan',
    label: 'Soạn KHBD Toán',
    description: 'Đại số, Hình học',
    icon: HiAcademicCap,
    color: 'from-blue-500 to-cyan-600',
    type: 'khbd',
    subject: 'toan',
  },
  {
    id: 'skkn',
    label: 'Viết SKKN',
    description: 'Sáng kiến kinh nghiệm',
    icon: HiLightBulb,
    color: 'from-yellow-500 to-orange-600',
    type: 'skkn',
  },
  {
    id: 'de_thi',
    label: 'Tạo Đề kiểm tra',
    description: 'Tự luận, Trắc nghiệm',
    icon: HiClipboardDocumentList,
    color: 'from-red-500 to-rose-600',
    type: 'exam',
  },
  {
    id: 'phan_tich',
    label: 'Phân tích Văn bản',
    description: 'Phân tích tác phẩm văn học',
    icon: HiDocumentText,
    color: 'from-pink-500 to-fuchsia-600',
    type: 'analysis',
  },
  {
    id: 'soan_bai',
    label: 'Soạn Bài giảng',
    description: 'PowerPoint, Slides',
    icon: HiPencilSquare,
    color: 'from-indigo-500 to-purple-600',
    type: 'slides',
  },
  {
    id: 'hoi_dap',
    label: 'Hỏi đáp Giáo dục',
    description: 'Tư vấn nghiệp vụ sư phạm',
    icon: HiChatBubbleLeftRight,
    color: 'from-teal-500 to-cyan-600',
    type: 'chat',
  },
]

function QuickActions({ onAction, compact = false }) {
  const [modalType, setModalType] = useState(null)
  const [selectedAction, setSelectedAction] = useState(null)

  const handleActionClick = (action) => {
    if (action.type === 'khbd') {
      setSelectedAction(action)
      setModalType('khbd')
    } else if (action.type === 'skkn') {
      setSelectedAction(action)
      setModalType('skkn')
    } else {
      // For other actions, just notify
      onAction(action)
    }
  }

  const handleModalSubmit = (data) => {
    onAction({
      ...selectedAction,
      ...data,
    })
    setModalType(null)
  }

  if (compact) {
    // Compact version - just small chips
    return (
      <>
        {QUICK_ACTIONS.slice(0, 4).map((action) => (
          <button
            key={action.id}
            onClick={() => handleActionClick(action)}
            className={`px-4 py-2 rounded-full bg-gradient-to-r ${action.color} 
                       text-white text-sm font-medium hover:opacity-90 transition-opacity
                       flex items-center gap-2`}
          >
            <action.icon className="w-4 h-4" />
            {action.label}
          </button>
        ))}
        
        {/* Modals */}
        {modalType === 'khbd' && (
          <KHBDModal 
            action={selectedAction}
            onSubmit={handleModalSubmit}
            onClose={() => setModalType(null)}
          />
        )}
        {modalType === 'skkn' && (
          <SKKNModal
            onSubmit={handleModalSubmit}
            onClose={() => setModalType(null)}
          />
        )}
      </>
    )
  }

  // Full version - grid of cards
  return (
    <>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl">
        {QUICK_ACTIONS.map((action) => (
          <button
            key={action.id}
            onClick={() => handleActionClick(action)}
            className="group p-4 bg-gemini-sidebar/50 hover:bg-gemini-sidebar border border-gemini-border 
                     rounded-2xl text-left transition-all duration-200 hover:scale-[1.02] hover:shadow-lg"
          >
            <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${action.color} 
                           flex items-center justify-center mb-3 group-hover:scale-110 transition-transform`}>
              <action.icon className="w-6 h-6 text-white" />
            </div>
            <h3 className="font-medium text-white mb-1">{action.label}</h3>
            <p className="text-sm text-gray-400">{action.description}</p>
          </button>
        ))}
      </div>

      {/* Modals */}
      {modalType === 'khbd' && (
        <KHBDModal 
          action={selectedAction}
          onSubmit={handleModalSubmit}
          onClose={() => setModalType(null)}
        />
      )}
      {modalType === 'skkn' && (
        <SKKNModal
          onSubmit={handleModalSubmit}
          onClose={() => setModalType(null)}
        />
      )}
    </>
  )
}

export default QuickActions
