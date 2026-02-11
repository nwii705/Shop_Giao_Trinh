# 📚 EduShop - Hướng Dẫn Sử Dụng

> **Phiên bản:** 1.0  
> **Cập nhật:** Tháng 2/2026  
> **Website:** https://docs-google.up.railway.app/

---

## 📋 MỤC LỤC

1. [Tổng quan](#1-tổng-quan)
2. [Dành cho khách hàng](#2-dành-cho-khách-hàng)
3. [Dành cho Admin](#3-dành-cho-admin)
4. [Các tính năng hoạt động](#4-các-tính-năng-hoạt-động)
5. [Hạn chế & Lưu ý](#5-hạn-chế--lưu-ý)

---

## 1. TỔNG QUAN

### Địa chỉ truy cập
| Trang | URL |
|-------|-----|
| Trang chủ | https://docs-google.up.railway.app/ |
| Tự soạn KHBD/SKKN | https://docs-google.up.railway.app/generator.html |
| Tạo đề thi | https://docs-google.up.railway.app/exam-generator.html |
| Lịch sử | https://docs-google.up.railway.app/history.html |
| Admin | https://docs-google.up.railway.app/admin.html |

### Công nghệ
- **Backend:** Node.js + Express, MongoDB Atlas
- **Hosting:** Railway (tự động deploy từ GitHub)
- **AI:** OpenRouter API (Gemini 2.0 Flash)

---

## 2. DÀNH CHO KHÁCH HÀNG

### 2.1. Xem & Mua giáo trình (✅ Hoạt động)

**Cách dùng:**
1. Vào trang chủ
2. Lọc theo danh mục: AI, STEM, Phương pháp, Kỹ năng
3. Click sản phẩm để xem chi tiết
4. Nhập thông tin: Họ tên, Email, SĐT
5. Thanh toán qua QR (hiển thị mã QR)
6. Đợi Admin xác nhận và gửi tài liệu qua email

**Lưu ý:**
- Quy trình thanh toán là **thủ công** - Admin cần kiểm tra và gửi file
- Không có hệ thống tự động gửi file

---

### 2.2. Tự soạn KHBD (✅ Hoạt động)

**Địa chỉ:** `/generator.html` → Tab **KHBD**

**Cách dùng:**
1. Nhập **API Key** (do bạn cung cấp)
2. Bấm **"Kiểm tra"** để xác nhận key hoạt động
3. (Tùy chọn) Upload file sách PDF/ảnh
4. Chọn: Cấp học → Lớp → Môn → Bộ sách → Bài học
5. Bấm **"🚀 Tạo KHBD"**
6. Đợi AI soạn (1-3 phút)
7. Bấm **"📄 Xuất Word"** để tải file

**Môn học hỗ trợ:**
- THCS (Lớp 6-9): Toán, Ngữ văn, Tiếng Anh, KHTN, Lịch sử, Địa lý, GDCD, Tin học, Công nghệ, Âm nhạc, Mỹ thuật, HĐTN
- THPT (Lớp 10-12): Tương tự + Vật lý, Hóa học, Sinh học riêng

**Bộ sách:**
- Kết nối tri thức
- Chân trời sáng tạo  
- Cánh diều

---

### 2.3. Tự soạn SKKN (✅ Hoạt động)

**Địa chỉ:** `/generator.html` → Tab **SKKN**

**Cách dùng:**
1. Nhập **API Key**
2. Bấm **"Kiểm tra"**
3. Điền thông tin cơ bản:
   - Vai trò (VD: Giáo viên Toán THCS)
   - Môn học
   - Cấp học  
   - Đề tài (hoặc để trống AI sẽ đề xuất)
4. (Tùy chọn) Cấu hình nâng cao:
   - Số từ: 5000 - 20000
   - Số giải pháp: 3 - 7
   - Deep Research: Bật/tắt nghiên cứu web
5. Bấm **"🚀 Tạo SKKN"**
6. Đợi AI soạn (3-10 phút tùy độ dài)
7. Xuất Word khi hoàn thành

**Cấu trúc SKKN:** Theo QĐ 658/QĐ-SGDĐT
- Phần I: Mở đầu (lý do, mục đích, đối tượng, phương pháp)
- Phần II: Nội dung (cơ sở lý luận, thực trạng, giải pháp)
- Phần III: Kết quả, kết luận, kiến nghị

---

### 2.4. Tạo đề thi (✅ Hoạt động)

**Địa chỉ:** `/exam-generator.html`

**Cách dùng:**
1. Nhập **API Key**
2. Chọn **Môn học** (12 môn)
3. Chọn **Lớp** (6-12)
4. Chọn **Loại đề**: 15 phút, 45 phút, Giữa kỳ, Cuối kỳ
5. Nhập **Nội dung kiến thức** cần ra đề
6. Chọn **Số mã đề** (1-4)
7. Bấm **"⚡ Tạo đề thi"**
8. Đợi AI tạo (1-3 phút)
9. Tải: **Đề thi Word** + **Đáp án Word**

**Môn học:** Toán, Vật lý, Hóa học, Sinh học, KHTN, Ngữ văn, Tiếng Anh, Lịch sử, Địa lý, GDCD, Tin học, Công nghệ

**Ma trận đề:** Theo Thông tư 22/2021
- Nhận biết
- Thông hiểu
- Vận dụng
- Vận dụng cao

---

### 2.5. Lịch sử tài liệu (✅ Hoạt động)

**Địa chỉ:** `/history.html`

- Xem lại KHBD/SKKN đã tạo
- Lọc theo loại (KHBD/SKKN)
- Tìm kiếm theo tên
- Xóa tài liệu không cần

**Lưu ý:** Dữ liệu lưu trong **localStorage** của trình duyệt. Nếu xóa cache sẽ mất.

---

### 2.6. Trang cá nhân (⚠️ Cơ bản)

**Địa chỉ:** `/profile.html`

**Có:**
- Xem lịch sử mua hàng (từ localStorage)
- Chat widget (giả lập - tự động trả lời random)

**Chưa có:**
- Đăng nhập/đăng ký thực sự
- Lưu thông tin user lên server

---

## 3. DÀNH CHO ADMIN

### 3.1. Đăng nhập Admin

**Địa chỉ:** `/admin.html`  
**Tài khoản mặc định:** `admin` / `admin123`

> ⚠️ **LƯU Ý:** Đây chỉ là kiểm tra client-side, không có bảo mật thực sự!

---

### 3.2. Dashboard (✅ Hoạt động)

- Thống kê số sản phẩm theo danh mục
- Tổng sản phẩm / Đã bán
- Server mode (MongoDB/Local)

---

### 3.3. Quản lý sản phẩm (✅ Hoạt động)

**Chức năng:**
- Xem danh sách sản phẩm
- **Seed Data:** Tạo dữ liệu mẫu (21 sản phẩm)
- **Reset:** Khôi phục sản phẩm mặc định
- **Xóa hết:** Xóa tất cả sản phẩm
- Xóa từng sản phẩm

---

### 3.4. AI SKKN Generator (✅ Hoạt động)

Tạo SKKN hàng loạt để bán:

1. Nhập **API Key**
2. Chọn **Danh mục**
3. Nhập **Số lượng** (1-5)
4. Điền **Vai trò, Môn học**
5. Nhập **Đề tài** (mỗi dòng 1 đề tài, hoặc để trống)
6. Đặt **Giá, Số từ**
7. Tích chọn:
   - ☑️ **Tự động upload lên Shop** → Sản phẩm tự thêm vào trang chủ
   - ☑️ **Xuất file Word** → Tải về máy
8. Bấm **"⚡ Bắt đầu tạo SKKN"**

---

### 3.5. Quản lý đơn hàng (✅ Hoạt động)

**Xem đơn hàng:**
- Mã đơn, sản phẩm, khách hàng, email, SĐT, số tiền, trạng thái

**Xử lý:**
- ✅ **Xác nhận:** Khi đã nhận tiền và gửi file
- ❌ **Từ chối:** Nếu có vấn đề

**Trạng thái:**
- Chờ xác nhận (pending)
- Đã xác nhận (confirmed)
- Đã từ chối (rejected)

> ⚠️ **Quy trình thủ công:** Sau khi xác nhận, bạn cần TỰ GỬI file qua email cho khách!

---

### 3.6. Chat Support (⚠️ Chưa hoàn thiện)

- Hiển thị "Chưa có tin nhắn nào"
- Chat lưu trong localStorage, không đồng bộ giữa user và admin
- **Thực tế:** Chưa có hệ thống chat real-time

---

### 3.7. Cài đặt (⚠️ UI only)

- Auto-Refill: Có checkbox nhưng **chưa kết nối logic**
- Ngưỡng kho tối thiểu: Có input nhưng **chưa hoạt động**

---

## 4. CÁC TÍNH NĂNG HOẠT ĐỘNG

| Tính năng | Trạng thái | Ghi chú |
|-----------|------------|---------|
| Xem/lọc sản phẩm | ✅ OK | Lọc theo danh mục, tìm kiếm |
| Mua sản phẩm | ✅ OK | Tạo đơn hàng, hiển thị QR |
| Tự soạn KHBD | ✅ OK | Cần API Key |
| Tự soạn SKKN | ✅ OK | Cần API Key |
| Tạo đề thi | ✅ OK | Cần API Key |
| Xuất Word | ✅ OK | KHBD, SKKN, Đề thi |
| Lịch sử tài liệu | ✅ OK | Lưu localStorage |
| Admin - Dashboard | ✅ OK | |
| Admin - Sản phẩm | ✅ OK | CRUD đầy đủ |
| Admin - Đơn hàng | ✅ OK | Xem, xác nhận, từ chối |
| Admin - AI Generator | ✅ OK | Tạo SKKN hàng loạt + upload |
| Mobile responsive | ✅ OK | Sidebar toggle |
| SEO Meta tags | ✅ OK | OG, Twitter |
| 404 Page | ✅ OK | |

---

## 5. HẠN CHẾ & LƯU Ý

### ⚠️ Chưa hoàn thiện

| Tính năng | Vấn đề |
|-----------|--------|
| Đăng nhập User | Không có - chỉ lưu localStorage |
| Bảo mật Admin | Chỉ check client-side, dễ bypass |
| Gửi file tự động | Không có - phải gửi thủ công |
| Chat real-time | Không đồng bộ giữa user/admin |
| Auto-Refill | UI có nhưng logic chưa kết nối |
| Thanh toán | Chỉ hiển thị QR, không verify |

### 🔑 Về API Key

- Khách cần API Key để sử dụng các tính năng AI
- Bạn tự tạo key và cấp cho khách
- **Nguồn key:** OpenRouter hoặc Google AI Studio (đã ẩn trên giao diện)

### ⏱️ Rate Limit

- Nếu tạo nhiều SKKN liên tục có thể bị giới hạn API
- Hệ thống đã có retry tự động (10s → 20s → 40s)
- Khuyến nghị: Không tạo quá 3 SKKN/lần

### 💾 Lưu trữ

- **Sản phẩm, Đơn hàng:** MongoDB Atlas (bền vững)
- **Lịch sử tạo tài liệu:** localStorage (mất khi xóa cache)
- **Chat:** localStorage (không đồng bộ)

---

## 📞 HỖ TRỢ

- **Lỗi kỹ thuật:** Zalo 0865063436
- **Đơn hàng:** Email từ form liên hệ

---

> **Lưu ý cuối:** Đây là phiên bản MVP. Một số tính năng cần phát triển thêm để production-ready.
