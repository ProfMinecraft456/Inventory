# Inventory App

Bienvenido a **Inventory App**, un sistema clásico y elegante de gestión de inventario y ventas, inspirado en el estilo Material You Vintage. Este proyecto utiliza Python y PyQt5 para ofrecer una experiencia de usuario sofisticada y atractiva, combinando una interfaz moderna con toques nostálgicos.

---

## Características:

- **Gestión de Inventario**  
  - Búsqueda en tiempo real de artículos.
  - Agregar y actualizar productos.
  - Eliminación de productos.
  - Visualización ordenada del inventario con indicadores de stock.

- **Módulo de Ventas**  
  - Adición de productos a la venta.
  - Cálculo automático del total y cambio.
  - Validación en tiempo real del stock disponible.
  - Interfaz intuitiva para registrar transacciones de venta.

- **Estilos y Diseño**  
  - Inspirado en Material You con un toque vintage.
  - Paleta de colores cálida y cómoda.
  - Interfaz clara y amigable para maximizar la eficiencia.

---

## Tecnologías Utilizadas:

- **Python**: Lenguaje de programación.
- **PyQt5**: Framework para desarrollar interfaces gráficas.
- **JSON**: Para almacenamiento y persistencia de datos.

---

## Requisitos del Sistema:

### Hardware:

- **CPU**: Cualquier procesador Intel o AMD de 2005 en adelante.
- **Memoria RAM**: Mínimo 512 MB (se recomienda 1 GB o más para un rendimiento óptimo).
- **Espacio en Disco**: Al menos 100 MB de espacio libre para el archivo JSON y dependencias.

### Software:

- **Sistema Operativo**:  
  - Windows, Linux o macOS (aplicable tanto para la versión en Python como para el ejecutable).
  - No se requieren privilegios administrativos en Windows para ejecutar la aplicación.
- **Python**: Versión 3.6 o superior (si se ejecuta el código fuente).
- **Dependencias de Python**:
  - PyQt5 (instalable mediante `pip install PyQt5`).

### Requisitos Adicionales:

- **Conexión a Internet**:  
  - No es necesaria para el funcionamiento de la aplicación.
  - Es necesaria únicamente para instalar las dependencias o si se desea modificar el código y obtener actualizaciones.

---

## Archivos Destacados:

- **inventory.py**: Código fuente principal de la aplicación.
- **Inventory.exe**: Archivo compilado ejecutable para Windows (ya incluido en el repositorio).

---

## Descargar la App:

Puedes descargar la aplicación de dos formas:

- **Para usuarios de Windows**:  
  Descarga el ejecutable [Inventory.exe](https://github.com/ProfMinecraft456/Inventory/blob/main/Inventory.exe) directamente desde el repositorio.  
  En Windows, se recomienda utilizar PowerShell para ejecutar el ejecutable.
  
- **Para usuarios de macOS y Linux**:  
  Clona el repositorio y compila la aplicación siguiendo las instrucciones de la sección [Compilación con PyInstaller](#compilación-con-pyinstaller).

---

## Cómo Ejecutar la Aplicación:

1. **Instalar Dependencias**  
   Asegúrate de tener Python instalado y procede a instalar las dependencias necesarias:
   ```bash
   pip install PyQt5
   ```

2. **Descargar el Código**  
   Clona el repositorio o descarga el proyecto utilizando GitHub Desktop o la línea de comandos:
   ```PowerShell
   git clone https://github.com/ProfMinecraft456/Inventory.git
   ```

3. **Ejecutar la Aplicación (Modo Desarrollo)**  
   Para correr la aplicación en modo desarrollo, ubica el archivo `inventory.py` y ejecútalo:
   ```PowerShell
   python inventory.py
   ```
   _Nota: Asegúrate de estar en el directorio correcto del proyecto._

4. **Utilizar el Ejecutable en Windows**  
   Para usuarios de Windows que prefieren no depender de un entorno de Python, ejecuta el archivo `Inventory.exe` directamente.

---

## Compilación con PyInstaller:

Para generar un único ejecutable utilizando PyInstaller, utiliza los siguientes comandos dependiendo de tu sistema operativo:

- **En Windows**  
  Ejecuta:
  ```Powershell
  pyinstaller.exe --onefile --noconsole Inventory.py --clean
  ```

- **En macOS y Linux**  
  Ejecuta:
  ```bash
  pyinstaller --onefile --noconsole Inventory.py --clean
  ```
  _Nota: Asegúrate de tener PyInstaller instalado y accesible en tu PATH._

---

## Contacto:

Si tienes alguna pregunta, sugerencia o necesitas ayuda, no dudes en contactarme a través de [profmcyt@hotmail.com](mailto:profmcyt@hotmail.com).

---

## Contribuciones:

Las contribuciones son bienvenidas. Si deseas mejorar la aplicación o agregar nuevas funcionalidades, siéntete libre de abrir un _pull request_ o reportar un _issue_.

---

## Licencia:

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para mayor información.

---

_Disfruta de una experiencia única que combina lo mejor del diseño moderno con un toque de nostalgia vintage._