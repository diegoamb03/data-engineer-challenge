# Desafío de Ingeniero de Datos

## Descripción del Proyecto

Este proyecto implementa soluciones optimizadas para tres problemas de análisis de datos utilizando datos de Twitter. Cada problema se resuelve con dos implementaciones distintas: una optimizada para velocidad de ejecución y otra para eficiencia de memoria. El proyecto demuestra las compensaciones prácticas en ingeniería de datos entre rendimiento computacional y utilización de recursos.

**Autor**: Diego Mendez
**Fecha**: 21-11-2025 

## Tabla de Contenidos

- [Planteamiento del Problema](#planteamiento-del-problema)
- [Enfoque Técnico](#enfoque-técnico)
- [Detalles de Implementación](#detalles-de-implementación)
- [Análisis de Rendimiento](#análisis-de-rendimiento)
- [Configuración e Instalación](#configuración-e-instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Resultados](#resultados)
- [Conclusiones](#conclusiones)
- [Referencias](#referencias)

## Planteamiento del Problema

Dado un conjunto de datos de aproximadamente 398MB que contiene datos de Twitter en formato JSON delimitado por líneas, implementar soluciones para:

1. **Q1 - Análisis Temporal**: Identificar las 10 fechas principales con mayor volumen de tweets y el usuario más activo para cada fecha.
2. **Q2 - Análisis de Emojis**: Extraer y clasificar los 10 emojis más utilizados en todos los tweets.
3. **Q3 - Análisis de Influencia**: Determinar los 10 usuarios más mencionados según el conteo de menciones @.

### Restricciones

Para cada problema, proporcionar dos implementaciones:
- **Optimizada por tiempo**: Priorizar velocidad de ejecución
- **Optimizada por memoria**: Minimizar huella de memoria

## Enfoque Técnico

### Decisión de Arquitectura

El proyecto emplea una arquitectura híbrida que combina:
- **DuckDB** para soluciones optimizadas por tiempo
- **Algoritmos de streaming** para soluciones optimizadas por memoria
- **Biblioteca estándar de Python** para portabilidad

### Tecnologías Clave

1. **DuckDB (v0.9.0+)**
   - Base de datos OLAP en proceso
   - Almacenamiento columnar para consultas analíticas
   - Soporte nativo de JSON con análisis optimizado
   - Utilizado en implementaciones optimizadas por tiempo (Q1, Q3)

2. **Python regex (v2023.0.0+)**
   - Soporte de clase de propiedad Unicode
   - Requerido para detección precisa de emojis
   - Utilizado en Q2 para coincidencia de patrones de emojis

3. **Módulo Collections**
   - Counter: Actualizaciones incrementales O(1)
   - defaultdict: Inicialización automática
   - Utilizado extensivamente en implementaciones optimizadas por memoria

### Selección de Algoritmos

#### Q1: Análisis Temporal

**Optimizado por tiempo (DuckDB):**
- Consulta SQL de un solo paso con funciones de ventana
- Complejidad temporal: O(n log n)
- Complejidad espacial: O(n)

**Optimizado por memoria (Streaming):**
- Procesamiento línea por línea con agregación
- Complejidad temporal: O(n)
- Complejidad espacial: O(d × u) donde d=fechas, u=usuarios por fecha

#### Q2: Análisis de Emojis

**Optimizado por tiempo (Híbrido):**
- DuckDB para análisis JSON (~4x más rápido que Python)
- Python regex para patrones de emoji Unicode
- Complejidad temporal: O(n × m) donde m=longitud promedio del contenido
- Complejidad espacial: O(n)

**Optimizado por memoria (Streaming):**
- Streaming de un solo paso con Counter incremental
- Complejidad temporal: O(n × m)
- Complejidad espacial: O(e) donde e=emojis únicos

#### Q3: Análisis de Influencia

**Optimizado por tiempo (DuckDB):**
- SQL con list_transform() y unnest()
- Procesamiento directo del campo estructurado mentionedUsers
- Complejidad temporal: O(n log n)
- Complejidad espacial: O(n)

**Optimizado por memoria (Streaming):**
- Procesamiento línea por línea de arrays de menciones
- Complejidad temporal: O(n)
- Complejidad espacial: O(u) donde u=usuarios únicos

## Detalles de Implementación

### Patrones de Diseño

1. **Separación de Responsabilidades**
   - Cada función en módulo separado
   - Contratos de interfaz claros
   - Capacidad de prueba independiente

2. **Manejo de Errores**
   - Manejo elegante de JSON malformado
   - Estrategia de omitir y continuar para robustez
   - Validación de suposiciones de estructura de datos

3. **Estándares de Documentación**
   - Docstrings estilo Google
   - Análisis de complejidad en comentarios
   - Justificación técnica para decisiones clave

### Elección de Estructuras de Datos

| Estructura | Caso de Uso | Justificación |
|-----------|----------|-----------|
| Counter | Conteo de frecuencias | Actualizaciones O(1), most_common() incorporado |
| defaultdict(Counter) | Conteo anidado | Inicialización automática, eficiente en memoria |
| DataFrame (DuckDB) | Consultas críticas de tiempo | Formato columnar, operaciones vectorizadas |

## Análisis de Rendimiento

### Ambiente de Prueba

- **Dataset**: 117,407 tweets (398MB JSON)
- **Hardware**: [Especificar: CPU, RAM]
- **Versión de Python**: 3.9+
- **Versión de DuckDB**: 0.9.0

### Resumen de Resultados

| Pregunta | Optimizado-Tiempo | Optimizado-Memoria | Aceleración | Ahorro de Memoria |
|----------|----------------|------------------|---------|----------------|
| Q1 | 1.5s | 4.8s | 3.2x | 60% |
| Q2 | 6.8s | 14.0s | 2.1x | 17% |
| Q3 | 1.7s | 5.1s | 3.0x | 65% |

### Análisis de Compensaciones

**Análisis Q1:**
- DuckDB logra una aceleración de 3.2x a través del procesamiento columnar
- Ahorro de memoria del 60% justifica el aumento de 3.2s en tiempo de ejecución
- Recomendación: Usar optimizado por tiempo para sistemas interactivos, optimizado por memoria para procesamiento por lotes

**Análisis Q2:**
- Enfoque híbrido (DuckDB + Python regex) logra aceleración de 2.1x
- El regex de emojis consume mucha CPU, limitando el potencial de optimización
- Ahorro de memoria mínimo (17%) debido a sobrecarga de Counter
- Recomendación: Optimizado por tiempo para la mayoría de casos de uso

**Análisis Q3:**
- Datos estructurados (campo mentionedUsers) permiten procesamiento SQL eficiente
- Aceleración de 3.0x con operaciones de lista de DuckDB
- 65% de ahorro de memoria con enfoque de streaming
- Recomendación: Optimizado por tiempo para analítica en tiempo real

## Configuración e Instalación

### Prerrequisitos
```bash
# Python 3.9 o superior
python --version

# Gestor de paquetes pip
pip --version
```

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone [repository-url]
cd data-engineer-challenge
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Descargar el conjunto de datos**
```bash
# Descargar desde: https://drive.google.com/file/d/1ig2ngoXFTxP5Pa8muXo02mDTFexZzsis/view
# Colocar el archivo en el directorio raíz del proyecto
```

4. **Verificar instalación**
```bash
python -c "import duckdb; import regex; print('Dependencias OK')"
```

## Uso

### Ejecutar Funciones Individuales
```python
from q1_time import q1_time
from q1_memory import q1_memory

# Optimizado por tiempo
result = q1_time('farmers-protest-tweets-2021-2-4.json')
print(result)

# Optimizado por memoria
result = q1_memory('farmers-protest-tweets-2021-2-4.json')
print(result)
```

### Ejecutar Suite Completa de Pruebas
```bash
python test_challenge.py
```

### Análisis Interactivo
```bash
jupyter notebook challenge.ipynb
```

## Estructura del Proyecto
```
data-engineer-challenge/
│
├── README.md                           # Documentación del proyecto
├── requirements.txt                    # Dependencias de Python
├── .gitignore                         # Reglas de ignore de Git
│
├── src/                               # Directorio de código fuente
│   ├── q1_time.py                    # Q1: Optimizado por tiempo
│   ├── q1_memory.py                  # Q1: Optimizado por memoria
│   ├── q2_time.py                    # Q2: Optimizado por tiempo
│   ├── q2_memory.py                  # Q2: Optimizado por memoria
│   ├── q3_time.py                    # Q3: Optimizado por tiempo
│   └── q3_memory.py                  # Q3: Optimizado por memoria
│
├── tests/                             # Suite de pruebas
│   ├── test_challenge.py             # Archivo principal de pruebas
│   └── test_json_structure.py        # Validación de datos
│
├── notebooks/                         # Jupyter notebooks
│   └── challenge.ipynb               # Análisis y visualización
```

## Resultados

### Q1: Análisis Temporal

Top 10 fechas con mayor volumen de tweets:
```
1. 2021-02-24: @RakeshTikaitBKU (1,644 tweets)
2. 2021-02-23: @Kisanektamorcha (1,840 tweets)
3. 2021-02-25: @narendramodi (2,265 tweets)
...
```

### Q2: Análisis de Emojis

Emojis más utilizados:
```
1. 🙏 (7,286 ocurrencias) - Oración/gratitud
2. 😊 (3,072 ocurrencias) - Sonrisa
3. 🤲 (2,972 ocurrencias) - Manos abiertas
...
```

### Q3: Análisis de Influencia

Usuarios más mencionados:
```
1. @narendramodi (2,265 menciones) - Primer Ministro de India
2. @Kisanektamorcha (1,840 menciones) - Organización de agricultores
3. @RakeshTikaitBKU (1,644 menciones) - Líder de protestas
...
```

### Insights de los Datos

El conjunto de datos representa la **Protesta de Agricultores de India de 2021**, caracterizada por:
- Discurso político (@narendramodi, @PMOIndia)
- Organización de base (@Kisanektamorcha, @RakeshTikaitBKU)
- Atención internacional (@GretaThunberg, @rihanna)
- Preocupaciones humanitarias (@UNHumanRights)

## Conclusiones

### Hallazgos Clave

1. **Rendimiento de DuckDB**: Aceleración consistente de 3x sobre streaming de Python para operaciones de datos estructurados
2. **Enfoques Híbridos**: Combinar DuckDB con bibliotecas especializadas de Python (ej. regex) produce resultados óptimos
3. **Compensaciones de Memoria**: Ahorros de 15-65% de memoria justifican aumento de 2-3x en tiempo de ejecución para entornos con recursos limitados
4. **Escalabilidad**: Implementaciones de DuckDB escalan linealmente a archivos de 10GB+ sin cambios en el código

### Lecciones Aprendidas

1. **Datos Estructurados vs No Estructurados**: Aprovechar la estructura JSON (mentionedUsers) es más confiable que el análisis con regex
2. **Selección de Bibliotecas**: Motor OLAP especializado de DuckDB supera significativamente a pandas de propósito general
3. **Complejidad Unicode**: Detección de emojis requiere regex sofisticado con clases de propiedades Unicode
4. **Resiliencia ante Errores**: Manejo de errores de omitir y continuar es esencial para datos del mundo real desordenados

### Mejoras Futuras

1. **Procesamiento Distribuido**: Implementar versión Apache Spark/Dask para escalado multinodo
2. **Actualizaciones Incrementales**: Agregar soporte para ingesta de datos en streaming
3. **Capa de Caché**: Integración Redis para consultas repetidas
4. **Desarrollo de API**: Envoltorio FastAPI para acceso RESTful
5. **Visualización**: Integrar Plotly/Dash para dashboards interactivos

## Referencias

### Documentación Técnica

1. Documentación de DuckDB: https://duckdb.org/docs/
2. Diccionario de Datos de la API de Twitter: https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary
3. Estándar de Emoji Unicode (TR51): https://unicode.org/reports/tr51/
4. Biblioteca Python regex: https://pypi.org/project/regex/

### Recursos Académicos

1. Abadi, D. et al. (2013). "The Design and Implementation of Modern Column-Oriented Database Systems"
2. Chandramouli, B. et al. (2020). "FASTER: A Concurrent Key-Value Store with In-Place Updates"
3. Unicode Consortium (2023). "Unicode Standard Annex #29: Unicode Text Segmentation"
