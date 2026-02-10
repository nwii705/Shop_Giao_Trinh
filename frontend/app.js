// ===== App State =====
let productsData = []; // Dữ liệu từ API
let soldProducts = []; // Không dùng localStorage nữa, dùng status từ DB
let currentFilter = 'all';
let selectedProduct = null;

// API Base URL - Auto detect production or localhost
const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000/api' 
    : `${window.location.origin}/api`;

// ===== DOM Elements =====
const productsGrid = document.getElementById('productsGrid');
const emptyState = document.getElementById('emptyState');
const modalOverlay = document.getElementById('modalOverlay');
const modalClose = document.getElementById('modalClose');
const cancelBtn = document.getElementById('cancelBtn');
const confirmBtn = document.getElementById('confirmBtn');
const successToast = document.getElementById('successToast');
const resetBtn = document.getElementById('resetBtn');
const categoryTabs = document.getElementById('categoryTabs');

// Search elements
const searchBtn = document.getElementById('searchBtn');
const searchOverlay = document.getElementById('searchOverlay');
const searchBox = document.getElementById('searchBox');
const searchClose = document.getElementById('searchClose');
const searchInput = document.getElementById('searchInput');
const searchClear = document.getElementById('searchClear');
const searchResults = document.getElementById('searchResults');

// ===== Initialize =====
document.addEventListener('DOMContentLoaded', () => {
    createParticles();
    fetchProducts();
    setupEventListeners();
});

// ===== Fetch Products from API =====
async function fetchProducts() {
    try {
        showLoading();
        
        const response = await fetch(`${API_URL}/products`);
        if (!response.ok) throw new Error('Network error');
        
        productsData = await response.json();
        
        // Map _id thành id để tương thích code cũ
        productsData = productsData.map(p => ({
            ...p,
            id: p._id
        }));
        
        await fetchStats();
        renderProducts();
        
    } catch (error) {
        console.error('Lỗi tải dữ liệu:', error);
        // Fallback: thử dùng data local nếu có
        if (typeof window.productsDataLocal !== 'undefined') {
            productsData = window.productsDataLocal;
            renderProducts();
        } else {
            showError('Không thể kết nối server. Vui lòng kiểm tra backend.');
        }
    }
}

// ===== Fetch Stats =====
async function fetchStats() {
    try {
        const response = await fetch(`${API_URL}/stats`);
        if (!response.ok) return;
        
        const stats = await response.json();
        
        document.getElementById('totalProducts').textContent = stats.available;
        document.getElementById('soldProducts').textContent = stats.sold;
        
        // Update category counts
        document.getElementById('countAll').textContent = stats.available;
        document.getElementById('countAi').textContent = stats.categories.ai || 0;
        document.getElementById('countStem').textContent = stats.categories.stem || 0;
        document.getElementById('countMethod').textContent = stats.categories.method || 0;
        document.getElementById('countSkill').textContent = stats.categories.skill || 0;
        
    } catch (error) {
        console.error('Lỗi tải stats:', error);
    }
}

// ===== Show Loading =====
function showLoading() {
    productsGrid.innerHTML = `
        <div class="loading-state">
            <div class="loading-spinner"></div>
            <p>Đang tải dữ liệu...</p>
        </div>
    `;
}

// ===== Show Error =====
function showError(message) {
    productsGrid.innerHTML = `
        <div class="error-state">
            <div class="error-icon">⚠️</div>
            <h3>Có lỗi xảy ra</h3>
            <p>${message}</p>
            <button class="btn-primary" onclick="fetchProducts()">Thử lại</button>
        </div>
    `;
}

// ===== Particle Effect =====
function createParticles() {
    const particlesContainer = document.getElementById('particles');
    const particleCount = 50;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 15 + 's';
        particle.style.animationDuration = (15 + Math.random() * 10) + 's';
        
        const colors = ['#6366f1', '#ec4899', '#14b8a6', '#f59e0b'];
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];
        
        particlesContainer.appendChild(particle);
    }
}

