<script setup>
import { ref, onMounted, reactive } from 'vue';
import { login, register, navigateToDashboard, authState } from '../services/auth';

const container = ref(null);
const alertMessage = ref('');
const isSuccess = ref(false);
const isLoading = ref(false);

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: ''
});

// 注册表单数据
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  role: 'listener' // 默认角色
});

// 角色选项
const roleOptions = [
  { value: 'listener', label: '听众' },
  { value: 'speaker', label: '演讲者' },
  { value: 'organizer', label: '组织者' }
];

// 处理登录
const handleLogin = async (e) => {
  e.preventDefault();
  
  // 表单验证
  if (!loginForm.username || !loginForm.password) {
    showAlert('用户名和密码不能为空', false);
    return;
  }
  
  isLoading.value = true;
  try {
    await login(loginForm);
    showAlert('登录成功！', true);
    navigateToDashboard();
  } catch (error) {
    if (error.message.includes('无法连接到服务器')) {
      showAlert('无法连接到后端服务器，请确保服务器正在运行', false);
    } else {
      showAlert(`登录失败: ${error.message}`, false);
    }
    console.error('登录错误详情:', error);
  } finally {
    isLoading.value = false;
  }
};

// 处理注册
const handleRegister = async (e) => {
  e.preventDefault();
  
  // 表单验证
  if (!registerForm.username || !registerForm.password) {
    showAlert('用户名和密码不能为空', false);
    return;
  }
  
  if (registerForm.password !== registerForm.confirmPassword) {
    showAlert('两次输入的密码不一致', false);
    return;
  }
  
  isLoading.value = true;
  try {
    // 提取要发送的数据（不包含confirmPassword字段）
    const { confirmPassword, ...userData } = registerForm;
    
    await register(userData);
    showAlert('注册成功！请登录', true);
    container.value.classList.remove("right-panel-active"); // 切换到登录面板
  } catch (error) {
    if (error.message.includes('无法连接到服务器')) {
      showAlert('无法连接到后端服务器，请确保服务器正在运行', false);
    } else {
      showAlert(`注册失败: ${error.message}`, false);
    }
    console.error('注册错误详情:', error);
  } finally {
    isLoading.value = false;
  }
};

// 显示警告消息
const showAlert = (message, success) => {
  alertMessage.value = message;
  isSuccess.value = success;
  
  // 自动清除消息
  setTimeout(() => {
    alertMessage.value = '';
  }, 3000);
};

onMounted(() => {
  const signUpButton = document.getElementById('signUp');
  const signInButton = document.getElementById('signIn');
  const containerElement = container.value;

  if (signUpButton && signInButton && containerElement) {
    signUpButton.addEventListener('click', () => {
      containerElement.classList.add("right-panel-active");
    });
    signInButton.addEventListener('click', () => {
      containerElement.classList.remove("right-panel-active");
    });
  }
});
</script>

<template>
    <div>
        <h2>欢迎使用Ai-PQ平台</h2>
        
        <!-- 警告消息 -->
        <div v-if="alertMessage" class="alert" :class="{ 'success': isSuccess, 'error': !isSuccess }">
            {{ alertMessage }}
        </div>
        
        <div class="container" id="container" ref="container">
            <div class="form-container sign-up-container">
                <form @submit="handleRegister">
                    <h1>注册账号</h1>
                    <span>请输入您的信息</span>
                    <input 
                        type="text" 
                        placeholder="用户名" 
                        v-model="registerForm.username"
                        :disabled="isLoading"
                    />
                    <input 
                        type="password" 
                        placeholder="密码" 
                        v-model="registerForm.password"
                        :disabled="isLoading"
                    />
                    <input 
                        type="password" 
                        placeholder="确认密码" 
                        v-model="registerForm.confirmPassword"
                        :disabled="isLoading"
                    />
                    <div class="select-container">
                        <select v-model="registerForm.role" :disabled="isLoading">
                            <option v-for="option in roleOptions" :key="option.value" :value="option.value">
                                {{ option.label }}
                            </option>
                        </select>
                    </div>
                    <button type="submit" :disabled="isLoading">
                        {{ isLoading ? '处理中...' : '注册' }}
                    </button>
                </form>
            </div>

            <div class="form-container sign-in-container">
                <form @submit="handleLogin">
                    <h1>登录</h1>
                    <input 
                        type="text" 
                        placeholder="用户名" 
                        v-model="loginForm.username"
                        :disabled="isLoading"
                    />
                    <input 
                        type="password" 
                        placeholder="密码" 
                        v-model="loginForm.password"
                        :disabled="isLoading"
                    />
                    <button type="submit" :disabled="isLoading">
                        {{ isLoading ? '处理中...' : '登录' }}
                    </button>
                </form>
            </div>
            
            <div class="overlay-container">
                <div class="overlay">
                    <div class="overlay-panel overlay-left">
                        <h1>欢迎回来!</h1>
                        <p>一起学习进步</p>
                        <button class="ghost" id="signIn" type="button">登录</button>
                    </div>
                    <div class="overlay-panel overlay-right">
                        <h1>没有账号？</h1>
                        <p>欢迎注册</p>
                        <button class="ghost" id="signUp" type="button">注册</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Montserrat:400,800');
