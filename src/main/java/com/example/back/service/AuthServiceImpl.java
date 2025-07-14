package com.example.back.service;

import com.example.back.dto.AuthResponse;
import com.example.back.dto.UserLoginRequest;
import com.example.back.dto.UserRegisterRequest;
import com.example.back.entity.User;
import com.example.back.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.time.LocalDateTime;

/**
 * 认证服务的实现类。
 * 负责处理用户注册和登录的业务逻辑。
 */
@Service
public class AuthServiceImpl implements AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    /**
     * 构造函数，通过依赖注入获取UserRepository和PasswordEncoder实例。
     * @param userRepository 用户数据仓库
     * @param passwordEncoder 密码编码器
     */
    @Autowired
    public AuthServiceImpl(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    /**
     * 注册新用户。
     * 检查用户名和邮箱是否已存在，然后对密码进行编码并保存用户。
     * @param request 包含用户注册信息的请求对象。
     * @return 注册成功的用户实体。
     * @throws RuntimeException 如果用户名或邮箱已存在。
     */
    @Override
    public User register(UserRegisterRequest request) {
        if (userRepository.findByUsername(request.getUsername()).isPresent()) {
            throw new RuntimeException("Username already exists"); // Custom exception later
        }
        if (request.getEmail() != null && userRepository.findByEmail(request.getEmail()).isPresent()) {
            throw new RuntimeException("Email already exists"); // Custom exception later
        }

        User user = new User();
        user.setUsername(request.getUsername());
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        user.setEmail(request.getEmail());
        user.setRole(request.getRole());
        user.setCreatedAt(LocalDateTime.now());
        return userRepository.save(user);
    }

    /**
     * 用户登录。
     * 验证用户凭据，并生成认证令牌。
     * @param request 包含用户登录凭据的请求对象。
     * @return 包含认证令牌和用户信息的响应对象。
     * @throws RuntimeException 如果凭据无效。
     */
    @Override
    public AuthResponse login(UserLoginRequest request) {
        User user = userRepository.findByUsername(request.getUsername())
                .orElseThrow(() -> new RuntimeException("Invalid credentials")); // Custom exception later

        if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            throw new RuntimeException("Invalid credentials"); // Custom exception later
        }

        // String token = jwtUtil.generateToken(user.getUsername(), user.getRole().name());
        String token = "dummy_jwt_token"; // Placeholder
        return new AuthResponse(token, user.getUsername(), user.getRole().name());
    }
}
