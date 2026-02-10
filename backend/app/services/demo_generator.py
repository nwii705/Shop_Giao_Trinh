"""
Demo Content Generator - Tạo KHBD động dựa trên thông tin người dùng nhập.
Theo chuẩn Công văn 5512/BGDĐT-GDTrH.

LƯU Ý QUAN TRỌNG:
- Nội dung được tạo ĐỘNG dựa trên bài học, lớp, môn được chọn
- KHÔNG sử dụng nội dung cố định
- Cấu trúc 4 hoạt động: Khởi động -> Hình thành kiến thức -> Luyện tập -> Vận dụng
"""

from typing import Optional
from datetime import datetime


def generate_khtn_demo_content(
    lesson_name: str,
    grade: int,
    duration: int = 2,
    textbook: str = "ctst",
    period_number: Optional[int] = None,
    week_number: Optional[int] = None,
) -> str:
    """
    Tạo KHBD môn KHTN theo đúng cấu trúc Công văn 5512.
    Nội dung được tạo ĐỘNG dựa trên thông tin bài học.
    """
    
    # Xác định thông tin bộ sách
    textbook_names = {
        "ctst": "Chân trời sáng tạo",
        "kntt": "Kết nối tri thức với cuộc sống",
        "cd": "Cánh diều"
    }
    textbook_name = textbook_names.get(textbook, "Chân trời sáng tạo")
    
    # Xác định phân môn từ tên bài
    phan_mon = _detect_phan_mon_khtn(lesson_name)
    
    # Lấy thông tin chi tiết bài học
    lesson_info = _get_lesson_info_khtn(lesson_name, grade, textbook)
    
    # Tính thời lượng cho các hoạt động
    total_minutes = duration * 45
    
    # Ngày hiện tại
    today = datetime.now().strftime("%d/%m/%Y")
    
    # Build content
    content = f"""# KẾ HOẠCH BÀI DẠY
## MÔN: KHOA HỌC TỰ NHIÊN - LỚP {grade}
**Bộ sách:** {textbook_name}

*(Theo Công văn 5512/BGDĐT-GDTrH ngày 18/12/2020)*

| Tuần | Tiết PPCT | Ngày soạn | Ngày dạy |
|:----:|:---------:|:---------:|:--------:|
| {week_number or "___"} | {period_number or "___"} | {today} | ___/___/______ |

---

# 📚 BÀI: {lesson_name.upper()}

| Thông tin | Chi tiết |
|-----------|----------|
| **Phân môn** | {phan_mon} |
| **Thời lượng** | {duration} tiết ({total_minutes} phút) |
| **Phương pháp chính** | Dạy học tích cực, Thí nghiệm thực hành |

---

## I. MỤC TIÊU 🎯

### 1. Kiến thức
Sau bài học này, học sinh sẽ:
{lesson_info['kien_thuc']}

{lesson_info.get('cong_thuc', '')}

### 2. Năng lực

#### a) Năng lực chung

| Năng lực | Biểu hiện cụ thể trong bài học |
|----------|-------------------------------|
| **Tự chủ và tự học** | Chủ động tìm hiểu về {lesson_name} từ SGK và nguồn tài liệu khác trước khi đến lớp |
| **Giao tiếp và hợp tác** | Trao đổi, thảo luận trong nhóm để hoàn thành PHT; Trình bày kết quả thí nghiệm/quan sát rõ ràng, mạch lạc |
| **Giải quyết vấn đề và sáng tạo** | Đề xuất phương án thực hiện; Giải thích các hiện tượng quan sát được |

#### b) Năng lực đặc thù (Khoa học tự nhiên)

| Năng lực KHTN | Yêu cầu cần đạt |
|---------------|-----------------|
| **Nhận thức KHTN** | {lesson_info['nang_luc_nhan_thuc']} |
| **Tìm hiểu tự nhiên** | {lesson_info['nang_luc_tim_hieu']} |
| **Vận dụng kiến thức** | {lesson_info['nang_luc_van_dung']} |

### 3. Phẩm chất

| Phẩm chất | Biểu hiện |
|-----------|-----------|
| **Trung thực** | Báo cáo kết quả thí nghiệm/quan sát chính xác, không sao chép |
| **Trách nhiệm** | Hoàn thành nhiệm vụ được giao trong nhóm, bảo quản thiết bị |
| **Chăm chỉ** | Tích cực tham gia các hoạt động học tập, ghi chép đầy đủ |
| **Yêu khoa học** | Có hứng thú tìm hiểu về {lesson_name}, yêu thích môn KHTN |

---

## II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU 📦

### 1. Giáo viên chuẩn bị

| STT | Thiết bị/Học liệu | Số lượng | Ghi chú |
|:---:|-------------------|:--------:|---------|
| 1 | SGK, SGV KHTN {grade} ({textbook_name}) | 1 bộ | |
{lesson_info['thiet_bi_gv']}
| | Phiếu học tập (PHT) 1, 2 | 40 tờ/loại | In sẵn theo mẫu đính kèm |
| | Slide bài giảng PowerPoint | 1 file | Có hình ảnh, video minh họa |

### 2. Học sinh chuẩn bị

- ✅ SGK Khoa học Tự nhiên {grade} ({textbook_name}), vở ghi, bút
- ✅ Đọc trước bài "{lesson_name}"
- ✅ Hoàn thành PHT chuẩn bị bài (nếu có)
{lesson_info.get('hs_chuan_bi', '')}

---

## III. TIẾN TRÌNH DẠY HỌC 📖

{_build_tien_trinh_khtn(lesson_name, lesson_info, duration, grade)}

---

## IV. HỒ SƠ DẠY HỌC 📋

{_build_pht_khtn(lesson_name, lesson_info)}

---

## V. RÚT KINH NGHIỆM SAU BÀI DẠY ✍️

| Nội dung đánh giá | Tốt | Khá | Đạt | Chưa đạt | Ghi chú |
|-------------------|:---:|:---:|:---:|:--------:|---------|
| 1. Thời gian thực hiện | ☐ | ☐ | ☐ | ☐ | |
| 2. Mức độ tham gia của HS | ☐ | ☐ | ☐ | ☐ | |
| 3. Thí nghiệm/Thực hành | ☐ | ☐ | ☐ | ☐ | |
| 4. Đạt mục tiêu bài học | ☐ | ☐ | ☐ | ☐ | |
| 5. Sử dụng thiết bị dạy học | ☐ | ☐ | ☐ | ☐ | |
| 6. Hoạt động nhóm | ☐ | ☐ | ☐ | ☐ | |

📝 **Những điều cần điều chỉnh cho tiết sau:**

_________________________________________________________________________

| 📅 Ngày soạn | 👨‍🏫 Người soạn | ✅ Tổ trưởng duyệt | 📋 BGH duyệt |
|:------------:|:--------------:|:------------------:|:------------:|
| {today} | ________________ | ________________ | ________________ |

---
*📝 Nội dung được tạo dựa trên sách {textbook_name} - Lớp {grade}*

*🤖 GiaoTrinh AI - Hỗ trợ Giáo viên Việt Nam*
"""
    
    return content


def _detect_phan_mon_khtn(lesson_name: str) -> str:
    """Xác định phân môn KHTN từ tên bài."""
    lesson_lower = lesson_name.lower()
    
    # Vật lý
    vat_ly_keywords = [
        'đo', 'chiều dài', 'khối lượng', 'thời gian', 'nhiệt độ', 'thể tích',
        'lực', 'ma sát', 'áp suất', 'điện', 'từ', 'quang', 'âm thanh', 
        'chuyển động', 'tốc độ', 'vận tốc', 'năng lượng', 'công', 'công suất',
        'thước', 'cân', 'đồng hồ', 'nhiệt kế', 'ánh sáng', 'gương', 'thấu kính',
        'kính lúp', 'kính hiển vi', 'điện trở', 'cường độ', 'hiệu điện thế',
        'nam châm', 'từ trường', 'sóng', 'dao động', 'các phép đo'
    ]
    
    # Hóa học  
    hoa_hoc_keywords = [
        'nguyên tử', 'phân tử', 'nguyên tố', 'hóa trị', 'liên kết',
        'oxygen', 'oxy', 'hydrogen', 'nước', 'acid', 'axit', 'base', 'bazơ',
        'muối', 'oxit', 'kim loại', 'phi kim', 'phản ứng', 'tách chất',
        'hỗn hợp', 'dung dịch', 'chất tinh khiết', 'hợp chất', 'đơn chất',
        'mol', 'nồng độ', 'carbon', 'nitrogen', 'không khí', 'cháy',
        'lọc', 'bay hơi', 'chiết', 'chưng cất', 'kết tinh'
    ]
    
    # Sinh học
    sinh_hoc_keywords = [
        'tế bào', 'mô', 'cơ quan', 'sinh vật', 'thực vật', 'động vật',
        'vi sinh vật', 'nấm', 'vi khuẩn', 'virus', 'gene', 'di truyền',
        'quang hợp', 'hô hấp', 'tiêu hóa', 'tuần hoàn', 'bài tiết',
        'sinh sản', 'sinh thái', 'môi trường', 'đa dạng sinh học',
        'lá', 'thân', 'rễ', 'hoa', 'quả', 'cơ thể', 'hệ cơ quan'
    ]
    
    for kw in vat_ly_keywords:
        if kw in lesson_lower:
            return "Vật lý"
    
    for kw in hoa_hoc_keywords:
        if kw in lesson_lower:
            return "Hóa học"
            
    for kw in sinh_hoc_keywords:
        if kw in lesson_lower:
            return "Sinh học"
    
    return "Khoa học tự nhiên"