* {
    box-sizing: border-box;
}
body {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    font-family: 'Montserrat', sans-serif;
    height: 100vh;
    margin: -20px 0 50px;
    background: #94dab8;
    background-image: linear-gradient(to bottom right, #91defe, #99c0f9, #bdb6ec, #d7b3e3, #efb3d5, #94dab8);
}
h1 {
    font-weight: bold;
    margin: 0;
}
h2 {
    text-align: center;
    font-size: 2.5rem;
    font-weight: normal;
    margin-bottom: 1.5rem;
    color: #333;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}
p {
    font-size: 14px;
    font-weight: 100;
    line-height: 20px;
    letter-spacing: 0.5px;
    margin: 20px 0 30px;
}
span {
    font-size: 12px;
}
a {
    color: #333;
    font-size: 14px;
    text-decoration: none;
    margin: 15px 0;
}
button {
    border-radius: 20px;
    border: 1px solid #4dc189;
    background-color: #4dc189;
    color: #FFFFFF;
    font-size: 12px;
    font-weight: bold;
    padding: 12px 45px;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: transform 80ms ease-in;
}
button:active {
    transform: scale(0.95);
}
button:focus {
    outline: none;
}
button.ghost {
    background-color: transparent;
    border-color: #FFFFFF;
}
form {
    background-color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    padding: 0 50px;
    height: 100%;
    text-align: center;
    color: #333; /* 将字体颜色改为黑色 */
}
input {
    background-color: #eee; /* 调整输入框背景颜色 */
    border: none; /* 移除边框 */
    padding: 12px 15px;
    margin: 8px 0;
    width: 100%;
    border-radius: 5px;
    color: #333; /* 将输入框字体颜色改为黑色 */
}
input:focus,
input:hover {
    outline: none;
    background-color: #fff;
    box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.1); /* 调整阴影颜色 */
}
.container {
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25),
        0 10px 10px rgba(0, 0, 0, 0.22);
    position: relative;
    overflow: hidden;
    width: 768px;
    max-width: 100%;
    min-height: 480px;
}
.form-container {
    position: absolute;
    top: 0;
    height: 100%;
    transition: all 0.6s ease-in-out;
}
.sign-in-container {
    left: 0;
    width: 50%;
    z-index: 2;
}
.container.right-panel-active .sign-in-container {
    transform: translateX(100%);
}
.sign-up-container {
    left: 0;
    width: 50%;
    opacity: 0;
    z-index: 1;
}
.container.right-panel-active .sign-up-container {
    transform: translateX(100%);
    opacity: 1;
    z-index: 5;
    animation: show 0.6s;
}
@keyframes show {
    0%,
    49.99% {
        opacity: 0;
        z-index: 1;
    }
    50%,
    100% {
        opacity: 1;
        z-index: 5;
    }
}
.overlay-container {
    position: absolute;
    top: 0;
    left: 50%;
    width: 50%;
    height: 100%;
    overflow: hidden;
    transition: transform 0.6s ease-in-out;
    z-index: 100;
}
.container.right-panel-active .overlay-container {
    transform: translateX(-100%);
}
.overlay {
    background: #4dc189;
    background: -webkit-linear-gradient(to right, #4dc189, #4dc189);
    background: linear-gradient(to right, #4dc189, #4dc189);
    background-repeat: no-repeat;
    background-size: cover;
    background-position: 0 0;
    color: #FFFFFF;
    position: relative;
    left: -100%;
    height: 100%;
    width: 200%;
    transform: translateX(0);
    transition: transform 0.6s ease-in-out;
}
.container.right-panel-active .overlay {
    transform: translateX(50%);
}
.overlay-panel {
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    padding: 0 40px;
    text-align: center;
    top: 0;
    height: 100%;
    width: 50%;
    transform: translateX(0);
    transition: transform 0.6s ease-in-out;
}
.overlay-left {
    transform: translateX(-20%);
}
.container.right-panel-active .overlay-left {
    transform: translateX(0);
}
.overlay-right {
    right: 0;
    transform: translateX(0);
}
.container.right-panel-active .overlay-right {
    transform: translateX(20%);
}
.social-container {
    margin: 20px 0;
}
.social-container a {
    border: 1px solid #DDDDDD;
    border-radius: 50%;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    margin: 0 5px;
    height: 40px;
    width: 40px;
}

/* 警告消息样式 */
.alert {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 10px 20px;
    border-radius: 5px;
    color: white;
    font-weight: bold;
    z-index: 1000;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    animation: fadeIn 0.3s, fadeOut 0.5s 2.5s;
    min-width: 300px;
    text-align: center;
}

.success {
    background-color: #4CAF50;
}

.error {
    background-color: #F44336;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

@keyframes fadeOut {
    from {opacity: 1;}
    to {opacity: 0;}
}

/* 下拉选择框样式 */
.select-container {
    width: 100%;
    margin: 8px 0;
}

select {
    width: 100%;
    background-color: #eee;
    border: none;
    border-radius: 5px;
    padding: 12px 15px;
    color: #333;
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    cursor: pointer;
    background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24'%3E%3Cpath fill='%23333' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 10px center;
    background-size: 16px;
}

select:focus,
select:hover {
    outline: none;
    background-color: #fff;
    box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.1);
}

/* 禁用状态 */
button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

input:disabled,
select:disabled {
    background-color: #f5f5f5;
    cursor: not-allowed;
    opacity: 0.7;
}
</style>
