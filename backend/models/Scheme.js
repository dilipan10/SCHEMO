const mongoose = require('mongoose');

// Define the Scheme schema
const schemeSchema = new mongoose.Schema({
    schemeName: {
        type: String,
        required: true
    },
    description: {
        type: String,
        required: true
    },
    eligibility: {
        type: String,
        required: true
    },
    benefits: {
        type: String,
        required: true
    },
    applyLink: {
        type: String,
        required: true
    }
}, {
    timestamps: true
});

const Scheme = mongoose.model('Scheme', schemeSchema);
module.exports = Scheme;
