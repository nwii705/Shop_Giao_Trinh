const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Phục vụ file PDF tĩnh
app.use('/docs', express.static(path.join(__dirname, 'public/docs')));

// Phục vụ Frontend
app.use(express.static(path.join(__dirname, '../frontend')));

// ==================== IN-MEMORY DATABASE ====================
// Dữ liệu lưu trong RAM (sẽ mất khi restart server)
let products = require('./seedData').map((p, index) => ({
    ...p,
    _id: `prod_${index + 1}`,
    id: `prod_${index + 1}`
}));

// ==================== API ROUTES ====================

// 1. Lấy danh sách sản phẩm (chỉ lấy available)
app.get('/api/products', (req, res) => {
    const { category } = req.query;
    let result = products.filter(p => p.status === 'available');
    
    if (category && category !== 'all') {
        result = result.filter(p => p.category === category);
    }
    
    res.json(result);
});

// 2. Lấy thống kê
app.get('/api/stats', (req, res) => {
    const available = products.filter(p => p.status === 'available').length;
    const sold = products.filter(p => p.status === 'sold').length;
    
    const categories = {
        ai: products.filter(p => p.status === 'available' && p.category === 'ai').length,
        stem: products.filter(p => p.status === 'available' && p.category === 'stem').length,
        method: products.filter(p => p.status === 'available' && p.category === 'method').length,
        skill: products.filter(p => p.status === 'available' && p.category === 'skill').length
    };
    
    res.json({ available, sold, categories });
});

// 3. Tìm kiếm sản phẩm
app.get('/api/search', (req, res) => {
    const { q } = req.query;
    if (!q) return res.json([]);
    
    const searchTerm = q.toLowerCase();
    const result = products.filter(p => {
        if (p.status !== 'available') return false;
        
        const titleMatch = p.title.toLowerCase().includes(searchTerm);
        const categoryMatch = p.categoryName.toLowerCase().includes(searchTerm);
        const featuresMatch = p.features.some(f => f.toLowerCase().includes(searchTerm));
        
        return titleMatch || categoryMatch || featuresMatch;
    });
    
    res.json(result);
});

// 4. Mua hàng
app.post('/api/buy', (req, res) => {
    const { productId } = req.body;

    const productIndex = products.findIndex(p => p._id === productId || p.id === productId);
    
    if (productIndex === -1) {
        return res.status(404).json({ error: "Không tìm thấy sản phẩm" });
    }

    const product = products[productIndex];
    products[productIndex].status = 'sold';

    console.log(`💰 Đã bán: ${product.title}`);

    // Kiểm tra kho
    const category = product.category;
    const count = products.filter(p => p.category === category && p.status === 'available').length;
    console.log(`📦 Kho mục ${category} còn: ${count} cuốn.`);

    if (count < 3) {
        console.log("⚡ Kho sắp hết! (Cần kết nối MongoDB + Gemini để tự động bổ sung)");
    }

    res.json({ 
        success: true, 
        message: "Mua hàng thành công!",
        fileUrl: product.fileUrl 
    });
});

// 5. Reset tất cả sản phẩm
app.post('/api/reset', (req, res) => {
    products.forEach(p => p.status = 'available');
    console.log('🔄 Đã reset tất cả sản phẩm');
    res.json({ success: true, message: "Đã khôi phục tất cả sản phẩm" });
});

// 6. Seed data (không cần vì đã load từ seedData.js)
app.post('/api/seed', (req, res) => {
    res.json({ message: "Dữ liệu đã được load từ seedData.js", count: products.length });
});

// Catch-all route để phục vụ frontend
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log('');
    console.log('========================================');
    console.log('   🎓 EduShop Server - LOCAL MODE');
    console.log('========================================');
    console.log(`   🚀 Server: http://localhost:${PORT}`);
    console.log(`   📂 Frontend: http://localhost:${PORT}`);
    console.log(`   📡 API: http://localhost:${PORT}/api`);
    console.log('');
    console.log('   ⚠️  Đang chạy chế độ IN-MEMORY');
    console.log('   📝 Dữ liệu sẽ reset khi restart server');
    console.log('========================================');
    console.log('');
    console.log(`   📦 Đã load ${products.length} sản phẩm`);
    console.log('');
});
