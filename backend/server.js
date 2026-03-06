// 1. Import dependencies
const express = require('express');
const cors = require('cors');
const connectDB = require('./config/db');

// 2. Import routes
const userRoutes = require('./routes/userRoutes');
const schemeRoutes = require('./routes/schemeRoutes');
const adminRoutes = require('./routes/adminRoutes');

// 3. Initialize Express app
const app = express();

// 4. Connect to MongoDB
connectDB();

// 5. Setup Middleware
// CORS allows your HTML/JS frontend to securely communicate with this backend
app.use(cors());
// express.json() parses incoming JSON requests so you can access req.body
app.use(express.json());

// 6. Basic Route
app.get('/', (req, res) => {
    res.send('Welcome to Schemo Backend API');
});

// 7. Mount Routers
app.use('/api/users', userRoutes);
app.use('/api/schemes', schemeRoutes);
app.use('/api/admin', adminRoutes);

// 8. Global Error Handling Middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ message: 'Something went wrong!', error: err.message });
});

// 9. Start Server
const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server is running beautifully on http://localhost:${PORT}`);
});
