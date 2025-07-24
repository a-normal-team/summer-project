import { reactive } from 'vue';
import router from '../router';
import { post, get } from './http';
import { AUTH_CONFIG } from '../config';
import { clearSessionToken, saveTokenToSession } from './token';

// 创建响应式状态对象
export const authState = reactive({
  user: null,
  token: localStorage.getItem(AUTH_CONFIG.TOKEN_KEY) || null,
  isAuthenticated: !!localStorage.getItem(AUTH_CONFIG.TOKEN_KEY),
  error: null,
  loading: false
});

/**
 * 调试函数：打印当前认证状态
 */
export function debugAuthState(message = '当前认证状态') {
  console.group(message);
  console.log('认证状态:', authState.isAuthenticated);
  console.log('令牌:', authState.token ? '存在' : '不存在');
  console.log('用户对象:', authState.user);
  if (authState.user) {
    console.log('用户ID (authState):', authState.user.id);
    console.log('用户角色:', authState.user.role);
  }
  console.log('localStorage中的用户ID:', localStorage.getItem('userId'));
  console.groupEnd();
}

/**
 * 获取当前登录用户的ID
 * @returns {number|null} - 用户ID或null（如果未登录）
 */
export function getUserId() {
  // 打印调试信息
  console.group('getUserId调用');
  
  // 优先从authState.user中获取ID
  if (authState.user?.id !== undefined && authState.user?.id !== null) {
    console.log('从authState.user获取到ID:', authState.user.id);
    const userId = Number(authState.user.id);
    console.log('转换后的userId:', userId);
    console.groupEnd();
    return userId;
  }
  
  // 如果authState.user中没有ID，尝试从localStorage获取
  const storedId = localStorage.getItem('userId');
  if (storedId) {
    console.log('从localStorage获取到ID:', storedId);
    const userId = Number(storedId);
    console.log('转换后的userId:', userId);
    console.groupEnd();
    return userId;
  }
  
  // 如果都没有，返回null
  console.log('无法获取用户ID');
  console.groupEnd();
  return null;
}

/**
 * 获取当前登录用户的用户名
 * @returns {string|null} - 用户名或null（如果未登录）
 */
export function getUsername() {
  console.group('getUsername调用');
  
  // 从authState.user中获取用户名
  if (authState.user?.username) {
    console.log('从authState.user获取到用户名:', authState.user.username);
    console.groupEnd();
    return authState.user.username;
  }
  
  // 如果authState.user中没有用户名，尝试从localStorage获取
  const storedUsername = localStorage.getItem('username');
  if (storedUsername) {
    console.log('从localStorage获取到用户名:', storedUsername);
    console.groupEnd();
    return storedUsername;
  }
  
  // 如果都没有，返回null
  console.log('无法获取用户名');
  console.groupEnd();
  return null;
}

/**
 * 用户注册
 * @param {Object} userData - 包含用户名和密码的对象
 * @returns {Promise} - 包含注册结果的Promise
 */
export async function register(userData) {
  authState.loading = true;
  authState.error = null;
  
  try {
    const data = await post('/auth/register', userData);
    return data;
  } catch (error) {
    authState.error = error.message || '注册过程中发生错误';
    throw error;
  } finally {
    authState.loading = false;
  }
}

/**
 * 用户登录
 * @param {Object} credentials - 包含用户名和密码的对象
 * @returns {Promise} - 包含登录结果的Promise
 */
