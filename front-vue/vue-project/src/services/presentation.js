/**
 * 演讲服务
 * 提供与演讲相关的API请求功能
 */

import { get, post, put, del } from './http';

/**
 * 创建新的演讲
 * @param {Object} presentationData - 包含演讲标题和描述的对象
 * @param {string} role - 创建者角色，可以是'speaker'或'organizer'
 * @returns {Promise} - 包含创建结果的Promise
 */
export async function createPresentation(presentationData, role = 'speaker') {
  try {
    // 确保数据中包含角色信息
    const dataWithRole = { 
      ...presentationData,
      role: role
    };
    
    // 根据角色设置请求头
    const options = {
      headers: {
        'X-User-Role': role
      }
    };
    
    console.log(`以${role}角色发送创建演讲请求:`, dataWithRole);
    
    const data = await post('/presentations/', dataWithRole, options);
    return data;
  } catch (error) {
    console.error(`以${role}角色创建演讲失败:`, error);
    
    // 如果服务器返回权限错误，提供更清晰的错误信息
    if (error.message && (error.message.includes('权限') || error.message.includes('只有'))) {
      throw new Error(`创建演讲失败：您的账户可能没有被正确设置为${role}角色`);
    }
    
    throw error;
  }
}

/**
 * 获取演讲列表
 * @param {string} role - 请求角色，可以是'speaker'或'organizer'
 * @returns {Promise} - 包含演讲列表的Promise
 */
export async function getPresentations(role = 'speaker') {
  try {
    // 根据角色设置请求头
    const options = {
      headers: {
        'X-User-Role': role
      }
    };
    
    // 获取所有演讲列表，将在前端根据需要进行过滤
    const url = '/presentations/';
    
    console.log(`以${role}角色获取演讲列表`);
    
    console.log('获取演讲列表请求选项:', options);
    console.log('请求URL:', url);
    const data = await get(url, options);
    
    // 详细记录API返回的数据结构
    console.log('原始演讲列表数据:', data);
    
    // 检查数据中的演讲者字段
    if (Array.isArray(data) && data.length > 0) {
      console.log('第一条演讲数据示例:');
      console.log(JSON.stringify(data[0], null, 2));
      
      // 检查每个演讲的speaker字段
      console.log('检查所有演讲的speaker字段:');
      data.forEach((presentation, index) => {
        console.log(`演讲${index + 1}: ID=${presentation.id}, 标题=${presentation.title}, 演讲者=${presentation.speaker}, 类型=${typeof presentation.speaker}`);
      });
    }
    return data;
  } catch (error) {
    console.error('获取演讲列表失败:', error);
    throw error;
  }
}

/**
 * 获取单个演讲详情
 * @param {number} presentationId - 演讲ID
 * @param {string} role - 请求角色，可以是'speaker'或'organizer'
 * @returns {Promise} - 包含演讲详情的Promise
 */
export async function getPresentationById(presentationId, role = 'speaker') {
  try {
    const options = {
      headers: {
        'X-User-Role': role
      }
    };
    
    const data = await get(`/presentations/${presentationId}`, options);
    return data;
  } catch (error) {
    console.error(`获取演讲(ID: ${presentationId})详情失败:`, error);
    throw error;
  }
}

/**
 * 更新演讲信息
 * @param {number} presentationId - 演讲ID
 * @param {Object} presentationData - 更新的演讲数据
 * @param {string} role - 请求角色，可以是'speaker'或'organizer'
 * @returns {Promise} - 包含更新结果的Promise
 */
export async function updatePresentation(presentationId, presentationData, role = 'speaker') {
  try {
    const options = {
      headers: {
        'X-User-Role': role
      }
    };
    
    const data = await put(`/presentations/${presentationId}`, presentationData, options);
    return data;
  } catch (error) {
    console.error(`更新演讲(ID: ${presentationId})失败:`, error);
    throw error;
  }
}

/**
 * 删除演讲
 * @param {number} presentationId - 演讲ID
 * @param {string} role - 请求角色，可以是'speaker'或'organizer'
 * @returns {Promise} - 包含删除结果的Promise
 */
export async function deletePresentation(presentationId, role = 'speaker') {
  try {
    const options = {
      headers: {
        'X-User-Role': role
      }
    };
    
    const data = await del(`/presentations/${presentationId}`, options);
    return data;
  } catch (error) {
    console.error(`删除演讲(ID: ${presentationId})失败:`, error);
    throw error;
  }
}

/**
 * 添加听众到演讲 (旧版本)
 * @deprecated 请使用文件底部的新版本
 * @param {number} presentationId - 演讲ID
 * @param {number} listenerId - 听众ID
 * @returns {Promise} - 包含操作结果的Promise
 */
