// ===== Product Data =====
// Export as window global for fallback
const productsDataLocal = [
    // Nhóm 1: AI & Công nghệ số
    {
        id: 1,
        title: "Ứng dụng AI trong dạy học phân môn Vật lí – Một bước chuyển mình trong giáo dục KHTN cấp THCS",
        category: "ai",
        categoryName: "AI & Công nghệ số",
        categoryIcon: "🤖",
        price: 450000,
        originalPrice: 550000,
        features: ["Vật lí", "THCS", "AI", "KHTN"]
    },
    {
        id: 2,
        title: "Ứng dụng A.I trong dạy học Vật lí 9 – Hướng đi mới nâng cao hiệu quả và hứng thú học tập cho học sinh trường THCS A",
        category: "ai",
        categoryName: "AI & Công nghệ số",
        categoryIcon: "🤖",
        price: 420000,
        originalPrice: 520000,
        features: ["Vật lí 9", "AI", "Hiệu quả học tập"]
    },
    {
        id: 3,
        title: "Trí tuệ nhân tạo – Cánh tay đắc lực nâng tầm chất lượng dạy học môn KHTN 6 (Phần Vật lý) ở trường THCS",
        category: "ai",
        categoryName: "AI & Công nghệ số",
        categoryIcon: "🤖",
        price: 400000,
        originalPrice: 500000,
        features: ["KHTN 6", "Vật lý", "Trí tuệ nhân tạo"]
    },
    {
        id: 4,
        title: "Ứng dụng trí tuệ nhân tạo kết hợp giáo dục STEM trong dạy học chủ đề Áp suất – KHTN 8 nhằm phát huy năng lực sáng tạo của học sinh",
        category: "ai",
        categoryName: "AI & Công nghệ số",
        categoryIcon: "🤖",
        price: 480000,
        originalPrice: 600000,
        features: ["STEM", "Áp suất", "KHTN 8", "Sáng tạo"]
    },
    {
        id: 5,
        title: "Ứng dụng trí tuệ nhân tạo Gemini Chatbot hỗ trợ đổi mới dạy học KHTN 9 theo hướng phát triển năng lực",
        category: "ai",
        categoryName: "AI & Công nghệ số",
        categoryIcon: "🤖",
        price: 520000,
        originalPrice: 650000,
        features: ["Gemini", "Chatbot", "KHTN 9", "Năng lực"]
    },
    {
        id: 6,
        title: "Tích hợp trí tuệ nhân tạo (AI) trong giảng dạy môn KHTN 6 (Vật lí) nhằm phát triển năng lực tự học và hứng thú của học sinh",
        category: "ai",
        categoryName: "AI & Công nghệ số",
        categoryIcon: "🤖",
        price: 430000,
        originalPrice: 530000,
        features: ["KHTN 6", "Tự học", "Hứng thú"]
    },
    {
        id: 7,
        title: "Azota – Trợ thủ đắc lực trong đổi mới kiểm tra đánh giá môn KHTN 7 (Phần Vật lý) ở trường THCS A",
        category: "ai",
        categoryName: "AI & Công nghệ số",
        categoryIcon: "🤖",
        price: 380000,
        originalPrice: 480000,
        features: ["Azota", "KHTN 7", "Kiểm tra đánh giá"]
    },
    {
        id: 8,
        title: "Sử dụng phần mềm Phyphox hướng dẫn học sinh tìm hiểu nội dung bài học trong chủ đề Âm thanh môn KHTN 7",
        category: "ai",
        categoryName: "AI & Công nghệ số",
        categoryIcon: "🤖",
        price: 360000,
        originalPrice: 450000,
        features: ["Phyphox", "Âm thanh", "KHTN 7"]
    },

    // Nhóm 2: STEM & Dự án
    {
        id: 9,
        title: "Ứng dụng mô hình STEM phát triển tư duy thực hành – Khám phá trong dạy học Vật lý lớp 9",
        category: "stem",
        categoryName: "STEM & Dự án",
        categoryIcon: "🔬",
        price: 460000,
        originalPrice: 580000,
        features: ["STEM", "Vật lý 9", "Thực hành"]
    },
    {
        id: 10,
        title: "Khi học sinh thành nhà khoa học nhỏ – Giải pháp tăng cường thực hành môn KHTN (Phần Vật lí) lớp 6",
        category: "stem",
        categoryName: "STEM & Dự án",
        categoryIcon: "🔬",
        price: 390000,
        originalPrice: 490000,
        features: ["KHTN 6", "Thực hành", "Khám phá"]
    },
    {
        id: 11,
        title: "Khơi nguồn đam mê khám phá khoa học qua các dự án STEM trong môn KHTN 6 (Phân môn Vật lí)",
        category: "stem",
        categoryName: "STEM & Dự án",
        categoryIcon: "🔬",
        price: 440000,
        originalPrice: 550000,
        features: ["Dự án STEM", "KHTN 6", "Đam mê"]
    },
    {
        id: 12,
        title: "Khơi dậy đam mê khoa học – Kết nối trò chơi và tri thức trong môn KHTN 6 (Phân môn Lý)",
        category: "stem",
        categoryName: "STEM & Dự án",
        categoryIcon: "🔬",
        price: 370000,
        originalPrice: 470000,
        features: ["Trò chơi", "KHTN 6", "Tri thức"]
    },

    // Nhóm 3: Phương pháp dạy học
    {
        id: 13,
        title: "Phát triển năng lực vận dụng kiến thức vào giải bài tập Vật lí qua chủ đề Đòn bẩy trong chương trình KHTN 8",
        category: "method",
        categoryName: "Phương pháp dạy học",
        categoryIcon: "📝",
        price: 410000,
        originalPrice: 510000,
        features: ["Đòn bẩy", "KHTN 8", "Bài tập"]
    },
    {
        id: 14,
        title: "Kích thích tư duy chủ động, sáng tạo - Tối ưu hóa công cụ giảng dạy chủ đề Năng lượng trong môn KHTN 8",
        category: "method",
        categoryName: "Phương pháp dạy học",
        categoryIcon: "📝",
        price: 430000,
        originalPrice: 540000,
        features: ["Năng lượng", "KHTN 8", "Tư duy sáng tạo"]
    },
    {
        id: 15,
        title: "Sơ đồ tư duy – Công cụ phát huy năng lực học sinh trong dạy học môn Khoa học tự nhiên 8 (Phân môn Vật lý)",
        category: "method",
        categoryName: "Phương pháp dạy học",
        categoryIcon: "📝",
        price: 350000,
        originalPrice: 440000,
        features: ["Sơ đồ tư duy", "KHTN 8", "Năng lực"]
    },
    {
        id: 16,
        title: "Ứng dụng kĩ thuật dạy học trạm nhằm phát triển năng lực tự học, nâng cao chất lượng học tập môn KHTN 9 – Phần Vật lí",
        category: "method",
        categoryName: "Phương pháp dạy học",
        categoryIcon: "📝",
        price: 470000,
        originalPrice: 590000,
        features: ["Dạy học trạm", "KHTN 9", "Tự học"]
    },
    {
        id: 17,
        title: "Tích hợp công nghệ và sáng tạo các phương pháp dạy học vào môn KHTN 8 nhằm tăng hứng thú và hiệu quả học tập",
        category: "method",
        categoryName: "Phương pháp dạy học",
        categoryIcon: "📝",
        price: 420000,
        originalPrice: 520000,
        features: ["Công nghệ", "KHTN 8", "Hiệu quả"]
    },
    {
        id: 18,
        title: "Đổi mới dạy học KHTN 8 theo định hướng phát triển năng lực tư duy phản biện qua bài Khối lượng riêng và Áp suất",
        category: "method",
        categoryName: "Phương pháp dạy học",
        categoryIcon: "📝",
        price: 400000,
        originalPrice: 500000,
        features: ["Tư duy phản biện", "KHTN 8", "Áp suất"]
    },

    // Nhóm 4: Kỹ năng & Thí nghiệm
    {
        id: 19,
        title: "Lồng ghép nội dung giáo dục kỹ năng sống trong dạy học Vật lí nhằm nâng cao hiệu quả giáo dục toàn diện cho học sinh THCS",
        category: "skill",
        categoryName: "Kỹ năng & Thí nghiệm",
        categoryIcon: "🧪",
        price: 450000,
        originalPrice: 560000,
        features: ["Kỹ năng sống", "Vật lí", "Giáo dục toàn diện"]
    },
    {
        id: 20,
        title: "Tích hợp giáo dục kỹ năng sống trong mạch Năng lượng và sự biến đổi môn KHTN 6 cho học sinh trường THCS A",
        category: "skill",
        categoryName: "Kỹ năng & Thí nghiệm",
        categoryIcon: "🧪",
        price: 380000,
        originalPrice: 480000,
        features: ["Năng lượng", "KHTN 6", "Kỹ năng sống"]
    },
    {
        id: 21,
        title: "Thí nghiệm vật lí – Chìa khóa khơi dậy hứng thú và tư duy khoa học trong môn KHTN 8, 9 ở trường THCS A",
        category: "skill",
        categoryName: "Kỹ năng & Thí nghiệm",
        categoryIcon: "🧪",
        price: 490000,
        originalPrice: 620000,
        features: ["Thí nghiệm", "KHTN 8-9", "Tư duy khoa học"]
    }
];

// Export to window for fallback access
window.productsDataLocal = productsDataLocal;

// Category info
const categoriesInfo = {
    all: { name: "Tất cả", icon: "🌟" },
    ai: { name: "AI & Công nghệ số", icon: "🤖" },
    stem: { name: "STEM & Dự án", icon: "🔬" },
    method: { name: "Phương pháp dạy học", icon: "📝" },
    skill: { name: "Kỹ năng & Thí nghiệm", icon: "🧪" }
};
