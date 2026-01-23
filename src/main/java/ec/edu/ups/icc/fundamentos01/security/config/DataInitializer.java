package ec.edu.ups.icc.fundamentos01.security.config;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import ec.edu.ups.icc.fundamentos01.security.models.RoleEntity;
import ec.edu.ups.icc.fundamentos01.security.models.RoleName;
import ec.edu.ups.icc.fundamentos01.security.repository.RoleRepository;

@Component
public class DataInitializer implements CommandLineRunner {

    private final RoleRepository roleRepository;

    public DataInitializer(RoleRepository roleRepository) {
        this.roleRepository = roleRepository;
    }

    @Override
    public void run(String... args) {
        seedRole(RoleName.ROLE_USER, "Usuario estándar");
        seedRole(RoleName.ROLE_ADMIN, "Administrador con permisos completos");
        seedRole(RoleName.ROLE_MODERATOR, "Moderador");
    }

    private void seedRole(RoleName name, String description) {
        roleRepository.findByName(name)
                .orElseGet(() -> roleRepository.save(new RoleEntity(name, description)));
    }
}
