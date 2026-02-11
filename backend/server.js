const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const path = require('path');
const { spawn } = require('child_process');
require('dotenv').config({ path: path.join(__dirname, '.env') });

// Deep Research Agent
const DeepResearchAgent = require('./deep-research');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Phục vụ file PDF tĩnh
app.use('/docs', express.static(path.join(__dirname, 'public/docs')));

// Phục vụ Frontend
app.use(express.static(path.join(__dirname, '../frontend')));

// ==================== DATABASE SETUP ====================
let useLocalData = false;
let localProducts = [];

// Mongoose Model
const ProductSchema = new mongoose.Schema({
    title: String,
    category: String,
    categoryName: String,
    categoryIcon: String,
    price: Number,
    originalPrice: Number,
    features: [String],
    status: { type: String, default: 'available' },
    fileUrl: String,
    createdAt: { type: Date, default: Date.now }
});
ProductSchema.virtual('id').get(function() { return this._id.toHexString(); });
ProductSchema.set('toJSON', { virtuals: true });
const Product = mongoose.model('Product', ProductSchema);

// Order Model - Đơn hàng
const OrderSchema = new mongoose.Schema({
    id: { type: String, required: true, unique: true }, // EDU + timestamp
    productId: { type: String, required: true },
    productTitle: String,
    productPrice: Number,
    buyerName: { type: String, required: true },
    buyerEmail: { type: String, required: true },
    buyerPhone: { type: String, required: true },
    buyerNote: String,
    status: { type: String, default: 'pending', enum: ['pending', 'confirmed', 'rejected', 'expired'] },
    confirmedAt: Date,
    createdAt: { type: Date, default: Date.now }
});
const Order = mongoose.model('Order', OrderSchema);

// Kết nối MongoDB
const MONGO_URI = process.env.MONGO_URI || '';

async function connectDB() {
    if (!MONGO_URI || MONGO_URI.includes('username:password')) {
        console.log('⚠️ Chưa cấu hình MongoDB, sử dụng dữ liệu local');
        useLocalData = true;
        loadLocalData();
        return;
    }
    
    console.log('📡 Đang kết nối MongoDB Atlas...');
    
    try {
        await mongoose.connect(MONGO_URI, {
            serverSelectionTimeoutMS: 15000,
            socketTimeoutMS: 30000,
        });
        console.log('🔥 Connected to MongoDB Atlas!');
        useLocalData = false;
    } catch (err) {
        console.error('❌ MongoDB error:', err.message);
        console.log('⚠️ Chuyển sang chế độ LOCAL DATA');
        useLocalData = true;
        loadLocalData();
    }
}

function loadLocalData() {
    try {
        const seedData = require('./seedData');
        localProducts = seedData.map((p, index) => ({
            ...p,
            _id: `local_${index + 1}`,
            id: `local_${index + 1}`,
            status: 'available'
        }));
        console.log(`📦 Đã load ${localProducts.length} sản phẩm từ local`);
    } catch (e) {
        console.error('Lỗi load local data:', e);
        localProducts = [];
    }
}

// ==================== API ROUTES ====================

// ========== DEEP RESEARCH API ==========
// POST /api/deep-research - Thực hiện nghiên cứu sâu cho SKKN
// Sử dụng Perplexity Sonar qua OpenRouter để search internet
app.post('/api/deep-research', async (req, res) => {
    try {
        const { topic, role, subject, level, geminiKey, openRouterKey, tavilyKey } = req.body;
        
        // Validate input
        if (!topic) {
            return res.status(400).json({ error: 'Thiếu tên đề tài' });
        }
        
        // Hỗ trợ cả geminiKey (cũ) và openRouterKey (mới)
        const apiKey = openRouterKey || geminiKey;
        if (!apiKey) {
            return res.status(400).json({ error: 'Thiếu OpenRouter API Key' });
        }
        
        console.log(`🔬 Deep Research Request: "${topic}"`);
        console.log(`   Using: Perplexity Sonar + Gemini via OpenRouter`);
        
        // Khởi tạo agent với OpenRouter key
        const agent = new DeepResearchAgent(apiKey, tavilyKey || null);
        
        // Thực hiện nghiên cứu
        const result = await agent.performDeepResearch(
            topic,
            role || 'Giáo viên bộ môn',
            subject || 'Giáo dục',
            level || 'THCS'
        );
        
        if (result.success) {
            console.log(`✅ Deep Research completed in ${result.duration}s`);
            res.json(result);
        } else {
            console.log(`❌ Deep Research failed: ${result.error}`);
            res.status(500).json({ error: result.error, logs: result.logs });
        }
        
    } catch (error) {
        console.error('Deep Research Error:', error);
        res.status(500).json({ error: error.message });
    }
});

