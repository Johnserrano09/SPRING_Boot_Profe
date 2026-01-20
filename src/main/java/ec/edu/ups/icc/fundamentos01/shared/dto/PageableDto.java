package ec.edu.ups.icc.fundamentos01.shared.dto;

import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;

/**
 * DTO para parámetros de paginación
 * Proporciona métodos helper para convertir a Pageable de Spring Data JPA
 */
public class PageableDto {

    private int page = 0;
    private int size = 10;
    private String[] sort = {"id"};

    // Constructores
    public PageableDto() {
    }

    public PageableDto(int page, int size, String[] sort) {
        this.page = page;
        this.size = size;
        this.sort = sort;
    }

    // Getters y setters
    public int getPage() {
        return page;
    }

    public void setPage(int page) {
        this.page = page;
    }

    public int getSize() {
        return size;
    }

    public void setSize(int size) {
        this.size = size;
    }

    public String[] getSort() {
        return sort;
    }

    public void setSort(String[] sort) {
        this.sort = sort;
    }

    // ============== MÉTODO HELPER ==============

    /**
     * Convierte a PageRequest de Spring Data JPA
     * Valida los parámetros antes de crear el Pageable
     */
    public Pageable toPageable() {
        validateParameters();
        return PageRequest.of(page, size, createSort());
    }

    /**
     * Valida los parámetros de paginación
     * @throws IllegalArgumentException si los parámetros son inválidos
     */
    private void validateParameters() {
        if (page < 0) {
            throw new IllegalArgumentException("La página debe ser mayor o igual a 0");
        }
        if (size < 1 || size > 100) {
            throw new IllegalArgumentException("El tamaño debe estar entre 1 y 100");
        }
    }

    /**
     * Crea el objeto Sort a partir del array de strings
     * Formato esperado: ["property,direction"] o ["property"]
     */
    private Sort createSort() {
        if (sort == null || sort.length == 0) {
            return Sort.by("id");
        }

        Sort.Order[] orders = new Sort.Order[sort.length];
        for (int i = 0; i < sort.length; i++) {
            String[] parts = sort[i].split(",");
            String property = parts[0];
            String direction = parts.length > 1 ? parts[1] : "asc";
            
            orders[i] = "desc".equalsIgnoreCase(direction) 
                ? Sort.Order.desc(property)
                : Sort.Order.asc(property);
        }
        
        return Sort.by(orders);
    }
}
