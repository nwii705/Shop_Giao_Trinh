const mongoose = require('mongoose');

const ProductSchema = new mongoose.Schema({
    title: {
        type: String,
        required: true
    },
    category: {
        type: String,
        required: true,
        enum: ['ai', 'stem', 'method', 'skill']
    },
    categoryName: {
        type: String,
        required: true
    },
    categoryIcon: {
        type: String,
        default: '📚'
    },
    price: {
        type: Number,
        required: true
    },
    originalPrice: {
        type: Number,
        required: true
    },
    features: [{
        type: String
    }],
    status: {
        type: String,
        enum: ['available', 'sold'],
        default: 'available'
    },
    fileUrl: {
        type: String,
        default: ''
    },
    createdAt: {
        type: Date,
        default: Date.now
    }
});

// Tự động tạo ID số cho frontend
ProductSchema.virtual('id').get(function() {
    return this._id.toHexString();
});

ProductSchema.set('toJSON', { virtuals: true });

module.exports = mongoose.model('Product', ProductSchema);
