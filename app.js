// ===== App State =====
let soldProducts = JSON.parse(localStorage.getItem('soldProducts')) || [];
let currentFilter = 'all';
let selectedProduct = null;

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
    renderProducts();
    updateStats();
    setupEventListeners();
    setupPlanningTool();
});

// ===== Planning Tool =====
function setupPlanningTool() {
    const classSelect = document.getElementById('classSelect');
    const subjectSelect = document.getElementById('subjectSelect');
    const lessonSelect = document.getElementById('lessonSelect');
    const requestInput = document.getElementById('requestInput');
    const generateBtn = document.getElementById('generateBtn');

    // Handle Class Change
    classSelect.addEventListener('change', (e) => {
        const selectedClass = parseInt(e.target.value);
        
        // Reset dependent fields
        subjectSelect.innerHTML = '<option value="">Chọn môn học...</option>';
        lessonSelect.innerHTML = '<option value="">Chọn bài học...</option>';
        subjectSelect.disabled = true;
        lessonSelect.disabled = true;
        generateBtn.disabled = true;

        if (!selectedClass) return;

        // Find data for selected class
        const classData = curriculumData.find(c => c.lop === selectedClass);
        if (classData && classData.mon_hoc_du_lieu) {
            classData.mon_hoc_du_lieu.forEach(subject => {
                const option = document.createElement('option');
                option.value = subject.id;
                option.textContent = subject.ten_mon;
                subjectSelect.appendChild(option);
            });
            subjectSelect.disabled = false;
        }
    });

    // Handle Subject Change
    subjectSelect.addEventListener('change', (e) => {
        const selectedSubjectId = e.target.value;
        const selectedClass = parseInt(classSelect.value);

        // Reset lesson field
        lessonSelect.innerHTML = '<option value="">Chọn bài học...</option>';
        lessonSelect.disabled = true;
        generateBtn.disabled = true;

        if (!selectedSubjectId) return;

        // Find data
        const classData = curriculumData.find(c => c.lop === selectedClass);
        if (classData) {
            const subjectData = classData.mon_hoc_du_lieu.find(s => s.id === selectedSubjectId);
            if (subjectData && subjectData.danh_sach_bai_full) {
                subjectData.danh_sach_bai_full.forEach(lesson => {
                    const option = document.createElement('option');
                    option.value = lesson.bai_so;
                    option.textContent = `${lesson.ten_bai} (${lesson.chu_de})`;
                    lessonSelect.appendChild(option);
                });
                lessonSelect.disabled = false;
            }
        }
    });

    // Handle Lesson Change
    lessonSelect.addEventListener('change', () => {
        checkFormValidity();
    });

    // Handle Input Change
    requestInput.addEventListener('input', () => {
        checkFormValidity();
    });

    function checkFormValidity() {
        const isValid = classSelect.value && subjectSelect.value && lessonSelect.value;
        generateBtn.disabled = !isValid;
    }

    // Handle Generate Button
    generateBtn.addEventListener('click', () => {
        const data = {
            class: classSelect.options[classSelect.selectedIndex].text,
            subject: subjectSelect.options[subjectSelect.selectedIndex].text,
            lesson: lessonSelect.options[lessonSelect.selectedIndex].text,
            request: requestInput.value
        };

        // Show loading state
        const originalBtnText = generateBtn.innerHTML;
        generateBtn.innerHTML = '<span>⏳</span> Đang xử lý...';
        generateBtn.disabled = true;

        // Simulate API call
        setTimeout(() => {
            generateBtn.innerHTML = '<span>✅</span> Đã gửi yêu cầu';
            alert(`Đã nhận yêu cầu:\n- Lớp: ${data.class}\n- Môn: ${data.subject}\n- Bài: ${data.lesson}\n- Yêu cầu: ${data.request || 'Không có'}`);
            
            setTimeout(() => {
                generateBtn.innerHTML = originalBtnText;
                generateBtn.disabled = false;
            }, 2000);
        }, 1000);
    });
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
        
        // Random colors
        const colors = ['#6366f1', '#ec4899', '#14b8a6', '#f59e0b'];
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];
        
        particlesContainer.appendChild(particle);
    }
}