def _get_lesson_info_khtn(lesson_name: str, grade: int, textbook: str) -> dict:
    """Lấy thông tin chi tiết bài học KHTN."""
    lesson_lower = lesson_name.lower()
    
    # === ĐO CHIỀU DÀI ===
    if 'đo chiều dài' in lesson_lower or ('chiều dài' in lesson_lower and 'đo' in lesson_lower):
        return {
            'kien_thuc': """
- Nêu được cách đo chiều dài bằng thước
- Xác định được giới hạn đo (GHĐ) và độ chia nhỏ nhất (ĐCNN) của thước
- Đo được chiều dài của một số vật thông dụng bằng thước
- Ước lượng được chiều dài trong một số trường hợp đơn giản
""",
            'cong_thuc': """
📐 **Kiến thức trọng tâm:**

| Khái niệm | Định nghĩa | Ví dụ |
|-----------|------------|-------|
| **Giới hạn đo (GHĐ)** | Độ dài lớn nhất ghi trên thước | Thước 30cm có GHĐ = 30cm |
| **Độ chia nhỏ nhất (ĐCNN)** | Độ dài giữa hai vạch chia liên tiếp | Thước có ĐCNN = 1mm |

**Quy tắc đo chiều dài:**
1. **Ước lượng** chiều dài cần đo → Chọn thước phù hợp
2. **Đặt thước** dọc theo chiều dài cần đo, vạch số 0 ngang với một đầu vật
3. **Đặt mắt** nhìn theo hướng vuông góc với thước tại vị trí đầu kia của vật
4. **Đọc kết quả** theo vạch chia gần nhất với đầu kia của vật
""",
            'nang_luc_nhan_thuc': 'Nhận biết được các loại dụng cụ đo chiều dài (thước thẳng, thước cuộn, thước dây); Xác định được GHĐ và ĐCNN của thước',
            'nang_luc_tim_hieu': 'Tiến hành đo chiều dài các vật, ghi kết quả đo chính xác theo đúng quy tắc',
            'nang_luc_van_dung': 'Lựa chọn thước phù hợp để đo chiều dài trong thực tế; Ước lượng chiều dài các vật trước khi đo',
            'thiet_bi_gv': """| 2 | Thước thẳng có ĐCNN 1mm | 8 cái | Cho 8 nhóm HS |
| 3 | Thước cuộn (5m), thước dây (1,5m) | 8 bộ | Cho 8 nhóm HS |
| 4 | Các vật cần đo: bút chì, SGK, bàn học | 8 bộ | Cho 8 nhóm HS |""",
            'hs_chuan_bi': '- ✅ Mang theo thước kẻ cá nhân',
            'hoat_dong_1': {
                'ten': 'Tìm hiểu dụng cụ đo chiều dài',
                'muc_tieu': 'Nhận biết được các loại thước đo chiều dài; Xác định được GHĐ và ĐCNN của thước',
                'noi_dung': """
**Nhiệm vụ 1:** Quan sát các loại thước và hoàn thành bảng sau:

| Loại thước | GHĐ | ĐCNN | Phạm vi sử dụng |
|------------|:---:|:----:|-----------------|
| Thước thẳng học sinh (20cm) | | | |
| Thước thẳng (30cm) | | | |
| Thước cuộn (5m) | | | |
| Thước dây (1,5m) | | | |

**Nhiệm vụ 2:** Trả lời câu hỏi:
- Khi nào dùng thước thẳng? Khi nào dùng thước cuộn hoặc thước dây?
- Làm thế nào để xác định GHĐ và ĐCNN của một thước bất kỳ?

[Hình ảnh: Các loại thước đo chiều dài thông dụng]
""",
                'san_pham': 'PHT số 1 hoàn thành với bảng phân loại các loại thước'
            },
            'hoat_dong_2': {
                'ten': 'Tìm hiểu cách đo chiều dài',
                'muc_tieu': 'Nắm được 4 bước đo chiều dài đúng cách; Tránh các lỗi thường gặp khi đo',
                'noi_dung': """
**Các bước đo chiều dài:**

| Bước | Nội dung | Lưu ý quan trọng |
|:----:|----------|------------------|
| **1** | **Ước lượng** chiều dài cần đo | Để chọn thước có GHĐ phù hợp |
| **2** | **Đặt thước** dọc theo chiều dài cần đo | Vạch số 0 ngang với một đầu của vật |
| **3** | **Đặt mắt** nhìn vuông góc với thước | Tại vị trí đầu kia của vật |
| **4** | **Đọc và ghi** kết quả đo | Theo vạch chia gần nhất, ghi cả đơn vị |

**Các lỗi thường gặp:**

| Lỗi | Hậu quả | Cách khắc phục |
|-----|---------|----------------|
| Đặt thước lệch | Kết quả sai | Đặt thước sát và dọc theo vật |
| Mắt nhìn xiên | Đọc sai giá trị | Mắt vuông góc với thước |
| Quên ghi đơn vị | Kết quả không ý nghĩa | Luôn ghi kèm đơn vị |

[Hình ảnh: Cách đặt mắt đúng khi đo chiều dài]
""",
                'san_pham': 'Nắm vững 4 bước đo chiều dài và các lỗi cần tránh'
            },
            'thuc_hanh': {
                'ten': 'Thực hành đo chiều dài',
                'noi_dung': """
**Thực hành theo nhóm (4-5 HS/nhóm):**

**Bảng kết quả đo:**

| STT | Vật cần đo | Ước lượng | Thước sử dụng | Kết quả đo | Sai số |
|:---:|------------|:---------:|---------------|:----------:|:------:|
| 1 | Chiều dài bút chì | ___cm | ĐCNN = ___mm | ___cm | |
| 2 | Chiều rộng quyển SGK | ___cm | ĐCNN = ___mm | ___cm | |
| 3 | Chiều dài mặt bàn học | ___cm | ĐCNN = ___mm | ___cm | |
| 4 | Chu vi cổ tay bạn | ___cm | ĐCNN = ___mm | ___cm | |
| 5 | Chiều cao ghế ngồi | ___cm | ĐCNN = ___mm | ___cm | |

**Câu hỏi thảo luận:**
1. Tại sao cần ước lượng trước khi đo?
2. Em đã chọn thước nào để đo từng vật? Vì sao lại chọn thước đó?
3. So sánh kết quả ước lượng với kết quả đo thực tế?
""",
                'san_pham': 'Bảng kết quả đo hoàn chỉnh với nhận xét'
            },
            'luyen_tap': """
**Câu 1:** Thước thẳng có GHĐ 20cm và ĐCNN 1mm. Số vạch chia trên thước (kể cả vạch 0) là:
- A. 20 vạch
- B. 200 vạch  
- C. 201 vạch ✓
- D. 21 vạch

**Câu 2:** Để đo chiều dài sân trường (khoảng 50m), em nên dùng thước nào?
- A. Thước thẳng 30cm
- B. Thước dây 1,5m
- C. Thước cuộn 50m ✓
- D. Thước kẻ học sinh

**Câu 3:** Khi đọc kết quả đo, mắt phải nhìn theo hướng nào?
- A. Song song với mặt thước
- B. Vuông góc với cạnh thước tại điểm đọc ✓
- C. Nghiêng một góc 45°
- D. Hướng nào cũng được

**Câu 4:** Một thước có 101 vạch chia, vạch đầu ghi 0cm, vạch cuối ghi 100cm. ĐCNN của thước là:
- A. 1mm
- B. 1cm ✓
- C. 10cm
- D. 100cm
""",
            'van_dung': """
1. Hãy ước lượng rồi đo chiều cao của em bằng thước dây. So sánh kết quả ước lượng và đo thực tế.

2. Tìm 5 tình huống trong đời sống cần đo chiều dài và nêu loại thước phù hợp:

| Tình huống | Loại thước phù hợp | Lý do |
|------------|-------------------|-------|
| Đo chiều cao cửa | Thước cuộn | GHĐ lớn, dễ đo vật thẳng đứng |
| ... | ... | ... |

3. Giải thích: Tại sao thợ may dùng thước dây mà không dùng thước thẳng để đo số đo cơ thể?

4. **Dự án nhỏ:** Thiết kế bảng hướng dẫn "4 bước đo chiều dài đúng cách" để treo trong phòng thí nghiệm.
"""
        }
    
    # === TÁCH CHẤT RA KHỎI HỖN HỢP ===
    elif 'tách chất' in lesson_lower or 'hỗn hợp' in lesson_lower:
        return {
            'kien_thuc': """
- Trình bày được một số phương pháp tách chất ra khỏi hỗn hợp: lọc, cô cạn, chiết
- Sử dụng được các dụng cụ, thiết bị để tách chất ra khỏi hỗn hợp bằng cách lọc, cô cạn, chiết
- Nêu được một số ứng dụng tách chất ra khỏi hỗn hợp trong đời sống và sản xuất
""",
            'cong_thuc': """
📐 **Kiến thức trọng tâm:**

| Phương pháp | Nguyên tắc | Điều kiện áp dụng | Ứng dụng thực tế |
|-------------|------------|-------------------|------------------|
| **Lọc** | Tách chất rắn không tan ra khỏi chất lỏng dựa vào kích thước hạt | Hỗn hợp gồm chất rắn không tan trong chất lỏng | Lọc nước, lọc bã cà phê |
| **Cô cạn (Bay hơi)** | Làm bay hơi dung môi để thu chất rắn tan | Chất rắn tan trong dung môi, không bay hơi cùng | Làm muối từ nước biển |
| **Chiết** | Tách hai chất lỏng không tan vào nhau dựa vào khối lượng riêng | Hai chất lỏng không hòa tan, có tỉ khối khác nhau | Tách dầu ra khỏi nước |
""",
            'nang_luc_nhan_thuc': 'Nhận biết và phân biệt được các phương pháp tách chất: lọc, cô cạn, chiết',
            'nang_luc_tim_hieu': 'Tiến hành được thí nghiệm lọc, cô cạn, chiết theo đúng quy trình an toàn',
            'nang_luc_van_dung': 'Giải thích được nguyên tắc các phương pháp làm sạch nước, làm muối trong thực tế',
            'thiet_bi_gv': """| 2 | Bộ dụng cụ lọc: phễu lọc, giấy lọc, bình tam giác, giá đỡ | 8 bộ | Cho 8 nhóm HS |
| 3 | Bộ dụng cụ cô cạn: đèn cồn, kiềng, lưới, chén sứ, kẹp | 8 bộ | Cho 8 nhóm HS |
| 4 | Phễu chiết, giá đỡ phễu chiết | 4 bộ | Demo GV |
| 5 | Hóa chất: hỗn hợp cát + nước, dung dịch nước muối, hỗn hợp dầu ăn + nước | 8 bộ | Cho 8 nhóm HS |""",
            'hs_chuan_bi': '',
            'hoat_dong_1': {
                'ten': 'Tìm hiểu phương pháp lọc',
                'muc_tieu': 'Nêu được nguyên tắc, điều kiện và thực hiện được phương pháp lọc',
                'noi_dung': """
**I. PHƯƠNG PHÁP LỌC**

**1. Định nghĩa:** Lọc là phương pháp tách chất rắn không tan ra khỏi hỗn hợp với chất lỏng.

**2. Dụng cụ:** 
- Phễu lọc (thủy tinh hoặc nhựa)
- Giấy lọc 
- Bình hứng (bình tam giác hoặc cốc thủy tinh)
- Giá đỡ, đũa thủy tinh

[Hình 1: Bộ dụng cụ lọc]

**3. Thí nghiệm: Lọc hỗn hợp cát và nước**

| Bước | Thao tác | Lưu ý |
|:----:|----------|-------|
| 1 | Gấp giấy lọc hình nón, đặt vào phễu | Giấy lọc khít với phễu |
| 2 | Dùng bình tia thấm ướt giấy lọc | Giấy dính chặt vào thành phễu |
| 3 | Đặt phễu lên giá, bình hứng phía dưới | Đầu phễu chạm thành bình |
| 4 | Rót từ từ hỗn hợp vào phễu theo đũa thủy tinh | Không đổ quá 2/3 phễu |
| 5 | Quan sát nước trong chảy xuống bình | Cát ở lại trên giấy lọc |

[Hình 2: Các bước tiến hành lọc]
""",
                'san_pham': 'Chất rắn (cát) trên giấy lọc; Nước trong ở bình hứng'
            },
            'hoat_dong_2': {
                'ten': 'Tìm hiểu phương pháp cô cạn (bay hơi)',
                'muc_tieu': 'Nêu được nguyên tắc và thực hiện được phương pháp cô cạn',
                'noi_dung': """
**II. PHƯƠNG PHÁP CÔ CẠN (BAY HƠI)**

**1. Định nghĩa:** Cô cạn là phương pháp làm bay hơi dung môi để thu chất rắn tan trong dung dịch.

**2. Dụng cụ:** 
- Đèn cồn, kiềng, lưới amiăng
- Chén sứ, kẹp gỗ
- Que diêm/bật lửa

[Hình 3: Bộ dụng cụ cô cạn]

**3. Thí nghiệm: Thu muối từ nước muối**

| Bước | Thao tác | Lưu ý an toàn |
|:----:|----------|---------------|
| 1 | Rót 10ml dung dịch nước muối vào chén sứ | Không đổ đầy quá |
| 2 | Đặt chén sứ lên kiềng có lưới amiăng | Kiểm tra ổn định |
| 3 | Đốt đèn cồn, đun nóng chén sứ | ⚠️ Cẩn thận với lửa |
| 4 | Đun đến khi nước bay hơi gần hết | Không đun khô hoàn toàn |
| 5 | Tắt đèn, để nguội, quan sát | Tinh thể muối trắng |

**⚠️ AN TOÀN:** 
- Không nghiêng người qua ngọn lửa
- Dùng kẹp để cầm chén nóng
- Tắt đèn đúng cách (dùng nắp đậy)

[Hình 4: Thí nghiệm cô cạn nước muối]
""",
                'san_pham': 'Tinh thể muối trắng trong chén sứ sau khi cô cạn'
            },
            'thuc_hanh': {
                'ten': 'Tìm hiểu phương pháp chiết',
                'noi_dung': """
**III. PHƯƠNG PHÁP CHIẾT**

**1. Định nghĩa:** Chiết là phương pháp tách các chất lỏng không tan vào nhau, dựa vào sự khác nhau về khối lượng riêng.

**2. Dụng cụ:** 
- Phễu chiết
- Giá đỡ
- Bình hứng

[Hình 5: Phễu chiết]

**3. Demo: Tách dầu ăn ra khỏi nước**

| Quan sát | Mô tả | Giải thích |
|----------|-------|------------|
| Trước chiết | Dầu nổi thành lớp trên nước | Dầu nhẹ hơn nước, không tan trong nước |
| Mở khóa phễu | Nước chảy ra trước | Nước nặng hơn, ở dưới |
| Sau chiết | Dầu và nước ở hai bình riêng | Tách thành công |

[Hình 6: Các bước tách dầu và nước bằng phễu chiết]

**4. Ứng dụng trong đời sống:**
- Tách dầu mỡ ra khỏi nước thải
- Chiết xuất tinh dầu từ thực vật
- Xử lý sự cố tràn dầu
""",
                'san_pham': 'Hai lớp chất lỏng (dầu và nước) được tách riêng'
            },
            'luyen_tap': """
**Câu 1:** Phương pháp nào dùng để tách cát ra khỏi nước?
- A. Cô cạn
- B. Lọc ✓
- C. Chiết
- D. Chưng cất

**Câu 2:** Người dân vùng biển làm muối từ nước biển bằng phương pháp:
- A. Lọc
- B. Cô cạn (bay hơi) ✓
- C. Chiết
- D. Kết tinh

**Câu 3:** Để tách dầu ăn ra khỏi nước, ta dùng phương pháp:
- A. Lọc
- B. Chiết ✓
- C. Cô cạn
- D. Đun sôi

**Câu 4:** Khi lọc, nếu giấy lọc bị thủng thì:
- A. Kết quả lọc không đổi
- B. Nước trong hơn
- C. Chất rắn lọt xuống bình hứng ✓
- D. Tốc độ lọc chậm hơn

**Bài tập tự luận:**
Có hỗn hợp gồm: cát, muối ăn, dầu ăn. Hãy thiết kế quy trình tách riêng từng chất.
""",
            'van_dung': """
1. **Quan sát và giải thích:** Gia đình em lọc nước sinh hoạt như thế nào? Phương pháp đó thuộc loại nào?

2. **Giải thích hiện tượng:** Tại sao người ta phơi nước biển để làm muối mà không đun sôi?

3. **Thiết kế quy trình:** Có hỗn hợp gồm: bột mì + nước + dầu ăn. Hãy đề xuất cách tách riêng từng chất.

| Bước | Phương pháp | Mục đích | Kết quả |
|:----:|-------------|----------|---------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

4. **Liên hệ thực tế:** Tìm hiểu cách xử lý sự cố tràn dầu trên biển. Người ta dùng phương pháp gì để tách dầu ra khỏi nước biển?
"""
        }
    
    # === MẶC ĐỊNH - BÀI HỌC CHUNG ===
    else:
        return _get_default_lesson_info(lesson_name, grade, textbook)


