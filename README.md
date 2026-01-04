# ESP32 Flash Tool GUI 🚀

Una herramienta gráfica moderna y ligera diseñada para flashear firmware en placas **ESP32**, desarrollada especialmente para el proyecto *ESP32 Relay X8 Control*.

![Interface](https://img.shields.io/badge/Interface-CustomTkinter-blue) ![Language](https://img.shields.io/badge/Language-Python-yellow) ![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux-green)

## ✨ Características

- 🖥️ **Interfaz Moderna**: Basada en `customtkinter` con soporte para modo oscuro.
- 🔌 **Auto-detección**: Lista automáticamente los puertos COM disponibles.
- ⚡ **Alta Velocidad**: Soporta baudrates de hasta 921600 para cargas ultrarrápidas.
- 🗑️ **Erase Flash**: Botón integrado para limpiar completamente la memoria antes de flashear.
- 📡 **Monitor Serie**: Terminal integrada para ver los logs del ESP32 en tiempo real después de la carga.
- 📦 **Portable**: Puede ser empaquetada en un solo archivo `.exe` o binario Linux.

## 🚀 Instalación (Desarrollo)

Si quieres ejecutar el código fuente desde el terminal:

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/aaguadomanchado/esp32-flash-tool-gui.git
   cd esp32-flash-tool-gui
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Instala soporte gráfico (Linux únicamente)**:
   ```bash
   sudo apt install python3-tk
   ```

4. **Ejecuta la App**:
   ```bash
   python3 main.py
   ```

## 📦 Cómo crear el Ejecutable Portable

Para generar un archivo único que funcione sin necesidad de instalar Python:

```bash
pyinstaller --noconsole --onefile --collect-all customtkinter main.py
```
El archivo resultante estará en la carpeta `dist/`.

## 🛠️ Cómo usar

1. Conecta tu placa ESP32 vía USB.
2. Presiona el botón de **actualizar (🔄)** si tu puerto no aparece.
3. Selecciona tu archivo firmware `.bin`.
4. (Opcional) Usa **BORRAR FLASH** si quieres una instalación limpia.
5. Presiona **FLASH** y espera a que termine.
6. El **Monitor Serie** se activará automáticamente al finalizar para mostrarte los logs.

## 📋 Requisitos

- Python 3.x
- Driver USB-Serie instalado (CH340 o CP2102 según tu placa).

---
Desarrollado para facilitar la gestión de sistemas de control basados en ESP32.