import pandas as pd
from tkinter import Tk, filedialog
import json

# Ocultar ventana principal de Tkinter
Tk().withdraw()

# Seleccionar archivo Excel
ruta_excel = filedialog.askopenfilename(
    title="Selecciona el archivo Excel del catálogo",
    filetypes=[("Excel files", "*.xlsx *.xls")]
)

# Leer Excel
df = pd.read_excel(ruta_excel)

# Convertir a lista de diccionarios
productos = df.to_dict(orient="records")

# Seleccionar ubicación para guardar JSON
ruta_json = filedialog.asksaveasfilename(
    title="Guardar catálogo en JSON",
    defaultextension=".json",
    filetypes=[("JSON files", "*.json")]
)

# Guardar JSON con indentación
with open(ruta_json, "w", encoding="utf-8") as f:
    json.dump(productos, f, ensure_ascii=False, indent=2)

print("✅ Catálogo convertido a JSON correctamente:", ruta_json)
