"""
Dữ liệu chương trình giảng dạy thực tế theo các bộ sách.
Nguồn: Chương trình GDPT 2018
"""

# ==============================================================
# KHTN LỚP 6 - CÁC BỘ SÁCH
# ==============================================================

KHTN_6_CTST = {
    # Chủ đề 1: Giới thiệu về Khoa học Tự nhiên
    "Bài 1": {
        "ten_bai": "Giới thiệu về Khoa học tự nhiên",
        "linh_vuc": "Tổng hợp",
        "khai_niem": ["Khoa học tự nhiên", "Vật sống", "Vật không sống", "Hiện tượng tự nhiên"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm Khoa học tự nhiên",
            "Phân biệt được vật sống và vật không sống",
            "Nêu được một số hiện tượng tự nhiên thường gặp"
        ],
        "thiet_bi": ["Tranh ảnh về thiên nhiên", "Video về các hiện tượng tự nhiên"],
    },
    "Bài 2": {
        "ten_bai": "Các lĩnh vực chủ yếu của Khoa học tự nhiên",
        "linh_vuc": "Tổng hợp",
        "khai_niem": ["Vật lý học", "Hóa học", "Sinh học", "Thiên văn học", "Khoa học Trái Đất"],
        "yeu_cau_can_dat": [
            "Trình bày được các lĩnh vực chủ yếu của KHTN",
            "Nêu được đối tượng nghiên cứu của từng lĩnh vực"
        ],
        "thiet_bi": ["SGK", "Tranh ảnh minh họa"],
    },
    "Bài 3": {
        "ten_bai": "Quy định an toàn trong phòng thực hành",
        "linh_vuc": "Tổng hợp",
        "khai_niem": ["An toàn phòng thí nghiệm", "Ký hiệu cảnh báo", "Dụng cụ bảo hộ"],
        "yeu_cau_can_dat": [
            "Nêu được các quy định an toàn khi làm thí nghiệm",
            "Nhận biết được các ký hiệu cảnh báo nguy hiểm",
            "Biết cách sử dụng dụng cụ bảo hộ"
        ],
        "thiet_bi": ["Kính bảo hộ", "Găng tay", "Bảng ký hiệu cảnh báo"],
    },
    "Bài 4": {
        "ten_bai": "Sử dụng kính lúp",
        "linh_vuc": "Sinh học",
        "khai_niem": ["Kính lúp", "Độ phóng đại", "Tiêu cự"],
        "yeu_cau_can_dat": [
            "Nêu được cấu tạo của kính lúp",
            "Trình bày được cách sử dụng kính lúp",
            "Sử dụng được kính lúp để quan sát vật nhỏ"
        ],
        "thiet_bi": ["Kính lúp cầm tay", "Mẫu vật (lá cây, côn trùng)"],
        "cong_thuc": ["Độ phóng đại: $G = \\frac{25}{f}$ (f tính bằng cm)"],
    },
    "Bài 5": {
        "ten_bai": "Sử dụng kính hiển vi quang học",
        "linh_vuc": "Sinh học",
        "khai_niem": ["Kính hiển vi", "Thị kính", "Vật kính", "Độ phóng đại"],
        "yeu_cau_can_dat": [
            "Nêu được cấu tạo kính hiển vi quang học",
            "Biết cách sử dụng kính hiển vi",
            "Quan sát được tế bào dưới kính hiển vi"
        ],
        "thiet_bi": ["Kính hiển vi quang học", "Tiêu bản tế bào"],
        "cong_thuc": ["Độ phóng đại tổng: $G = G_{tk} \\times G_{vk}$"],
    },
    "Bài 6": {
        "ten_bai": "Đo chiều dài",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Chiều dài", "Đơn vị đo", "Dụng cụ đo", "GHĐ", "ĐCNN"],
        "yeu_cau_can_dat": [
            "Nêu được đơn vị đo chiều dài trong hệ SI",
            "Xác định được GHĐ và ĐCNN của thước",
            "Đo được chiều dài của một vật"
        ],
        "thiet_bi": ["Thước kẻ", "Thước cuộn", "Thước dây"],
        "cong_thuc": ["$1m = 10dm = 100cm = 1000mm$", "$1km = 1000m$"],
    },
    "Bài 7": {
        "ten_bai": "Đo khối lượng",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Khối lượng", "Cân", "Đơn vị kilogram"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm khối lượng",
            "Biết cách sử dụng cân để đo khối lượng",
            "Đổi được các đơn vị khối lượng"
        ],
        "thiet_bi": ["Cân đồng hồ", "Cân điện tử", "Các vật mẫu"],
        "cong_thuc": ["$1kg = 1000g$", "$1 tấn = 1000kg$"],
    },
    "Bài 8": {
        "ten_bai": "Đo thời gian",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Thời gian", "Đồng hồ", "Đơn vị giây"],
        "yeu_cau_can_dat": [
            "Nêu được đơn vị đo thời gian trong hệ SI",
            "Biết cách sử dụng đồng hồ bấm giây",
            "Đo được khoảng thời gian của một hoạt động"
        ],
        "thiet_bi": ["Đồng hồ bấm giây", "Đồng hồ treo tường"],
        "cong_thuc": ["$1h = 60 phút = 3600s$", "$1 phút = 60s$"],
    },
    "Bài 9": {
        "ten_bai": "Đo nhiệt độ",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Nhiệt độ", "Nhiệt kế", "Thang nhiệt độ Celsius"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm nhiệt độ",
            "Biết cách sử dụng nhiệt kế",
            "Đo được nhiệt độ cơ thể, nước"
        ],
        "thiet_bi": ["Nhiệt kế y tế", "Nhiệt kế thủy ngân", "Nhiệt kế điện tử"],
        "cong_thuc": ["Nhiệt độ đông đặc nước: $0°C$", "Nhiệt độ sôi nước: $100°C$"],
    },
    "Bài 10": {
        "ten_bai": "Các thể của chất",
        "linh_vuc": "Hóa học",
        "khai_niem": ["Thể rắn", "Thể lỏng", "Thể khí", "Sự chuyển thể"],
        "yeu_cau_can_dat": [
            "Nêu được đặc điểm của các thể rắn, lỏng, khí",
            "Phân biệt được 3 thể của chất",
            "Nêu ví dụ về sự chuyển thể"
        ],
        "thiet_bi": ["Nước đá", "Nước lỏng", "Hơi nước"],
    },
    "Bài 11": {
        "ten_bai": "Oxygen và không khí",
        "linh_vuc": "Hóa học",
        "khai_niem": ["Oxygen", "Không khí", "Thành phần không khí", "Sự cháy"],
        "yeu_cau_can_dat": [
            "Nêu được tính chất của oxygen",
            "Trình bày được thành phần của không khí",
            "Giải thích được vai trò của oxygen"
        ],
        "thiet_bi": ["Bình oxygen", "Nến", "Que đóm"],
        "cong_thuc": ["Công thức phân tử: $O_2$", "Không khí: ~78% $N_2$, ~21% $O_2$"],
    },
    "Bài 12": {
        "ten_bai": "Một số vật liệu thông dụng",
        "linh_vuc": "Hóa học",
        "khai_niem": ["Vật liệu", "Kim loại", "Nhựa", "Gỗ", "Cao su"],
        "yeu_cau_can_dat": [
            "Nêu được tính chất của một số vật liệu",
            "Phân loại được các loại vật liệu",
            "Nêu được ứng dụng của từng loại vật liệu"
        ],
        "thiet_bi": ["Mẫu vật liệu: kim loại, nhựa, gỗ"],
    },
    "Bài 13": {
        "ten_bai": "Một số nguyên liệu",
        "linh_vuc": "Hóa học",
        "khai_niem": ["Nguyên liệu", "Quặng", "Dầu mỏ", "Đá vôi"],
        "yeu_cau_can_dat": [
            "Phân biệt được nguyên liệu và vật liệu",
            "Nêu được nguồn gốc một số nguyên liệu",
            "Trình bày ứng dụng của nguyên liệu"
        ],
        "thiet_bi": ["Mẫu quặng", "Tranh ảnh về khai thác nguyên liệu"],
    },
    "Bài 14": {
        "ten_bai": "Một số nhiên liệu",
        "linh_vuc": "Hóa học",
        "khai_niem": ["Nhiên liệu", "Than đá", "Dầu mỏ", "Khí thiên nhiên", "Năng lượng"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm nhiên liệu",
            "Phân loại được các loại nhiên liệu",
            "Nêu được tác dụng của việc sử dụng nhiên liệu"
        ],
        "thiet_bi": ["Mẫu than đá", "Video về khai thác dầu mỏ"],
        "cong_thuc": ["Phản ứng cháy: $C + O_2 \\xrightarrow{t^o} CO_2$"],
    },
    "Bài 15": {
        "ten_bai": "Một số lương thực, thực phẩm",
        "linh_vuc": "Hóa học",
        "khai_niem": ["Lương thực", "Thực phẩm", "Chất dinh dưỡng", "Carbohydrate", "Protein"],
        "yeu_cau_can_dat": [
            "Phân biệt được lương thực và thực phẩm",
            "Nêu được vai trò của các chất dinh dưỡng",
            "Biết cách bảo quản lương thực, thực phẩm"
        ],
        "thiet_bi": ["Mẫu lương thực: gạo, ngô", "Mẫu thực phẩm"],
    },
    "Bài 16": {
        "ten_bai": "Hỗn hợp các chất",
        "linh_vuc": "Hóa học",
        "khai_niem": ["Hỗn hợp", "Chất tinh khiết", "Hỗn hợp đồng nhất", "Hỗn hợp không đồng nhất"],
        "yeu_cau_can_dat": [
            "Phân biệt được hỗn hợp và chất tinh khiết",
            "Nêu được ví dụ về hỗn hợp trong đời sống",
            "Phân loại được hỗn hợp đồng nhất và không đồng nhất"
        ],
        "thiet_bi": ["Nước muối", "Cát và nước", "Không khí"],
    },
    "Bài 17": {
        "ten_bai": "Tách chất ra khỏi hỗn hợp",
        "linh_vuc": "Hóa học",
        "khai_niem": ["Lọc", "Bay hơi", "Chiết", "Tách chất"],
        "yeu_cau_can_dat": [
            "Nêu được các phương pháp tách chất",
            "Thực hiện được thí nghiệm tách chất đơn giản",
            "Vận dụng tách chất trong đời sống"
        ],
        "thiet_bi": ["Phễu lọc", "Giấy lọc", "Đèn cồn", "Cốc thủy tinh"],
    },
    # Sinh học
    "Bài 18": {
        "ten_bai": "Tế bào - Đơn vị cơ bản của sự sống",
        "linh_vuc": "Sinh học",
        "khai_niem": ["Tế bào", "Màng tế bào", "Tế bào chất", "Nhân tế bào"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm tế bào",
            "Mô tả được cấu tạo cơ bản của tế bào",
            "Phân biệt được tế bào động vật và thực vật"
        ],
        "thiet_bi": ["Kính hiển vi", "Tiêu bản tế bào"],
    },
    "Bài 19": {
        "ten_bai": "Cấu tạo và chức năng các thành phần của tế bào",
        "linh_vuc": "Sinh học",
        "khai_niem": ["Màng sinh chất", "Ti thể", "Lục lạp", "Không bào", "Ribosome"],
        "yeu_cau_can_dat": [
            "Nêu được cấu tạo và chức năng của các bào quan",
            "So sánh tế bào nhân sơ và nhân thực",
            "Giải thích vai trò của từng bào quan"
        ],
        "thiet_bi": ["Tranh cấu tạo tế bào", "Mô hình tế bào"],
    },
    "Bài 20": {
        "ten_bai": "Sự lớn lên và sinh sản của tế bào",
        "linh_vuc": "Sinh học",
        "khai_niem": ["Phân bào", "Nguyên phân", "Chu kỳ tế bào"],
        "yeu_cau_can_dat": [
            "Mô tả được sự lớn lên của tế bào",
            "Trình bày được quá trình phân chia tế bào",
            "Nêu được ý nghĩa của sự phân chia tế bào"
        ],
        "thiet_bi": ["Video về phân bào", "Tranh các kỳ phân bào"],
    },
    # Vật lý - Lực
    "Bài 21": {
        "ten_bai": "Lực và tác dụng của lực",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Lực", "Tác dụng đẩy", "Tác dụng kéo", "Biến dạng", "Thay đổi chuyển động"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm lực",
            "Nêu được các tác dụng của lực",
            "Lấy được ví dụ về tác dụng của lực"
        ],
        "thiet_bi": ["Lò xo", "Xe đẩy", "Quả bóng"],
        "cong_thuc": ["Đơn vị lực: Newton (N)"],
    },
    "Bài 22": {
        "ten_bai": "Biểu diễn lực",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Véc tơ lực", "Điểm đặt", "Phương", "Chiều", "Độ lớn"],
        "yeu_cau_can_dat": [
            "Nêu được các đặc trưng của lực",
            "Biểu diễn được lực bằng véc tơ",
            "Đọc được các yếu tố của lực từ hình vẽ"
        ],
        "thiet_bi": ["Thước kẻ", "Bảng phụ"],
        "cong_thuc": ["$\\vec{F}$: véc tơ lực"],
    },
    "Bài 23": {
        "ten_bai": "Lực hấp dẫn và trọng lực",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Lực hấp dẫn", "Trọng lực", "Trọng lượng", "Gia tốc trọng trường"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm lực hấp dẫn",
            "Phân biệt được trọng lực và trọng lượng",
            "Tính được trọng lượng của vật"
        ],
        "thiet_bi": ["Quả nặng", "Lực kế"],
        "cong_thuc": ["$P = m \\times g$", "Trong đó: P (N), m (kg), g ≈ 10 m/s²"],
    },
    "Bài 24": {
        "ten_bai": "Lực ma sát",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Lực ma sát", "Ma sát trượt", "Ma sát lăn", "Ma sát nghỉ", "Hệ số ma sát"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm lực ma sát",
            "Phân biệt được 3 loại ma sát",
            "Nêu được ví dụ về lực ma sát trong đời sống"
        ],
        "thiet_bi": ["Khối gỗ", "Mặt phẳng nghiêng", "Lực kế"],
        "cong_thuc": ["$F_{ms} = \\mu \\times N$"],
    },
    "Bài 25": {
        "ten_bai": "Lực cản của nước",
        "linh_vuc": "Vật lý", 
        "khai_niem": ["Lực cản", "Lực cản nước", "Hình dạng khí động học"],
        "yeu_cau_can_dat": [
            "Nhận biết được lực cản của nước",
            "Nêu được các yếu tố ảnh hưởng đến lực cản",
            "Vận dụng giảm lực cản trong thực tế"
        ],
        "thiet_bi": ["Bể nước", "Các vật có hình dạng khác nhau"],
    },
}

