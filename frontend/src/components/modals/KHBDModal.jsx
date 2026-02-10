import { useState } from 'react'
import { HiXMark, HiBeaker, HiBookOpen, HiAcademicCap } from 'react-icons/hi2'

// Các bộ sách giáo khoa phổ biến
const TEXTBOOK_CONFIG = {
  ctst: {
    name: 'Chân trời sáng tạo',
    publisher: 'NXB Giáo dục Việt Nam',
    shortCode: 'CTST',
  },
  kntt: {
    name: 'Kết nối tri thức với cuộc sống', 
    publisher: 'NXB Giáo dục Việt Nam',
    shortCode: 'KNTT',
  },
  cd: {
    name: 'Cánh diều',
    publisher: 'NXB Đại học Sư phạm',
    shortCode: 'CD',
  },
}

// Cấu trúc chương trình giảng dạy theo môn
const SUBJECT_CONFIG = {
  khtn: {
    name: 'Khoa học Tự nhiên',
    icon: HiBeaker,
    grades: ['6', '7', '8', '9'],
    fields: ['Vật lý', 'Hóa học', 'Sinh học'],
    defaultField: 'Vật lý',
  },
  nguvan: {
    name: 'Ngữ văn',
    icon: HiBookOpen,
    grades: ['6', '7', '8', '9', '10', '11', '12'],
    fields: ['Đọc hiểu', 'Viết', 'Nói và nghe'],
    defaultField: 'Đọc hiểu',
  },
  toan: {
    name: 'Toán học',
    icon: HiAcademicCap,
    grades: ['6', '7', '8', '9', '10', '11', '12'],
    fields: ['Đại số', 'Hình học', 'Thống kê và Xác suất'],
    defaultField: 'Đại số',
  },
}

