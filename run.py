import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

try:
    from main_modular import main

    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"Error: No se pudo encontrar el modulo principal: {e}")
    print("Asegurate de que 'main_modular.py' este dentro de la carpeta 'src'.")