// Helper: Get products based on mode
async function getProducts(query = {}) {
    if (useLocalData) {
        let result = [...localProducts];
        if (query.status) result = result.filter(p => p.status === query.status);
        if (query.category) result = result.filter(p => p.category === query.category);
        return result;
    }
    return await Product.find(query).sort({ createdAt: -1 });
}

// 1. Lấy danh sách sản phẩm
app.get('/api/products', async (req, res) => {
    try {
        const { category } = req.query;
        let query = { status: 'available' };
        if (category && category !== 'all') {
            query.category = category;
        }
        
        const products = await getProducts(query);
        res.json(products);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 1.5 Tạo sản phẩm mới (AI Generator upload)
app.post('/api/products', async (req, res) => {
    try {
        const { title, category, categoryName, categoryIcon, price, originalPrice, features, status } = req.body;
        
        if (!title || !category || !price) {
            return res.status(400).json({ error: 'Thiếu thông tin: title, category, price' });
        }
        
        if (useLocalData) {
            // Local mode
            const newProduct = {
                _id: Date.now().toString(),
                title,
                category,
                categoryName: categoryName || category,
                categoryIcon: categoryIcon || '📄',
                price: parseInt(price),
                originalPrice: originalPrice || Math.round(price * 1.25),
                features: features || ['SKKN', 'AI Generated', 'Word'],
                status: status || 'available',
                createdAt: new Date()
            };
            localProducts.unshift(newProduct);
            return res.json({ success: true, product: newProduct });
        }
        
        // MongoDB mode
        const newProduct = new Product({
            title,
            category,
            categoryName: categoryName || category,
            categoryIcon: categoryIcon || '📄',
            price: parseInt(price),
            originalPrice: originalPrice || Math.round(price * 1.25),
            features: features || ['SKKN', 'AI Generated', 'Word'],
            status: status || 'available'
        });
        
        await newProduct.save();
        res.json({ success: true, product: newProduct });
    } catch (error) {
        console.error('Error creating product:', error);
        res.status(500).json({ error: error.message });
    }
});

// 2. Lấy thống kê
app.get('/api/stats', async (req, res) => {
    try {
        if (useLocalData) {
            const available = localProducts.filter(p => p.status === 'available').length;
            const sold = localProducts.filter(p => p.status === 'sold').length;
            const categories = {
                ai: localProducts.filter(p => p.status === 'available' && p.category === 'ai').length,
                stem: localProducts.filter(p => p.status === 'available' && p.category === 'stem').length,
                method: localProducts.filter(p => p.status === 'available' && p.category === 'method').length,
                skill: localProducts.filter(p => p.status === 'available' && p.category === 'skill').length
            };
            return res.json({ available, sold, categories, mode: 'local' });
        }
        
        const available = await Product.countDocuments({ status: 'available' });
        const sold = await Product.countDocuments({ status: 'sold' });
        const categories = {
            ai: await Product.countDocuments({ status: 'available', category: 'ai' }),
            stem: await Product.countDocuments({ status: 'available', category: 'stem' }),
            method: await Product.countDocuments({ status: 'available', category: 'method' }),
            skill: await Product.countDocuments({ status: 'available', category: 'skill' })
        };
        
        res.json({ available, sold, categories, mode: 'mongodb' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 3. Tìm kiếm sản phẩm
app.get('/api/search', async (req, res) => {
    try {
        const { q } = req.query;
        if (!q) return res.json([]);
        
        if (useLocalData) {
            const searchTerm = q.toLowerCase();
            const results = localProducts.filter(p => {
                if (p.status !== 'available') return false;
                const titleMatch = p.title.toLowerCase().includes(searchTerm);
                const categoryMatch = p.categoryName.toLowerCase().includes(searchTerm);
                const featuresMatch = p.features.some(f => f.toLowerCase().includes(searchTerm));
                return titleMatch || categoryMatch || featuresMatch;
            });
            return res.json(results);
        }
        
        const products = await Product.find({
            status: 'available',
            $or: [
                { title: { $regex: q, $options: 'i' } },
                { categoryName: { $regex: q, $options: 'i' } },
                { features: { $in: [new RegExp(q, 'i')] } }
            ]
        }).sort({ createdAt: -1 });
        
        res.json(products);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 4. Mua hàng & Kích hoạt Refill
app.post('/api/buy', async (req, res) => {
    const { productId } = req.body;

    try {
        let product;
        let category;
        let count;
        
        if (useLocalData) {
            const idx = localProducts.findIndex(p => p._id === productId || p.id === productId);
            if (idx === -1) return res.status(404).json({ error: "Không tìm thấy" });
            
            product = localProducts[idx];
            localProducts[idx].status = 'sold';
            category = product.category;
            count = localProducts.filter(p => p.category === category && p.status === 'available').length;
        } else {
            product = await Product.findByIdAndUpdate(productId, { status: 'sold' }, { new: true });
            if (!product) return res.status(404).json({ error: "Không tìm thấy" });
            
            category = product.category;
            count = await Product.countDocuments({ category, status: 'available' });
        }

        console.log(`💰 Đã bán: ${product.title.substring(0, 50)}...`);
        console.log(`📦 Kho [${category}] còn: ${count} cuốn`);

        // REFILL: Nếu kho < 3 thì gọi AI Worker
        if (count < 3 && !useLocalData) {
            console.log("⚡ Kho sắp hết! Gọi AI Worker...");
            
            const pythonPath = 'python';
            const scriptPath = path.join(__dirname, '../ai_worker/generator.py');
            
            const pythonProcess = spawn(pythonPath, [scriptPath, category, '2']);
            
            pythonProcess.stdout.on('data', (data) => console.log(`🤖 ${data}`));
            pythonProcess.stderr.on('data', (data) => console.error(`❌ ${data}`));
            pythonProcess.on('close', (code) => console.log(`✅ AI Worker done: ${code}`));
        }

        res.json({ 
            success: true, 
            message: "Mua hàng thành công!",
            fileUrl: product.fileUrl,
            remaining: count
        });
        
    } catch (error) {
        console.error('Buy error:', error);
        res.status(500).json({ error: error.message });
    }
});

// 5. Reset tất cả
app.post('/api/reset', async (req, res) => {
    try {
        if (useLocalData) {
            localProducts.forEach(p => p.status = 'available');
        } else {
            await Product.updateMany({ status: 'sold' }, { status: 'available' });
        }
        console.log('🔄 Đã reset tất cả sản phẩm');
        res.json({ success: true, message: "Đã khôi phục tất cả" });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 6. Xóa tất cả sản phẩm (để test auto-refill)
app.delete('/api/products/all', async (req, res) => {
    try {
        if (useLocalData) {
            return res.json({ message: "Đang dùng local data" });
        }
        
        const result = await Product.deleteMany({});
        console.log(`🗑️ Đã xóa ${result.deletedCount} sản phẩm`);
        res.json({ success: true, deleted: result.deletedCount });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 6b. Xóa một sản phẩm cụ thể
app.delete('/api/products/:id', async (req, res) => {
    try {
        const { id } = req.params;
        
        if (useLocalData) {
            const index = localProducts.findIndex(p => p.id === id || p._id === id);
            if (index === -1) {
                return res.status(404).json({ error: 'Sản phẩm không tồn tại' });
            }
            localProducts.splice(index, 1);
            return res.json({ success: true, message: 'Đã xóa sản phẩm' });
        }
        
        const result = await Product.findByIdAndDelete(id);
        if (!result) {
            return res.status(404).json({ error: 'Sản phẩm không tồn tại' });
        }
        console.log(`🗑️ Đã xóa sản phẩm: ${result.title}`);
        res.json({ success: true, message: 'Đã xóa sản phẩm' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 7. Seed data
app.post('/api/seed', async (req, res) => {
    try {
        if (useLocalData) {
            return res.json({ message: "Đang dùng local data", count: localProducts.length });
        }
        
        const count = await Product.countDocuments();
        if (count > 0) {
            return res.json({ message: "Database đã có dữ liệu", count });
        }
        
        const seedData = require('./seedData');
        await Product.insertMany(seedData);
        
        console.log('🌱 Đã seed data!');
        res.json({ success: true, count: seedData.length });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// ==================== ORDER MANAGEMENT API ====================
// Local orders storage (for fallback)
let localOrders = [];

// 8. Tạo đơn hàng mới
app.post('/api/orders', async (req, res) => {
    try {
        const { id, productId, productTitle, productPrice, buyerName, buyerEmail, buyerPhone, buyerNote } = req.body;
        
        if (!id || !productId || !buyerName || !buyerEmail || !buyerPhone) {
            return res.status(400).json({ error: 'Thiếu thông tin đơn hàng' });
        }
        
        const orderData = {
            id,
            productId,
            productTitle,
            productPrice,
            buyerName,
            buyerEmail,
            buyerPhone,
            buyerNote: buyerNote || '',
            status: 'pending',
            createdAt: new Date()
        };
        
        if (useLocalData) {
            localOrders.push(orderData);
            console.log(`📝 [LOCAL] Đơn hàng mới: ${id} - ${productTitle}`);
            return res.json({ success: true, order: orderData });
        }
        
        const order = new Order(orderData);
        await order.save();
        
        console.log(`📝 Đơn hàng mới: ${id} - ${productTitle}`);
        console.log(`   👤 ${buyerName} | ${buyerEmail} | ${buyerPhone}`);
        
        res.json({ success: true, order });
    } catch (error) {
        console.error('Lỗi tạo đơn hàng:', error);
        res.status(500).json({ error: error.message });
    }
});

// 9. Lấy danh sách đơn hàng (admin)
app.get('/api/orders', async (req, res) => {
    try {
        const { status } = req.query;
        
        if (useLocalData) {
            let orders = [...localOrders];
            if (status) orders = orders.filter(o => o.status === status);
            return res.json(orders.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt)));
        }
        
        let query = {};
        if (status) query.status = status;
        
        const orders = await Order.find(query).sort({ createdAt: -1 });
        res.json(orders);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 10. Xác nhận đơn hàng (admin)
app.put('/api/orders/:id/confirm', async (req, res) => {
    try {
        const { id } = req.params;
        
        if (useLocalData) {
            const idx = localOrders.findIndex(o => o.id === id);
            if (idx === -1) return res.status(404).json({ error: 'Không tìm thấy đơn hàng' });
            
            localOrders[idx].status = 'confirmed';
            localOrders[idx].confirmedAt = new Date();
            console.log(`✅ [LOCAL] Đã xác nhận đơn: ${id}`);
            return res.json({ success: true, order: localOrders[idx] });
        }
        
        const order = await Order.findOneAndUpdate(
            { id },
            { status: 'confirmed', confirmedAt: new Date() },
            { new: true }
        );
        
        if (!order) {
            return res.status(404).json({ error: 'Không tìm thấy đơn hàng' });
        }
        
        console.log(`✅ Đã xác nhận đơn hàng: ${id} - ${order.productTitle}`);
        res.json({ success: true, order });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 11. Từ chối đơn hàng (admin)
app.put('/api/orders/:id/reject', async (req, res) => {
    try {
        const { id } = req.params;
        
        if (useLocalData) {
            const idx = localOrders.findIndex(o => o.id === id);
            if (idx === -1) return res.status(404).json({ error: 'Không tìm thấy đơn hàng' });
            
            localOrders[idx].status = 'rejected';
            console.log(`❌ [LOCAL] Đã từ chối đơn: ${id}`);
            return res.json({ success: true, order: localOrders[idx] });
        }
        
        const order = await Order.findOneAndUpdate(
            { id },
            { status: 'rejected' },
            { new: true }
        );
        
        if (!order) {
            return res.status(404).json({ error: 'Không tìm thấy đơn hàng' });
        }
        
        console.log(`❌ Đã từ chối đơn hàng: ${id} - ${order.productTitle}`);
        res.json({ success: true, order });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 12. Kiểm tra và hết hạn đơn hàng sau 24h
async function expireOldOrders() {
    const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
    
    if (useLocalData) {
        localOrders = localOrders.map(o => {
            if (o.status === 'pending' && new Date(o.createdAt) < oneDayAgo) {
                console.log(`⏰ [LOCAL] Đơn hết hạn: ${o.id}`);
                return { ...o, status: 'expired' };
            }
            return o;
        });
        return;
    }
    
    try {
        const result = await Order.updateMany(
            { status: 'pending', createdAt: { $lt: oneDayAgo } },
            { status: 'expired' }
        );
        
        if (result.modifiedCount > 0) {
            console.log(`⏰ Đã hết hạn ${result.modifiedCount} đơn hàng`);
        }
    } catch (error) {
        console.error('Lỗi expire orders:', error);
    }
}

// Chạy kiểm tra mỗi giờ
setInterval(expireOldOrders, 60 * 60 * 1000);

// 7. Tạo AI content
app.post('/api/generate', async (req, res) => {
    const { category, quantity } = req.body;
    
    if (useLocalData) {
        return res.json({ error: "Cần kết nối MongoDB để sử dụng AI Generator" });
    }
    
    try {
        console.log(`🚀 Tạo ${quantity || 1} sản phẩm [${category}]...`);
        
        const pythonPath = 'python';
        const scriptPath = path.join(__dirname, '../ai_worker/generator.py');
        
        const pythonProcess = spawn(pythonPath, [scriptPath, category || 'ai', String(quantity || 1)]);
        
        let output = '';
        pythonProcess.stdout.on('data', (data) => { output += data; console.log(`🤖 ${data}`); });
        pythonProcess.stderr.on('data', (data) => console.error(`❌ ${data}`));
        
        pythonProcess.on('close', (code) => {
            res.json({ success: code === 0, output });
        });
        
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 8. Health check
app.get('/api/health', (req, res) => {
    res.json({
        status: 'ok',
        mode: useLocalData ? 'local' : 'mongodb',
        mongoConnected: mongoose.connection.readyState === 1
    });
});

// Serve known pages
const knownPages = ['index.html', 'admin.html', 'generator.html', 'profile.html', 'history.html', '404.html'];

app.get('*', (req, res) => {
    const requestedPath = req.path;
    
    // If it's a known page or root, serve it
    if (requestedPath === '/' || requestedPath === '/index.html') {
        return res.sendFile(path.join(__dirname, '../frontend/index.html'));
    }
    
    // Check if file exists in frontend folder
    const filePath = path.join(__dirname, '../frontend', requestedPath);
    const fs = require('fs');
    
    if (fs.existsSync(filePath)) {
        return res.sendFile(filePath);
    }
    
    // Otherwise serve 404 page
    res.status(404).sendFile(path.join(__dirname, '../frontend/404.html'));
});

// ==================== AUTO REFILL ====================
async function autoRefillCheck() {
    if (useLocalData) {
        console.log('⚠️ Đang dùng local data, bỏ qua auto-refill');
        return;
    }
    
    console.log('🔍 Kiểm tra kho hàng...');
    
    const categories = ['ai', 'stem', 'method', 'skill'];
    const MIN_STOCK = 3;
    const REFILL_AMOUNT = 3;
    
    for (const category of categories) {
        const count = await Product.countDocuments({ category, status: 'available' });
        console.log(`   📦 [${category}]: ${count} sản phẩm`);
        
        if (count < MIN_STOCK) {
            const needed = REFILL_AMOUNT;
            console.log(`   ⚡ Kho [${category}] thiếu! Đang gọi AI tạo ${needed} sản phẩm...`);
            
            const pythonPath = 'python';
            const scriptPath = path.join(__dirname, '../ai_worker/generator.py');
            
            try {
                const pythonProcess = spawn(pythonPath, [scriptPath, category, String(needed)]);
                
                pythonProcess.stdout.on('data', (data) => console.log(`🤖 ${data.toString().trim()}`));
                pythonProcess.stderr.on('data', (data) => console.error(`❌ ${data.toString().trim()}`));
                pythonProcess.on('close', (code) => {
                    if (code === 0) {
                        console.log(`✅ Đã tạo xong ${needed} sản phẩm [${category}]`);
                    }
                });
                
                // Đợi 5 giây giữa các category để không quá tải API
                await new Promise(resolve => setTimeout(resolve, 5000));
            } catch (err) {
                console.error(`❌ Lỗi gọi AI Worker [${category}]:`, err.message);
            }
        }
    }
    
    console.log('✅ Hoàn tất kiểm tra kho!');
}

// ==================== START SERVER ====================
const PORT = process.env.PORT || 5000;

async function start() {
    await connectDB();
    
    app.listen(PORT, () => {
        console.log('');
        console.log('========================================');
        console.log('   🎓 EduShop Server');
        console.log('========================================');
        console.log(`   🚀 http://localhost:5000`);
        console.log(`   📡 Mode: ${useLocalData ? 'LOCAL DATA' : 'MONGODB'}`);
        console.log('========================================');
        console.log('');
        
        // Auto-refill sau khi server khởi động
        if (!useLocalData) {
            setTimeout(() => autoRefillCheck(), 2000);
        }
    });
}

start();