def _get_default_lesson_info(lesson_name: str, grade: int, textbook: str) -> dict:
    """Tạo thông tin mặc định cho bài học chưa có dữ liệu chi tiết."""
    phan_mon = _detect_phan_mon_khtn(lesson_name)
    
    return {
        'kien_thuc': f"""
- Trình bày được các khái niệm cơ bản về {lesson_name}
- Mô tả được đặc điểm, tính chất chính liên quan đến {lesson_name}
- Vận dụng được kiến thức để giải thích các hiện tượng thực tế
""",
        'cong_thuc': '',
        'nang_luc_nhan_thuc': f'Nhận biết và mô tả được các khái niệm, hiện tượng liên quan đến {lesson_name}',
        'nang_luc_tim_hieu': 'Tiến hành được thí nghiệm/quan sát, ghi chép kết quả chính xác',
        'nang_luc_van_dung': f'Giải thích được các hiện tượng trong đời sống liên quan đến {lesson_name}',
        'thiet_bi_gv': f"""| 2 | Dụng cụ thí nghiệm/mô hình liên quan | 8 bộ | Cho 8 nhóm HS |
| 3 | Mẫu vật/Hóa chất (nếu cần) | đủ dùng | Theo hướng dẫn SGK |""",
        'hs_chuan_bi': '',
        'hoat_dong_1': {
            'ten': f'Tìm hiểu khái niệm về {lesson_name}',
            'muc_tieu': f'Nêu được khái niệm và đặc điểm cơ bản của {lesson_name}',
            'noi_dung': f"""
**Nhiệm vụ 1:** Nghiên cứu SGK và hoàn thành PHT số 1

**Câu 1:** {lesson_name} là gì?

**Câu 2:** Nêu các đặc điểm chính:

| STT | Đặc điểm | Mô tả |
|:---:|----------|-------|
| 1 | | |
| 2 | | |
| 3 | | |

**Câu 3:** Cho ví dụ trong thực tế:

[Hình ảnh minh họa]
""",
            'san_pham': 'PHT số 1 hoàn thành'
        },
        'hoat_dong_2': {
            'ten': 'Tìm hiểu tính chất và ứng dụng',
            'muc_tieu': f'Trình bày được tính chất và ứng dụng của {lesson_name}',
            'noi_dung': f"""
**Nhiệm vụ:** Thảo luận nhóm và hoàn thành bảng sau:

| Tính chất | Ứng dụng | Ví dụ thực tế |
|-----------|----------|---------------|
| | | |
| | | |
| | | |
""",
            'san_pham': 'Bảng tổng hợp tính chất và ứng dụng'
        },
        'thuc_hanh': {
            'ten': 'Thực hành/Thí nghiệm',
            'noi_dung': f"""
**Tiến hành theo hướng dẫn SGK**

| Bước | Thao tác | Quan sát |
|:----:|----------|----------|
| 1 | | |
| 2 | | |
| 3 | | |

**Kết luận:**
""",
            'san_pham': 'Kết quả thí nghiệm/quan sát và kết luận'
        },
        'luyen_tap': f"""
**Câu 1:** (Trắc nghiệm) Câu hỏi về khái niệm {lesson_name}?
- A. Đáp án A
- B. Đáp án B  
- C. Đáp án C
- D. Đáp án D

**Câu 2:** (Trắc nghiệm) Câu hỏi về tính chất/đặc điểm?
- A. Đáp án A
- B. Đáp án B  
- C. Đáp án C
- D. Đáp án D

**Câu 3:** (Tự luận) Nêu 3 ví dụ về {lesson_name} trong đời sống và giải thích?
""",
        'van_dung': f"""
1. Tìm 5 ví dụ về {lesson_name} trong đời sống hàng ngày

2. Giải thích một hiện tượng thực tế liên quan đến kiến thức vừa học

3. **Dự án nhỏ:** Thiết kế poster/infographic giới thiệu về {lesson_name}
"""
    }


