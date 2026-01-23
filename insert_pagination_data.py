#!/usr/bin/env python3
"""
Script para insertar datos masivos de prueba en la base de datos
Práctica 10: Paginación de Datos con Spring Data JPA

Este script crea:
- 5 usuarios
- 3 categorías
- 1000+ productos distribuidos entre usuarios y categorías

Uso:
    python3 insert_pagination_data.py

Requisitos:
    pip install requests

Notas:
    - La aplicación Spring Boot debe estar ejecutándose en http://localhost:8080
    - Los productos tendrán precios variados entre $10 y $5000
    - Cada producto tendrá 1-3 categorías asignadas
"""

import sys
import time
import random
from typing import List, Dict, Any
import json

# Verificar que requests está instalado
try:
    import requests
except ImportError:
    print("ERROR: La librería 'requests' no está instalada.")
    print("Instala con: pip install requests")
    sys.exit(1)

# ==================== CONFIGURACIÓN ====================
BASE_URL = "http://localhost:8080"
API_USERS = f"{BASE_URL}/api/users"
API_CATEGORIES = f"{BASE_URL}/api/categories"
API_PRODUCTS = f"{BASE_URL}/api/products"

# Nombres de productos realistas
PRODUCT_NAMES = [
    "Laptop Gaming", "Monitor 4K", "Teclado Mecánico", "Ratón Gamer", "Mousepad XL",
    "Auriculares Inalámbricos", "Webcam Full HD", "Micrófono USB", "Hub USB-C",
    "Cargador Rápido", "Cable HDMI", "Adaptador USBC", "SSD 1TB", "RAM DDR4",
    "Refrigeración Líquida", "Ventilador RGB", "Fuente de Poder", "Carcasa Gaming",
    "Procesador Intel", "Tarjeta Gráfica", "Disco Duro 2TB", "Router 5G",
    "Impresora Láser", "Scanner Documento", "Monitor LED", "Escritorio Gamer",
    "Silla Gamer", "Iluminación RGB", "Control Remoto", "Power Bank",
    "Dock Multi-función", "Adaptador HDMI", "Cable Ethernet", "Panel Solar",
    "Batería Externa", "Cargador Inalámbrico", "Protector Pantalla", "Funda Laptop",
    "Mochila Antirobo", "Organizador Cables", "Pasta Térmica", "Limpiador Pantalla",
    "Alfombrilla Refrigerante", "Soporte Monitor", "Brazo Articulado", "Luz LED",
    "Concentrador USB", "Cable Lightning", "Adaptador USB", "Capacitores",
    "Resistencias", "Transistores", "Diodos", "Circuitos Integrados",
    "Placa Madre", "Procesador AMD", "Memoria Cache", "Acelerador Gráfico"
]

# Palabras para descripciones
DESCRIPTION_WORDS = [
    "Potente", "Rápido", "Eficiente", "Duradero", "Moderno",
    "Elegante", "Compacto", "Ligero", "Resistente", "Premium",
    "Profesional", "Gaming", "Portátil", "Silencioso", "Económico",
    "Alto rendimiento", "Bajo consumo", "Conectividad", "Sincronización",
    "Compatible", "Versátil", "Intuitivo", "Confiable", "Innovador",
    "Ergonómico", "Seguro", "Rápida carga", "Batería duradera", "Precisión"
]

# ==================== FUNCIONES AUXILIARES ====================

