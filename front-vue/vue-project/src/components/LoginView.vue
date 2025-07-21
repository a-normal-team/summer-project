<script setup>
import { ref, onMounted } from 'vue';

const container = ref(null);

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
        <div class="container" id="container" ref="container">
            <div class="form-container sign-up-container">
                <form action="#">
                    <h1>注册账号</h1>
                    <span>请输入</span>
                    <input type="text" placeholder="Name" />
                    <input type="password" placeholder="Password" />
                    <input type="password" placeholder="Confirm Password" />
                    <input type="text" placeholder="Role" />
                    <button>注册</button>
                </form>
            </div>

            <div class="form-container sign-in-container">
                <form action="#">
                    <h1>登录</h1>
                    <input type="text" placeholder="Name" />
                    <input type="password" placeholder="Password" />
                    <button>登录</button>
                </form>
            </div>
            

            <div class="overlay-container">
                <div class="overlay">
                    <div class="overlay-panel overlay-left">
                        <h1>欢迎回来!</h1>
                        <p>一起学习进步</p>
                        <button class="ghost" id="signIn">登录</button>
                    </div>
                    <div class="overlay-panel overlay-right">
                        <h1>没有账号？</h1>
                        <p>欢迎注册</p>
                        <button class="ghost" id="signUp">注册</button>
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
</style>