def _build_tien_trinh_khtn(lesson_name: str, lesson_info: dict, duration: int, grade: int) -> str:
    """Xây dựng phần III. Tiến trình dạy học."""
    
    tiet_1 = f"""
### 🕐 TIẾT 1 (45 phút)

---

### A. HOẠT ĐỘNG KHỞI ĐỘNG ⏱️ 5 phút

#### a) Mục tiêu
- Tạo hứng thú, kích thích tò mò của học sinh
- Kết nối kiến thức thực tiễn với nội dung bài học
- Xác định những gì HS đã biết về chủ đề (kỹ thuật KWL)

#### b) Nội dung
📌 **Tình huống mở đầu:**

GV chiếu hình ảnh/video thực tế liên quan đến {lesson_name} và đặt câu hỏi:

- *"Các em quan sát được điều gì trong hình ảnh/video?"*
- *"Em đã từng thấy/thực hiện điều này trong đời sống chưa?"*
- *"Theo em, hoạt động này dựa trên nguyên tắc nào?"*

[Hình ảnh: Tình huống thực tế liên quan đến {lesson_name}]

#### c) Sản phẩm
- Câu trả lời, dự đoán ban đầu của học sinh
- Bảng KWL (cột K - Know: những gì đã biết; W - Want to know: muốn biết)

#### d) Tổ chức thực hiện

| Hoạt động của GV và HS | Sản phẩm dự kiến |
|------------------------|------------------|
| **Bước 1: Chuyển giao nhiệm vụ**<br>- GV chiếu hình ảnh/video liên quan đến {lesson_name}<br>- GV đặt câu hỏi gợi mở<br>- GV phát phiếu KWL | |
| **Bước 2: Thực hiện nhiệm vụ**<br>- HS quan sát, suy nghĩ cá nhân (1 phút)<br>- HS điền cột K (đã biết) và W (muốn biết) (2 phút) | Phiếu KWL (cột K, W) |
| **Bước 3: Báo cáo, thảo luận**<br>- GV gọi 2-3 HS chia sẻ<br>- HS trình bày ý kiến cá nhân<br>- Các HS khác nhận xét, bổ sung | Câu trả lời của HS |
| **Bước 4: Kết luận, nhận định**<br>- GV nhận xét, khen ngợi các câu trả lời<br>- GV dẫn dắt: "Để trả lời câu hỏi này, hôm nay chúng ta sẽ tìm hiểu bài..."<br>- GV ghi tên bài lên bảng | Tên bài học trong vở |

---

### B. HOẠT ĐỘNG HÌNH THÀNH KIẾN THỨC ⏱️ 30 phút

---

#### Hoạt động 1: {lesson_info.get('hoat_dong_1', {}).get('ten', 'Tìm hiểu kiến thức')} (15 phút)

##### a) Mục tiêu
{lesson_info.get('hoat_dong_1', {}).get('muc_tieu', '')}

##### b) Nội dung
{lesson_info.get('hoat_dong_1', {}).get('noi_dung', '')}

##### c) Sản phẩm
✅ {lesson_info.get('hoat_dong_1', {}).get('san_pham', 'PHT hoàn thành')}

##### d) Tổ chức thực hiện

| Hoạt động của GV và HS | Sản phẩm dự kiến |
|------------------------|------------------|
| **Bước 1: Chuyển giao nhiệm vụ**<br>- GV chia lớp thành 8 nhóm (4-5 HS/nhóm)<br>- GV phát PHT số 1 và dụng cụ thí nghiệm (nếu có)<br>- GV nêu yêu cầu rõ ràng, hướng dẫn an toàn<br>- GV quy định thời gian: 7 phút | |
| **Bước 2: Thực hiện nhiệm vụ**<br>- HS nhận PHT và dụng cụ<br>- HS phân công: nhóm trưởng, thư ký, báo cáo viên<br>- HS nghiên cứu SGK/tiến hành thí nghiệm<br>- HS thảo luận, thống nhất, ghi kết quả vào PHT<br>- GV quan sát, hỗ trợ các nhóm gặp khó khăn | PHT số 1 hoàn thành |
| **Bước 3: Báo cáo, thảo luận**<br>- GV gọi 2 nhóm trình bày (mỗi nhóm 2 phút)<br>- Các nhóm khác lắng nghe, đặt câu hỏi<br>- GV tổ chức thảo luận, giải đáp thắc mắc | Bài trình bày của nhóm |
| **Bước 4: Kết luận, nhận định**<br>- GV nhận xét quá trình làm việc của các nhóm<br>- GV chốt kiến thức trọng tâm (chiếu slide)<br>- GV yêu cầu HS ghi nội dung chính vào vở | Ghi chép trong vở |

---

#### Hoạt động 2: {lesson_info.get('hoat_dong_2', {}).get('ten', 'Tìm hiểu sâu hơn')} (15 phút)

##### a) Mục tiêu
{lesson_info.get('hoat_dong_2', {}).get('muc_tieu', '')}

##### b) Nội dung
{lesson_info.get('hoat_dong_2', {}).get('noi_dung', '')}

##### c) Sản phẩm
✅ {lesson_info.get('hoat_dong_2', {}).get('san_pham', 'Kết quả thảo luận')}

##### d) Tổ chức thực hiện

| Hoạt động của GV và HS | Sản phẩm dự kiến |
|------------------------|------------------|
| **Bước 1: Chuyển giao nhiệm vụ**<br>- GV phát PHT số 2<br>- GV nêu nhiệm vụ cụ thể cho từng nhóm<br>- GV hướng dẫn cách thực hiện<br>- GV quy định thời gian: 7 phút | |
| **Bước 2: Thực hiện nhiệm vụ**<br>- HS nghiên cứu nội dung được giao<br>- HS tiến hành thí nghiệm/quan sát (nếu có)<br>- HS thảo luận, hoàn thành PHT<br>- GV đi quanh lớp, quan sát, hỗ trợ | PHT số 2 hoàn thành |
| **Bước 3: Báo cáo, thảo luận**<br>- Đại diện nhóm trình bày kết quả<br>- Các nhóm khác nhận xét, đặt câu hỏi phản biện<br>- GV điều phối thảo luận | Nội dung trình bày |
| **Bước 4: Kết luận, nhận định**<br>- GV tổng hợp các ý kiến<br>- GV chốt kiến thức chuẩn<br>- HS hoàn thiện ghi chép vào vở | Ghi bảng/vở |

---

### C. HOẠT ĐỘNG LUYỆN TẬP ⏱️ 7 phút

#### a) Mục tiêu
- Củng cố, khắc sâu kiến thức đã học
- Rèn kỹ năng vận dụng kiến thức giải quyết vấn đề
- Phát hiện và sửa chữa sai lầm (nếu có)

#### b) Nội dung
📝 **BÀI TẬP:**

{lesson_info.get('luyen_tap', '')}

#### c) Sản phẩm
- Đáp án của học sinh (trắc nghiệm + tự luận)
- Điểm số/phản hồi từ GV

#### d) Tổ chức thực hiện

| Hoạt động của GV và HS | Sản phẩm dự kiến |
|------------------------|------------------|
| **Bước 1: Chuyển giao nhiệm vụ**<br>- GV chiếu/phát bài tập<br>- GV nêu yêu cầu: làm cá nhân, thời gian 4 phút<br>- GV hướng dẫn cách trình bày | |
| **Bước 2: Thực hiện nhiệm vụ**<br>- HS làm bài cá nhân vào vở<br>- GV quan sát, không gợi ý đáp án<br>- GV nhắc nhở thời gian | Bài làm của HS |
| **Bước 3: Báo cáo, thảo luận**<br>- HS đổi bài chấm chéo (hoặc GV chữa)<br>- GV chiếu đáp án, giải thích<br>- HS nêu thắc mắc (nếu có) | Đáp án đúng |
| **Bước 4: Kết luận, nhận định**<br>- GV công bố đáp án và biểu điểm<br>- GV phân tích các lỗi sai phổ biến<br>- HS tự sửa lỗi vào vở | Bài đã sửa lỗi |

---

### D. HOẠT ĐỘNG VẬN DỤNG ⏱️ 3 phút

#### a) Mục tiêu
- Đánh giá mức độ hiểu bài của HS
- Mở rộng, liên hệ kiến thức với thực tiễn
- Phát triển năng lực tự học

#### b) Nội dung
🏠 **NHIỆM VỤ VỀ NHÀ:**

{lesson_info.get('van_dung', '')}

#### c) Sản phẩm
- Bài tập về nhà hoàn thành
- Sản phẩm dự án (poster/infographic) - nếu có

#### d) Tổ chức thực hiện

| Hoạt động của GV và HS | Sản phẩm dự kiến |
|------------------------|------------------|
| **Bước 1: Chuyển giao nhiệm vụ**<br>- GV giao bài tập về nhà (chiếu lên màn hình)<br>- GV nêu rõ yêu cầu và hạn nộp<br>- GV giới thiệu dự án nhóm (nếu có) | |
| **Bước 2: Thực hiện nhiệm vụ**<br>- HS ghi nhận nhiệm vụ vào vở<br>- HS hoàn thành cột L (Learned) của phiếu KWL<br>- HS hỏi nếu chưa rõ yêu cầu | Phiếu KWL hoàn chỉnh |
| **Bước 3: Báo cáo, thảo luận**<br>- GV hỏi: "Em đã học được gì hôm nay?"<br>- 1-2 HS chia sẻ | Tổng kết bài học |
| **Bước 4: Kết luận, nhận định**<br>- GV nhận xét tiết học (thái độ, kết quả)<br>- GV dặn dò chuẩn bị bài sau | |
"""
    
    if duration >= 2:
        tiet_2 = f"""

---

### 🕐 TIẾT 2 (45 phút)

---

### HOẠT ĐỘNG 5: THỰC HÀNH - THÍ NGHIỆM ⏱️ 35 phút

#### a) Mục tiêu
- Rèn luyện kỹ năng thực hành, thí nghiệm
- Vận dụng kiến thức lý thuyết vào thực tiễn
- Phát triển năng lực làm việc nhóm

#### b) Nội dung
🔬 **THỰC HÀNH:**

{lesson_info.get('thuc_hanh', {}).get('noi_dung', 'Thực hành theo hướng dẫn SGK')}

#### c) Sản phẩm
✅ {lesson_info.get('thuc_hanh', {}).get('san_pham', 'Kết quả thực hành')}

#### d) Tổ chức thực hiện

| Hoạt động của GV và HS | Sản phẩm dự kiến |
|------------------------|------------------|
| **Bước 1: Chuyển giao nhiệm vụ**<br>- GV kiểm tra sự chuẩn bị của các nhóm<br>- GV phát dụng cụ, PHT thực hành<br>- GV hướng dẫn các bước thực hiện (demo nếu cần)<br>- GV nhấn mạnh quy tắc an toàn | |
| **Bước 2: Thực hiện nhiệm vụ**<br>- HS tiến hành thực hành theo nhóm<br>- HS quan sát, ghi kết quả vào PHT<br>- HS thảo luận, rút ra kết luận<br>- GV quan sát, hỗ trợ, đảm bảo an toàn | PHT thực hành hoàn thành |
| **Bước 3: Báo cáo, thảo luận**<br>- Các nhóm báo cáo kết quả thực hành<br>- So sánh kết quả giữa các nhóm<br>- Giải thích sự khác biệt (nếu có) | Bảng kết quả |
| **Bước 4: Kết luận, nhận định**<br>- GV nhận xét quá trình thực hành của các nhóm<br>- GV chốt kiến thức qua thực hành<br>- GV hướng dẫn thu dọn, vệ sinh | Kết luận trong vở |

---

### HOẠT ĐỘNG 6: TỔNG KẾT - ĐÁNH GIÁ ⏱️ 10 phút

#### a) Mục tiêu
- Tổng kết kiến thức toàn bài
- Đánh giá kết quả học tập của HS
- Định hướng học tập tiếp theo

#### b) Nội dung
- Hoàn thành sơ đồ tư duy tổng kết bài
- Kiểm tra nhanh 5 phút (5 câu trắc nghiệm)

#### c) Sản phẩm
- Sơ đồ tư duy hoàn chỉnh
- Bài kiểm tra nhanh

#### d) Tổ chức thực hiện

| Hoạt động của GV và HS | Sản phẩm dự kiến |
|------------------------|------------------|
| **Bước 1: Chuyển giao nhiệm vụ**<br>- GV phát giấy A4 cho các nhóm<br>- GV yêu cầu HS tổng kết bài bằng sơ đồ tư duy<br>- GV phát đề kiểm tra nhanh | |
| **Bước 2: Thực hiện nhiệm vụ**<br>- HS thảo luận, vẽ sơ đồ tư duy (3 phút)<br>- HS làm bài kiểm tra cá nhân (5 phút)<br>- GV quan sát | Sơ đồ tư duy, bài kiểm tra |
| **Bước 3: Báo cáo, thảo luận**<br>- 1-2 nhóm trình bày sơ đồ tư duy<br>- GV thu bài kiểm tra | |
| **Bước 4: Kết luận, nhận định**<br>- GV tổng kết bài học, chiếu sơ đồ tư duy mẫu<br>- GV dặn dò chuẩn bị bài sau<br>- GV thông báo điểm kiểm tra (tiết sau) | |
"""
        return tiet_1 + tiet_2
    
    return tiet_1