def print_section(title: str):
    """Imprime un encabezado de sección"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_status(status: str, message: str):
    """Imprime estado de operación"""
    colors = {
        "OK": "\033[92m",      # Verde
        "ERROR": "\033[91m",   # Rojo
        "INFO": "\033[94m",    # Azul
        "WARNING": "\033[93m", # Amarillo
        "RESET": "\033[0m"     # Reset
    }
    color = colors.get(status, colors["RESET"])
    print(f"{color}[{status}]{colors['RESET']} {message}")

def test_connection():
    """Verifica que la aplicación esté disponible"""
    print_section("VERIFICANDO CONEXIÓN")
    try:
        response = requests.get(f"{BASE_URL}/actuator/health", timeout=5)
        if response.status_code == 200:
            print_status("OK", "Conexión establecida con la aplicación")
            return True
        else:
            print_status("ERROR", f"Aplicación retornó status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_status("ERROR", f"No se puede conectar a {BASE_URL}")
        print_status("INFO", "Asegúrese de que la aplicación Spring Boot está ejecutándose")
        return False
    except Exception as e:
        print_status("ERROR", f"Error al conectar: {str(e)}")
        return False

# ==================== CREACIÓN DE DATOS ====================

def create_users() -> List[int]:
    """Crea 5 usuarios de prueba"""
    print_section("CREANDO USUARIOS")
    
    users = [
        {"name": "Juan Pérez", "email": "juan.perez@email.com", "password": "password123"},
        {"name": "María García", "email": "maria.garcia@email.com", "password": "password123"},
        {"name": "Carlos López", "email": "carlos.lopez@email.com", "password": "password123"},
        {"name": "Ana Martínez", "email": "ana.martinez@email.com", "password": "password123"},
        {"name": "Roberto Díaz", "email": "roberto.diaz@email.com", "password": "password123"},
    ]
    
    user_ids = []
    for user_data in users:
        try:
            response = requests.post(API_USERS, json=user_data, timeout=10)
            if response.status_code in [200, 201]:
                user = response.json()
                user_id = user.get("id")
                user_ids.append(user_id)
                print_status("OK", f"Usuario creado: {user_data['name']} (ID: {user_id})")
            else:
                print_status("WARNING", f"No se pudo crear usuario {user_data['name']}: {response.status_code}")
        except Exception as e:
            print_status("ERROR", f"Error creando usuario {user_data['name']}: {str(e)}")
    
    print_status("INFO", f"Total usuarios creados: {len(user_ids)}")
    return user_ids

def create_categories() -> List[int]:
    """Crea 3 categorías de prueba"""
    print_section("CREANDO CATEGORÍAS")
    
    categories = [
        {"name": "Electrónica", "description": "Dispositivos electrónicos y componentes"},
        {"name": "Gaming", "description": "Productos para videojuegos y gaming"},
        {"name": "Accesorios", "description": "Accesorios y periféricos para computadoras"},
    ]
    
    category_ids = []
    for category_data in categories:
        try:
            response = requests.post(API_CATEGORIES, json=category_data, timeout=10)
            if response.status_code in [200, 201]:
                category = response.json()
                category_id = category.get("id")
                category_ids.append(category_id)
                print_status("OK", f"Categoría creada: {category_data['name']} (ID: {category_id})")
            else:
                print_status("WARNING", f"No se pudo crear categoría {category_data['name']}: {response.status_code}")
        except Exception as e:
            print_status("ERROR", f"Error creando categoría {category_data['name']}: {str(e)}")
    
    print_status("INFO", f"Total categorías creadas: {len(category_ids)}")
    return category_ids

def generate_product_name() -> str:
    """Genera un nombre aleatorio de producto"""
    base_name = random.choice(PRODUCT_NAMES)
    suffix = random.choice(["Pro", "Ultra", "Max", "X", "2024", "Gaming", "Professional"])
    if random.random() > 0.5:
        return f"{base_name} {suffix}"
    return base_name

def generate_description() -> str:
    """Genera una descripción aleatoria de producto"""
    words = random.sample(DESCRIPTION_WORDS, k=random.randint(3, 6))
    return f"Producto {' y '.join(words)}. Ideal para profesionales y entusiastas."

def create_products(user_ids: List[int], category_ids: List[int], count: int = 1000) -> int:
    """Crea productos masivamente"""
    print_section(f"CREANDO {count} PRODUCTOS")
    
    created_count = 0
    failed_count = 0
    batch_size = 50
    
    for i in range(count):
        # Mostrar progreso cada 50 productos
        if i % batch_size == 0:
            print_status("INFO", f"Progreso: {i}/{count} productos creados")
        
        try:
            # Generar datos del producto
            product_data = {
                "name": generate_product_name(),
                "price": round(random.uniform(10, 5000), 2),
                "description": generate_description(),
                "userId": random.choice(user_ids),
                "categoryIds": random.sample(category_ids, k=random.randint(1, 3))
            }
            
            # Enviar solicitud
            response = requests.post(API_PRODUCTS, json=product_data, timeout=10)
            
            if response.status_code in [200, 201]:
                created_count += 1
            else:
                failed_count += 1
                if i < 10:  # Mostrar primeros errores
                    print_status("WARNING", f"Error creando producto {i+1}: Status {response.status_code}")
        
        except Exception as e:
            failed_count += 1
            if i < 10:  # Mostrar primeros errores
                print_status("WARNING", f"Error creando producto {i+1}: {str(e)}")
    
    print_status("OK", f"Productos creados: {created_count}/{count}")
    if failed_count > 0:
        print_status("WARNING", f"Productos no creados: {failed_count}")
    
    return created_count

# ==================== VERIFICACIÓN DE DATOS ====================

def verify_data():
    """Verifica que los datos se hayan insertado correctamente"""
    print_section("VERIFICANDO DATOS INSERTADOS")
    
    try:
        # Verificar usuarios
        response = requests.get(API_USERS, timeout=10)
        if response.status_code == 200:
            users = response.json()
            user_count = len(users) if isinstance(users, list) else users.get("totalElements", 0)
            print_status("OK", f"Total usuarios en BD: {user_count}")
        
        # Verificar categorías
        response = requests.get(API_CATEGORIES, timeout=10)
        if response.status_code == 200:
            categories = response.json()
            category_count = len(categories) if isinstance(categories, list) else categories.get("totalElements", 0)
            print_status("OK", f"Total categorías en BD: {category_count}")
        
        # Verificar productos (con paginación)
        response = requests.get(f"{API_PRODUCTS}?page=0&size=1", timeout=10)
        if response.status_code == 200:
            result = response.json()
            product_count = result.get("totalElements", 0)
            print_status("OK", f"Total productos en BD: {product_count}")
            
            # Información de paginación
            total_pages = result.get("totalPages", 0)
            page_size = result.get("size", 0)
            print_status("INFO", f"Paginación: {total_pages} páginas de {page_size} elementos")
    
    except Exception as e:
        print_status("ERROR", f"Error al verificar datos: {str(e)}")

# ==================== TESTS DE PAGINACIÓN ====================

def test_pagination_endpoints():
    """Prueba los diferentes endpoints de paginación"""
    print_section("PRUEBAS DE ENDPOINTS DE PAGINACIÓN")
    
    test_cases = [
        {
            "name": "Paginación básica (Página 0, tamaño 5)",
            "url": f"{API_PRODUCTS}?page=0&size=5",
            "expected_status": 200
        },
        {
            "name": "Paginación con ordenamiento (Precio descendente)",
            "url": f"{API_PRODUCTS}?page=0&size=10&sort=price,desc",
            "expected_status": 200
        },
        {
            "name": "Paginación Slice (mejor performance)",
            "url": f"{API_PRODUCTS}/slice?page=0&size=10",
            "expected_status": 200
        },
        {
            "name": "Búsqueda con filtros",
            "url": f"{API_PRODUCTS}/search?minPrice=100&maxPrice=500&page=0&size=5",
            "expected_status": 200
        },
    ]
    
    for test in test_cases:
        try:
            response = requests.get(test["url"], timeout=10)
            if response.status_code == test["expected_status"]:
                data = response.json()
                if "content" in data:
                    count = len(data.get("content", []))
                    print_status("OK", f"{test['name']}: {count} elementos retornados")
                else:
                    print_status("OK", f"{test['name']}: Respuesta recibida")
            else:
                print_status("ERROR", f"{test['name']}: Status {response.status_code}")
        except Exception as e:
            print_status("ERROR", f"{test['name']}: {str(e)}")

# ==================== FUNCIÓN PRINCIPAL ====================

def main():
    """Ejecuta el script principal"""
    print("\n" + "="*60)
    print("  INSERTOR DE DATOS PARA PAGINACIÓN - PRÁCTICA 10")
    print("  Spring Boot + PostgreSQL")
    print("="*60)
    
    # Verificar conexión
    if not test_connection():
        sys.exit(1)
    
    # Crear datos
    user_ids = create_users()
    if not user_ids:
        print_status("ERROR", "No se pudieron crear usuarios")
        sys.exit(1)
    
    category_ids = create_categories()
    if not category_ids:
        print_status("ERROR", "No se pudieron crear categorías")
        sys.exit(1)
    
    # Crear productos (1000+ para pruebas de paginación)
    print_section("CREACIÓN MASIVA DE PRODUCTOS")
    print_status("INFO", "Esto puede tomar algunos minutos...")
    start_time = time.time()
    
    created = create_products(user_ids, category_ids, count=1000)
    
    elapsed_time = time.time() - start_time
    print_status("INFO", f"Tiempo total: {elapsed_time:.2f} segundos")
    print_status("INFO", f"Velocidad: {created/elapsed_time:.0f} productos/segundo")
    
    # Verificar datos
    verify_data()
    
    # Probar endpoints
    test_pagination_endpoints()
    
    # Resumen final
    print_section("RESUMEN")
    print_status("OK", "Script completado exitosamente")
    print_status("INFO", "Ahora puede probar los endpoints de paginación:")
    print()
    print("  Paginación básica:")
    print(f"    curl '{BASE_URL}/api/products?page=0&size=10'")
    print()
    print("  Con ordenamiento:")
    print(f"    curl '{BASE_URL}/api/products?page=0&size=10&sort=price,desc'")
    print()
    print("  Con Slice:")
    print(f"    curl '{BASE_URL}/api/products/slice?page=0&size=10'")
    print()
    print("  Con filtros:")
    print(f"    curl '{BASE_URL}/api/products/search?minPrice=100&maxPrice=500&page=0&size=5'")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_status("WARNING", "Script interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print_status("ERROR", f"Error inesperado: {str(e)}")
        sys.exit(1)
