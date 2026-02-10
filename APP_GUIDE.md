# GiaoTrinh AI - Hướng dẫn vận hành & Luồng hoạt động

Tài liệu này hướng dẫn cách chạy ứng dụng và giải thích luồng hoạt động của hệ thống GiaoTrinh AI.

## 1. Hướng dẫn chạy ứng dụng (Development)

Để chạy trọn vẹn hệ thống, bạn cần mở 2 terminal riêng biệt: một cho **Backend** và một cho **Frontend**.

### A. Backend (Python/FastAPI)

Backend chịu trách nhiệm xử lý logic, kết nối CSDL và gọi AI (Gemini).

1. Mở terminal tại thư mục gốc `d:\APP_GV_GiaoTrinh`.
2. Di chuyển vào thư mục backend:
   ```powershell
   cd backend
   ```
3. Kích hoạt môi trường ảo (Virtual Environment):
   ```powershell
   .\venv\Scripts\activate
   ```
4. Chạy server (Sử dụng script `run.py` để tự động kiểm tra thư viện):
   ```powershell
   python run.py
   ```
   *Backend sẽ khởi động tại: `http://localhost:8000`*
   *API Documentation: `http://localhost:8000/docs`*

### B. Frontend (React/Vite)

Frontend là giao diện người dùng web.

1. Mở terminal **mới** tại thư mục gốc.
2. Di chuyển vào thư mục frontend:
   ```powershell
   cd frontend
   ```
3. Cài đặt thư viện (nếu chưa cài):
   ```powershell
   npm install
   ```
4. Chạy server phát triển:
   ```powershell
   npm run dev
   ```
   *Frontend thường sẽ chạy tại: `http://localhost:5173` hoặc `http://localhost:3000` (xem thông báo trên terminal)*

---

## 2. Cấu trúc Dự án

```
APP_GV_GiaoTrinh/
├── backend/                # Server xử lý logic chính
│   ├── app/
│   │   ├── routers/        # Các API endpoints (API Login, KHBD, SKKN...)
│   │   ├── services/       # Logic nghiệp vụ (Gọi Gemini AI, tạo file Word)
│   │   ├── database/       # Cấu hình CSDL (SQLite) và Models
│   │   └── prompts/        # Template câu lệnh (prompt) gửi cho AI
│   ├── outputs/            # Nơi lưu file Word được tạo ra tạm thời
│   ├── run.py              # Script khởi động server
│   └── requirements.txt    # Danh sách thư viện Python
│
├── frontend/               # Giao diện người dùng
│   ├── src/
│   │   ├── components/     # Các thành phần giao diện (Chat, Modal...)
│   │   ├── pages/          # Các màn hình chính (Login, Chat Dashboard)
│   │   ├── services/       # File gọi API xuống backend
│   │   └── stores/         # Quản lý trạng thái (Zustand) - lưu user login
│   ├── package.json        # Cấu hình dự án React
│   └── vite.config.js      # Cấu hình Vite
```

---

## 3. Luồng hoạt động (App Flow)

### A. Quy trình Đăng nhập & Xác thực
1. **User** nhập Email/Password tại Frontend.
2. **Frontend** gửi request `POST /api/auth/login` xuống Backend.
3. **Backend** kiểm tra database, nếu đúng trả về `access_token` (JWT).
4. **Frontend** lưu token vào `localStorage` và chuyển hướng vào Dashboard.
5. Mọi request sau đó (tạo bài giảng, chat) đều đính kèm Token này để xác thực.

### B. Tính năng: Soạn Kế hoạch Bài dạy (KHBD)
1. **Input:** Người dùng chọn Môn, Lớp, Bộ sách, Tên bài học và Yêu cầu cần đạt.
2. **Trigger:** Bấm "Tạo kế hoạch".
3. **Process:**
   - Frontend gửi thông tin đến `POST /api/khbd/generate`.
   - Backend nhận dữ liệu -> Ghép vào Prompt mẫu (trong `app/prompts`).
   - Backend gọi **Gemini Service** -> Gửi prompt sang Google Gemini API.
   - Gemini trả về nội dung bài soạn dưới dạng Markdown.
4. **Output:** Frontend hiển thị bài soạn ra màn hình chat.
5. **Export:** Người dùng bấm nút "Tải về Word" -> Backend sử dụng `DocumentConverter` để chuyển Markdown thành `.docx` và trả file về.

### C. Tính năng: Viết Sáng kiến Kinh nghiệm (SKKN)
Tương tự KHBD nhưng chia thành nhiều bước (Step-by-step):
1. User chọn đề tài/lĩnh vực.
2. AI đề xuất Đề cương chi tiết.
3. User duyệt đề cương -> AI viết chi tiết từng mục.
4. Hợp nhất nội dung thành văn bản hoàn chỉnh để xuất file.

## 4. Tài khoản Demo

- **Admin/User:** `demo@giaotrinh.ai`
- **Mật khẩu:** `demo123456`