// 这个函数已被移除，防止重复定义

/**
 * 从演讲中移除听众
 * @param {number} presentationId - 演讲ID
 * @param {number} listenerId - 听众ID
 * @returns {Promise} - 包含操作结果的Promise
 */
export async function removeListenerFromPresentation(presentationId, listenerId) {
  try {
    const data = await post(`/presentations/${presentationId}/remove_listener`, { listener_id: listenerId });
    return data;
  } catch (error) {
    console.error(`从演讲中移除听众失败:`, error);
    throw error;
  }
}

/**
 * 获取演讲的整体统计数据
 * @param {number} presentationId - 演讲ID
 * @returns {Promise} - 包含演讲统计数据的Promise
 */
export async function getPresentationStats(presentationId) {
  try {
    // 组织者获取演讲统计数据时使用organizer角色头信息
    const options = {
      headers: {
        'X-User-Role': 'organizer'
      }
    };
    
    console.log(`获取演讲(ID: ${presentationId})的统计数据`);
    
    // 根据API文档修正URL路径
    const data = await get(`/quiz/presentations/${presentationId}/overall_stats`, options);
    return data;
  } catch (error) {
    console.error(`获取演讲(ID: ${presentationId})统计数据失败:`, error);
    throw error;
  }
}

/**
 * 获取演讲的听众表现数据
 * @param {number} presentationId - 演讲ID
 * @returns {Promise} - 包含听众表现数据的Promise
 */
export async function getListenerPerformance(presentationId) {
  try {
    // 组织者获取听众表现数据时使用organizer角色头信息
    const options = {
      headers: {
        'X-User-Role': 'organizer'
      }
    };
    
    console.log(`获取演讲(ID: ${presentationId})的听众表现数据`);
    
    // 根据API文档，听众表现数据包含在整体统计接口的返回结果中
    const data = await get(`/quiz/presentations/${presentationId}/overall_stats`, options);
    
    // 从整体统计数据中提取听众表现列表
    if (data && data.listener_performance) {
      return data.listener_performance;
    } else {
      console.warn('整体统计数据中缺少听众表现信息');
      return [];
    }
  } catch (error) {
    console.error(`获取演讲(ID: ${presentationId})的听众表现数据失败:`, error);
    throw error;
  }
}

/**
 * 组织者分配演讲者到演讲
 * @param {number} presentationId - 演讲ID
 * @param {number} speakerId - 演讲者ID
 * @returns {Promise} - 包含操作结果的Promise
 */
export async function assignSpeakerToPresentation(presentationId, speakerId) {
  try {
    const options = {
      headers: {
        'X-User-Role': 'organizer'
      }
    };
    
    const data = await post(`/presentations/${presentationId}/assign_speaker`, { speaker_id: speakerId }, options);
    return data;
  } catch (error) {
    console.error(`分配演讲者到演讲失败:`, error);
    throw error;
  }
}

/**
 * 组织者创建演讲
 * @param {Object} presentationData - 包含演讲标题和描述的对象
 * @returns {Promise} - 包含创建结果的Promise
 */
export async function createPresentationAsOrganizer(presentationData) {
  try {
    // 确保数据中包含角色信息
    const dataWithRole = { 
      ...presentationData,
      role: 'organizer'
    };
    
    // 创建演讲时强制设置organizer角色头信息
    const options = {
      headers: {
        'X-User-Role': 'organizer'
      }
    };
    
    console.log('组织者发送创建演讲请求:', dataWithRole);
    
    const data = await post('/presentations/', dataWithRole, options);
    return data;
  } catch (error) {
    console.error('组织者创建演讲失败:', error);
    
    // 如果服务器返回权限错误，提供更清晰的错误信息
    if (error.message && (error.message.includes('权限') || error.message.includes('只有组织者'))) {
      throw new Error('创建演讲失败：您的账户可能没有被正确设置为组织者角色');
    }
    
    throw error;
  }
}

/**
 * 将听众添加到演讲
 * @param {number} presentationId - 演讲ID
 * @param {number} listenerId - 听众ID
 * @returns {Promise} - 包含操作结果的Promise
 */
export async function addListenerToPresentation(presentationId, listenerId) {
  try {
    const options = {
      headers: {
        'X-User-Role': 'listener'
      }
    };
    
    const data = await post(`/presentations/${presentationId}/add_listener`, {
      listener_id: listenerId
    }, options);
    
    console.log(`将听众(ID: ${listenerId})添加到演讲(ID: ${presentationId})成功`);
    return data;
  } catch (error) {
    console.error(`将听众添加到演讲(ID: ${presentationId})失败:`, error);
    throw error;
  }
}
