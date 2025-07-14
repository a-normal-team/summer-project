package com.example.back.service;

import com.example.back.dto.AuthResponse;
import com.example.back.dto.UserLoginRequest;
import com.example.back.dto.UserRegisterRequest;
import com.example.back.entity.User;

/**
 * 认证服务接口。
 * 定义了用户注册和登录操作。
 */
public interface AuthService {
    /**
     * 注册新用户。
     * @param request 包含用户注册信息的请求对象。
     * @return 注册成功的用户实体。
     */
    User register(UserRegisterRequest request);

    /**
     * 用户登录。
     * @param request 包含用户登录凭据的请求对象。
     * @return 包含认证令牌和用户信息的响应对象。
     */
    AuthResponse login(UserLoginRequest request);
}