KHTN_6_KNTT = {
    "Bài 1": {
        "ten_bai": "Giới thiệu về Khoa học tự nhiên",
        "linh_vuc": "Tổng hợp",
        "khai_niem": ["Khoa học tự nhiên", "Phương pháp nghiên cứu", "Quan sát", "Thí nghiệm"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm và vai trò của KHTN",
            "Trình bày được các phương pháp nghiên cứu KHTN"
        ],
        "thiet_bi": ["SGK", "Video giới thiệu"],
    },
    # Thêm các bài khác...
}

KHTN_6_CD = {
    "Bài 1": {
        "ten_bai": "Mở đầu về Khoa học tự nhiên",
        "linh_vuc": "Tổng hợp",
        "khai_niem": ["Khoa học tự nhiên", "Vật chất", "Năng lượng", "Sự sống"],
        "yeu_cau_can_dat": [
            "Hiểu được Khoa học tự nhiên nghiên cứu gì",
            "Nhận biết được các hiện tượng tự nhiên"
        ],
        "thiet_bi": ["SGK", "Tranh ảnh"],
    },
    # Thêm các bài khác...
}

# ==============================================================
# KHTN LỚP 7
# ==============================================================

KHTN_7_CTST = {
    "Bài 1": {
        "ten_bai": "Nguyên tử",
        "linh_vuc": "Hóa học",
        "khai_niem": ["Nguyên tử", "Proton", "Neutron", "Electron", "Hạt nhân"],
        "yeu_cau_can_dat": [
            "Nêu được cấu tạo của nguyên tử",
            "Xác định được số proton, neutron, electron",
            "Giải thích được tính trung hòa điện của nguyên tử"
        ],
        "thiet_bi": ["Mô hình nguyên tử", "Bảng tuần hoàn"],
        "cong_thuc": ["Số p = Số e", "A = Z + N"],
    },
    "Bài 2": {
        "ten_bai": "Nguyên tố hóa học",
        "linh_vuc": "Hóa học",
        "khai_niem": ["Nguyên tố hóa học", "Ký hiệu hóa học", "Nguyên tử khối"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm nguyên tố hóa học",
            "Viết được ký hiệu hóa học",
            "Tra cứu được nguyên tử khối"
        ],
        "thiet_bi": ["Bảng tuần hoàn"],
        "cong_thuc": ["$^A_Z X$ với A: số khối, Z: số hiệu nguyên tử"],
    },
    "Bài 3": {
        "ten_bai": "Sơ lược về bảng tuần hoàn các nguyên tố hóa học",
        "linh_vuc": "Hóa học",
        "khai_niem": ["Bảng tuần hoàn", "Chu kỳ", "Nhóm", "Kim loại", "Phi kim"],
        "yeu_cau_can_dat": [
            "Mô tả được cấu trúc bảng tuần hoàn",
            "Xác định được vị trí nguyên tố",
            "Suy ra được tính chất cơ bản của nguyên tố"
        ],
        "thiet_bi": ["Bảng tuần hoàn lớn"],
    },
    "Bài 4": {
        "ten_bai": "Phân tử, đơn chất, hợp chất",
        "linh_vuc": "Hóa học",
        "khai_niem": ["Phân tử", "Đơn chất", "Hợp chất", "Công thức hóa học"],
        "yeu_cau_can_dat": [
            "Phân biệt được phân tử, đơn chất, hợp chất",
            "Viết được công thức hóa học đơn giản",
            "Tính được phân tử khối"
        ],
        "thiet_bi": ["Mô hình phân tử"],
        "cong_thuc": ["$H_2O$: phân tử nước", "PTK = Tổng NTK các nguyên tử"],
    },
    "Bài 5": {
        "ten_bai": "Giới thiệu về liên kết hóa học",
        "linh_vuc": "Hóa học",
        "khai_niem": ["Liên kết hóa học", "Liên kết ion", "Liên kết cộng hóa trị"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm liên kết hóa học",
            "Phân biệt được liên kết ion và cộng hóa trị"
        ],
        "thiet_bi": ["Mô hình liên kết"],
    },
    "Bài 6": {
        "ten_bai": "Hóa trị và công thức hóa học",
        "linh_vuc": "Hóa học",
        "khai_niem": ["Hóa trị", "Quy tắc hóa trị", "Lập công thức hóa học"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm hóa trị",
            "Vận dụng quy tắc hóa trị lập công thức",
            "Xác định được hóa trị của nguyên tố"
        ],
        "thiet_bi": ["Bảng hóa trị"],
        "cong_thuc": ["Quy tắc: $a \\times x = b \\times y$", "Với $A_x B_y$"],
    },
    "Bài 7": {
        "ten_bai": "Tốc độ chuyển động",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Tốc độ", "Quãng đường", "Thời gian", "Đơn vị tốc độ"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm tốc độ",
            "Tính được tốc độ chuyển động",
            "Đổi được đơn vị tốc độ"
        ],
        "thiet_bi": ["Đồng hồ bấm giây", "Thước dây"],
        "cong_thuc": ["$v = \\frac{s}{t}$", "$1 km/h = \\frac{1}{3,6} m/s$"],
    },
    "Bài 8": {
        "ten_bai": "Đồ thị quãng đường - thời gian",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Đồ thị", "Chuyển động đều", "Tốc độ từ đồ thị"],
        "yeu_cau_can_dat": [
            "Vẽ được đồ thị s-t",
            "Đọc được thông tin từ đồ thị",
            "Xác định được tốc độ từ đồ thị"
        ],
        "thiet_bi": ["Giấy kẻ ô", "Thước kẻ"],
    },
    "Bài 9": {
        "ten_bai": "Đo tốc độ",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Tốc kế", "Cổng quang", "Đo gián tiếp"],
        "yeu_cau_can_dat": [
            "Biết các dụng cụ đo tốc độ",
            "Thực hiện được phép đo tốc độ",
            "Phân tích được sai số phép đo"
        ],
        "thiet_bi": ["Đồng hồ bấm giây", "Cổng quang điện", "Xe trượt"],
    },
    "Bài 10": {
        "ten_bai": "Âm thanh",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Sóng âm", "Nguồn âm", "Dao động", "Môi trường truyền âm"],
        "yeu_cau_can_dat": [
            "Nêu được nguồn gốc của âm thanh",
            "Giải thích được sự truyền âm",
            "Nêu được ví dụ về truyền âm trong các môi trường"
        ],
        "thiet_bi": ["Âm thoa", "Trống", "Cốc nước"],
    },
    "Bài 11": {
        "ten_bai": "Độ cao và độ to của âm",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Tần số", "Biên độ", "Độ cao", "Độ to", "Hertz"],
        "yeu_cau_can_dat": [
            "Phân biệt được độ cao và độ to của âm",
            "Nêu được mối liên hệ giữa tần số và độ cao",
            "Giải thích được một số hiện tượng liên quan"
        ],
        "thiet_bi": ["Âm thoa", "Dao động kí"],
        "cong_thuc": ["Tần số: f (Hz)", "Tai người nghe được: 20Hz - 20000Hz"],
    },
    "Bài 12": {
        "ten_bai": "Phản xạ và hấp thụ âm",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Phản xạ âm", "Tiếng vang", "Hấp thụ âm", "Vật liệu cách âm"],
        "yeu_cau_can_dat": [
            "Nêu được hiện tượng phản xạ âm",
            "Giải thích được tiếng vang",
            "Nêu được ứng dụng của phản xạ và hấp thụ âm"
        ],
        "thiet_bi": ["Các vật liệu khác nhau", "Loa"],
    },
    "Bài 13": {
        "ten_bai": "Ánh sáng, tia sáng",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Ánh sáng", "Nguồn sáng", "Tia sáng", "Vật sáng"],
        "yeu_cau_can_dat": [
            "Phân biệt được nguồn sáng và vật sáng",
            "Nhận biết được tia sáng",
            "Giải thích được ta nhìn thấy vật"
        ],
        "thiet_bi": ["Đèn pin", "Hộp tối", "Màn chắn"],
    },
    "Bài 14": {
        "ten_bai": "Sự phản xạ ánh sáng",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Phản xạ ánh sáng", "Tia tới", "Tia phản xạ", "Định luật phản xạ"],
        "yeu_cau_can_dat": [
            "Phát biểu được định luật phản xạ ánh sáng",
            "Vẽ được tia phản xạ khi biết tia tới",
            "Giải thích được một số hiện tượng"
        ],
        "thiet_bi": ["Gương phẳng", "Đèn laser", "Thước đo góc"],
        "cong_thuc": ["Góc phản xạ = Góc tới: $i' = i$"],
    },
    "Bài 15": {
        "ten_bai": "Ảnh của vật qua gương phẳng",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Gương phẳng", "Ảnh ảo", "Đối xứng gương"],
        "yeu_cau_can_dat": [
            "Nêu được tính chất ảnh qua gương phẳng",
            "Vẽ được ảnh của vật qua gương phẳng",
            "Giải thích được ứng dụng của gương phẳng"
        ],
        "thiet_bi": ["Gương phẳng", "Nến", "Thước kẻ"],
    },
    # Sinh học lớp 7
    "Bài 20": {
        "ten_bai": "Quang hợp ở thực vật",
        "linh_vuc": "Sinh học",
        "khai_niem": ["Quang hợp", "Lục lạp", "Diệp lục", "Glucose"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm quang hợp",
            "Viết được phương trình quang hợp",
            "Nêu được vai trò của quang hợp"
        ],
        "thiet_bi": ["Cây xanh", "Giấy thử tinh bột"],
        "cong_thuc": ["$6CO_2 + 6H_2O \\xrightarrow{ánh sáng} C_6H_{12}O_6 + 6O_2$"],
    },
    "Bài 21": {
        "ten_bai": "Hô hấp ở thực vật",
        "linh_vuc": "Sinh học",
        "khai_niem": ["Hô hấp", "Ti thể", "ATP", "Năng lượng"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm hô hấp",
            "Viết được phương trình hô hấp",
            "So sánh được quang hợp và hô hấp"
        ],
        "thiet_bi": ["Hạt nảy mầm", "Nhiệt kế"],
        "cong_thuc": ["$C_6H_{12}O_6 + 6O_2 \\rightarrow 6CO_2 + 6H_2O + ATP$"],
    },
}

