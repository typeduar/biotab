import flet as ft
from alta import Registro  # Supongo que `alta` es el módulo que maneja los registros.

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

    # Variable para almacenar la fila seleccionada
    selected_row = None

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
            # Guardar los datos en la base de datos
            nuevo_registro = Registro(
                registro_id=int(id_value),
                nombre=nombre_value,
                tipo=tipo_value,
                puesto=puesto_value,
                proyecto=titulo_value
            )
            nuevo_registro.save()

            page.snack_bar = ft.SnackBar(
                content=ft.Text("Datos guardados correctamente"),
                bgcolor="green",
                show_close_icon=True
            )
            page.snack_bar.open = True
            page.update()

            # Limpiar campos después de registrar
            limpiar_campos()

            # Actualizar la tabla de datos automáticamente
            cargar_datos()

    # Función para cargar los datos en la tabla
    def cargar_datos():
        data_table.rows.clear()

        # Obtener todos los registros desde la base de datos
        registros = Registro.all()

        for reg in registros:
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(reg.registro_id))),  # ID
                    ft.DataCell(ft.Text(reg.nombre)),            # Nombre
                    ft.DataCell(ft.Text(reg.tipo)),              # Tipo
                    ft.DataCell(ft.Text(reg.puesto)),            # Puesto
                    ft.DataCell(ft.Text(reg.proyecto)),          # Título del proyecto
                ],
                on_select_changed=lambda e, r=reg: seleccionar_fila(r)
            )
            data_table.rows.append(row)

        data_table.update()

    # Función para seleccionar una fila y llenar los campos
    def seleccionar_fila(registro):
        nonlocal selected_row
        selected_row = registro
        txt_nombre.value = registro.nombre
        drp_tipo.value = registro.tipo
        drp_puesto.value = registro.puesto
        txt_titulo.value = registro.proyecto
        page.update()

    # Función para actualizar datos
    def actualizar_datos(e: ft.ControlEvent):
        nonlocal selected_row
        if selected_row is None:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Por favor, seleccione un registro para actualizar."),
                bgcolor="red",
                show_close_icon=True
            )
            page.snack_bar.open = True
            page.update()
            return

        # Actualizar los datos
        selected_row.nombre = txt_nombre.value.strip() or selected_row.nombre
        selected_row.tipo = drp_tipo.value or selected_row.tipo
        selected_row.puesto = drp_puesto.value or selected_row.puesto
        selected_row.proyecto = txt_titulo.value.strip() or selected_row.proyecto

        selected_row.save()

        page.snack_bar = ft.SnackBar(
            content=ft.Text("Registro actualizado correctamente."),
            bgcolor="green",
            show_close_icon=True
        )
        page.snack_bar.open = True
        page.update()

        # Limpiar campos después de actualizar
        limpiar_campos()

        cargar_datos()

    # Función para eliminar datos
    def eliminar_datos(e: ft.ControlEvent):
        nonlocal selected_row
        if selected_row is None:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Por favor, seleccione un registro para eliminar."),
                bgcolor="red",
                show_close_icon=True
            )
            page.snack_bar.open = True
            page.update()
            return

        try:
            Registro.delete(selected_row)  # Eliminar registro

            page.snack_bar = ft.SnackBar(
                content=ft.Text("Registro eliminado correctamente."),
                bgcolor="green",
                show_close_icon=True
            )
            page.snack_bar.open = True
            page.update()

            # Limpiar campos después de eliminar
            limpiar_campos()

            cargar_datos()

        except Exception as error:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error al eliminar el registro: {error}"),
                bgcolor="red",
                show_close_icon=True
            )
            page.snack_bar.open = True
            page.update()

    # Función para limpiar los campos de texto
    def limpiar_campos():
        txt_id.value = ""
        txt_nombre.value = ""
        drp_tipo.value = None
        drp_puesto.value = None
        txt_titulo.value = ""
        page.update()

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
                    ft.ElevatedButton("Cancelar", icon="close", bgcolor="#9d1d46", color="white", on_click=lambda e: page.window.close()),
                ]
            ),
            ft.Row(
                [
                    ft.ElevatedButton("Actualizar", icon="REFRESH", bgcolor="#9d1d46", color="white", on_click=actualizar_datos),
                    ft.ElevatedButton("Eliminar", icon="REMOVE_CIRCLE", bgcolor="#9d1d46", color="white", on_click=eliminar_datos),
                ]
            ),
        ],
        spacing=10,
    )

    # Segunda columna con tabla de datos
    second_col = ft.Column([data_table], spacing=10)

    main_row = ft.Row([first_col, second_col], spacing=20)

    # Añadir el logo y el contenedor principal a la página
    page.add(ft.Image(src="logo.png", width=300, height=163))
    page.add(main_row)

    cargar_datos()

ft.app(target=main, view=ft.AppView.WEB_BROWSER)