package com.example.back.service;

import com.example.back.dto.PresentationCreateRequest;
import com.example.back.dto.PresentationDto;
import com.example.back.entity.Presentation;
import com.example.back.entity.User;

import java.util.List;
import java.util.Optional;

/**
 * 演示文稿服务接口。
 * 定义了演示文稿相关的业务操作，包括创建、查询、更新、删除以及参会者管理。
 */
public interface PresentationService {
    /**
     * 创建新的演示文稿。
     * @param request 包含演示文稿创建信息的请求对象。
     * @param currentUser 当前用户，作为演示文稿的创建者。
     * @return 创建成功的演示文稿实体。
     */
    Presentation createPresentation(PresentationCreateRequest request, User currentUser);

    /**
     * 根据ID获取演示文稿的DTO。
     * @param id 演示文稿ID。
     * @return 包含演示文稿DTO的Optional，如果找不到则为空。
     */
    Optional<PresentationDto> getPresentationById(Long id);

    /**
     * 根据主讲人获取演示文稿列表。
     * @param speaker 主讲人用户实体。
     * @return 主讲人创建的演示文稿DTO列表。
     */
    List<PresentationDto> getPresentationsBySpeaker(User speaker);

    /**
     * 根据组织者获取演示文稿列表。
     * @param organizer 组织者用户实体。
     * @return 组织者创建的演示文稿DTO列表。
     */
    List<PresentationDto> getPresentationsByOrganizer(User organizer);

    /**
     * 获取所有演示文稿列表。
     * @return 所有演示文稿的DTO列表。
     */
    List<PresentationDto> getAllPresentations();

    /**
     * 更新演示文稿信息。
     * @param id 演示文稿ID。
     * @param request 包含更新信息的请求对象。
     * @param currentUser 当前用户，用于权限验证。
     * @return 更新后的演示文稿DTO。
     */
    PresentationDto updatePresentation(Long id, PresentationCreateRequest request, User currentUser);

    /**
     * 删除演示文稿。
     * @param id 演示文稿ID。
     * @param currentUser 当前用户，用于权限验证。
     */
    void deletePresentation(Long id, User currentUser);

    /**
     * 注册参会者到指定演示文稿。
     * @param presentationId 演示文稿ID。
     * @param attendee 参会者用户实体。
     */
    void registerAttendee(Long presentationId, User attendee);

    /**
     * 从指定演示文稿中取消注册参会者。
     * @param presentationId 演示文稿ID。
     * @param attendee 参会者用户实体。
     */
    void unregisterAttendee(Long presentationId, User attendee);

    /**
     * 获取指定演示文稿的所有参会者。
     * @param presentationId 演示文稿ID。
     * @return 参会者用户列表。
     */
    List<User> getAttendees(Long presentationId);
}