# ==============================================================
# KHTN LỚP 8
# ==============================================================

KHTN_8_CTST = {
    "Bài 1": {
        "ten_bai": "Phản ứng hóa học",
        "linh_vuc": "Hóa học",
        "khai_niem": ["Phản ứng hóa học", "Chất phản ứng", "Sản phẩm", "Phương trình hóa học"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm phản ứng hóa học",
            "Phân biệt được chất phản ứng và sản phẩm",
            "Viết được phương trình hóa học đơn giản"
        ],
        "thiet_bi": ["Ống nghiệm", "Đèn cồn", "Hóa chất"],
        "cong_thuc": ["$2H_2 + O_2 \\xrightarrow{t^o} 2H_2O$"],
    },
    "Bài 2": {
        "ten_bai": "Định luật bảo toàn khối lượng",
        "linh_vuc": "Hóa học",
        "khai_niem": ["Định luật bảo toàn khối lượng", "Lavoisier", "Cân bằng phương trình"],
        "yeu_cau_can_dat": [
            "Phát biểu được định luật bảo toàn khối lượng",
            "Vận dụng tính khối lượng chất",
            "Cân bằng được phương trình hóa học"
        ],
        "thiet_bi": ["Cân điện tử", "Bình kín", "Hóa chất"],
        "cong_thuc": ["$m_{chất\\ tham\\ gia} = m_{sản\\ phẩm}$"],
    },
    "Bài 3": {
        "ten_bai": "Mol và tỉ khối",
        "linh_vuc": "Hóa học",
        "khai_niem": ["Mol", "Số Avogadro", "Khối lượng mol", "Thể tích mol", "Tỉ khối"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm mol",
            "Tính được số mol, khối lượng, thể tích",
            "Tính được tỉ khối của chất khí"
        ],
        "thiet_bi": ["Bảng khối lượng mol"],
        "cong_thuc": ["$n = \\frac{m}{M}$", "$V = n \\times 22,4$ (đktc)", "$d_{A/B} = \\frac{M_A}{M_B}$"],
    },
    "Bài 4": {
        "ten_bai": "Dung dịch và nồng độ dung dịch",
        "linh_vuc": "Hóa học",
        "khai_niem": ["Dung dịch", "Dung môi", "Chất tan", "Nồng độ phần trăm", "Nồng độ mol"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm dung dịch",
            "Tính được nồng độ phần trăm",
            "Tính được nồng độ mol"
        ],
        "thiet_bi": ["Cốc thủy tinh", "Ống đong", "Cân"],
        "cong_thuc": ["$C\\% = \\frac{m_{ct}}{m_{dd}} \\times 100\\%$", "$C_M = \\frac{n}{V}$"],
    },
    "Bài 5": {
        "ten_bai": "Áp suất",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Áp suất", "Áp lực", "Diện tích bị ép", "Pascal"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm áp suất",
            "Tính được áp suất",
            "Giải thích được các hiện tượng liên quan"
        ],
        "thiet_bi": ["Bộ thí nghiệm áp suất"],
        "cong_thuc": ["$p = \\frac{F}{S}$", "Đơn vị: Pa = N/m²"],
    },
    "Bài 6": {
        "ten_bai": "Áp suất chất lỏng. Áp suất khí quyển",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Áp suất chất lỏng", "Áp suất khí quyển", "Bình thông nhau"],
        "yeu_cau_can_dat": [
            "Tính được áp suất chất lỏng",
            "Nêu được sự tồn tại của áp suất khí quyển",
            "Giải thích được nguyên lý bình thông nhau"
        ],
        "thiet_bi": ["Bình thông nhau", "Ống nghiệm"],
        "cong_thuc": ["$p = d \\times h = \\rho \\times g \\times h$"],
    },
    "Bài 7": {
        "ten_bai": "Lực đẩy Archimedes",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Lực đẩy Archimedes", "Vật nổi", "Vật chìm", "Trọng lượng riêng"],
        "yeu_cau_can_dat": [
            "Phát biểu được định luật Archimedes",
            "Tính được lực đẩy Archimedes",
            "Giải thích được điều kiện nổi, chìm"
        ],
        "thiet_bi": ["Lực kế", "Cốc nước", "Vật kim loại"],
        "cong_thuc": ["$F_A = d \\times V = \\rho \\times g \\times V$"],
    },
}

