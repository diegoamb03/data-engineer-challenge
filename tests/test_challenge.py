"""
test_challenge.py
----------------
Data Engineer Challenge - Suite de Pruebas

Uso:
    python tests/test_challenge.py
"""

import sys
from pathlib import Path

# Agregar carpeta src/ al path de Python
# Esto permite importar módulos desde src/
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Ahora puedes importar normalmente
from q1_time import q1_time
from q1_memory import q1_memory
from q2_time import q2_time
from q2_memory import q2_memory
from q3_time import q3_time
from q3_memory import q3_memory

import time
from datetime import datetime

# Perfilamiento de memoria
try:
    from memory_profiler import memory_usage
    MEMORY_PROFILER_AVAILABLE = True
except ImportError:
    MEMORY_PROFILER_AVAILABLE = False
    print("Advertencia: memory_profiler no está instalado.")

# Configuración
FILE_PATH = project_root / "src/farmers-protest-tweets-2021-2-4.json"

class PerformanceMetrics:
    """Contenedor para resultados de medición de desempeño."""
    
    def __init__(self, func_name: str, execution_time: float, 
                 memory_usage: float = None, result=None):
        self.func_name = func_name
        self.execution_time = execution_time
        self.memory_usage = memory_usage
        self.result = result
        
    def __repr__(self):
        mem_str = f"{self.memory_usage:.2f}MB" if self.memory_usage else "N/A"
        return (f"{self.func_name}: {self.execution_time:.3f}s, "
                f"Memoria: {mem_str}")


def measure_performance(func, file_path: str, func_name: str) -> PerformanceMetrics:
    """
    Mide tiempo de ejecución y uso de memoria de una función.
    
    Args:
        func: Función a medir
        file_path: Ruta del archivo de entrada
        func_name: Nombre descriptivo
        
    Returns:
        Objeto PerformanceMetrics con mediciones y resultados
    """
    print(f"\nEjecutando: {func_name}")
    print("-" * 70)
    
    # Medir tiempo de ejecución
    start_time = time.time()
    result = func(file_path)
    execution_time = time.time() - start_time
    
    # Medir uso de memoria si está disponible
    memory_peak = None
    if MEMORY_PROFILER_AVAILABLE:
        memory_peak = memory_usage((func, (file_path,)), max_usage=True)
    
    # Mostrar resultados
    print(f"Estado: Completado")
    print(f"Tiempo de ejecución: {execution_time:.3f}s")
    if memory_peak:
        print(f"Memoria pico: {memory_peak:.2f}MB")
    
    print(f"\nTop 10 Resultados:")
    for i, item in enumerate(result[:10], 1):
        print(f"  {i:2d}. {item}")
    
    return PerformanceMetrics(func_name, execution_time, memory_peak, result)


def validate_consistency(result1, result2, q_num: int) -> bool:
    """
    Valida que las implementaciones de tiempo y memoria produzcan resultados consistentes.
    
    Args:
        result1: Resultado de implementación optimizada por tiempo
        result2: Resultado de implementación optimizada por memoria
        q_num: Número de pregunta
        
    Returns:
        True si los resultados coinciden, False si difieren
    """
    print(f"\nValidando consistencia Q{q_num}...")
    
    if result1 == result2:
        print(f"Resultado: APROBADO - Ambas implementaciones generan resultados idénticos")
        return True
    else:
        print(f"Resultado: ADVERTENCIA - Los resultados difieren entre implementaciones")
        print("Puede deberse a empates en ranking o diferencias de implementación.")
        
        # Mostrar diferencias
        print("\nComparación de los primeros 3 elementos:")
        print("Optimizado por tiempo:", result1[:3])
        print("Optimizado por memoria:", result2[:3])
        return False


def print_header(title: str):
    """Imprime encabezado formateado."""
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)