def _build_pht_khtn(lesson_name: str, lesson_info: dict) -> str:
    """Xây dựng phần IV. Hồ sơ dạy học (PHT)."""
    
    return f"""
### 📄 PHIẾU HỌC TẬP SỐ 1 - TÌM HIỂU KIẾN THỨC

| | |
|---|---|
| **Họ và tên:** ___________________________ | **Lớp:** ______ |
| **Nhóm:** ______ | **Ngày:** ___/___/______ |

---

**BÀI: {lesson_name.upper()}**

---

**Câu 1:** Nêu khái niệm/định nghĩa chính của bài học?

> _______________________________________________________________
> _______________________________________________________________
> _______________________________________________________________

**Câu 2:** Hoàn thành bảng sau:

| STT | Nội dung | Mô tả chi tiết |
|:---:|----------|----------------|
| 1 | | |
| 2 | | |
| 3 | | |

**Câu 3:** Ghi kết quả quan sát/thí nghiệm (nếu có):

| TT | Thí nghiệm/Quan sát | Hiện tượng | Giải thích |
|:--:|---------------------|------------|------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

---

### 📄 PHIẾU HỌC TẬP SỐ 2 - KỸ THUẬT KWL

| K (Know) - Em đã biết gì? | W (Want to know) - Em muốn biết gì? | L (Learned) - Em đã học được gì? |
|---------------------------|-------------------------------------|----------------------------------|
| | | |
| | | |
| | | |
| | | |

---

### 📄 PHIẾU QUAN SÁT THÍ NGHIỆM

| Thông tin | Nội dung |
|-----------|----------|
| **Nhóm** | ______ |
| **Tên thí nghiệm** | |
| **Dụng cụ - Hóa chất** | |

---

**CÁCH TIẾN HÀNH:**

| Bước | Thao tác | Lưu ý an toàn |
|:----:|----------|---------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |

---

**HIỆN TƯỢNG QUAN SÁT:**
> _______________________________________________________________
> _______________________________________________________________

**GIẢI THÍCH:**
> _______________________________________________________________
> _______________________________________________________________

**KẾT LUẬN:**
> _______________________________________________________________
> _______________________________________________________________

| ☐ Thí nghiệm thành công | ☐ Cần làm lại | ☐ Ghi chú: _______________ |

---

### 📊 ĐÁP ÁN VÀ THANG ĐIỂM

| Câu | Nội dung đáp án | Điểm |
|:---:|-----------------|:----:|
| 1 | Nêu đúng định nghĩa/khái niệm theo SGK | 2.0 |
| 2 | Nêu được đầy đủ các đặc điểm/nội dung (mỗi ý đúng 1 điểm) | 3.0 |
| 3 | Mỗi ví dụ/giải thích đúng và đầy đủ: 1.5 điểm | 4.5 |
| | Trình bày sạch đẹp, rõ ràng, khoa học | 0.5 |
| **TỔNG** | | **10** |
"""