# ==============================================================
# KHTN LỚP 9
# ==============================================================

KHTN_9_CTST = {
    "Bài 1": {
        "ten_bai": "Điện trở và định luật Ohm",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Điện trở", "Cường độ dòng điện", "Hiệu điện thế", "Định luật Ohm"],
        "yeu_cau_can_dat": [
            "Phát biểu được định luật Ohm",
            "Tính được điện trở, cường độ, hiệu điện thế",
            "Mắc được mạch điện đơn giản"
        ],
        "thiet_bi": ["Điện trở", "Ampe kế", "Vôn kế", "Nguồn điện"],
        "cong_thuc": ["$I = \\frac{U}{R}$", "Đơn vị: A, V, Ω"],
    },
    "Bài 2": {
        "ten_bai": "Định luật Ohm cho đoạn mạch nối tiếp, song song",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Mạch nối tiếp", "Mạch song song", "Điện trở tương đương"],
        "yeu_cau_can_dat": [
            "Viết được công thức điện trở tương đương",
            "Tính được các đại lượng trong mạch",
            "Phân biệt được mạch nối tiếp và song song"
        ],
        "thiet_bi": ["Bộ điện trở", "Ampe kế", "Vôn kế"],
        "cong_thuc": ["Nối tiếp: $R_{tđ} = R_1 + R_2$", "Song song: $\\frac{1}{R_{tđ}} = \\frac{1}{R_1} + \\frac{1}{R_2}$"],
    },
    "Bài 3": {
        "ten_bai": "Điện năng. Công suất điện",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Điện năng", "Công suất điện", "Kilowatt-giờ"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm điện năng, công suất điện",
            "Tính được điện năng tiêu thụ",
            "Tính được tiền điện phải trả"
        ],
        "thiet_bi": ["Công tơ điện", "Các thiết bị điện"],
        "cong_thuc": ["$P = U \\times I = I^2 \\times R = \\frac{U^2}{R}$", "$A = P \\times t$"],
    },
    "Bài 4": {
        "ten_bai": "Từ trường",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Từ trường", "Nam châm", "Đường sức từ", "Cực Bắc", "Cực Nam"],
        "yeu_cau_can_dat": [
            "Nêu được khái niệm từ trường",
            "Vẽ được đường sức từ của nam châm",
            "Xác định được cực của nam châm"
        ],
        "thiet_bi": ["Nam châm thẳng", "Nam châm chữ U", "Mạt sắt"],
    },
    "Bài 5": {
        "ten_bai": "Từ trường của dòng điện",
        "linh_vuc": "Vật lý",
        "khai_niem": ["Từ trường dòng điện", "Quy tắc nắm tay phải", "Ống dây"],
        "yeu_cau_can_dat": [
            "Nêu được từ trường của dòng điện",
            "Vận dụng quy tắc nắm tay phải",
            "Xác định được chiều đường sức từ"
        ],
        "thiet_bi": ["Dây dẫn", "Kim nam châm", "Nguồn điện"],
    },
}

