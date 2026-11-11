import subprocess
import time
import shutil
from typing import List, Dict, Any
from radon.complexity import cc_visit
from radon.metrics import h_visit

# =====================================================================
# 1. EVALUADOR DE MÉTRICAS DE CÓDIGO FUENTE (Radon: McCabe & Halstead)
# =====================================================================

def analizar_calidad_codigo_fuente(ruta_archivo: str) -> Dict[str, Any]:
    """
    Analiza un archivo Python para calcular Complejidad Ciclomática y Volumen.
    """
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        codigo = f.read()

    # Complejidad Ciclomática (McCabe)
    bloques_complejidad = cc_visit(codigo)
    complejidad_total = sum(b.complexity for b in bloques_complejidad)
    promedio_complejidad = complejidad_total / len(bloques_complejidad) if bloques_complejidad else 1

    # Métricas de Halstead (Volumen y Esfuerzo)
    metricas_halstead = h_visit(codigo)
    
    return {
        "funciones_analizadas": len(bloques_complejidad),
        "complejidad_promedio": round(promedio_complejidad, 2),
        "volumen_halstead": round(metricas_halstead.total.volume, 2),
        "esfuerzo_halstead": round(metricas_halstead.total.effort, 2)
    }


# =====================================================================
# 2. RUNNER DE PRUEBAS PARA HERRAMIENTAS CLI DE UBUNTU
# =====================================================================

class RunnerPruebasUbuntuCLI:
    def __init__(self, nombre_comando: str):
        self.comando = nombre_comando
        self.resultados_pruebas: List[Dict[str, Any]] = []

    def verificar_instalacion(f) -> bool:
        """Verifica si la herramienta está en el PATH del sistema."""
        return shutil.which(f) is not None

    def ejecutar_caso_prueba(self, id_prueba: str, argumentos: List[str], codigo_esperado: int = 0) -> Dict[str, Any]:
        """
        Ejecuta un comando en la consola de Ubuntu, mide el tiempo de respuesta
        y valida el código de salida (exit code) y los errores.
        """
        comando_completo = [self.comando] + argumentos
        
        tiempo_inicio = time.perf_counter()
        proceso = subprocess.run(
            comando_completo,
            capture_output=True,
            text=True
        )
        tiempo_ejecucion = time.perf_counter() - tiempo_inicio

        es_exitoso = proceso.returncode == codigo_esperado

        resultado = {
            "id": id_prueba,
            "comando": " ".join(comando_completo),
            "exit_code": proceso.returncode,
            "exitoso": es_exitoso,
            "tiempo_respuesta_ms": round(tiempo_ejecucion * 1000, 2),
            "stdout": proceso.stdout.strip(),
            "stderr": proceso.stderr.strip()
        }
        self.resultados_pruebas.append(resultado)
        return resultado

    def generar_reporte_calidad_ejecucion(self) -> Dict[str, Any]:
        """Mide la tasa de fallos y el tiempo de respuesta promedio."""
        if not self.resultados_pruebas:
            return {}

        total_pruebas = len(self.resultados_pruebas)
        pruebas_exitosas = sum(1 for p in self.resultados_pruebas if p["exitoso"])
        pruebas_fallidas = total_pruebas - pruebas_exitosas
        
        tiempo_total = sum(p["tiempo_respuesta_ms"] for p in self.resultados_pruebas)
        
        return {
            "total_ejecutadas": total_pruebas,
            "exitosas": pruebas_exitosas,
            "fallidas": pruebas_fallidas,
            "tasa_exito_porcentaje": round((pruebas_exitosas / total_pruebas) * 100, 2),
            "tiempo_promedio_ms": round(tiempo_total / total_pruebas, 2)
        }


# =====================================================================
# EJECUCIÓN: PRUEBA DE CALIDAD SOBRE 'curl' EN UBUNTU
# =====================================================================

if __name__ == "__main__":
    HERRAMIENTA = "curl"
    
    print(f"=== 1. VERIFICACIÓN DE INSTALACIÓN EN UBUNTU ===")
    if not RunnerPruebasUbuntuCLI.verificar_instalacion(HERRAMIENTA):
        print(f"Error: La herramienta '{HERRAMIENTA}' no está instalada en el sistema.")
        print(f"Instálala corriendo: sudo apt update && sudo apt install {HERRAMIENTA}")
        exit(1)
    
    print(f"✔ Herramienta '{HERRAMIENTA}' encontrada en el sistema.\n")

    print(f"=== 2. EJECUCIÓN DE PRUEBAS DE INTEGRACIÓN/SISTEMA ===")
    runner = RunnerPruebasUbuntuCLI(HERRAMIENTA)

    # Caso 1: Obtener la versión de la CLI
    runner.ejecutar_caso_prueba("TC01_Version", ["--version"])

    # Caso 2: Petición HTTP válida
    runner.ejecutar_caso_prueba("TC02_PeticionValida", ["-I", "https://ubuntu.com"])

    # Caso 3: Forzar un error (dominio inexistente)
    runner.ejecutar_caso_prueba("TC03_DominioInvalido", ["https://dominio-inexistente-12345.com"], codigo_esperado=6)

    # Mostramos los resultados de las pruebas
    for r in runner.resultados_pruebas:
        estado = "PASS" if r["exitoso"] else "FAIL"
        print(f"[{estado}] {r['id']} | Tiempo: {r['tiempo_respuesta_ms']} ms | Código salida: {r['exit_code']}")

    print("\n=== 3. INFORME DE MÉTRICAS EN TIEMPO DE EJECUCIÓN ===")
    reporte_ejecucion = runner.generar_reporte_calidad_ejecucion()
    print(f"• Pruebas pasadas:       {reporte_ejecucion['exitosas']}/{reporte_ejecucion['total_ejecutadas']}")
    print(f"• Tasa de Éxito:         {reporte_ejecucion['tasa_exito_porcentaje']}%")
    print(f"• Tiempo Medio Respuesta: {reporte_ejecucion['tiempo_promedio_ms']} ms")

    print("\n=== 4. MÉTRICAS DE CÓDIGO FUENTE DEL SUITE (McCabe & Halstead) ===")
    try:
        # Analiza este mismo archivo de pruebas
        metricas_codigo = analizar_calidad_codigo_fuente(__file__)
        print(f"• Funciones analizadas:    {metricas_codigo['funciones_analizadas']}")
        print(f"• Complejidad Ciclomática: {metricas_codigo['complejidad_promedio']} (Ideal: < 10)")
        print(f"• Volumen de Halstead:    {metricas_codigo['volumen_halstead']}")
    except Exception as e:
        print(f"Para ver métricas estáticas de código, instala radon: pip install radon. Error: {e}")