function KHBDModal({ action, onSubmit, onClose }) {
  const config = SUBJECT_CONFIG[action.subject] || SUBJECT_CONFIG.khtn
  
  const [formData, setFormData] = useState({
    baiHoc: '',
    lopHoc: config.grades[0],
    linhVuc: config.defaultField,
    boSach: 'ctst',  // Mặc định: Chân trời sáng tạo
    soTiet: 2,
    yeuCauCanDat: '',
    phuongPhap: 'Dạy học tích cực',
    thietBi: '',
    ghiChu: '',
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!formData.baiHoc.trim()) return
    
    onSubmit({
      type: 'khbd',
      subject: action.subject,
      data: formData,
    })
  }

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-[#1e1e30] border border-gemini-border rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gemini-border sticky top-0 bg-[#1e1e30]">
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-xl bg-gradient-to-r ${action.color} flex items-center justify-center`}>
              <config.icon className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-white">Soạn Kế hoạch Bài dạy</h2>
              <p className="text-sm text-gray-400">{config.name}</p>
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
          {/* Bộ sách giáo khoa */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Bộ sách giáo khoa <span className="text-red-400">*</span>
            </label>
            <select
              value={formData.boSach}
              onChange={(e) => setFormData({ ...formData, boSach: e.target.value })}
              className="w-full px-4 py-3 bg-gemini-sidebar border border-gemini-border rounded-xl
                       text-white focus:outline-none focus:border-gemini-blue"
            >
              {Object.entries(TEXTBOOK_CONFIG).map(([key, book]) => (
                <option key={key} value={key}>
                  {book.name} ({book.shortCode})
                </option>
              ))}
            </select>
            <p className="text-xs text-gray-500 mt-1">
              Nội dung sẽ được tra cứu từ sách giáo khoa thực tế
            </p>
          </div>

          {/* Tên bài học */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Tên bài học <span className="text-red-400">*</span>
            </label>
            <input
              type="text"
              value={formData.baiHoc}
              onChange={(e) => setFormData({ ...formData, baiHoc: e.target.value })}
              placeholder="VD: Bài 5. Lực ma sát, Bài 12. Cấu tạo nguyên tử..."
              className="w-full px-4 py-3 bg-gemini-sidebar border border-gemini-border rounded-xl
                       text-white placeholder-gray-500 focus:outline-none focus:border-gemini-blue"
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              Nhập chính xác tên bài theo sách để AI tra cứu đúng nội dung
            </p>
          </div>

          {/* Lớp và Lĩnh vực */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Lớp</label>
              <select
                value={formData.lopHoc}
                onChange={(e) => setFormData({ ...formData, lopHoc: e.target.value })}
                className="w-full px-4 py-3 bg-gemini-sidebar border border-gemini-border rounded-xl
                         text-white focus:outline-none focus:border-gemini-blue"
              >
                {config.grades.map(grade => (
                  <option key={grade} value={grade}>Lớp {grade}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Lĩnh vực/Phân môn</label>
              <select
                value={formData.linhVuc}
                onChange={(e) => setFormData({ ...formData, linhVuc: e.target.value })}
                className="w-full px-4 py-3 bg-gemini-sidebar border border-gemini-border rounded-xl
                         text-white focus:outline-none focus:border-gemini-blue"
              >
                {config.fields.map(field => (
                  <option key={field} value={field}>{field}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Số tiết */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Số tiết</label>
            <input
              type="number"
              min="1"
              max="10"
              value={formData.soTiet}
              onChange={(e) => setFormData({ ...formData, soTiet: parseInt(e.target.value) })}
              className="w-full px-4 py-3 bg-gemini-sidebar border border-gemini-border rounded-xl
                       text-white focus:outline-none focus:border-gemini-blue"
            />
          </div>

          {/* Yêu cầu cần đạt */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Yêu cầu cần đạt (mục tiêu bài học)
            </label>
            <textarea
              value={formData.yeuCauCanDat}
              onChange={(e) => setFormData({ ...formData, yeuCauCanDat: e.target.value })}
              placeholder="VD: Học sinh mô tả được lực ma sát, phân biệt ma sát trượt, lăn, nghỉ..."
              rows={3}
              className="w-full px-4 py-3 bg-gemini-sidebar border border-gemini-border rounded-xl
                       text-white placeholder-gray-500 focus:outline-none focus:border-gemini-blue resize-none"
            />
          </div>

          {/* Phương pháp */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Phương pháp dạy học</label>
            <select
              value={formData.phuongPhap}
              onChange={(e) => setFormData({ ...formData, phuongPhap: e.target.value })}
              className="w-full px-4 py-3 bg-gemini-sidebar border border-gemini-border rounded-xl
                       text-white focus:outline-none focus:border-gemini-blue"
            >
              <option value="Dạy học tích cực">Dạy học tích cực</option>
              <option value="Dạy học dự án">Dạy học dự án</option>
              <option value="Dạy học theo nhóm">Dạy học theo nhóm</option>
              <option value="Dạy học qua trải nghiệm">Dạy học qua trải nghiệm</option>
              <option value="Dạy học STEM">Dạy học STEM</option>
              <option value="Kết hợp">Kết hợp nhiều phương pháp</option>
            </select>
          </div>

          {/* Thiết bị */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Thiết bị dạy học (nếu có)
            </label>
            <input
              type="text"
              value={formData.thietBi}
              onChange={(e) => setFormData({ ...formData, thietBi: e.target.value })}
              placeholder="VD: Máy chiếu, bộ thí nghiệm, phiếu học tập..."
              className="w-full px-4 py-3 bg-gemini-sidebar border border-gemini-border rounded-xl
                       text-white placeholder-gray-500 focus:outline-none focus:border-gemini-blue"
            />
          </div>

          {/* Ghi chú */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Yêu cầu khác (ghi chú)
            </label>
            <textarea
              value={formData.ghiChu}
              onChange={(e) => setFormData({ ...formData, ghiChu: e.target.value })}
              placeholder="VD: Tích hợp GDMT, phù hợp với HS vùng khó khăn..."
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
              className="flex-1 px-6 py-3 bg-gradient-to-r from-gemini-blue to-gemini-purple 
                       text-white rounded-xl hover:opacity-90 transition-opacity font-medium"
            >
              Bắt đầu soạn
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default KHBDModal
