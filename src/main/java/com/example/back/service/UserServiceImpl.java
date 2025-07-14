package com.example.back.service;

import com.example.back.entity.User;
import com.example.back.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

/**
 * 用户服务接口的实现类。
 * 提供了用户实体的CRUD操作。
 */
@Service
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;

    /**
     * 构造函数，通过依赖注入获取UserRepository实例。
     * @param userRepository 用户数据仓库
     */
    @Autowired
    public UserServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    /**
     * 根据ID查找用户。
     * @param id 用户ID。
     * @return 包含用户的Optional，如果找不到则为空。
     */
    @Override
    public Optional<User> findById(Long id) {
        return userRepository.findById(id);
    }

    /**
     * 根据用户名查找用户。
     * @param username 用户名。
     * @return 包含用户的Optional，如果找不到则为空。
     */
    @Override
    public Optional<User> findByUsername(String username) {
        return userRepository.findByUsername(username);
    }

    /**
     * 查找所有用户。
     * @return 所有用户的列表。
     */
    @Override
    public List<User> findAll() {
        return userRepository.findAll();
    }

    /**
     * 保存用户。
     * @param user 要保存的用户实体。
     * @return 保存后的用户实体。
     */
    @Override
    public User save(User user) {
        return userRepository.save(user);
    }

    /**
     * 根据ID删除用户。
     * @param id 要删除的用户ID。
     */
    @Override
    public void deleteById(Long id) {
        userRepository.deleteById(id);
    }
}
