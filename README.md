## Memoria de comandos

  1. Crear e inicializar el entorno con pipenv (convirtiendo `requirements.txt` a `Pipfile`):

  pipenv install -r requirements.txt
  pipenv install


  pipenv install pyside6 pyinstaller


  3. (Opcional) Instalar PyInstaller global con pipx:

  pipx install pyinstaller


  4. Verificar versiones en el entorno:

  pipenv run python -c "import PySide6, PySide6.QtCore as QC, PyInstaller; \
  print('PySide6', PySide6.version); print('Qt', QC.qVersion()); \
  print('PyInstaller', PyInstaller.version)"


  5. Construir el ejecutable (incluyendo carpeta `Images`):

  pipenv run pyinstaller --clean --noconfirm --windowed --onefile \
  --name MiniOffice --add-data "Images;Images" MiniOffice.py


  6. (Consulta de resultado y avisos):
  - Ejecutable generado en `dist/MiniOffice.exe`.
  - Avisos de PyInstaller en `build/MiniOffice/warn-MiniOffice.txt`.
