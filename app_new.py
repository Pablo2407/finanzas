"""
Punto de entrada de la aplicación Finanzas
Importa la aplicación desde src/
"""
import sys
import os

# Agregar src al path para que los imports funcionen
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importar la aplicación desde src
from core import app

if __name__ == '__main__':
    app.run(debug=True)