# ==================== NGỮ VĂN ====================

def generate_nguvan_demo_content(
    lesson_name: str,
    grade: int,
    duration: int = 2,
    textbook: str = "ctst",
    period_number: Optional[int] = None,
    week_number: Optional[int] = None,
) -> str:
    """Tạo KHBD môn Ngữ văn theo đúng cấu trúc Công văn 5512."""
    
    textbook_names = {
        "ctst": "Chân trời sáng tạo",
        "kntt": "Kết nối tri thức với cuộc sống",
        "cd": "Cánh diều"
    }
    textbook_name = textbook_names.get(textbook, "Chân trời sáng tạo")
    
    # Lấy thông tin bài học
    lesson_info = _get_lesson_info_nguvan(lesson_name, grade, textbook)
    
    today = datetime.now().strftime("%d/%m/%Y")
    total_minutes = duration * 45
    
    content = f"""# KẾ HOẠCH BÀI DẠY
## MÔN: NGỮ VĂN - LỚP {grade}
**Bộ sách:** {textbook_name}

*(Theo Công văn 5512/BGDĐT-GDTrH ngày 18/12/2020)*

| Tuần | Tiết PPCT | Ngày soạn | Ngày dạy |
|:----:|:---------:|:---------:|:--------:|
| {week_number or "___"} | {period_number or "___"} | {today} | ___/___/______ |

---

# 📚 BÀI: {lesson_name.upper()}

| Thông tin | Chi tiết |
|-----------|----------|
| **Thể loại** | {lesson_info['the_loai']} |
| **Thời lượng** | {duration} tiết ({total_minutes} phút) |
| **Phương pháp chính** | Dạy học tích cực, Đọc hiểu văn bản |

---

## I. MỤC TIÊU 🎯

### 1. Kiến thức
Sau bài học này, học sinh sẽ:
{lesson_info['kien_thuc']}

### 2. Năng lực

#### a) Năng lực chung

| Năng lực | Biểu hiện cụ thể trong bài học |
|----------|-------------------------------|
| **Tự chủ và tự học** | Chủ động đọc văn bản, tìm hiểu về {lesson_name} từ SGK và nguồn tài liệu khác |
| **Giao tiếp và hợp tác** | Trao đổi, thảo luận trong nhóm; Trình bày cảm nhận mạch lạc, thuyết phục |
| **Giải quyết vấn đề và sáng tạo** | Đề xuất cách hiểu mới; Sáng tạo trong hoạt động viết/nói |

#### b) Năng lực đặc thù (Ngữ văn)

| Năng lực | Yêu cầu cần đạt |
|----------|-----------------|
| **Năng lực ngôn ngữ** | {lesson_info['nang_luc_ngon_ngu']} |
| **Năng lực văn học** | {lesson_info['nang_luc_van_hoc']} |

### 3. Phẩm chất

| Phẩm chất | Biểu hiện |
|-----------|-----------|
| **Yêu nước** | {lesson_info['pham_chat_yeu_nuoc']} |
| **Nhân ái** | Biết cảm thông, chia sẻ với nhân vật trong tác phẩm |
| **Chăm chỉ** | Tích cực tham gia các hoạt động học tập |
| **Trách nhiệm** | Hoàn thành nhiệm vụ được giao đúng hạn |

---

## II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU 📦

### 1. Giáo viên chuẩn bị

| STT | Thiết bị/Học liệu | Số lượng | Ghi chú |
|:---:|-------------------|:--------:|---------|
| 1 | SGK, SGV Ngữ văn {grade} ({textbook_name}) | 1 bộ | |
| 2 | Phiếu học tập (PHT) 1, 2, 3 | 40 tờ/loại | In sẵn |
| 3 | Slide bài giảng PowerPoint | 1 file | Có hình ảnh, video minh họa |
| 4 | {lesson_info.get('hoc_lieu_bo_sung', 'Tranh ảnh, video liên quan')} | | |

### 2. Học sinh chuẩn bị

- ✅ SGK Ngữ văn {grade} ({textbook_name}), vở ghi, bút
- ✅ Đọc trước văn bản "{lesson_name}"
- ✅ Hoàn thành PHT chuẩn bị bài (nếu có)
- ✅ Tìm hiểu về tác giả, hoàn cảnh sáng tác (nếu có)

---

## III. TIẾN TRÌNH DẠY HỌC 📖

{_build_tien_trinh_nguvan(lesson_name, lesson_info, duration, grade)}

---

## IV. HỒ SƠ DẠY HỌC 📋

{_build_pht_nguvan(lesson_name, lesson_info)}

---

## V. RÚT KINH NGHIỆM SAU BÀI DẠY ✍️

| Nội dung đánh giá | Tốt | Khá | Đạt | Chưa đạt | Ghi chú |
|-------------------|:---:|:---:|:---:|:--------:|---------|
| 1. Thời gian thực hiện | ☐ | ☐ | ☐ | ☐ | |
| 2. Mức độ tham gia của HS | ☐ | ☐ | ☐ | ☐ | |
| 3. Hoạt động đọc hiểu | ☐ | ☐ | ☐ | ☐ | |
| 4. Đạt mục tiêu bài học | ☐ | ☐ | ☐ | ☐ | |
| 5. Hoạt động viết/nói | ☐ | ☐ | ☐ | ☐ | |
| 6. Hoạt động nhóm | ☐ | ☐ | ☐ | ☐ | |

📝 **Những điều cần điều chỉnh cho tiết sau:**

_________________________________________________________________________

| 📅 Ngày soạn | 👨‍🏫 Người soạn | ✅ Tổ trưởng duyệt | 📋 BGH duyệt |
|:------------:|:--------------:|:------------------:|:------------:|
| {today} | ________________ | ________________ | ________________ |

---
*📝 Nội dung được tạo dựa trên sách {textbook_name} - Lớp {grade}*

*🤖 GiaoTrinh AI - Hỗ trợ Giáo viên Việt Nam*
"""
    
    return content


