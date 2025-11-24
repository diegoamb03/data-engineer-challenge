"""
q1_memory.py
-----------
Desafío de Ingeniero de Datos - Pregunta 1: Solución Optimizada para Memoria

Autor: Diego Mendez
Fecha: 21-11-2025
Descripción:
    Identifica las 10 fechas con mayor volumen de tweets y determina
    el usuario más activo para cada una de esas fechas. Esta implementación
    prioriza un uso mínimo de memoria utilizando procesamiento en streaming.

Características de Rendimiento:
    - Complejidad de Tiempo: O(n) con una pasada en streaming
    - Complejidad de Espacio: O(d * u) donde d=fechas, u=usuarios únicos por fecha
    - Tiempo de ejecución esperado: ~4-5s para 117K tweets
    - Uso de Memoria: ~5-10MB

Dependencias:
    - Solo librerías estándar de Python

Referencias:
    - Especificación del desafío: Ver sección 1 de README.md
"""

from typing import List, Tuple
from datetime import datetime
from collections import defaultdict, Counter
import json


def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Calcula las 10 fechas con mayor volumen de tweets junto con el usuario 
    más activo en cada fecha.
    
    Esta implementación utiliza procesamiento en streaming para minimizar 
    el uso de memoria. Las estructuras de datos están optimizadas para 
    almacenar únicamente conteos agregados en lugar de datos completos 
    del tweet.
    
    Algoritmo:
        1. Leer el archivo línea por línea para evitar cargar todo el dataset
        2. Mantener un Counter para frecuencias por fecha
        3. Mantener un Counter anidado para frecuencias de usuario por fecha
        4. Extraer las 10 fechas principales y sus usuarios más activos
    
    Argumentos:
        file_path: Ruta al archivo JSON delimitado por líneas que contiene tweets
        
    Retorna:
        Lista de tuplas con pares (fecha, usuario) ordenados por volumen de tweets.
        Ejemplo: [(date(2021, 2, 24), 'narendramodi'), ...]
        
    Excepciones:
        FileNotFoundError: Si la ruta especificada no existe
        json.JSONDecodeError: Si falla el parseo de JSON (se omite con try/except)
        
    Notas Técnicas:
        - Usa Counter para operaciones de incremento O(1)
        - defaultdict(Counter) para estructura de conteo anidada
        - Algoritmo de una sola pasada para máxima eficiencia en memoria
        - Las líneas JSON mal formadas se omiten silenciosamente
    """
    
    # Inicializa las estructuras de datos para la agregación
    # Counter permite acceso O(1) e inicialización automática
    date_counts = Counter()
    
    # Estructura anidada: fecha -> {usuario: conteo}
    date_user_counts = defaultdict(Counter)
    
    # Procesamiento en streaming: leer el archivo línea por línea
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                # Parsear línea JSON
                tweet = json.loads(line)
                
                # Extraer fecha en forma de string
                date_str = tweet.get('date', '')
                if not date_str:
                    continue
                
                # Parsear fecha ISO 8601 y extraer componente de fecha
                # Soporta formatos 'Z' y '+00:00'
                date_obj = datetime.fromisoformat(
                    date_str.replace('Z', '+00:00')
                ).date()
                
                # Extraer nombre de usuario
                username = tweet.get('user', {}).get('username', '')
                if not username:
                    continue
                
                # Actualizar contadores de agregación
                date_counts[date_obj] += 1
                date_user_counts[date_obj][username] += 1
                
            except (json.JSONDecodeError, ValueError, KeyError):
                # Se omiten líneas mal formadas
                continue
    
    # Obtener las 10 fechas con mayor cantidad de tweets
    top_10_dates = [date for date, _ in date_counts.most_common(10)]
    
    # Para cada fecha, obtener el usuario con más tweets
    result = []
    for date_obj in top_10_dates:
        # most_common(1) devuelve [(usuario, conteo)]
        top_user = date_user_counts[date_obj].most_common(1)[0][0]
        result.append((date_obj, top_user))
    
    return result
