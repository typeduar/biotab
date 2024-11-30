from pyairtable import Api
from pprint import pprint

api = Api("patJAcnzXoKrZ5kZs.9729454de33415bac9b52904d3b52e67b806862d92626bc829cb7c103a6f088a")
tabla = api.table("appMOohPbcCVXTXn9", "estudios")

# Crear un nuevo registro
#nuevo = {"id_estudios": 101,
#         "nombre": "TikTokero",
#         "clasificacion": "Doctorado"}
#tabla.create(nuevo)

# Mostrar todos los registros
registros = tabla.all()
for r in registros:
    pprint(r)
    # Imprimir solamente mis campos
    #pprint(r['fields'])