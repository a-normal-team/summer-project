<template>
  <div class="login-container">
    <h2>用户登录</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">用户名:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="password">密码:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">登录</button>
    </form>
    <p>没有账号？<router-link to="/register">立即注册</router-link></p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
// import axios from 'axios'; // 假设使用axios进行API请求

const username = ref('');
const password = ref('');
const router = useRouter();

const handleLogin = async () => {
  // try {
  //   const response = await axios.post('http://127.0.0.1:5000/api/auth/login', {
  //     username: username.value,
  //     password: password.value,
  //   });
  //   if (response.data.access_token) {
  //     // 存储JWT令牌，例如使用localStorage或Pinia
  //     localStorage.setItem('access_token', response.data.access_token);
  //     alert('登录成功！');
  //     // 根据用户角色跳转到不同的仪表盘
  //     // 这里需要一个API来获取用户角色，或者在登录响应中包含角色信息
  //     router.push('/dashboard'); // 暂时跳转到通用仪表盘
  //   } else {
  //     alert(response.data.msg || '登录失败');
  //   }
  // } catch (error: any) {
  //   alert(error.response?.data?.msg || '登录请求失败');
  // }
  console.log('登录尝试:', username.value, password.value);
  alert('登录成功！'); // 模拟登录成功
  router.push('/dashboard'); // 暂时跳转到仪表盘页面
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input[type="text"],
.form-group input[type="password"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background-color: #0056b3;
}

p {
  margin-top: 20px;
}

p router-link {
  color: #007bff;
  text-decoration: none;
}

p router-link:hover {
  text-decoration: underline;
}
</style>
