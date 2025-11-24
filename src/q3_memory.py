""" 
q3_memory.py
-----------
Data Engineer Challenge - Question 3: Memory-Optimized Solution

Author: Diego Mendez
Date: 21-11-2025
Descripción:
    Identifica los 10 usuarios más influyentes basados en la cantidad de 
    menciones usando un procesamiento en streaming que minimiza el uso 
    de memoria. Procesa la información estructurada del campo 
    mentionedUsers del JSON.

Características de rendimiento:
    - Complejidad temporal: O(n) en un recorrido único (streaming)
    - Complejidad espacial: O(u) donde u = usuarios únicos mencionados
    - Tiempo estimado de ejecución: ~5-6s para 117K tweets
    - Uso de memoria: ~5-10MB

Dependencias:
    - Solo librerías estándar de Python

Referencias:
    - Diccionario de datos de Twitter: https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary
    - Especificación del reto: ver sección 3 del README.md
"""

from typing import List, Tuple
from collections import Counter
import json


def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Identifica los 10 usuarios más mencionados utilizando procesamiento en streaming.
    
    Esta implementación lee el archivo línea por línea para minimizar el uso 
    de memoria. Solo se mantiene un contador agregado de menciones, no los 
    tweets completos.
    
    Algoritmo:
        1. Leer el archivo línea por línea (streaming)
        2. Parsear cada línea JSON y extraer el arreglo mentionedUsers
        3. Recorrer los objetos de mención y extraer usernames
        4. Actualizar el Counter de forma incremental
        5. Retornar el top 10 al finalizar el procesamiento
    
    Args:
        file_path: Ruta del archivo JSON delimitado por nuevas líneas
        
    Returns:
        Lista de tuplas (username, cantidad_de_menciones) ordenadas por frecuencia.
        Ejemplo: [('narendramodi', 2265), ('Kisanektamorcha', 1840), ...]
        
    Excepciones:
        FileNotFoundError: Si el archivo no existe
        json.JSONDecodeError: Si ocurre un error al parsear JSON (se omite esa línea)
        
    Notas técnicas:
        - Algoritmo de una sola pasada
        - Counter utiliza O(1) por usuario único
        - Usuarios únicos esperados: 1000-10000
        - La memoria la domina el Counter, no los tweets
        - Maneja arreglos mentionedUsers vacíos o ausentes
    """
    # Inicializa el contador para agregación incremental
    mention_counter = Counter()
    
    # Procesamiento en streaming: leer el archivo línea por línea
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                # Parsear la línea JSON
                tweet = json.loads(line.strip())
                
                # Extraer el arreglo mentionedUsers (puede no existir o estar vacío)
                mentioned_users = tweet.get('mentionedUsers', [])
                
                # Procesar si el arreglo no está vacío
                if mentioned_users:
                    for user in mentioned_users:
                        # Validar estructura del objeto de usuario
                        if isinstance(user, dict) and 'username' in user:
                            username = user['username']
                            # Ignorar cadenas vacías
                            if username:
                                mention_counter[username] += 1
                
            except (json.JSONDecodeError, KeyError, TypeError):
                # Omitir líneas mal formadas
                continue
    
    # Retornar los 10 usuarios más mencionados
    return mention_counter.most_common(10)