export async function login(credentials) {
  authState.loading = true;
  authState.error = null;
  
  try {
    const data = await post('/auth/login', credentials);
    
    // 存储令牌 - 使用用户ID和角色
    // 从响应中获取用户角色和ID
    const userRole = data.role || credentials.role || 'listener';
    
    // 尝试从响应获取用户ID
    let userId = null;
    const idFields = ['user_id', 'userId', 'id'];
    for (const field of idFields) {
      if (data[field] !== undefined && data[field] !== null) {
        userId = data[field];
        break;
      }
    }
    
    // 如果找不到用户ID，使用用户名作为备选标识符
    const userIdentifier = userId || credentials.username || 'unknown';
    
    // 创建用户特定的令牌键：userRole_userIdentifier_token
    const userSpecificTokenKey = `${userRole}_${userIdentifier}_token`;
    
    // 根据角色选择适当的角色特定令牌键
    let roleTokenKey = AUTH_CONFIG.TOKEN_KEY; // 默认令牌键
    if (userRole === 'speaker') {
      roleTokenKey = AUTH_CONFIG.SPEAKER_TOKEN_KEY;
    } else if (userRole === 'listener') {
      roleTokenKey = AUTH_CONFIG.LISTENER_TOKEN_KEY;
    } else if (userRole === 'organizer') {
      roleTokenKey = AUTH_CONFIG.ORGANIZER_TOKEN_KEY;
    }
    
    // 存储令牌到用户特定的键、角色特定的键和通用键
    localStorage.setItem(userSpecificTokenKey, data.access_token);
    localStorage.setItem(roleTokenKey, data.access_token); 
    localStorage.setItem(AUTH_CONFIG.TOKEN_KEY, data.access_token); // 同时保留通用键以兼容现有代码
    
    // 记录当前用户信息到localStorage（用于跨标签页共享）
    localStorage.setItem('currentUserRole', userRole);
    localStorage.setItem('currentUserIdentifier', userIdentifier);
    localStorage.setItem('currentUserTokenKey', userSpecificTokenKey);
    
    // 保存当前标签页的认证信息
    saveTokenToSession(data.access_token, userSpecificTokenKey, userRole, userIdentifier);
    
    // 获取当前会话ID用于日志
    const sessionId = sessionStorage.getItem('browserTabSessionId') || '未知会话';
    console.log(`[认证] 标签页会话 ${sessionId} 登录为 ${userRole} (${userIdentifier})`);
    
    authState.token = data.access_token;
    authState.isAuthenticated = true;
    
    // 向所有打开的页面广播令牌更新事件
    try {
      // 确保有sessionId
      const currentSessionId = sessionStorage.getItem('browserTabSessionId') || '未知会话';
      const tokenUpdateEvent = new CustomEvent('auth_token_updated', {
        detail: {
          tokenKey: userSpecificTokenKey,
          token: data.access_token,
          userRole: userRole,
          userId: userIdentifier,
          timestamp: new Date().getTime(),
          sessionId: currentSessionId
        }
      });
      window.dispatchEvent(tokenUpdateEvent);
      console.log('已分发令牌更新事件:', userSpecificTokenKey);
    } catch (eventError) {
      console.error('分发令牌更新事件失败:', eventError);
    }
    
    // 如果响应中包含用户ID，则存储 - 检查多种可能的字段名
    const userIdFields = ['user_id', 'userId', 'id'];
    let foundUserId = null;
    let fieldName = null;
    
    for (const field of userIdFields) {
      if (data[field] !== undefined && data[field] !== null) {
        foundUserId = data[field];
        fieldName = field;
        break;
      }
    }
    
    if (foundUserId !== null) {
      localStorage.setItem('userId', foundUserId);
      console.log(`登录成功，从字段${fieldName}保存用户ID到localStorage:`, foundUserId);
    } else {
      console.error('登录响应中没有找到任何用户ID字段:', data);
      // 检查响应中的所有顶级字段
      console.log('登录响应中的所有字段:', Object.keys(data));
    }
    
    // 存储用户名，用于后续匹配演讲者
    if (credentials.username) {
      localStorage.setItem('username', credentials.username);
      console.log('登录成功，保存用户名到localStorage:', credentials.username);
    }
    
    // 尝试获取用户资料，但即使失败也继续登录流程
    try {
      await fetchUserProfile();
    } catch (profileError) {
      console.error('获取用户资料失败，但继续登录流程:', profileError);
      
      // 如果没有用户对象，创建一个基本的用户对象
      if (!authState.user) {
        const userId = localStorage.getItem('userId');
        const username = credentials.username || '用户';
        
        // 保存用户名到localStorage以便与演讲的speaker字段匹配
        localStorage.setItem('username', username);
        
        authState.user = {
          id: userId ? Number(userId) : null,  // 尝试从localStorage获取用户ID
          username: username,
          // 根据登录重定向规则猜测角色
          role: 'speaker'  // 假设默认角色是speaker
        };
        
        console.log('创建基本用户对象:', authState.user);
      }
    }
    
    // 打印调试信息
    debugAuthState('登录流程完成');
    
    return data;
  } catch (error) {
    authState.error = error.message || '登录过程中发生错误';
    throw error;
  } finally {
    authState.loading = false;
  }
}

/**
 * 获取用户资料
 * @returns {Promise} - 包含用户资料的Promise
 */
