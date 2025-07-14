package com.example.back.service;

import com.example.back.dto.PresentationCreateRequest;
import com.example.back.dto.PresentationDto;
import com.example.back.entity.Presentation;
import com.example.back.entity.PresentationAttendee;
import com.example.back.entity.PresentationAttendeeId;
import com.example.back.entity.User;
import com.example.back.repository.PresentationAttendeeRepository;
import com.example.back.repository.PresentationRepository;
import com.example.back.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * 演示文稿服务接口的实现类。
 * 负责处理演示文稿的业务逻辑，包括创建、查询、更新、删除以及参会者管理。
 */
@Service
public class PresentationServiceImpl implements PresentationService {

    private final PresentationRepository presentationRepository;
    private final UserRepository userRepository;
    private final PresentationAttendeeRepository presentationAttendeeRepository;

    /**
     * 构造函数，通过依赖注入获取Repository实例。
     * @param presentationRepository 演示文稿数据仓库
     * @param userRepository 用户数据仓库
     * @param presentationAttendeeRepository 演示文稿参会者数据仓库
     */
    @Autowired
    public PresentationServiceImpl(PresentationRepository presentationRepository,
                                   UserRepository userRepository,
                                   PresentationAttendeeRepository presentationAttendeeRepository) {
        this.presentationRepository = presentationRepository;
        this.userRepository = userRepository;
        this.presentationAttendeeRepository = presentationAttendeeRepository;
    }

    /**
     * 创建新的演示文稿。
     * 验证主讲人和组织者是否存在，并检查当前用户是否有权限创建。
     * @param request 包含演示文稿创建信息的请求对象。
     * @param currentUser 当前用户，作为演示文稿的创建者。
     * @return 创建成功的演示文稿实体。
     * @throws RuntimeException 如果主讲人或组织者未找到，或当前用户无权限。
     */
    @Override
    @Transactional
    public Presentation createPresentation(PresentationCreateRequest request, User currentUser) {
        User speaker = userRepository.findById(request.getSpeakerId())
                .orElseThrow(() -> new RuntimeException("Speaker not found")); // Custom exception
        User organizer = userRepository.findById(request.getOrganizerId())
                .orElseThrow(() -> new RuntimeException("Organizer not found")); // Custom exception

        // Ensure current user has permission to create presentation for this speaker/organizer
        // For simplicity, assuming current user is either speaker or organizer, or an admin
        if (!currentUser.getId().equals(speaker.getId()) && !currentUser.getId().equals(organizer.getId()) && currentUser.getRole() != User.Role.ADMIN) {
            throw new RuntimeException("Unauthorized to create presentation for specified speaker/organizer"); // Custom exception
        }

        Presentation presentation = new Presentation();
        presentation.setTitle(request.getTitle());
        presentation.setDescription(request.getDescription());
        presentation.setSpeaker(speaker);
        presentation.setOrganizer(organizer);
        presentation.setStatus(Presentation.Status.DRAFT); // Initial status
        presentation.setCreatedAt(LocalDateTime.now());
        return presentationRepository.save(presentation);
    }

    /**
     * 根据ID获取演示文稿的DTO。
     * @param id 演示文稿ID。
     * @return 包含演示文稿DTO的Optional，如果找不到则为空。
     */
    @Override
    public Optional<PresentationDto> getPresentationById(Long id) {
        return presentationRepository.findById(id)
                .map(PresentationDto::new);
    }

    /**
     * 根据主讲人获取演示文稿列表。
     * @param speaker 主讲人用户实体。
     * @return 主讲人创建的演示文稿DTO列表。
     */
    @Override
    public List<PresentationDto> getPresentationsBySpeaker(User speaker) {
        return presentationRepository.findBySpeaker(speaker).stream()
                .map(PresentationDto::new)
                .collect(Collectors.toList());
    }

    /**
     * 根据组织者获取演示文稿列表。
     * @param organizer 组织者用户实体。
     * @return 组织者创建的演示文稿DTO列表。
     */
    @Override
    public List<PresentationDto> getPresentationsByOrganizer(User organizer) {
        return presentationRepository.findByOrganizer(organizer).stream()
                .map(PresentationDto::new)
                .collect(Collectors.toList());
    }

    /**
     * 获取所有演示文稿列表。
     * @return 所有演示文稿的DTO列表。
     */
    @Override
    public List<PresentationDto> getAllPresentations() {
        return presentationRepository.findAll().stream()
                .map(PresentationDto::new)
                .collect(Collectors.toList());
    }

