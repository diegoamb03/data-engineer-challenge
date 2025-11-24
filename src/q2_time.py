"""
q2_time.py
---------
Desafío de Ingeniero de Datos - Pregunta 2: Solución Optimizada para Tiempo

Autor: Diego Mendez
Fecha: 21-11-2025
Descripción:
    Extrae y cuenta las ocurrencias de emojis en todos los tweets para
    identificar los 10 emojis más utilizados. Esta implementación usa un
    enfoque híbrido combinando DuckDB para un parseo JSON rápido con la
    librería regex de Python para patrones Unicode complejos de emojis.

Características de Rendimiento:
    - Complejidad de Tiempo: O(n * m) donde n=tweets, m=longitud promedio del contenido
    - Complejidad de Espacio: O(n) para almacenamiento de contenido
    - Tiempo de Ejecución Esperado: ~6-8s para 117K tweets
    - Uso de Memoria: ~100-150MB

Dependencias:
    - duckdb >= 0.9.0
    - regex >= 2023.0.0 (para propiedades Unicode)

Justificación Técnica:
    El motor SQL de DuckDB no puede manejar clases de propiedades Unicode
    (\p{Emoji}) necesarias para la detección precisa de emojis. Este enfoque
    híbrido usa DuckDB para I/O y parseo JSON (~4x más rápido que Python),
    luego aplica regex de Python para el reconocimiento Unicode avanzado.

Referencias:
    - Estándar Unicode Emoji: https://unicode.org/reports/tr51/
    - Especificación del Desafío: Ver sección 2 de README.md
"""

from typing import List, Tuple
from collections import Counter
import regex


# Precompilar patrón regex para rendimiento
# Explicación del patrón:
#   \p{Emoji_Presentation}: Caracteres con presentación de emoji por defecto
#   \p{Extended_Pictographic}: Caracteres pictográficos extendidos
#   \uFE0F: Selector de variación emoji (opcional)
#   \u200d: Unión de ancho cero para emojis compuestos (ej: familia)
EMOJI_PATTERN = regex.compile(
    r'[\p{Emoji_Presentation}\p{Extended_Pictographic}]'
    r'(?:\uFE0F)?'
    r'(?:\u200d[\p{Emoji_Presentation}\p{Extended_Pictographic}]\uFE0F?)*',
    flags=regex.UNICODE
)


def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Identifica los 10 emojis más frecuentemente utilizados en todos los tweets.
    
    Esta implementación híbrida combina el parseo rápido de JSON de DuckDB con
    la librería regex de Python para la detección precisa de emojis. DuckDB
    maneja el I/O y parseo JSON, mientras que regex maneja los patrones Unicode
    complejos, incluyendo secuencias ZWJ (Zero-Width Joiner).
    
    Algoritmo:
        1. Usar DuckDB para extraer rápidamente el campo de contenido del tweet
        2. Aplicar regex compatible con Unicode para detectar emojis
        3. Agregar conteos de emojis usando Counter
        4. Retornar el top 10 por frecuencia
    
    Argumentos:
        file_path: Ruta del archivo JSON delimitado por líneas con tweets
        
    Retorna:
        Lista de tuplas con pares (emoji, conteo) ordenados por frecuencia.
        Ejemplo: [('🙏', 7286), ('😊', 3072), ...]
        
    Excepciones:
        FileNotFoundError: Si la ruta especificada no existe
        ImportError: Si las librerías duckdb o regex no están instaladas
        
    Notas Técnicas:
        - Maneja los campos 'content' y 'renderedContent'
        - COALESCE asegura selección segura ante valores nulos
        - Secuencias ZWJ (ej: 👨‍👩‍👧) se tratan como un solo emoji
        - Los selectores de variación (FE0F) son manejados correctamente
    """
    import duckdb
    
    # Inicializar conexión DuckDB en memoria
    con = duckdb.connect(':memory:')
    
    # Query para extraer contenido usando el parser JSON optimizado de DuckDB
    query = f"""
        SELECT 
            COALESCE(content, renderedContent, '') as content
        FROM read_json_auto('{file_path}', format='newline_delimited')
        WHERE content IS NOT NULL 
           OR renderedContent IS NOT NULL
    """
    
    # Ejecutar query y obtener resultados como DataFrame
    result_df = con.execute(query).fetchdf()
    con.close()
    
    # Inicializar contador para agregación de emojis
    emoji_counter = Counter()
    
    # Aplicar patrón regex a cada contenido de tweet
    for content in result_df['content']:
        if content:
            # findall() retorna todas las coincidencias sin superposición
            emojis = EMOJI_PATTERN.findall(content)
            emoji_counter.update(emojis)
    
    # Retornar los 10 emojis más comunes
    return emoji_counter.most_common(10)
