package ec.edu.ups.icc.fundamentos01.categories.service;

import java.util.List;

import org.springframework.stereotype.Service;

import ec.edu.ups.icc.fundamentos01.categories.dtos.CategoryCreateDto;
import ec.edu.ups.icc.fundamentos01.categories.dtos.CategoryResponseDto;
import ec.edu.ups.icc.fundamentos01.categories.entity.CategoryEntity;
import ec.edu.ups.icc.fundamentos01.categories.mappers.CategoryMapper;
import ec.edu.ups.icc.fundamentos01.categories.reporitory.CategoryRepository;

@Service
public class CategoryServiceImpl implements CategoryService {

    private final CategoryRepository categoryRepository;

    public CategoryServiceImpl(CategoryRepository categoryRepository) {
        this.categoryRepository = categoryRepository;
    }

    @Override
    public List<CategoryResponseDto> findAll() {
        return categoryRepository.findAll()
                .stream()
                .map(CategoryMapper::toResponseDto)
                .toList();
    }

    @Override
    public CategoryResponseDto save(CategoryCreateDto createDto) {
        // Idempotencia: si ya existe la categoría por nombre, retornamos la existente
        return categoryRepository.findByNameIgnoreCase(createDto.name)
                .map(CategoryMapper::toResponseDto)
                .orElseGet(() -> {
                    var categoryEntity = new CategoryEntity();
                    categoryEntity.setName(createDto.name);
                    categoryEntity.setDescription(createDto.description);
                    CategoryEntity saved = categoryRepository.save(categoryEntity);
                    return CategoryMapper.toResponseDto(saved);
                });
    }

}