// ===== Render Products =====
function renderProducts() {
    const filteredProducts = currentFilter === 'all' 
        ? productsData 
        : productsData.filter(p => p.category === currentFilter);

    if (filteredProducts.length === 0) {
        productsGrid.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }

    emptyState.style.display = 'none';
    productsGrid.innerHTML = filteredProducts.map((product, index) => `
        <div class="product-card" data-id="${product.id}" style="animation-delay: ${index * 0.1}s">
            <div class="card-header">
                <span class="card-category ${product.category}">
                    ${product.categoryIcon} ${product.categoryName}
                </span>
                <span class="card-number">${product.features?.includes('AI Generated') ? '🤖' : '#' + (index + 1)}</span>
                <h3 class="card-title">${product.title}</h3>
            </div>
            <div class="card-body">
                <div class="card-features">
                    ${(product.features || []).map(f => `<span class="feature-tag">${f}</span>`).join('')}
                </div>
            </div>
            <div class="card-footer">
                <div class="price-container">
                    <span class="price-original">${formatPrice(product.originalPrice)}</span>
                    <span class="price-current">${formatPrice(product.price)}</span>
                </div>
                <button class="btn-buy" onclick="openPaymentModalById('${product.id}')">
                    <span>🛒</span> Mua ngay
                </button>
            </div>
        </div>
    `).join('');
}

// ===== Format Price =====
function formatPrice(price) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(price);
}

// ===== Update Stats =====
function updateStats() {
    fetchStats();
}

// ===== Open Purchase Modal =====
function openPurchaseModal(productId) {
    selectedProduct = productsData.find(p => p.id === productId);
    if (!selectedProduct) return;

    const preview = document.getElementById('modalProductPreview');
    preview.innerHTML = `
        <div class="preview-category">${selectedProduct.categoryIcon} ${selectedProduct.categoryName}</div>
        <div class="preview-title">${selectedProduct.title}</div>
    `;

    document.getElementById('modalOriginalPrice').textContent = formatPrice(selectedProduct.originalPrice);
    document.getElementById('modalFinalPrice').textContent = formatPrice(selectedProduct.price);

    modalOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
}

// ===== Close Modal =====
function closeModal() {
    modalOverlay.classList.remove('active');
    document.body.style.overflow = '';
    selectedProduct = null;
}

// ===== Confirm Purchase (API) =====
async function confirmPurchase() {
    if (!selectedProduct) return;

    // Disable button và hiện loading
    confirmBtn.disabled = true;
    confirmBtn.innerHTML = '<span>⏳</span> Đang xử lý...';

    try {
        const response = await fetch(`${API_URL}/buy`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ productId: selectedProduct.id })
        });

        const result = await response.json();

        if (result.success) {
            // Lưu lịch sử mua hàng
            savePurchaseHistory(selectedProduct);
            
            // Animation card biến mất
            const card = document.querySelector(`.product-card[data-id="${selectedProduct.id}"]`);
            if (card) {
                card.classList.add('selling');
            }

            closeModal();
            showToast();

            // Tải lại danh sách sau animation
            setTimeout(() => {
                fetchProducts();
            }, 800);

            // Nếu có file PDF, có thể mở tab mới
            // if (result.fileUrl) {
            //     window.open(`http://localhost:5000${result.fileUrl}`, '_blank');
            // }
        } else {
            alert('Lỗi: ' + (result.error || 'Không thể hoàn tất giao dịch'));
        }
    } catch (error) {
        console.error('Purchase error:', error);
        alert('Lỗi kết nối server!');
    } finally {
        confirmBtn.disabled = false;
        confirmBtn.innerHTML = '<span>💳</span> Xác nhận mua';
    }
}

// ===== Save Purchase History =====
function savePurchaseHistory(product) {
    const purchases = JSON.parse(localStorage.getItem('purchaseHistory') || '[]');
    purchases.unshift({
        id: product.id,
        title: product.title,
        category: product.categoryName || product.category,
        price: product.price,
        date: new Date().toLocaleDateString('vi-VN')
    });
    localStorage.setItem('purchaseHistory', JSON.stringify(purchases));
}

// ===== Show Toast =====
function showToast() {
    successToast.classList.add('show');
    setTimeout(() => {
        successToast.classList.remove('show');
    }, 3000);
}

