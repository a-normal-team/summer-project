<template>
  <div class="register-container">
    <h2>用户注册</h2>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="username">用户名:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="password">密码:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <div class="form-group">
        <label for="confirmPassword">确认密码:</label>
        <input type="password" id="confirmPassword" v-model="confirmPassword" required />
      </div>
      <div class="form-group">
        <label for="role">角色:</label>
        <select id="role" v-model="role">
          <option value="listener">听众</option>
          <option value="speaker">演讲者</option>
          <option value="organizer">组织者</option>
        </select>
      </div>
      <button type="submit">注册</button>
    </form>
    <p>已有账号？<router-link to="/login">立即登录</router-link></p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
// import axios from 'axios'; // 假设使用axios进行API请求

const username = ref('');
const password = ref('');
const confirmPassword = ref('');
const role = ref('listener'); // 默认角色为listener
const router = useRouter();

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    alert('两次输入的密码不一致！');
    return;
  }

  // try {
  //   const response = await axios.post('http://127.0.0.1:5000/api/auth/register', {
  //     username: username.value,
  //     password: password.value,
  //     role: role.value,
  //   });
  //   if (response.data.msg === 'User registered successfully') {
  //     alert('注册成功！请登录。');
  //     router.push('/login');
  //   } else {
  //     alert(response.data.msg || '注册失败');
  //   }
  // } catch (error: any) {
  //   alert(error.response?.data?.msg || '注册请求失败');
  // }
  console.log('注册尝试:', username.value, password.value, role.value);
  alert('注册成功！请登录。'); // 模拟注册成功
  router.push('/login');
};
</script>

<style scoped>
.register-container {
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
.form-group input[type="password"],
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background-color: #218838;
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