export async function fetchUserProfile() {
  if (!authState.token) {
    return null;
  }
  
  authState.loading = true;
  
  try {
    // 尝试不使用尾斜杠的版本
    const data = await get('/auth/profile');
    console.log('获取用户资料成功:', data);
    console.log('用户角色:', data.role);
    
    // 如果后端返回的数据没有角色信息，根据路由路径推断当前角色
    if (!data.role) {
      // 检查当前路径来确定用户角色
      const path = window.location.pathname;
      if (path.includes('/speaker/')) {
        data.role = 'speaker';
        console.log('根据路由路径设置角色为: speaker');
      } else if (path.includes('/organizer/')) {
        data.role = 'organizer';
        console.log('根据路由路径设置角色为: organizer');
      } else if (path.includes('/listener/')) {
        data.role = 'listener';
        console.log('根据路由路径设置角色为: listener');
      }
    }
    
    // 确保用户对象至少有基本信息
    if (!data.username && authState.user?.username) {
      data.username = authState.user.username;
    }
    
    // 检查API返回的用户数据中可能的ID字段
    const userIdFields = ['id', 'user_id', 'userId'];
    let hasIdField = false;
    
    for (const field of userIdFields) {
      if (data[field] !== undefined && data[field] !== null) {
        // 确保data.id字段存在（作为统一的ID访问点）
        if (field !== 'id') {
          data.id = data[field];
          console.log(`从返回数据的${field}字段复制ID到id字段:`, data.id);
        }
        hasIdField = true;
        break;
      }
    }
    
    // 如果API返回的用户数据没有任何ID字段，但localStorage中有userId
    if (!hasIdField && localStorage.getItem('userId')) {
      data.id = Number(localStorage.getItem('userId'));
      console.log('从localStorage补充用户ID:', data.id);
    }
    
    // 如果有ID，确保保存到localStorage
    if (data.id && !localStorage.getItem('userId')) {
      localStorage.setItem('userId', data.id);
      console.log('保存用户ID到localStorage:', data.id);
    }
    
    // 记录最终的用户数据结构
    console.log('最终的用户数据结构:', JSON.stringify(data, null, 2));
    
    authState.user = data;
    
    // 打印调试信息
    debugAuthState('获取用户资料成功');
    return data;
  } catch (error) {
    console.error('获取用户资料失败:', error);
    authState.error = error.message || '获取用户资料过程中发生错误';
    
    // 即使获取资料失败，也要确保用户对象存在基本信息
    if (!authState.user) {
      // 创建一个基本用户对象
      const userId = localStorage.getItem('userId');
      const storedUsername = localStorage.getItem('username') || '用户';
      
      authState.user = {
        id: userId ? Number(userId) : null,  // 尝试从localStorage获取用户ID
        username: storedUsername,
        role: 'default'
      };
      
      console.log('创建基本用户对象(获取资料失败):', authState.user);
      
      // 尝试从路径确定角色
      const path = window.location.pathname;
      if (path.includes('/speaker/')) {
        authState.user.role = 'speaker';
      } else if (path.includes('/organizer/')) {
        authState.user.role = 'organizer';
      } else if (path.includes('/listener/')) {
        authState.user.role = 'listener';
      }
    }
    
    // 只有在特定情况下才清除认证状态
    if (error.message === 'User not found' || error.message.includes('token')) {
      logout();
      throw error;
    }
    
    // 对于其他错误（如404 Not Found），我们只记录错误但不中断流程
    console.warn('获取用户资料失败，但不中断认证流程:', error);
  } finally {
    authState.loading = false;
  }
}

/**
 * 用户登出
 */
export function logout() {
  console.log('执行登出操作');
  
  // 获取当前用户信息，用于广播事件
  const currentUserTokenKey = localStorage.getItem('currentUserTokenKey');
  const currentUserRole = localStorage.getItem('currentUserRole');
  const currentUserIdentifier = localStorage.getItem('currentUserIdentifier');
  
  // 清除用户特定的令牌
  if (currentUserTokenKey) {
    localStorage.removeItem(currentUserTokenKey);
  }
  
  // 清除所有角色的令牌存储
  localStorage.removeItem(AUTH_CONFIG.TOKEN_KEY);
  localStorage.removeItem(AUTH_CONFIG.SPEAKER_TOKEN_KEY);
  localStorage.removeItem(AUTH_CONFIG.LISTENER_TOKEN_KEY);
  localStorage.removeItem(AUTH_CONFIG.ORGANIZER_TOKEN_KEY);
  
  // 清除其他存储的用户信息
  localStorage.removeItem('userId');
  localStorage.removeItem('currentUserRole');
  localStorage.removeItem('currentUserIdentifier');
  localStorage.removeItem('currentUserTokenKey');
  localStorage.removeItem('username');
  
  // 使用从文件顶部导入的 clearSessionToken 函数
  // 清除会话存储中的认证信息
  clearSessionToken();
  
  // 清除所有认证相关状态
  authState.token = null;
  authState.user = null;
  authState.isAuthenticated = false;
  authState.error = null;
  
  // 向所有打开的页面广播退出登录事件
  try {
    const logoutEvent = new CustomEvent('auth_logout', {
      detail: {
        tokenKey: currentUserTokenKey,
        userRole: currentUserRole,
        userId: currentUserIdentifier,
        timestamp: new Date().getTime()
      }
    });
    window.dispatchEvent(logoutEvent);
    console.log('已分发退出登录事件');
  } catch (eventError) {
    console.error('分发退出登录事件失败:', eventError);
  }
  
  // 导航到登录页面
  router.push('/login');
  
  console.log('登出完成，当前认证状态:', authState);
}

/**
 * 根据用户角色导航到相应的仪表板
 */
export function navigateToDashboard() {
  if (!authState.user) return;
  
  switch (authState.user.role) {
    case 'organizer':
      router.push('/organizer/dashboard');
      break;
    case 'speaker':
      router.push('/speaker/dashboard');
      break;
    case 'listener':
      router.push('/listener/dashboard');
      break;
    default:
      router.push('/login');
  }
}

/**
 * 检查并验证当前存储的token
 * 用于应用初始化时检查认证状态
 */
export async function checkAuth() {
  if (!authState.token) {
    return false;
  }
  
  try {
    await fetchUserProfile();
    return !!authState.user;
  } catch (error) {
    return false;
  }
}
