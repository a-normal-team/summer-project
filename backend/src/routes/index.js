const express = require('express');
const apiController = require('../controllers/api');

const router = express.Router();

router.get('/api', apiController.handleRequest);

module.exports = router;