def print_summary(metrics_dict: dict):
    """Imprime un resumen completo del desempeño."""
    print_header("RESUMEN DE DESEMPEÑO")
    
    for q_name, metrics in metrics_dict.items():
        print(f"\n{q_name}:")
        
        time_metrics = metrics['time']
        memory_metrics = metrics['memory']
        
        print(f"\n  Implementación optimizada por tiempo:")
        print(f"    Tiempo de ejecución: {time_metrics.execution_time:.3f}s")
        if time_metrics.memory_usage:
            print(f"    Memoria pico:        {time_metrics.memory_usage:.2f}MB")
        
        print(f"\n  Implementación optimizada por memoria:")
        print(f"    Tiempo de ejecución: {memory_metrics.execution_time:.3f}s")
        if memory_metrics.memory_usage:
            print(f"    Memoria pico:        {memory_metrics.memory_usage:.2f}MB")
        
        # Calcular trade-offs
        if time_metrics.execution_time > 0:
            time_diff_pct = ((memory_metrics.execution_time - time_metrics.execution_time) 
                            / time_metrics.execution_time * 100)
            print(f"\n  Análisis de trade-offs:")
            print(f"    Diferencia de tiempo: {time_diff_pct:+.1f}%")
            
            if (time_metrics.memory_usage and memory_metrics.memory_usage):
                mem_diff_pct = ((memory_metrics.memory_usage - time_metrics.memory_usage) 
                               / time_metrics.memory_usage * 100)
                print(f"    Diferencia de memoria: {mem_diff_pct:+.1f}%")


def main():
    """Función principal de ejecución de pruebas."""
    print_header("DATA ENGINEER CHALLENGE - SUITE DE PRUEBAS")
    print(f"\nConfiguración:")
    print(f"  Archivo de entrada: {FILE_PATH}")
    print(f"  Hora de inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Memory Profiler: {'Habilitado' if MEMORY_PROFILER_AVAILABLE else 'Deshabilitado'}")
    
    # Validar archivo de entrada
    if not Path(FILE_PATH).exists():
        print(f"\nError: El archivo '{FILE_PATH}' no existe.")
        print("Por favor descarga el archivo y colócalo en el directorio actual.")
        sys.exit(1)
    
    metrics = {}
    
    try:
        # Pregunta 1
        print_header("Q1: Top 10 Fechas con Más Tweets")
        
        q1_time_metrics = measure_performance(
            q1_time, FILE_PATH, "q1_time (basado en DuckDB)"
        )
        q1_memory_metrics = measure_performance(
            q1_memory, FILE_PATH, "q1_memory (streaming)"
        )
        
        validate_consistency(q1_time_metrics.result, q1_memory_metrics.result, 1)
        
        metrics['Q1'] = {'time': q1_time_metrics, 'memory': q1_memory_metrics}
        
        # Pregunta 2
        print_header("Q2: Top 10 Emojis Más Usados")
        
        q2_time_metrics = measure_performance(
            q2_time, FILE_PATH, "q2_time (DuckDB + regex)"
        )
        q2_memory_metrics = measure_performance(
            q2_memory, FILE_PATH, "q2_memory (streaming)"
        )
        
        validate_consistency(q2_time_metrics.result, q2_memory_metrics.result, 2)
        
        metrics['Q2'] = {'time': q2_time_metrics, 'memory': q2_memory_metrics}
        
        # Pregunta 3
        print_header("Q3: Top 10 Usuarios Más Mencionados")
        
        q3_time_metrics = measure_performance(
            q3_time, FILE_PATH, "q3_time (basado en DuckDB)"
        )
        q3_memory_metrics = measure_performance(
            q3_memory, FILE_PATH, "q3_memory (streaming)"
        )
        
        validate_consistency(q3_time_metrics.result, q3_memory_metrics.result, 3)
        
        metrics['Q3'] = {'time': q3_time_metrics, 'memory': q3_memory_metrics}
        
        # Resumen general
        print_summary(metrics)
        
        print_header("SUITE DE PRUEBAS FINALIZADA")
        print(f"\nHora de finalización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Estado: Todas las pruebas fueron ejecutadas con éxito")
        
        # Tiempo total
        total_time = sum(
            m['time'].execution_time + m['memory'].execution_time 
            for m in metrics.values()
        )
        print(f"Tiempo total de ejecución: {total_time:.3f}s")
        
    except Exception as e:
        print(f"\nError durante la ejecución de pruebas: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