// ===== Reset Products (API) =====
async function resetProducts() {
    // Confirm before reset
    if (!confirm('Khôi phục tất cả sản phẩm về trạng thái "còn hàng"?')) {
        return;
    }
    
    try {
        resetBtn.disabled = true;
        resetBtn.innerHTML = '<span>⏳</span> Đang reset...';
        
        const response = await fetch(`${API_URL}/reset`, {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Animate the reset button
            resetBtn.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                resetBtn.style.transform = '';
            }, 500);
            
            // Reload products
            await fetchProducts();
        }
    } catch (error) {
        console.error('Reset error:', error);
        alert('Lỗi reset!');
    } finally {
        resetBtn.disabled = false;
        resetBtn.innerHTML = '<span>🔄</span> Reset';
    }
}

// ===== Filter by Category =====
function filterByCategory(category) {
    currentFilter = category;
    
    // Update active tab
    document.querySelectorAll('.category-tab').forEach(tab => {
        tab.classList.remove('active');
        if (tab.dataset.category === category) {
            tab.classList.add('active');
        }
    });

    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.filter === category) {
            link.classList.add('active');
        }
    });

    renderProducts();
}

// ===== Setup Event Listeners =====
function setupEventListeners() {
    // Modal events
    modalClose.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);
    confirmBtn.addEventListener('click', confirmPurchase);
    
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            closeModal();
        }
    });

    // Reset button
    resetBtn.addEventListener('click', resetProducts);

    // Category tabs
    categoryTabs.addEventListener('click', (e) => {
        const tab = e.target.closest('.category-tab');
        if (tab) {
            filterByCategory(tab.dataset.category);
        }
    });

    // Nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            filterByCategory(link.dataset.filter);
        });
    });

    // Keyboard events
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modalOverlay.classList.contains('active')) {
            closeModal();
        }
    });

    // Scroll effect for header
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const header = document.querySelector('.header');
        const currentScroll = window.pageYOffset;

        if (currentScroll > lastScroll && currentScroll > 100) {
            header.style.transform = 'translateY(-100%)';
        } else {
            header.style.transform = 'translateY(0)';
        }
        lastScroll = currentScroll;
    });
}

// ===== Expose functions globally =====
window.openPurchaseModal = openPurchaseModal;
window.resetProducts = resetProducts;

// ===== Search Functions =====
function openSearch() {
    searchOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
    setTimeout(() => {
        searchInput.focus();
    }, 300);
}

function closeSearch() {
    searchOverlay.classList.remove('active');
    document.body.style.overflow = '';
    searchInput.value = '';
    searchClear.classList.remove('show');
    resetSearchResults();
}

function resetSearchResults() {
    searchResults.innerHTML = `
        <div class="search-placeholder">
            <span class="placeholder-icon">📚</span>
            <p>Nhập từ khóa để bắt đầu tìm kiếm...</p>
        </div>
    `;
}

async function performSearch(keyword) {
    if (!keyword.trim()) {
        resetSearchResults();
        return;
    }

    try {
        // Tìm kiếm qua API
        const response = await fetch(`${API_URL}/search?q=${encodeURIComponent(keyword)}`);
        let results = await response.json();
        
        // Map _id thành id
        results = results.map(p => ({ ...p, id: p._id }));

        if (results.length === 0) {
            searchResults.innerHTML = `
                <div class="search-no-result">
                    <span class="no-result-icon">😕</span>
                    <p>Không tìm thấy đề tài nào với từ khóa "<strong>${escapeHtml(keyword)}</strong>"</p>
                    <p style="font-size: 0.85rem; margin-top: 10px;">Hãy thử các từ khóa khác như: AI, STEM, KHTN, Vật lý...</p>
                </div>
            `;
            return;
        }

        searchResults.innerHTML = `
            <div class="search-count">Tìm thấy <strong>${results.length}</strong> đề tài</div>
            ${results.map((product, index) => `
                <div class="search-result-item" onclick="selectSearchResult('${product.id}')" style="animation-delay: ${index * 0.05}s">
                    <div class="result-number">#${index + 1}</div>
                    <div class="result-content">
                        <div class="result-category">${product.categoryIcon} ${product.categoryName}</div>
                        <div class="result-title">${highlightText(product.title, keyword)}</div>
                    </div>
                    <div class="result-price">${formatPrice(product.price)}</div>
                </div>
            `).join('')}
        `;
    } catch (error) {
        console.error('Search error:', error);
        // Fallback: tìm trong local data
        performLocalSearch(keyword);
    }
}

