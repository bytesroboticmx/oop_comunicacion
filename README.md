# oop_comunicacion

Repositorio con ejemplos y utilidades en **Python 3**.

## Contenido

- [`carrito.py`](carrito.py): ejemplo sencillo de comunicación entre objetos (OOP).
- [`cli_qa_tester.py`](cli_qa_tester.py): ejecutor de pruebas para herramientas CLI en Ubuntu con métricas de ejecución y análisis estático del código.

## Requisitos

- **Python 3**
- Para `cli_qa_tester.py`:
  - Dependencia de Python: [`radon`](https://pypi.org/project/radon/)
  - Herramienta del sistema usada en el ejemplo: `curl` (disponible en Ubuntu)

Instalación de dependencias (ejemplo):

```bash
pip install radon
```

En Ubuntu, si no tienes `curl`:

```bash
sudo apt update && sudo apt install curl
```

## Programas

### `carrito.py`

Demuestra la interacción entre objetos mediante el envío de mensajes (llamadas a métodos):

- `Producto`: representa un producto con nombre y precio (`obtener_precio()`).
- `CarritoDeCompras`: mantiene un total y permite agregar productos (`agregar_producto(producto, cantidad)`), consultando el precio del producto.

Al ejecutarse, crea un producto y un carrito, y agrega unidades del producto al carrito.

**Ejecución:**

```bash
python3 carrito.py
```

> Nota: el script realiza la operación de ejemplo pero no imprime salida por pantalla.

### `cli_qa_tester.py`

Herramienta de ejemplo para evaluar calidad en dos niveles:

1. **Pruebas de integración/sistema sobre una CLI** (`RunnerPruebasUbuntuCLI`):
   - Verifica que el comando esté instalado en el sistema (`shutil.which`).
   - Ejecuta casos de prueba con `subprocess.run`, mide tiempo de respuesta y valida el código de salida.
   - Genera un reporte con total de pruebas, éxitos/fallos, tasa de éxito y tiempo promedio.

2. **Métricas de código fuente** (`analizar_calidad_codigo_fuente`) usando `radon`:
   - Complejidad ciclomática (McCabe).
   - Métricas de Halstead (volumen y esfuerzo).

En su bloque principal (`if __name__ == "__main__":`) ejecuta un conjunto de pruebas de ejemplo contra `curl` (`--version`, una petición HTTP válida y un caso de dominio inválido con código de salida esperado) y muestra un informe en consola, incluyendo métricas del propio archivo de pruebas.

**Ejecución:**

```bash
python3 cli_qa_tester.py
```
