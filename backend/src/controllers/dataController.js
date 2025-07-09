// 简单的内存数据存储
let items = [];
let nextId = 1;

// 获取所有数据项
exports.getAllItems = (req, res) => {
  res.status(200).json({
    success: true,
    count: items.length,
    data: items
  });
};

// 获取单个数据项
exports.getItemById = (req, res) => {
  const id = parseInt(req.params.id);
  const item = items.find(item => item.id === id);
  
  if (!item) {
    return res.status(404).json({
      success: false,
      message: `未找到ID为${id}的数据项`
    });
  }
  
  res.status(200).json({
    success: true,
    data: item
  });
};

// 创建新数据项
exports.createItem = (req, res) => {
  const { name, description, value } = req.body;
  
  if (!name) {
    return res.status(400).json({
      success: false,
      message: '请提供数据项名称'
    });
  }
  
  const newItem = {
    id: nextId++,
    name,
    description: description || '',
    value: value || null,
    createdAt: new Date().toISOString()
  };
  
  items.push(newItem);
  
  res.status(201).json({
    success: true,
    data: newItem
  });
};

// 更新数据项
exports.updateItem = (req, res) => {
  const id = parseInt(req.params.id);
  const itemIndex = items.findIndex(item => item.id === id);
  
  if (itemIndex === -1) {
    return res.status(404).json({
      success: false,
      message: `未找到ID为${id}的数据项`
    });
  }
  
  const { name, description, value } = req.body;
  const updatedItem = {
    ...items[itemIndex],
    name: name || items[itemIndex].name,
    description: description !== undefined ? description : items[itemIndex].description,
    value: value !== undefined ? value : items[itemIndex].value,
    updatedAt: new Date().toISOString()
  };
  
  items[itemIndex] = updatedItem;
  
  res.status(200).json({
    success: true,
    data: updatedItem
  });
};

// 删除数据项
exports.deleteItem = (req, res) => {
  const id = parseInt(req.params.id);
  const itemIndex = items.findIndex(item => item.id === id);
  
  if (itemIndex === -1) {
    return res.status(404).json({
      success: false,
      message: `未找到ID为${id}的数据项`
    });
  }
  
  items.splice(itemIndex, 1);
  
  res.status(200).json({
    success: true,
    message: `ID为${id}的数据项已删除`
  });
};