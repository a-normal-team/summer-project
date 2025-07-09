import React from 'react';

function Welcome() {
  return (
    <div className="welcome-container">
      <div className="welcome-content">
        <h1>欢迎使用演示Web项目</h1>
        <p>这是一个使用React和Express构建的全栈应用示例</p>
        <div className="features">
          <div className="feature-card">
            <h3>前端技术</h3>
            <p>使用React构建的现代化用户界面</p>
          </div>
          <div className="feature-card">
            <h3>后端技术</h3>
            <p>基于Express的RESTful API服务</p>
          </div>
          <div className="feature-card">
            <h3>简洁架构</h3>
            <p>前后端分离的应用架构设计</p>
          </div>
        </div>
        <button className="start-button">开始体验</button>
      </div>
    </div>
  );
}

export default Welcome;