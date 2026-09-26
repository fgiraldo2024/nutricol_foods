import pandas as pd
from tkinter import Tk, filedialog

# Ocultar ventana principal de Tkinter
Tk().withdraw()

# Seleccionar archivo JSON
ruta_json = filedialog.askopenfilename(
    title="Selecciona el archivo JSON del catálogo",
    filetypes=[("JSON files", "*.json")]
)

# Leer JSON
df = pd.read_json(ruta_json)

# Seleccionar dónde guardar el Excel
ruta_excel = filedialog.asksaveasfilename(
    title="Guardar catálogo en Excel",
    defaultextension=".xlsx",
    filetypes=[("Excel files", "*.xlsx")]
)

# Guardar como Excel
df.to_excel(ruta_excel, index=False)

print("✅ Catálogo convertido a Excel correctamente:", ruta_excel)
