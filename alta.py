from pyairtable.orm import Model  # Importa el modelo base
from pyairtable.orm import fields as F  # Importa los campos con un alias 'F'

class Registro(Model):
    registro_id = F.IntegerField("id")  # Campo de ID
    nombre = F.TextField("nombre")
    tipo = F.SelectField("tipo")
    puesto = F.SelectField("puesto")
    proyecto = F.TextField("proyecto")

    class Meta:
        api_key = "patJMgdIkhAYY9k9c.50bb22ba05794422b39ded86b994a50030b0a04b0f4e4d2df085f253bdd6cfd2"
        base_id = "appAWeEzV9HYXEAHi"
        table_name = "Clientes"