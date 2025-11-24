  ## Entorno de trabajo - Pipenv / Pipx
  1) Instalar pipx (opcional si ya lo tienes):
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
