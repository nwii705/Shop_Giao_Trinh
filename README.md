# 🎓 EduShop - Hệ Thống Bán Giáo Trình Tự Động

## 📁 Cấu Trúc Dự Án

```
Shop_giao_trinh/
├── backend/                 # Server Node.js
│   ├── server.js           # API server chính
│   ├── models/             # MongoDB models
│   ├── seedData.js         # Dữ liệu mẫu
│   ├── public/docs/        # Chứa file PDF
│   └── .env                # Cấu hình MongoDB
├── ai_worker/              # AI Worker Python
│   ├── generator.py        # Tạo nội dung bằng Gemini
│   └── .env                # Cấu hình API keys
├── frontend/               # Giao diện web
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── README.md
```

## 🚀 Hướng Dẫn Cài Đặt

### 1. Cấu hình MongoDB

1. Đăng ký tài khoản tại [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Tạo Cluster miễn phí (M0 Sandbox)
3. Vào **Network Access** → **Add IP Address** → **Allow Access from Anywhere**
4. Vào **Database Access** → Tạo user với password
5. Lấy **Connection String**

### 2. Cập nhật Connection String

**File `backend/.env`:**
```
MONGO_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@cluster.mongodb.net/EduShopDB?retryWrites=true&w=majority
PORT=5000
```

**File `ai_worker/.env`:**
```
MONGO_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@cluster.mongodb.net/EduShopDB?retryWrites=true&w=majority
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Lấy Gemini API Key

1. Truy cập [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Tạo API Key mới
3. Copy vào file `ai_worker/.env`

### 4. Chạy Hệ Thống

**Terminal 1 - Chạy Backend:**
```bash
cd backend
node server.js
```

**Terminal 2 - Seed dữ liệu lần đầu:**
```bash
# Gọi API seed data
curl -X POST http://localhost:5000/api/seed
```

**Hoặc tạo sản phẩm bằng AI:**
```bash
cd ai_worker
python generator.py ai 3    # Tạo 3 giáo trình AI
python generator.py stem 2  # Tạo 2 giáo trình STEM
```

### 5. Truy cập Web

Mở trình duyệt: http://localhost:5000

---

## 📡 API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/products` | Lấy danh sách sản phẩm available |
| GET | `/api/stats` | Lấy thống kê |
| GET | `/api/search?q=keyword` | Tìm kiếm sản phẩm |
| POST | `/api/buy` | Mua sản phẩm (body: {productId}) |
| POST | `/api/reset` | Reset tất cả về available |
| POST | `/api/seed` | Seed dữ liệu mẫu |
| POST | `/api/generate` | Tạo sản phẩm AI (body: {category, quantity}) |

---

## 🔄 Luồng Hoạt Động

1. **Khách hàng** truy cập web → Xem danh sách giáo trình
2. **Bấm Mua** → Backend cập nhật status = "sold"
3. **Backend kiểm tra kho** → Nếu < 3 sản phẩm trong category
4. **Tự động gọi AI Worker** → Tạo sản phẩm mới bằng Gemini AI
5. **Sản phẩm mới** xuất hiện trên web

---

## 🛠️ Troubleshooting

### Lỗi kết nối MongoDB
- Kiểm tra Connection String trong file `.env`
- Kiểm tra Network Access đã allow IP

### Lỗi Gemini API
- Kiểm tra API Key còn hiệu lực
- Kiểm tra quota còn đủ

### Lỗi Python packages
```bash
pip install --upgrade pymongo google-generativeai fpdf2 python-dotenv
```

---

## 📝 License

MIT License - Tự do sử dụng và chỉnh sửa.