# ==============================================================
# NGỮ VĂN
# ==============================================================

NGUVAN_6_CTST = {
    "Bài 1": {
        "ten_bai": "Lắng nghe lịch sử nước mình",
        "linh_vuc": "Đọc hiểu",
        "the_loai": "Truyền thuyết",
        "van_ban": ["Con Rồng cháu Tiên", "Bánh chưng bánh giầy"],
        "yeu_cau_can_dat": [
            "Nhận biết được đặc điểm của truyền thuyết",
            "Hiểu được ý nghĩa của truyền thuyết về nguồn gốc dân tộc",
            "Kể lại được truyện bằng lời của mình"
        ],
    },
    "Bài 2": {
        "ten_bai": "Miền cổ tích",
        "linh_vuc": "Đọc hiểu",
        "the_loai": "Truyện cổ tích",
        "van_ban": ["Thạch Sanh", "Sọ Dừa"],
        "yeu_cau_can_dat": [
            "Nhận biết được đặc điểm của truyện cổ tích",
            "Phân tích được nhân vật trong truyện",
            "Nêu được bài học từ truyện"
        ],
    },
    "Bài 3": {
        "ten_bai": "Vẻ đẹp quê hương",
        "linh_vuc": "Đọc hiểu",
        "the_loai": "Thơ lục bát",
        "van_ban": ["Những câu hát về quê hương"],
        "yeu_cau_can_dat": [
            "Nhận biết được thể thơ lục bát",
            "Cảm nhận được vẻ đẹp quê hương qua thơ",
            "Viết được đoạn văn cảm nhận"
        ],
    },
}