    /**
     * 更新演示文稿信息。
     * 验证演示文稿是否存在，并检查当前用户是否有权限更新。
     * @param id 演示文稿ID。
     * @param request 包含更新信息的请求对象。
     * @param currentUser 当前用户，用于权限验证。
     * @return 更新后的演示文稿DTO。
     * @throws RuntimeException 如果演示文稿未找到，或当前用户无权限。
     */
    @Override
    @Transactional
    public PresentationDto updatePresentation(Long id, PresentationCreateRequest request, User currentUser) {
        Presentation presentation = presentationRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Presentation not found")); // Custom exception

        // Authorization check: Only speaker, organizer, or admin can update
        if (!currentUser.getId().equals(presentation.getSpeaker().getId()) &&
            !currentUser.getId().equals(presentation.getOrganizer().getId()) &&
            currentUser.getRole() != User.Role.ADMIN) {
            throw new RuntimeException("Unauthorized to update this presentation"); // Custom exception
        }

        User speaker = userRepository.findById(request.getSpeakerId())
                .orElseThrow(() -> new RuntimeException("Speaker not found"));
        User organizer = userRepository.findById(request.getOrganizerId())
                .orElseThrow(() -> new RuntimeException("Organizer not found"));

        presentation.setTitle(request.getTitle());
        presentation.setDescription(request.getDescription());
        presentation.setSpeaker(speaker);
        presentation.setOrganizer(organizer);
        // Status changes might be handled by separate methods or specific logic
        return new PresentationDto(presentationRepository.save(presentation));
    }

    /**
     * 删除演示文稿。
     * 验证演示文稿是否存在，并检查当前用户是否有权限删除。
     * 同时删除与演示文稿相关联的参会者记录。
     * @param id 演示文稿ID。
     * @param currentUser 当前用户，用于权限验证。
     * @throws RuntimeException 如果演示文稿未找到，或当前用户无权限。
     */
    @Override
    @Transactional
    public void deletePresentation(Long id, User currentUser) {
        Presentation presentation = presentationRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Presentation not found")); // Custom exception

        // Authorization check: Only organizer or admin can delete
        if (!currentUser.getId().equals(presentation.getOrganizer().getId()) &&
            currentUser.getRole() != User.Role.ADMIN) {
            throw new RuntimeException("Unauthorized to delete this presentation"); // Custom exception
        }

        // Delete associated attendees first due to foreign key constraints
        presentationAttendeeRepository.findByPresentation(presentation).forEach(presentationAttendeeRepository::delete);
        // Delete associated quizzes and their answers, feedback, discussions (cascading might be handled by JPA or manually)
        // For now, assuming manual deletion or cascade on Quiz, Feedback, etc.
        // quizRepository.findByPresentation(presentation).forEach(quiz -> {
        //     quizAnswerRepository.findByQuiz(quiz).forEach(quizAnswerRepository::delete);
        //     discussionRepository.findByQuizId(quiz.getId()).ifPresent(discussionRepository::delete);
        //     quizRepository.delete(quiz);
        // });
        // feedbackRepository.findByPresentation(presentation).forEach(feedbackRepository::delete);

        presentationRepository.delete(presentation);
    }

    /**
     * 注册参会者到指定演示文稿。
     * 验证演示文稿是否存在，并检查参会者是否已注册。
     * @param presentationId 演示文稿ID。
     * @param attendee 参会者用户实体。
     * @throws RuntimeException 如果演示文稿未找到，或参会者已注册。
     */
    @Override
    @Transactional
    public void registerAttendee(Long presentationId, User attendee) {
        Presentation presentation = presentationRepository.findById(presentationId)
                .orElseThrow(() -> new RuntimeException("Presentation not found")); // Custom exception

        if (presentationAttendeeRepository.findByPresentationAndAttendee(presentation, attendee).isPresent()) {
            throw new RuntimeException("Attendee already registered for this presentation"); // Custom exception
        }

        // PresentationAttendeeId id = new PresentationAttendeeId(presentationId, attendee.getId()); // No need to set ID explicitly for @IdClass
        PresentationAttendee presentationAttendee = new PresentationAttendee();
        presentationAttendee.setPresentation(presentation);
        presentationAttendee.setAttendee(attendee);
        presentationAttendee.setRegisteredAt(LocalDateTime.now());
        presentationAttendeeRepository.save(presentationAttendee);
    }

    /**
     * 从指定演示文稿中取消注册参会者。
     * 验证演示文稿和参会者注册信息是否存在。
     * @param presentationId 演示文稿ID。
     * @param attendee 参会者用户实体。
     * @throws RuntimeException 如果演示文稿未找到，或参会者未注册。
     */
    @Override
    @Transactional
    public void unregisterAttendee(Long presentationId, User attendee) {
        Presentation presentation = presentationRepository.findById(presentationId)
                .orElseThrow(() -> new RuntimeException("Presentation not found")); // Custom exception

        PresentationAttendee presentationAttendee = presentationAttendeeRepository.findByPresentationAndAttendee(presentation, attendee)
                .orElseThrow(() -> new RuntimeException("Attendee not registered for this presentation")); // Custom exception

        presentationAttendeeRepository.delete(presentationAttendee);
    }

    /**
     * 获取指定演示文稿的所有参会者。
     * @param presentationId 演示文稿ID。
     * @return 参会者用户列表。
     * @throws RuntimeException 如果演示文稿未找到。
     */
    @Override
    public List<User> getAttendees(Long presentationId) {
        Presentation presentation = presentationRepository.findById(presentationId)
                .orElseThrow(() -> new RuntimeException("Presentation not found")); // Custom exception

        return presentationAttendeeRepository.findByPresentation(presentation).stream()
                .map(PresentationAttendee::getAttendee)
                .collect(Collectors.toList());
    }
}