function performLocalSearch(keyword) {
    const searchTerm = keyword.toLowerCase().trim();
    
    const results = productsData.filter(product => {
        const titleMatch = product.title.toLowerCase().includes(searchTerm);
        const categoryMatch = product.categoryName.toLowerCase().includes(searchTerm);
        const featuresMatch = (product.features || []).some(f => f.toLowerCase().includes(searchTerm));
        return titleMatch || categoryMatch || featuresMatch;
    });

    if (results.length === 0) {
        searchResults.innerHTML = `
            <div class="search-no-result">
                <span class="no-result-icon">😕</span>
                <p>Không tìm thấy đề tài nào với từ khóa "<strong>${escapeHtml(keyword)}</strong>"</p>
            </div>
        `;
        return;
    }

    searchResults.innerHTML = `
        <div class="search-count">Tìm thấy <strong>${results.length}</strong> đề tài</div>
        ${results.map((product, index) => `
            <div class="search-result-item" onclick="selectSearchResult('${product.id}')" style="animation-delay: ${index * 0.05}s">
                <div class="result-number">#${index + 1}</div>
                <div class="result-content">
                    <div class="result-category">${product.categoryIcon} ${product.categoryName}</div>
                    <div class="result-title">${highlightText(product.title, keyword)}</div>
                </div>
                <div class="result-price">${formatPrice(product.price)}</div>
            </div>
        `).join('')}
    `;
}

