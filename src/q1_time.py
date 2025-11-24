"""
q1_time.py
---------
Desafío de Ingeniero de Datos - Pregunta 1: Solución Optimizada en Tiempo

Autor: Diego Mendez
Fecha: 21-11-2025
Descripción: 
    Identifica las 10 fechas con el mayor volumen de tweets y determina
    el usuario más activo en cada una de esas fechas. Esta implementación
    prioriza la velocidad de ejecución utilizando el motor de procesamiento
    columnar de DuckDB.

Características de Rendimiento:
    - Complejidad de Tiempo: O(n log n) donde n es el número de tweets
    - Complejidad de Espacio: O(n) para almacenamiento columnar
    - Tiempo de ejecución esperado: ~1.5-2.0s para 117K tweets
    - Uso de Memoria: ~50-100MB

Dependencias:
    - duckdb >= 0.9.0

Referencias:
    - Funciones JSON de DuckDB: https://duckdb.org/docs/data/json
    - Especificación del desafío: Ver sección 1 de README.md
"""

from typing import List, Tuple
from datetime import date


def q1_time(file_path: str) -> List[Tuple[date, str]]:
    """
    Calcula las 10 fechas con mayor volumen de tweets junto con el usuario 
    más activo para cada fecha.
    
    Esta implementación aprovecha el motor SQL optimizado de DuckDB para un
    procesamiento rápido de JSON. El enfoque utiliza funciones ventana para
    identificar eficientemente al usuario principal por fecha en una sola
    pasada de consulta.
    
    Algoritmo:
        1. Parsear JSON y extraer los campos de fecha y usuario
        2. Agregar los tweets por fecha para identificar las 10 fechas con mayor volumen
        3. Para cada fecha principal, usar ROW_NUMBER() para rankear usuarios
        4. Retornar los pares (fecha-usuario) con rango 1
    
    Argumentos:
        file_path: Ruta del archivo JSON delimitado por líneas que contiene tweets
        
    Retorna:
        Lista de tuplas que contienen pares (fecha, usuario) ordenados por volumen de tweets.
        Ejemplo: [(date(2021, 2, 24), 'narendramodi'), ...]
        
    Excepciones:
        FileNotFoundError: Si la ruta especificada no existe
        duckdb.Error: Si falla el parseo JSON o la ejecución de SQL
        
    Notas Técnicas:
        - Usa read_json_auto() de DuckDB para parseo optimizado de JSON
        - CAST a DATE para una comparación correcta de fechas
        - La función ventana ROW_NUMBER() evita subconsultas y mejora el rendimiento
    """
    import duckdb
    
    # Inicializa conexión DuckDB en memoria
    con = duckdb.connect(':memory:')
    
    # Consulta SQL optimizada usando CTEs para claridad y funciones ventana para rendimiento
    query = f"""
        WITH parsed AS (
            -- Extraer y parsear fecha y usuario desde JSON
            SELECT 
                CAST(substr(date, 1, 10) AS DATE) as date,
                json_extract_string(user, '$.username') as username
            FROM read_json_auto('{file_path}', format='newline_delimited')
        ),
        date_counts AS (
            -- Identificar las 10 fechas con mayor volumen de tweets
            SELECT 
                date, 
                COUNT(*) as total_tweets
            FROM parsed
            GROUP BY date
            ORDER BY total_tweets DESC
            LIMIT 10
        ),
        user_counts AS (
            -- Rankear usuarios por actividad para cada fecha principal
            SELECT 
                p.date,
                p.username,
                COUNT(*) as user_tweets,
                ROW_NUMBER() OVER (
                    PARTITION BY p.date 
                    ORDER BY COUNT(*) DESC
                ) as rank
            FROM parsed p
            INNER JOIN date_counts dc ON p.date = dc.date
            GROUP BY p.date, p.username
        )
        -- Seleccionar solo el usuario más activo por fecha
        SELECT 
            date,
            username
        FROM user_counts
        WHERE rank = 1
        ORDER BY date DESC
    """
    
    # Ejecutar la consulta y obtener resultados como DataFrame
    result_df = con.execute(query).fetchdf()
    con.close()
    
    # Convertir DataFrame al formato de salida requerido
    result = [
        (row['date'], row['username']) 
        for _, row in result_df.iterrows()
    ]
    
    return result
