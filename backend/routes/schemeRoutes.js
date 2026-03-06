const express = require('express');
const router = express.Router();
const {
    getSchemes,
    getSchemeById,
    createScheme,
    updateScheme,
    deleteScheme
} = require('../controllers/schemeController');

// Map operations to routes
router.route('/')
    .get(getSchemes)
    .post(createScheme);

router.route('/:id')
    .get(getSchemeById)
    .put(updateScheme)
    .delete(deleteScheme);

module.exports = router;
