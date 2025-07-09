const express = require('express');
const router = express.Router();
const apiController = require('../controllers/api');
const dataRoutes = require('./dataRoutes');

// 基本API路由
router.get('/api/status', apiController.getStatus);

// 数据存储API路由
router.use('/api/data', dataRoutes);

module.exports = router;