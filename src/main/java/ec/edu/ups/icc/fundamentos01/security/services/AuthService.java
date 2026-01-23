package ec.edu.ups.icc.fundamentos01.security.services;

import java.util.HashSet;
import java.util.Set;
import java.util.stream.Collectors;

import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import ec.edu.ups.icc.fundamentos01.exceptions.domain.BadRequestException;
import ec.edu.ups.icc.fundamentos01.exceptions.domain.ConflictException;
import ec.edu.ups.icc.fundamentos01.security.dtos.AuthResponseDto;
import ec.edu.ups.icc.fundamentos01.security.dtos.LoginRequestDto;
import ec.edu.ups.icc.fundamentos01.security.dtos.RegisterRequestDto;
import ec.edu.ups.icc.fundamentos01.security.models.RoleEntity;
import ec.edu.ups.icc.fundamentos01.security.models.RoleName;
import ec.edu.ups.icc.fundamentos01.security.repository.RoleRepository;
import ec.edu.ups.icc.fundamentos01.security.utils.JwtUtil;
import ec.edu.ups.icc.fundamentos01.users.models.UserEntity;
import ec.edu.ups.icc.fundamentos01.users.repository.UserRepository;

@Service
public class AuthService {

    private final AuthenticationManager authenticationManager;
    private final UserRepository userRepository;
    private final RoleRepository roleRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;

    public AuthService(AuthenticationManager authenticationManager,
            UserRepository userRepository,
            RoleRepository roleRepository,
            PasswordEncoder passwordEncoder,
            JwtUtil jwtUtil) {
        this.authenticationManager = authenticationManager;
        this.userRepository = userRepository;
        this.roleRepository = roleRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtUtil = jwtUtil;
    }

    @Transactional(readOnly = true)
    public AuthResponseDto login(LoginRequestDto request) {
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getEmail(), request.getPassword()));
        SecurityContextHolder.getContext().setAuthentication(authentication);

        String token = jwtUtil.generateToken(authentication);
        UserDetailsImpl userDetails = (UserDetailsImpl) authentication.getPrincipal();
        Set<String> roles = userDetails.getAuthorities().stream()
                .map(auth -> auth.getAuthority())
                .collect(Collectors.toSet());

        return new AuthResponseDto(token, userDetails.getId(), userDetails.getName(), userDetails.getEmail(), roles);
    }

    @Transactional
    public AuthResponseDto register(RegisterRequestDto request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new ConflictException("El email ya está registrado");
        }

        UserEntity user = new UserEntity();
        user.setName(request.getName());
        user.setEmail(request.getEmail());
        user.setPassword(passwordEncoder.encode(request.getPassword()));

        RoleEntity roleUser = roleRepository.findByName(RoleName.ROLE_USER)
                .orElseThrow(() -> new BadRequestException("Rol por defecto no encontrado"));

        Set<RoleEntity> roles = new HashSet<>();
        roles.add(roleUser);
        user.setRoles(roles);

        user = userRepository.save(user);

        UserDetailsImpl userDetails = UserDetailsImpl.build(user);
        String token = jwtUtil.generateTokenFromUserDetails(userDetails);
        Set<String> roleNames = roles.stream().map(r -> r.getName().name()).collect(Collectors.toSet());

        return new AuthResponseDto(token, user.getId(), user.getName(), user.getEmail(), roleNames);
    }
}