// ===== Render Products =====
function renderProducts() {
    // Get pending product IDs
    const pendingProductIds = pendingOrders
        .filter(o => o.status === 'pending')
        .map(o => o.productId);
    
    // Only hide confirmed sold products (not pending ones)
    const confirmedSoldIds = soldProducts.filter(id => !pendingProductIds.includes(id));
    
    const availableProducts = productsData.filter(p => !confirmedSoldIds.includes(p.id));
    const filteredProducts = currentFilter === 'all' 
        ? availableProducts 
        : availableProducts.filter(p => p.category === currentFilter);

    if (filteredProducts.length === 0) {
        productsGrid.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }

    emptyState.style.display = 'none';
    productsGrid.innerHTML = filteredProducts.map((product, index) => {
        const isPending = pendingProductIds.includes(product.id);
        return `
        <div class="product-card ${isPending ? 'pending' : ''}" data-id="${product.id}" style="animation-delay: ${index * 0.1}s">
            ${isPending ? '<div class="pending-badge">⏳ Đang chờ xác nhận</div>' : ''}
            <div class="card-header">
                <span class="card-category ${product.category}">
                    ${product.categoryIcon} ${product.categoryName}
                </span>
                <span class="card-number">#${product.id}</span>
                <h3 class="card-title">${product.title}</h3>
            </div>
            <div class="card-body">
                <div class="card-features">
                    ${product.features.map(f => `<span class="feature-tag">${f}</span>`).join('')}
                </div>
            </div>
            <div class="card-footer">
                <div class="price-container">
                    <span class="price-original">${formatPrice(product.originalPrice)}</span>
                    <span class="price-current">${formatPrice(product.price)}</span>
                </div>
                <button class="btn-buy ${isPending ? 'disabled' : ''}" onclick="${isPending ? '' : 'openPurchaseModal(' + product.id + ')'}" ${isPending ? 'disabled' : ''}>
                    <span>${isPending ? '⏳' : '🛒'}</span> ${isPending ? 'Đang chờ' : 'Mua ngay'}
                </button>
            </div>
        </div>
    `}).join('');
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
    const availableProducts = productsData.filter(p => !soldProducts.includes(p.id));
    
    document.getElementById('totalProducts').textContent = availableProducts.length;
    document.getElementById('soldProducts').textContent = soldProducts.length;

    // Update category counts
    updateCategoryCounts(availableProducts);
}

