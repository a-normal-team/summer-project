const express = require('express');
const router = express.Router();
const dataController = require('../controllers/dataController');

// 获取所有数据项
router.get('/', dataController.getAllItems);

// 获取单个数据项
router.get('/:id', dataController.getItemById);

// 创建新数据项
router.post('/', dataController.createItem);

// 更新数据项
router.put('/:id', dataController.updateItem);

// 删除数据项
router.delete('/:id', dataController.deleteItem);

module.exports = router;