function highlightText(text, keyword) {
    if (!keyword.trim()) return text;
    const regex = new RegExp(`(${escapeRegex(keyword)})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function selectSearchResult(productId) {
    closeSearch();
    setTimeout(() => {
        openPurchaseModal(productId);
    }, 300);
}

// Search event listeners
searchBtn.addEventListener('click', openSearch);

searchClose.addEventListener('click', closeSearch);

searchOverlay.addEventListener('click', (e) => {
    if (e.target === searchOverlay) {
        closeSearch();
    }
});

let searchTimeout;
searchInput.addEventListener('input', (e) => {
    const value = e.target.value;
    searchClear.classList.toggle('show', value.length > 0);
    
    // Debounce search
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        performSearch(value);
    }, 300);
});

searchClear.addEventListener('click', () => {
    searchInput.value = '';
    searchClear.classList.remove('show');
    resetSearchResults();
    searchInput.focus();
});

// Search tags
document.querySelectorAll('.search-tag').forEach(tag => {
    tag.addEventListener('click', () => {
        const keyword = tag.dataset.keyword;
        searchInput.value = keyword;
        searchClear.classList.add('show');
        performSearch(keyword);
    });
});

// Keyboard shortcut for search
document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        if (searchOverlay.classList.contains('active')) {
            closeSearch();
        } else {
            openSearch();
        }
    }
    if (e.key === 'Escape' && searchOverlay.classList.contains('active')) {
        closeSearch();
    }
});

window.selectSearchResult = selectSearchResult;

// ===== PAYMENT FLOW =====
const paymentModalOverlay = document.getElementById('paymentModalOverlay');
const paymentModalClose = document.getElementById('paymentModalClose');
const confirmPaymentBtn = document.getElementById('confirmPaymentBtn');
const closeSuccessBtn = document.getElementById('closeSuccessBtn');

// Open payment modal by product ID (called from "Mua ngay" button)
function openPaymentModalById(productId) {
    selectedProduct = productsData.find(p => p.id === productId);
    if (!selectedProduct) return;
    
    // Setup payment amount
    document.getElementById('paymentAmount').textContent = formatPrice(selectedProduct.price);
    
    // Generate order code and store it
    const orderCode = 'EDU' + Date.now().toString().slice(-6);
    paymentModalOverlay.dataset.orderCode = orderCode;
    paymentModalOverlay.dataset.productId = selectedProduct.id;
    paymentModalOverlay.dataset.productTitle = selectedProduct.title;
    paymentModalOverlay.dataset.productPrice = selectedProduct.price;
    
    // Reset form and show main content
    document.getElementById('buyerInfoForm').reset();
    document.getElementById('paymentMainContent').style.display = 'flex';
    document.getElementById('paymentSuccess').style.display = 'none';
    
    // Show modal
    paymentModalOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
}

// Close payment modal
function closePaymentModal() {
    paymentModalOverlay.classList.remove('active');
    document.body.style.overflow = '';
    document.getElementById('buyerInfoForm').reset();
}

// Validate buyer info
function validateBuyerInfo() {
    const name = document.getElementById('buyerName').value.trim();
    const email = document.getElementById('buyerEmail').value.trim();
    const phone = document.getElementById('buyerPhone').value.trim();
    
    if (!name) {
        alert('Vui lòng nhập họ tên');
        document.getElementById('buyerName').focus();
        return false;
    }
    
    if (!email || !email.includes('@')) {
        alert('Vui lòng nhập email hợp lệ');
        document.getElementById('buyerEmail').focus();
        return false;
    }
    
    if (!phone || phone.length < 9) {
        alert('Vui lòng nhập số điện thoại hợp lệ');
        document.getElementById('buyerPhone').focus();
        return false;
    }
    
    return true;
}

// Confirm payment
async function confirmPayment() {
    if (!validateBuyerInfo()) return;
    
    const name = document.getElementById('buyerName').value.trim();
    const email = document.getElementById('buyerEmail').value.trim();
    const phone = document.getElementById('buyerPhone').value.trim();
    const orderCode = paymentModalOverlay.dataset.orderCode;
    const productId = paymentModalOverlay.dataset.productId;
    const productTitle = paymentModalOverlay.dataset.productTitle;
    const productPrice = paymentModalOverlay.dataset.productPrice;
    
    const order = {
        id: orderCode,
        productId: productId,
        productTitle: productTitle,
        productPrice: productPrice,
        buyerName: name,
        buyerEmail: email,
        buyerPhone: phone,
        status: 'pending',
        createdAt: new Date().toISOString()
    };
    
    // Try to send to backend
    try {
        await fetch('/api/orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(order)
        });
    } catch (e) {
        console.log('Backend not available, order logged');
    }
    
    // Show success
    document.getElementById('orderCode').textContent = orderCode;
    document.getElementById('orderProduct').textContent = productTitle;
    document.getElementById('orderEmail').textContent = email;
    
    // Switch to success view
    document.getElementById('paymentMainContent').style.display = 'none';
    document.getElementById('paymentSuccess').style.display = 'block';
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Đã copy: ' + text);
    });
}

// Payment event listeners
if (paymentModalClose) {
    paymentModalClose.addEventListener('click', closePaymentModal);
}

if (paymentModalOverlay) {
    paymentModalOverlay.addEventListener('click', (e) => {
        if (e.target === paymentModalOverlay) {
            closePaymentModal();
        }
    });
}

if (confirmPaymentBtn) {
    confirmPaymentBtn.addEventListener('click', confirmPayment);
}

if (closeSuccessBtn) {
    closeSuccessBtn.addEventListener('click', closePaymentModal);
}

// Expose functions globally
window.openPaymentModalById = openPaymentModalById;
window.copyToClipboard = copyToClipboard;

// ===== CHAT WIDGET =====
const chatToggle = document.getElementById('chatToggle');
const chatBox = document.getElementById('chatBox');
const chatClose = document.getElementById('chatClose');

if (chatToggle) {
    chatToggle.addEventListener('click', () => {
        chatBox.classList.toggle('active');
    });
}

if (chatClose) {
    chatClose.addEventListener('click', () => {
        chatBox.classList.remove('active');
    });
}

// Close chat when clicking outside
document.addEventListener('click', (e) => {
    if (chatBox && chatBox.classList.contains('active')) {
        if (!e.target.closest('.chat-widget')) {
            chatBox.classList.remove('active');
        }
    }
});

