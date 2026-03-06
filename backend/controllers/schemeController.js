const Scheme = require('../models/Scheme');

// @desc    Get all government schemes
// @route   GET /api/schemes
const getSchemes = async (req, res) => {
    try {
        const schemes = await Scheme.find({});
        res.status(200).json(schemes);
    } catch (error) {
        res.status(500).json({ message: 'Server error fetching schemes', error: error.message });
    }
};

// @desc    Get a single scheme by ID
// @route   GET /api/schemes/:id
const getSchemeById = async (req, res) => {
    try {
        const scheme = await Scheme.findById(req.params.id);

        if (scheme) {
            res.status(200).json(scheme);
        } else {
            res.status(404).json({ message: 'Scheme not found' });
        }
    } catch (error) {
        res.status(500).json({ message: 'Server error', error: error.message });
    }
};

// @desc    Create a new scheme (Admin purpose)
// @route   POST /api/schemes
const createScheme = async (req, res) => {
    try {
        const { schemeName, description, eligibility, benefits, applyLink } = req.body;

        // Validation
        if (!schemeName || !description || !eligibility || !benefits || !applyLink) {
            return res.status(400).json({ message: 'Please provide all required fields' });
        }

        const scheme = await Scheme.create({
            schemeName,
            description,
            eligibility,
            benefits,
            applyLink
        });

        res.status(201).json({ message: 'Scheme added successfully!', scheme });
    } catch (error) {
        res.status(500).json({ message: 'Server error while creating scheme', error: error.message });
    }
};

// @desc    Update a scheme
// @route   PUT /api/schemes/:id
const updateScheme = async (req, res) => {
    try {
        const scheme = await Scheme.findById(req.params.id);

        if (!scheme) {
            return res.status(404).json({ message: 'Scheme not found' });
        }

        const updatedScheme = await Scheme.findByIdAndUpdate(
            req.params.id,
            req.body,
            { new: true } // Return updated doc
        );

        res.status(200).json({ message: 'Scheme updated successfully!', updatedScheme });
    } catch (error) {
        res.status(500).json({ message: 'Server error while updating scheme', error: error.message });
    }
};

// @desc    Delete a scheme
// @route   DELETE /api/schemes/:id
const deleteScheme = async (req, res) => {
    try {
        const scheme = await Scheme.findById(req.params.id);

        if (!scheme) {
            return res.status(404).json({ message: 'Scheme not found' });
        }

        await scheme.deleteOne();

        res.status(200).json({ message: 'Scheme deleted successfully', id: req.params.id });
    } catch (error) {
        res.status(500).json({ message: 'Server error deleting scheme', error: error.message });
    }
};

module.exports = {
    getSchemes,
    getSchemeById,
    createScheme,
    updateScheme,
    deleteScheme
};
