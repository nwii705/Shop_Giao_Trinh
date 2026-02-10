import { useState } from 'react'
import { HiXMark, HiLightBulb } from 'react-icons/hi2'

// Các lĩnh vực SKKN phổ biến
const SKKN_FIELDS = [
  'Đổi mới phương pháp dạy học',
  'Ứng dụng CNTT trong dạy học',
  'Giáo dục kỹ năng sống',
  'Nâng cao chất lượng dạy học môn học',
  'Công tác chủ nhiệm lớp',
  'Quản lý giáo dục',
  'Giáo dục hướng nghiệp',
  'Dạy học tích hợp',
  'Dạy học STEM',
  'Kiểm tra đánh giá',
]

const LEVELS = ['Trường', 'Phòng', 'Sở', 'Tỉnh/Thành phố', 'Quốc gia']

function SKKNModal({ onSubmit, onClose }) {
  const [formData, setFormData] = useState({
    tenSangKien: '',
    linhVuc: SKKN_FIELDS[0],
    vanDe: '',
    giaiPhap: '',
    ketQua: '',
    cap: 'Trường',
    monHoc: '',
    namAp: new Date().getFullYear(),
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!formData.tenSangKien.trim()) return
    
    onSubmit({
      type: 'skkn',
      data: formData,
    })
  }

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-[#1e1e30] border border-gemini-border rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gemini-border sticky top-0 bg-[#1e1e30]">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-yellow-500 to-orange-600 flex items-center justify-center">
              <HiLightBulb className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-white">Viết Sáng kiến Kinh nghiệm</h2>
              <p className="text-sm text-gray-400">AI sẽ hỗ trợ bạn viết SKKN hoàn chỉnh</p>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-2 hover:bg-gemini-hover rounded-lg transition-colors"
          >
            <HiXMark className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-5">
          {/* Tên sáng kiến */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Tên sáng kiến <span className="text-red-400">*</span>
            </label>
            <input
              type="text"
              value={formData.tenSangKien}
              onChange={(e) => setFormData({ ...formData, tenSangKien: e.target.value })}
              placeholder="VD: Một số biện pháp nâng cao chất lượng dạy học Vật lý lớp 8"
              className="w-full px-4 py-3 bg-gemini-sidebar border border-gemini-border rounded-xl
                       text-white placeholder-gray-500 focus:outline-none focus:border-gemini-blue"
              required
            />
          </div>

          {/* Lĩnh vực và Cấp */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Lĩnh vực</label>
              <select
                value={formData.linhVuc}
                onChange={(e) => setFormData({ ...formData, linhVuc: e.target.value })}
                className="w-full px-4 py-3 bg-gemini-sidebar border border-gemini-border rounded-xl
                         text-white focus:outline-none focus:border-gemini-blue"
              >
                {SKKN_FIELDS.map(field => (
                  <option key={field} value={field}>{field}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Cấp đề tài</label>
              <select
                value={formData.cap}
                onChange={(e) => setFormData({ ...formData, cap: e.target.value })}
                className="w-full px-4 py-3 bg-gemini-sidebar border border-gemini-border rounded-xl
                         text-white focus:outline-none focus:border-gemini-blue"
              >
                {LEVELS.map(level => (
                  <option key={level} value={level}>Cấp {level}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Môn học */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Môn học áp dụng
            </label>
            <input
              type="text"
              value={formData.monHoc}
              onChange={(e) => setFormData({ ...formData, monHoc: e.target.value })}
              placeholder="VD: Vật lý, Toán, Ngữ văn..."
              className="w-full px-4 py-3 bg-gemini-sidebar border border-gemini-border rounded-xl
                       text-white placeholder-gray-500 focus:outline-none focus:border-gemini-blue"
            />
          </div>

          {/* Vấn đề cần giải quyết */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Vấn đề cần giải quyết (thực trạng)
            </label>
            <textarea
              value={formData.vanDe}
              onChange={(e) => setFormData({ ...formData, vanDe: e.target.value })}
              placeholder="Mô tả ngắn gọn những khó khăn, hạn chế cần khắc phục..."
              rows={3}
              className="w-full px-4 py-3 bg-gemini-sidebar border border-gemini-border rounded-xl
                       text-white placeholder-gray-500 focus:outline-none focus:border-gemini-blue resize-none"
            />
          </div>

          {/* Giải pháp đề xuất */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Ý tưởng giải pháp chính
            </label>
            <textarea
              value={formData.giaiPhap}
              onChange={(e) => setFormData({ ...formData, giaiPhap: e.target.value })}
              placeholder="Mô tả ý tưởng hoặc giải pháp bạn đã/muốn áp dụng..."
              rows={3}
              className="w-full px-4 py-3 bg-gemini-sidebar border border-gemini-border rounded-xl
                       text-white placeholder-gray-500 focus:outline-none focus:border-gemini-blue resize-none"
            />
          </div>

          {/* Kết quả mong đợi */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Kết quả đã đạt được (nếu có)
            </label>
            <textarea
              value={formData.ketQua}
              onChange={(e) => setFormData({ ...formData, ketQua: e.target.value })}
              placeholder="Số liệu, minh chứng về hiệu quả của sáng kiến..."
              rows={2}
              className="w-full px-4 py-3 bg-gemini-sidebar border border-gemini-border rounded-xl
                       text-white placeholder-gray-500 focus:outline-none focus:border-gemini-blue resize-none"
            />
          </div>

          {/* Submit buttons */}
          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-6 py-3 bg-gemini-hover text-gray-300 rounded-xl
                       hover:bg-gemini-border transition-colors font-medium"
            >
              Hủy
            </button>
            <button
              type="submit"
              className="flex-1 px-6 py-3 bg-gradient-to-r from-yellow-500 to-orange-600 
                       text-white rounded-xl hover:opacity-90 transition-opacity font-medium"
            >
              Bắt đầu viết SKKN
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default SKKNModal
