"""
q2_memory.py
-----------
Desafío de Ingeniero de Datos - Pregunta 2: Solución Optimizada para Memoria

Autor: Diego Mendez
Fecha: 21-11-2025
Descripción:
    Extrae y cuenta las ocurrencias de emojis en todos los tweets usando
    procesamiento en streaming para minimizar el uso de memoria. Solo se
    almacenan en memoria los conteos de emojis, no el contenido completo
    del tweet.

Características de Rendimiento:
    - Complejidad de Tiempo: O(n * m) donde n=tweets, m=longitud promedio del contenido
    - Complejidad de Espacio: O(e) donde e=emojis únicos (~100-1000)
    - Tiempo de ejecución esperado: ~12-14s para 117K tweets
    - Uso de Memoria: ~5-10MB

Dependencias:
    - regex >= 2023.0.0 (para propiedades Unicode)

Referencias:
    - Estándar Unicode Emoji: https://unicode.org/reports/tr51/
    - Especificación del desafío: Ver sección 2 de README.md
"""

from typing import List, Tuple
from collections import Counter
import json
import regex


# Precompilar patrón regex (compartido con q2_time.py)
EMOJI_PATTERN = regex.compile(
    r'[\p{Emoji_Presentation}\p{Extended_Pictographic}]'
    r'(?:\uFE0F)?'
    r'(?:\u200d[\p{Emoji_Presentation}\p{Extended_Pictographic}]\uFE0F?)*',
    flags=regex.UNICODE
)


def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Identifica los 10 emojis más utilizados usando procesamiento en streaming.
    
    Esta implementación prioriza el uso mínimo de memoria procesando los tweets
    línea por línea y manteniendo solo los conteos agregados de emojis. El
    contenido del tweet nunca se almacena completo en memoria.
    
    Algoritmo:
        1. Leer el archivo línea por línea
        2. Extraer el campo 'content' de cada objeto JSON
        3. Aplicar el patrón regex de emojis
        4. Actualizar el Counter de forma incremental
        5. Retornar el top 10 después de procesar todas las líneas
    
    Argumentos:
        file_path: Ruta del archivo JSON delimitado por líneas que contiene tweets
        
    Retorna:
        Lista de tuplas con pares (emoji, conteo) ordenados por frecuencia.
        Ejemplo: [('🙏', 7286), ('😊', 3072), ...]
        
    Excepciones:
        FileNotFoundError: Si la ruta especificada no existe
        json.JSONDecodeError: Si falla el parseo JSON (omisión con try/except)
        
    Notas Técnicas:
        - Algoritmo de una sola pasada (streaming)
        - Counter usa espacio O(1) por emoji único
        - Típicamente hay entre 100 y 1000 emojis únicos
        - El uso de memoria está dominado por el Counter, no por el contenido
          del tweet
    """
    # Inicializar contador para agregación incremental
    emoji_counter = Counter()
    
    # Procesamiento en streaming: leer archivo línea por línea
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                # Parsear línea JSON
                tweet = json.loads(line.strip())
                
                # Extraer contenido, dando prioridad a 'content' sobre 'renderedContent'
                content = tweet.get('content', '') or tweet.get('renderedContent', '')
                
                if content:
                    # Extraer emojis usando el patrón precompilado
                    emojis = EMOJI_PATTERN.findall(content)
                    # Actualizar contador incrementalmente (O(1) por emoji)
                    emoji_counter.update(emojis)
                    
            except (json.JSONDecodeError, KeyError):
                # Omitir líneas mal formadas
                continue
    
    # Retornar los 10 emojis más comunes
    return emoji_counter.most_common(10)
