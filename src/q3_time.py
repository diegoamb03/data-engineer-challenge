"""
q3_time.py
---------
Data Engineer Challenge - Question 3: Time-Optimized Solution

Autor: Diego Mendez
Fecha: 21-11-2025
Descripción:
    Identifica los 10 usuarios más influyentes basados en la cantidad 
    de menciones (@username). Esta implementación usa el motor SQL 
    optimizado de DuckDB para procesar la información estructurada 
    del campo mentionedUsers del JSON.

Características de rendimiento:
    - Complejidad temporal: O(n log n), donde n es el total de menciones
    - Complejidad espacial: O(n) por el almacenamiento columnar
    - Tiempo estimado de ejecución: ~1.5-2.0s para 117K tweets
    - Uso de memoria: ~50-100MB

Dependencias:
    - duckdb >= 0.9.0

Justificación técnica:
    La estructura JSON incluye un arreglo 'mentionedUsers' que contiene 
    los datos estructurados de cada mención. Esto es más confiable que 
    analizar menciones mediante regex en el texto del tweet, ya que 
    regex puede perder menciones o generar falsos positivos.

Referencias:
    - Diccionario de Datos de Twitter: https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary
    - Especificación del reto: ver sección 3 del README.md
"""

from typing import List, Tuple


def q3_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Identifica los 10 usuarios más mencionados en todos los tweets.
    
    Esta implementación aprovecha las funciones de procesamiento de listas 
    de DuckDB para extraer usernames del campo estructurado 'mentionedUsers'. 
    Es más precisa que usar regex y se beneficia del procesamiento columnar 
    de DuckDB.
    
    Algoritmo:
        1. Leer el JSON usando el parser optimizado de DuckDB
        2. Utilizar list_transform() para extraer el campo username de cada objeto
        3. Usar unnest() para aplanar arreglos en filas
        4. Agregar menciones por username con COUNT()
        5. Retornar el top 10
    
    Args:
        file_path: Ruta del archivo JSON con tweets delimitados por líneas
        
    Returns:
        Lista de tuplas (username, cantidad_de_menciones) ordenadas por frecuencia.
        Ejemplo: [('narendramodi', 2265), ('Kisanektamorcha', 1840), ...]
        
    Excepciones:
        FileNotFoundError: Si el archivo no existe
        duckdb.Error: Si ocurre un error al parsear JSON o ejecutar SQL
        
    Notas técnicas:
        - Usa list_transform() para manipular arreglos
        - unnest() aplana arreglos eficientemente en formato columnar
        - json_extract_string() extrae campos anidados en JSON
        - Los WHERE eliminan valores NULL o vacíos antes de agregar
    """
    import duckdb
    
    # Inicializa conexión DuckDB en memoria
    con = duckdb.connect(':memory:')
    
    # Query SQL usando funciones avanzadas de listas en DuckDB
    query = f"""
        WITH mentions AS (
            -- Extraer usernames del arreglo mentionedUsers
            -- list_transform aplica una función lambda a cada elemento
            SELECT 
                unnest(
                    list_transform(
                        mentionedUsers,
                        x -> json_extract_string(x, '$.username')
                    )
                ) as username
            FROM read_json_auto('{file_path}', format='newline_delimited')
            WHERE mentionedUsers IS NOT NULL 
              AND len(mentionedUsers) > 0
        )
        SELECT 
            username,
            COUNT(*) as mention_count
        FROM mentions
        WHERE username IS NOT NULL AND username != ''
        GROUP BY username
        ORDER BY mention_count DESC
        LIMIT 10
    """
    
    # Ejecutar query y obtener resultado
    result = con.execute(query).fetchall()
    con.close()
    
    return result