# ==============================================================
# MAPPING FUNCTION
# ==============================================================

def get_curriculum_data(subject: str, grade: int, textbook: str = "ctst"):
    """Lấy dữ liệu chương trình theo môn, lớp, bộ sách."""
    curriculum_map = {
        ("khtn", 6, "ctst"): KHTN_6_CTST,
        ("khtn", 6, "kntt"): KHTN_6_KNTT,
        ("khtn", 6, "cd"): KHTN_6_CD,
        ("khtn", 7, "ctst"): KHTN_7_CTST,
        ("khtn", 8, "ctst"): KHTN_8_CTST,
        ("khtn", 9, "ctst"): KHTN_9_CTST,
        ("nguvan", 6, "ctst"): NGUVAN_6_CTST,
    }
    
    return curriculum_map.get((subject.lower(), grade, textbook.lower()), {})


def find_lesson(subject: str, grade: int, lesson_name: str, textbook: str = "ctst"):
    """Tìm bài học theo tên."""
    data = get_curriculum_data(subject, grade, textbook)
    
    # Tìm chính xác
    for key, lesson in data.items():
        if lesson_name.lower() in key.lower() or lesson_name.lower() in lesson.get("ten_bai", "").lower():
            return lesson
    
    # Tìm gần đúng (chứa số bài)
    import re
    match = re.search(r'bài\s*(\d+)', lesson_name.lower())
    if match:
        bai_so = f"Bài {match.group(1)}"
        if bai_so in data:
            return data[bai_so]
    
    return None


def get_textbook_name(textbook: str) -> str:
    """Lấy tên đầy đủ của bộ sách."""
    names = {
        "ctst": "Chân trời sáng tạo",
        "kntt": "Kết nối tri thức với cuộc sống",
        "cd": "Cánh diều",
    }
    return names.get(textbook.lower(), "Chân trời sáng tạo")
