package com.example.back.service;

import com.example.back.entity.User;

import java.util.List;
import java.util.Optional;

/**
 * 用户服务接口。
 * 定义了用户相关的业务操作。
 */
public interface UserService {
    /**
     * 根据ID查找用户。
     * @param id 用户ID。
     * @return 包含用户的Optional，如果找不到则为空。
     */
    Optional<User> findById(Long id);

    /**
     * 根据用户名查找用户。
     * @param username 用户名。
     * @return 包含用户的Optional，如果找不到则为空。
     */
    Optional<User> findByUsername(String username);

    /**
     * 查找所有用户。
     * @return 所有用户的列表。
     */
    List<User> findAll();

    /**
     * 保存用户。
     * @param user 要保存的用户实体。
     * @return 保存后的用户实体。
     */
    User save(User user);

    /**
     * 根据ID删除用户。
     * @param id 要删除的用户ID。
     */
    void deleteById(Long id);
}
