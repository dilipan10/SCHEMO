const mongoose = require('mongoose');

// Define the User schema
const userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true // Name is mandatory
    },
    email: {
        type: String,
        required: true,
        unique: true // Email must be unique for each user
    },
    password: {
        type: String,
        required: true // Password is required
    }
}, {
    timestamps: true // Automatically adds createdAt and updatedAt fields
});

// Create and export the User model
const User = mongoose.model('User', userSchema);
module.exports = User;
