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

// Catch-all
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/index.html'));
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