def _get_lesson_info_nguvan(lesson_name: str, grade: int, textbook: str) -> dict:
    """Lấy thông tin bài học Ngữ văn."""
    lesson_lower = lesson_name.lower()
    
    # Xác định thể loại
    the_loai = "Văn bản"
    if any(x in lesson_lower for x in ['thơ', 'lục bát', 'ca dao', 'tục ngữ', 'vần']):
        the_loai = "Thơ / Ca dao"
    elif any(x in lesson_lower for x in ['truyện', 'truyền thuyết', 'cổ tích', 'ngụ ngôn']):
        the_loai = "Truyện"
    elif any(x in lesson_lower for x in ['văn bản thông tin', 'thuyết minh']):
        the_loai = "Văn bản thông tin"
    elif any(x in lesson_lower for x in ['nghị luận', 'bình luận']):
        the_loai = "Văn bản nghị luận"
    
    return {
        'the_loai': the_loai,
        'kien_thuc': f"""
- Đọc hiểu được nội dung và nghệ thuật của văn bản "{lesson_name}"
- Nhận biết được đặc điểm thể loại {the_loai}
- Phân tích được giá trị nội dung và nghệ thuật của tác phẩm
""",
        'nang_luc_ngon_ngu': f'Đọc hiểu văn bản {the_loai}; Viết đoạn văn ngắn nêu cảm nhận; Nói và nghe hiệu quả trong thảo luận',
        'nang_luc_van_hoc': f'Cảm thụ được cái hay, cái đẹp của ngôn ngữ văn học; Phân tích, đánh giá tác phẩm',
        'pham_chat_yeu_nuoc': 'Yêu quý vẻ đẹp ngôn ngữ và văn hóa dân tộc',
        'hoc_lieu_bo_sung': 'Tranh ảnh, video minh họa nội dung văn bản',
        'cau_hoi_khoi_dong': f'Em đã biết gì về {lesson_name}? Theo em, văn bản này sẽ nói về điều gì?',
        'noi_dung_1': {
            'ten': 'Đọc và tìm hiểu chung',
            'muc_tieu': f'Nắm được thông tin chung về văn bản "{lesson_name}"; Xác định được thể loại, bố cục',
            'noi_dung': f"""
**Nhiệm vụ 1:** Đọc văn bản và trả lời:
- Văn bản thuộc thể loại gì? Căn cứ vào đâu để xác định?
- Bố cục văn bản gồm mấy phần? Nội dung từng phần?

**Nhiệm vụ 2:** Hoàn thành PHT số 1

| Nội dung | Thông tin |
|----------|-----------|
| Thể loại | |
| Bố cục | |
| Phần 1 | |
| Phần 2 | |
| Phần 3 | |
""",
            'san_pham': 'PHT số 1 hoàn thành với thông tin chung về văn bản'
        },
        'noi_dung_2': {
            'ten': 'Đọc hiểu chi tiết',
            'muc_tieu': 'Phân tích được nội dung và nghệ thuật của văn bản; Nêu được cảm nhận cá nhân',
            'noi_dung': f"""
**Thảo luận nhóm (Kỹ thuật khăn trải bàn):**

| Câu hỏi thảo luận | Gợi ý trả lời |
|-------------------|---------------|
| 1. Nội dung chính của văn bản là gì? | |
| 2. Tác giả sử dụng những biện pháp nghệ thuật nào? Tác dụng? | |
| 3. Chi tiết/hình ảnh nào em ấn tượng nhất? Vì sao? | |
| 4. Thông điệp tác giả muốn gửi gắm? | |
""",
            'san_pham': 'Bài phân tích của nhóm hoàn thành'
        },
        'luyen_tap': f"""
**Bài tập 1:** Viết đoạn văn (5-7 câu) nêu cảm nhận của em về văn bản "{lesson_name}"

*Gợi ý:*
- Mở đoạn: Giới thiệu văn bản, nêu cảm nhận chung
- Thân đoạn: Phân tích 1-2 chi tiết/hình ảnh ấn tượng
- Kết đoạn: Khái quát giá trị, liên hệ bản thân

**Bài tập 2:** Trả lời các câu hỏi đọc hiểu trong SGK
""",
        'van_dung': f"""
1. Tìm thêm các văn bản/tác phẩm cùng chủ đề với "{lesson_name}"

2. Sưu tầm hình ảnh, tư liệu liên quan đến nội dung văn bản

3. Viết bài cảm nhận ngắn (1 trang A4) về giá trị của văn bản

4. **Dự án nhóm (1 tuần):** Thiết kế poster/infographic giới thiệu văn bản "{lesson_name}"
"""
    }


