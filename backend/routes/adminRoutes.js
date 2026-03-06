const express = require('express');
const router = express.Router();

// Simple admin login route
router.post('/login', (req, res) => {
    const { email, password } = req.body;

    // Hardcoded logic for simplicity
    if (email === 'admin@schemo.com' && password === 'admin123') {
        res.status(200).json({ message: 'Admin login successful!' });
    } else {
        res.status(401).json({ message: 'Invalid admin credentials' });
    }
});

module.exports = router;
