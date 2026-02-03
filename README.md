  1) Instalar pipx:
     - `python -m pip install --user pipx`
     - `python -m pipx ensurepath`  (reabre la terminal)
     - `pipx install pipenv`

  2) Inicializar el entorno con Python 3.13:
     - `pipenv --python 3.13`
     - Importar requirements (convirtió a Pipfile): `pipenv install -r requirements.txt`
     - Instalar dependencias: `pipenv install pyside6 pyinstaller`

  3) Entrar al subshell y probar:
     - `pipenv shell`
     - `python MiniOffice.py`

  ## PyInstaller - Generar el ejecutable (MiniOffice)

  pipenv run pyinstaller --clean --noconfirm --windowed --onefile \
  --name MiniOffice --add-data "Images;Images" MiniOffice.py

  - Crea:
  - `dist/MiniOffice.exe` ← ejecutable
  - `build/` (archivos temporales y avisos)
  - `MiniOffice.spec`

  ## Reconocimiento de voz (dependencias)
  - Instalar paquetes de voz en el entorno pipenv:
    - `pipenv install "SpeechRecognition[audio]" pyaudio`
  - Si usas el `requirements.txt`, sincroniza primero:
  - `pipenv install -r requirements.txt`

## Componentes Personalizados (MiniOffice)

### WordCounterWidget

El archivo `contadorWidget.py` implementa la clase `WordCounterWidget`, un widget personalizado basado en `QWidget` diseñado para proporcionar métricas de texto en tiempo real. Este componente sustituye a la implementación nativa básica de conteo de palabras.

#### Características Principales
- **Conteo de Palabras:** Calcula el número total de palabras en el texto.
- **Conteo de Caracteres:** Muestra el número total de caracteres.
- **Tiempo de Lectura:** Estima el tiempo necesario para leer el texto basándose en palabras por minuto (WPM).
- **Configurable:** Permite ajustar la visibilidad de cada métrica y la velocidad de lectura.

#### API del Componente

**Constructor:**
```python
WordCounterWidget(wpm=200, mostrarPalabras=True, mostrarCaracteres=True, mostrarTiempoLectura=True, parent=None)
```
- `wpm` (int): Velocidad de lectura en palabras por minuto (por defecto 200).
- `mostrarPalabras` (bool): Visibilidad del contador de palabras.
- `mostrarCaracteres` (bool): Visibilidad del contador de caracteres.
- `mostrarTiempoLectura` (bool): Visibilidad del tiempo estimado.

**Señales:**
- `conteoActualizado(int palabras, int caracteres)`
  Esta señal se emite automáticamente cada vez que se recalculan las métricas (generalmente al llamar a `update_from_text`).
  
  **Parámetros:**
  - `palabras` (int): Nuevo conteo total de palabras.
  - `caracteres` (int): Nuevo conteo total de caracteres.

  **Ejemplo de uso:**
  ```python
  def mi_slot(palabras, caracteres):
      print(f"El texto tiene {palabras} palabras.")

  widget = WordCounterWidget()
  widget.conteoActualizado.connect(mi_slot)
  ```

**Métodos Públicos:**
- `update_from_text(text: str)`: Procesa la cadena de texto proporcionada, recalcula todas las métricas y actualiza la interfaz gráfica.

#### Integración en MiniOffice
En `MiniOffice.py`, la clase `VentanaPrincipal` integra este widget en la barra de estado (`QStatusBar`).
- **Inicialización:** Se instancia `WordCounterWidget` y se añade como widget permanente.
- **Conexión:** El método `al_cambiar_texto` del editor captura el texto actual y llama a `word_counter.update_from_text(texto)` para refrescar los datos automáticamente.