function updateCategoryCounts(availableProducts) {
    const counts = {
        all: availableProducts.length,
        ai: availableProducts.filter(p => p.category === 'ai').length,
        stem: availableProducts.filter(p => p.category === 'stem').length,
        method: availableProducts.filter(p => p.category === 'method').length,
        skill: availableProducts.filter(p => p.category === 'skill').length
    };

    document.getElementById('countAll').textContent = counts.all;
    document.getElementById('countAi').textContent = counts.ai;
    document.getElementById('countStem').textContent = counts.stem;
    document.getElementById('countMethod').textContent = counts.method;
    document.getElementById('countSkill').textContent = counts.skill;
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

// ===== Confirm Purchase =====
function confirmPurchase() {
    if (!selectedProduct) return;

    // Find and animate the card
    const card = document.querySelector(`.product-card[data-id="${selectedProduct.id}"]`);
    if (card) {
        card.classList.add('selling');
    }

    // Add to sold products
    soldProducts.push(selectedProduct.id);
    localStorage.setItem('soldProducts', JSON.stringify(soldProducts));

    // Close modal
    closeModal();

    // Show success toast
    showToast();

    // Update UI after animation
    setTimeout(() => {
        renderProducts();
        updateStats();
    }, 800);
}

// ===== Show Toast =====
function showToast(message) {
    if (message) {
        successToast.textContent = message;
    } else {
        successToast.textContent = '🎉 Giao dịch thành công! Sản phẩm đã được gửi qua Email.';
    }
    successToast.classList.add('show');
    setTimeout(() => {
        successToast.classList.remove('show');
    }, 3000);
}

// ===== Reset Products =====
function resetProducts() {
    soldProducts = [];
    localStorage.removeItem('soldProducts');
    renderProducts();
    updateStats();
    
    // Animate the reset button
    resetBtn.style.transform = 'rotate(360deg)';
    setTimeout(() => {
        resetBtn.style.transform = '';
    }, 500);
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
    // confirmBtn now handled in payment flow section below
    
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

function performSearch(keyword) {
    if (!keyword.trim()) {
        resetSearchResults();
        return;
    }

    const availableProducts = productsData.filter(p => !soldProducts.includes(p.id));
    const searchTerm = keyword.toLowerCase().trim();
    
    // Tìm kiếm trong title, category, features
    const results = availableProducts.filter(product => {
        const titleMatch = product.title.toLowerCase().includes(searchTerm);
        const categoryMatch = product.categoryName.toLowerCase().includes(searchTerm);
        const featuresMatch = product.features.some(f => f.toLowerCase().includes(searchTerm));
        return titleMatch || categoryMatch || featuresMatch;
    });

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
            <div class="search-result-item" onclick="selectSearchResult(${product.id})" style="animation-delay: ${index * 0.05}s">
                <div class="result-number">#${product.id}</div>
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

searchInput.addEventListener('input', (e) => {
    const value = e.target.value;
    searchClear.classList.toggle('show', value.length > 0);
    performSearch(value);
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
    // Ctrl/Cmd + K to open search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        if (searchOverlay.classList.contains('active')) {
            closeSearch();
        } else {
            openSearch();
        }
    }
    // Escape to close search
    if (e.key === 'Escape' && searchOverlay.classList.contains('active')) {
        closeSearch();
    }
});

window.selectSearchResult = selectSearchResult;

// ===== PAYMENT FLOW =====
const paymentModalOverlay = document.getElementById('paymentModalOverlay');
const paymentModalClose = document.getElementById('paymentModalClose');
const backToProductBtn = document.getElementById('backToProductBtn');
const toPaymentBtn = document.getElementById('toPaymentBtn');
const backToInfoBtn = document.getElementById('backToInfoBtn');
const confirmPaymentBtn = document.getElementById('confirmPaymentBtn');
const closeSuccessBtn = document.getElementById('closeSuccessBtn');

// Pending orders (local storage)
let pendingOrders = JSON.parse(localStorage.getItem('pendingOrders')) || [];

// Check and restore expired orders on page load
function checkExpiredOrders() {
    const now = Date.now();
    const oneDayMs = 24 * 60 * 60 * 1000;
    let hasChanges = false;
    
    pendingOrders = pendingOrders.filter(order => {
        const orderTime = new Date(order.createdAt).getTime();
        if (now - orderTime > oneDayMs && order.status === 'pending') {
            // Order expired, remove from pending
            hasChanges = true;
            return false;
        }
        return true;
    });
    
    if (hasChanges) {
        localStorage.setItem('pendingOrders', JSON.stringify(pendingOrders));
        renderProducts();
    }
}

// Run check on load
checkExpiredOrders();

// Open payment modal
function openPaymentModal() {
    if (!selectedProduct) return;
    
    // Close product modal
    closeModal();
    
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
    // Show modal
    paymentModalOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
}

// Close payment modal
function closePaymentModal() {
    paymentModalOverlay.classList.remove('active');
    document.body.style.overflow = '';
    
    // Reset form
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
        buyerNote: '',
        status: 'pending',
        createdAt: new Date().toISOString()
    };
    
    // Save to local storage
    pendingOrders.push(order);
    localStorage.setItem('pendingOrders', JSON.stringify(pendingOrders));
    
    // Add to sold products (temporarily hide)
    soldProducts.push(selectedProduct.id);
    localStorage.setItem('soldProducts', JSON.stringify(soldProducts));
    
    // Try to send to backend (optional)
    try {
        const API_URL = window.location.hostname === 'localhost' 
            ? 'http://localhost:5000' 
            : '';
        await fetch(`${API_URL}/api/orders`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(order)
        });
    } catch (e) {
        console.log('Backend not available, order saved locally');
    }
    
    // Show success
    document.getElementById('orderCode').textContent = orderCode;
    document.getElementById('orderProduct').textContent = productTitle;
    document.getElementById('orderEmail').textContent = email;
    
    // Switch to success view
    document.getElementById('paymentMainContent').style.display = 'none';
    document.getElementById('paymentSuccess').style.display = 'block';
    
    // Update UI
    renderProducts();
    updateStats();
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Đã copy!');
    });
}

// Event listeners
if (confirmBtn) {
    confirmBtn.addEventListener('click', openPaymentModal);
}

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
    closeSuccessBtn.addEventListener('click', () => {
        closePaymentModal();
    });
}

// Expose functions globally
window.copyToClipboard = copyToClipboard;