def _build_tien_trinh_nguvan(lesson_name: str, lesson_info: dict, duration: int, grade: int) -> str:
    """Xây dựng tiến trình dạy học Ngữ văn."""
    
    return f"""
### 🕐 TIẾT 1 (45 phút)

---

### A. HOẠT ĐỘNG KHỞI ĐỘNG ⏱️ 5 phút

#### a) Mục tiêu
- Tạo hứng thú, kích thích tò mò của học sinh
- Kết nối kiến thức thực tiễn với nội dung bài học
- Huy động vốn hiểu biết của HS về chủ đề

#### b) Nội dung
📌 **Câu hỏi gợi mở:**

{lesson_info.get('cau_hoi_khoi_dong', f'Em đã biết gì về {lesson_name}?')}

[Hình ảnh/Video: Liên quan đến nội dung văn bản]

#### c) Sản phẩm
- Câu trả lời, chia sẻ ban đầu của học sinh
- Phiếu KWL (cột K và W)

#### d) Tổ chức thực hiện

| Hoạt động của GV và HS | Sản phẩm dự kiến |
|------------------------|------------------|
| **Bước 1: Chuyển giao nhiệm vụ**<br>- GV chiếu hình ảnh/video liên quan đến bài học<br>- GV đặt câu hỏi gợi mở<br>- GV phát phiếu KWL | |
| **Bước 2: Thực hiện nhiệm vụ**<br>- HS suy nghĩ, nhớ lại kiến thức (1 phút)<br>- HS điền cột K (đã biết) và W (muốn biết) (2 phút) | Phiếu KWL |
| **Bước 3: Báo cáo, thảo luận**<br>- GV gọi 2-3 HS chia sẻ<br>- HS trình bày ý kiến cá nhân | Câu trả lời của HS |
| **Bước 4: Kết luận, nhận định**<br>- GV nhận xét, khen ngợi<br>- GV dẫn dắt vào bài mới: "Để tìm hiểu rõ hơn, hôm nay chúng ta cùng đọc văn bản..." | Tên bài học |

---

### B. HOẠT ĐỘNG HÌNH THÀNH KIẾN THỨC ⏱️ 30 phút

---

#### Hoạt động 1: {lesson_info['noi_dung_1']['ten']} (15 phút)

##### a) Mục tiêu
{lesson_info['noi_dung_1']['muc_tieu']}

##### b) Nội dung
{lesson_info['noi_dung_1']['noi_dung']}

##### c) Sản phẩm
✅ {lesson_info['noi_dung_1']['san_pham']}

##### d) Tổ chức thực hiện

| Hoạt động của GV và HS | Sản phẩm dự kiến |
|------------------------|------------------|
| **Bước 1: Chuyển giao nhiệm vụ**<br>- GV hướng dẫn HS đọc văn bản (đọc mẫu hoặc gọi HS đọc)<br>- GV phát PHT số 1<br>- GV nêu yêu cầu nhiệm vụ, thời gian: 7 phút | |
| **Bước 2: Thực hiện nhiệm vụ**<br>- HS đọc văn bản cá nhân (hoặc theo nhóm)<br>- HS thảo luận, hoàn thành PHT<br>- GV quan sát, hỗ trợ các nhóm | PHT số 1 hoàn thành |
| **Bước 3: Báo cáo, thảo luận**<br>- Đại diện 2 nhóm trình bày (mỗi nhóm 2 phút)<br>- Các nhóm khác nhận xét, bổ sung | Nội dung trình bày |
| **Bước 4: Kết luận, nhận định**<br>- GV nhận xét quá trình làm việc<br>- GV chốt kiến thức về thể loại, bố cục<br>- HS ghi chép vào vở | Ghi bảng/vở |

---

#### Hoạt động 2: {lesson_info['noi_dung_2']['ten']} (15 phút)

##### a) Mục tiêu
{lesson_info['noi_dung_2']['muc_tieu']}

##### b) Nội dung
{lesson_info['noi_dung_2']['noi_dung']}

##### c) Sản phẩm
✅ {lesson_info['noi_dung_2']['san_pham']}

##### d) Tổ chức thực hiện

| Hoạt động của GV và HS | Sản phẩm dự kiến |
|------------------------|------------------|
| **Bước 1: Chuyển giao nhiệm vụ**<br>- GV chia nhóm (4-5 HS/nhóm)<br>- GV giao nhiệm vụ phân tích (kỹ thuật khăn trải bàn)<br>- GV phát PHT số 2, thời gian: 7 phút | |
| **Bước 2: Thực hiện nhiệm vụ**<br>- HS đọc lại văn bản (đoạn cần phân tích)<br>- HS thảo luận theo câu hỏi định hướng<br>- HS ghi kết quả vào PHT<br>- GV quan sát, đặt câu hỏi gợi mở | PHT số 2 hoàn thành |
| **Bước 3: Báo cáo, thảo luận**<br>- Các nhóm trình bày kết quả (2 phút/nhóm)<br>- Thảo luận, tranh biện về các ý kiến khác nhau<br>- GV điều phối, đặt câu hỏi mở rộng | Bài trình bày của nhóm |
| **Bước 4: Kết luận, nhận định**<br>- GV tổng kết nội dung phân tích<br>- GV chốt kiến thức trọng tâm (giá trị nội dung, nghệ thuật)<br>- HS ghi nội dung chính vào vở | Nội dung chính trong vở |

---

### C. HOẠT ĐỘNG LUYỆN TẬP ⏱️ 7 phút

#### a) Mục tiêu
- Củng cố kiến thức đã học
- Rèn kỹ năng viết đoạn văn ngắn
- Phát triển năng lực diễn đạt

#### b) Nội dung
{lesson_info['luyen_tap']}

#### c) Sản phẩm
- Đoạn văn của học sinh (5-7 câu)
- Câu trả lời các bài tập SGK

#### d) Tổ chức thực hiện

| Hoạt động của GV và HS | Sản phẩm dự kiến |
|------------------------|------------------|
| **Bước 1: Chuyển giao nhiệm vụ**<br>- GV nêu yêu cầu viết đoạn văn<br>- GV hướng dẫn cấu trúc đoạn văn (Mở - Thân - Kết)<br>- Thời gian: 5 phút | |
| **Bước 2: Thực hiện nhiệm vụ**<br>- HS viết đoạn văn cá nhân vào vở<br>- GV quan sát, hỗ trợ HS gặp khó khăn | Đoạn văn của HS |
| **Bước 3: Báo cáo, thảo luận**<br>- GV gọi 2-3 HS đọc đoạn văn<br>- Lớp nhận xét, góp ý theo tiêu chí | |
| **Bước 4: Kết luận, nhận định**<br>- GV nhận xét, khen ngợi các đoạn văn hay<br>- GV hướng dẫn sửa lỗi phổ biến<br>- HS hoàn thiện đoạn văn | Đoạn văn hoàn chỉnh |

---

### D. HOẠT ĐỘNG VẬN DỤNG ⏱️ 3 phút

#### a) Mục tiêu
- Mở rộng, liên hệ thực tiễn
- Phát triển năng lực tự học, sáng tạo

#### b) Nội dung
🏠 **NHIỆM VỤ VỀ NHÀ:**

{lesson_info['van_dung']}

#### c) Sản phẩm
- Bài tập về nhà hoàn thành
- Tư liệu sưu tầm
- Sản phẩm dự án (poster/bài viết)

#### d) Tổ chức thực hiện

| Hoạt động của GV và HS | Sản phẩm dự kiến |
|------------------------|------------------|
| **Bước 1: Chuyển giao nhiệm vụ**<br>- GV giao nhiệm vụ về nhà (chiếu màn hình)<br>- GV nêu rõ yêu cầu và hạn nộp<br>- GV giới thiệu dự án nhóm | |
| **Bước 2: Thực hiện nhiệm vụ**<br>- HS ghi nhận nhiệm vụ vào vở<br>- HS hoàn thành cột L của phiếu KWL | Phiếu KWL hoàn chỉnh |
| **Bước 3: Báo cáo, thảo luận**<br>- GV hỏi: "Hôm nay em đã học được điều gì?"<br>- 1-2 HS chia sẻ | Tổng kết bài học |
| **Bước 4: Kết luận, nhận định**<br>- GV nhận xét tiết học<br>- GV dặn dò chuẩn bị bài sau | |
"""


def _build_pht_nguvan(lesson_name: str, lesson_info: dict) -> str:
    """Xây dựng PHT môn Ngữ văn."""
    
    return f"""
### 📄 PHIẾU HỌC TẬP SỐ 1 - ĐỌC VÀ TÌM HIỂU CHUNG

| | |
|---|---|
| **Họ và tên:** ___________________________ | **Lớp:** ______ |
| **Nhóm:** ______ | **Ngày:** ___/___/______ |

---

**BÀI: {lesson_name.upper()}**

---

**Câu 1:** Văn bản thuộc thể loại gì? Căn cứ vào đâu để xác định?

> Thể loại: ________________________________________________________
> Căn cứ: __________________________________________________________

**Câu 2:** Xác định bố cục văn bản:

| Phần | Giới hạn (từ... đến...) | Nội dung chính |
|:----:|-------------------------|----------------|
| 1 | | |
| 2 | | |
| 3 | | |

**Câu 3:** Nêu nội dung chính của văn bản (2-3 câu):

> _______________________________________________________________
> _______________________________________________________________
> _______________________________________________________________

---

### 📄 PHIẾU HỌC TẬP SỐ 2 - ĐỌC HIỂU CHI TIẾT

**Câu 1:** Phân tích nội dung văn bản:

| Khía cạnh | Nội dung phân tích |
|-----------|-------------------|
| **Chủ đề chính** | |
| **Nhân vật/Hình ảnh trung tâm** | |
| **Tình cảm/Cảm xúc** | |
| **Thông điệp** | |

**Câu 2:** Phân tích nghệ thuật:

| Biện pháp nghệ thuật | Ví dụ trong văn bản | Tác dụng |
|---------------------|---------------------|----------|
| | | |
| | | |
| | | |

**Câu 3:** Chi tiết/hình ảnh em ấn tượng nhất? Vì sao?

> Chi tiết: _______________________________________________________
> Lý do: __________________________________________________________
> ________________________________________________________________

---

### 📄 PHIẾU KWL

| K (Know) - Em đã biết gì? | W (Want to know) - Em muốn biết gì? | L (Learned) - Em đã học được gì? |
|---------------------------|-------------------------------------|----------------------------------|
| | | |
| | | |
| | | |
| | | |

---

### 📊 RUBRIC ĐÁNH GIÁ ĐOẠN VĂN

| Tiêu chí | Mức 4 (9-10đ) | Mức 3 (7-8đ) | Mức 2 (5-6đ) | Mức 1 (<5đ) |
|----------|---------------|--------------|--------------|-------------|
| **Nội dung (4đ)** | Đầy đủ, sâu sắc, có sáng tạo | Đầy đủ, đúng yêu cầu | Thiếu 1-2 ý chính | Thiếu nhiều ý, lạc đề |
| **Diễn đạt (3đ)** | Mạch lạc, giàu hình ảnh, cảm xúc | Mạch lạc, rõ ràng | Còn lủng củng đôi chỗ | Khó hiểu, rời rạc |
| **Ngữ pháp, chính tả (2đ)** | Không có lỗi | 1-2 lỗi nhỏ | 3-4 lỗi | Nhiều lỗi (>5) |
| **Trình bày (1đ)** | Sạch đẹp, đúng quy cách | Sạch sẽ, rõ ràng | Chưa gọn gàng | Cẩu thả |

---

### 📊 ĐÁP ÁN VÀ THANG ĐIỂM (PHT)

| Câu | Nội dung đáp án | Điểm |
|:---:|-----------------|:----:|
| 1 | Xác định đúng thể loại + nêu căn cứ hợp lý | 2.0 |
| 2 | Xác định đúng bố cục (mỗi phần đúng 1 điểm) | 3.0 |
| 3 | Nêu được nội dung chính, đầy đủ, ngắn gọn | 2.0 |
| 4 | Phân tích nghệ thuật có ví dụ và tác dụng | 2.5 |
| | Trình bày sạch đẹp, rõ ràng | 0.5 |
| **TỔNG** | | **10** |
"""
