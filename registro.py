import flet as ft
from alta import Registro
import update  # Importamos el archivo update.py

def main(page: ft.Page):

    # Configurar la página para que esté en pantalla completa
    page.horizontal_alignment = "center"
    page.theme_mode = "light"
    page.window_maximized = True

    # Añadir la barra de aplicaciones con el título
    page.appbar = ft.AppBar(
        title=ft.Text(
            "Consulta de Proyectos",
            style=ft.TextStyle(
                size=30,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.WHITE,
            ),
        ),
        center_title=True,
        bgcolor="#9d1d46",
    )

    # Función para registrar datos
    def registrar_datos(e: ft.ControlEvent):
        # Validar que los campos no estén vacíos
        id_value = txt_id.value.strip()
        nombre_value = txt_nombre.value.strip()
        tipo_value = drp_tipo.value
        puesto_value = drp_puesto.value
        titulo_value = txt_titulo.value.strip()

        error = ""
        if id_value == "":
            error = "ID vacío"
        if nombre_value == "":
            error = "Nombre vacío"
        if tipo_value is None:
            error = "Por favor seleccione un tipo"
        if puesto_value is None:
            error = "Por favor seleccione un puesto"
        if titulo_value == "":
            error = "Título del proyecto vacío"
        
        if error:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(error),
                bgcolor="red",
                show_close_icon=True
            )
            page.snack_bar.open = True
            page.update()
        else:
            # Guardar los datos en Airtable
            nuevo_registro = Registro(
                registro_id=int(id_value),  # Usamos 'registro_id' en lugar de 'id'
                nombre=nombre_value,
                tipo=tipo_value,
                puesto=puesto_value,
                proyecto=titulo_value
            )
            nuevo_registro.save()

            # Mostrar mensaje de éxito
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Datos guardados correctamente"),
                bgcolor="green",
                show_close_icon=True
            )
            page.snack_bar.open = True
            page.update()

            # Limpiar campos después de registrar
            txt_id.value = ""
            txt_nombre.value = ""
            drp_tipo.value = None
            drp_puesto.value = None
            txt_titulo.value = ""
            page.update()

            # Actualizar la tabla de datos automáticamente
            cargar_datos()

    # Función para redirigir al archivo update.py
    def abrir_update(e: ft.ControlEvent):
        ft.app(target=update.main)  # Cambiar el objetivo de la aplicación a la ventana de update.py

    # Función para cargar los datos en la tabla
    def cargar_datos():
        # Limpiar filas existentes
        data_table.rows.clear()
        
        # Obtener todos los registros desde la base de datos
        registros = Registro.all()  # Suponiendo que tienes un método `all` para obtener todos los registros
        
        # Agregar cada registro a la tabla
        for reg in registros:
            data_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(reg.registro_id))),  # ID
                    ft.DataCell(ft.Text(reg.nombre)),            # Nombre
                    ft.DataCell(ft.Text(reg.tipo)),              # Tipo
                    ft.DataCell(ft.Text(reg.puesto)),            # Puesto
                    ft.DataCell(ft.Text(reg.proyecto)),          # Título del proyecto
                ])
            )

        # Actualizar la tabla
        data_table.update()

    # Función para cerrar la aplicación
    def cerrar_ventana(e: ft.ControlEvent):
        page.window.close()

    # Crear los componentes de la primera columna
    txt_id = ft.TextField(label="ID")
    txt_nombre = ft.TextField(label="Nombre")
    drp_tipo = ft.Dropdown(
        label="Tipo",
        options=[
            ft.dropdown.Option("Ganaderos"),
            ft.dropdown.Option("Agroindustriales"),
            ft.dropdown.Option("Aguas Residuales")
        ]
    )
    drp_puesto = ft.Dropdown(
        label="Puesto",
        options=[
            ft.dropdown.Option("Estudiantes"),
            ft.dropdown.Option("Investigadores")
        ]
    )
    txt_titulo = ft.TextField(label="Título del proyecto")

    # Crear la tabla de datos
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("NOMBRE")),
            ft.DataColumn(ft.Text("TIPO")),
            ft.DataColumn(ft.Text("PUESTO")),
            ft.DataColumn(ft.Text("TÍTULO DEL PROYECTO")),
        ],
        rows=[],
    )

    # Primera columna con campos de texto
    first_col = ft.Column(
        [
            txt_id,
            txt_nombre,
            drp_tipo,
            drp_puesto,
            txt_titulo,
            ft.Row(
                [
                    ft.ElevatedButton("Registrar", icon="PERSON_ADD", bgcolor="#9d1d46", color="white", on_click=registrar_datos),
                    ft.ElevatedButton("Cancelar", icon="close", bgcolor="#9d1d46", color="white", on_click=cerrar_ventana),
                ]
            )
        ],
        spacing=10,
    )

    # Segunda columna con tabla de datos
    second_col = ft.Column(
        [
            data_table,
            ft.Row(
                [
                    ft.ElevatedButton("Actualizar", icon="REFRESH", bgcolor="#9d1d46", color="white", on_click=abrir_update),
                    ft.ElevatedButton("Dar de Baja", icon="REMOVE_CIRCLE", bgcolor="#9d1d46", color="white"),
                ]
            )
        ],
        spacing=10,
    )

    # Contenedor principal que tiene las dos columnas
    main_row = ft.Row(
        [
            first_col,
            second_col,
        ],
        spacing=20,
    )

    # Añadir el logo y el contenedor principal a la página
    page.add(ft.Image(src="logo.png", width=300, height=163))
    page.add(main_row)

    # Cargar los datos automáticamente cuando la página se carga
    cargar_datos()

# Ejecutar la aplicación
ft.app(target=main)
