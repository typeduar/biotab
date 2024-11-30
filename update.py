import flet as ft
from alta import Registro

def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.theme_mode = "light"
    page.window_maximized = True

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

    def cargar_datos():
        data_table.rows.clear()

        registros = Registro.all()  # Obtener todos los registros

        for reg in registros:
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(reg.registro_id))),
                    ft.DataCell(ft.Text(reg.nombre)),
                    ft.DataCell(ft.Text(reg.tipo)),
                    ft.DataCell(ft.Text(reg.puesto)),
                    ft.DataCell(ft.Text(reg.proyecto)),
                ],
                on_select_changed=lambda e, r=reg: seleccionar_fila(r)
            )
            data_table.rows.append(row)

        data_table.update()

    # Función para seleccionar una fila y llenar los campos
    def seleccionar_fila(registro):
        nonlocal selected_row  # Hacer la variable accesible dentro de esta función
        selected_row = registro
        txt_nombre.value = registro.nombre
        drp_tipo.value = registro.tipo
        drp_puesto.value = registro.puesto
        txt_titulo.value = registro.proyecto
        print(registro.id)
        #Registro.delete(registro.id)

        page.update()

    def actualizar_datos(e: ft.ControlEvent):
        nonlocal selected_row  # Asegurarse de que selected_row esté disponible en la función
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

        cargar_datos()  # Recargar la tabla

    def eliminar_datos(e: ft.ControlEvent):
        nonlocal selected_row  # Hacer que la variable sea accesible en la función eliminar
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
            Registro.delete(selected_row) # Si selected_row ya es un ID


            # Reiniciar la selección y limpiar los campos
            selected_row = None
            txt_nombre.value = ""
            drp_tipo.value = None
            drp_puesto.value = None
            txt_titulo.value = ""

            page.snack_bar = ft.SnackBar(
                content=ft.Text("Registro eliminado correctamente."),
                bgcolor="green",
                show_close_icon=True
            )
            page.snack_bar.open = True
            page.update()

            # Recargar la tabla
            cargar_datos()

        except Exception as error:
            # En caso de error, mostrar un mensaje de error
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error al eliminar el registro: {error}"),
                bgcolor="red",
                show_close_icon=True
            )
            page.snack_bar.open = True
            page.update()

    # Crear los componentes de la primera columna
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

    first_col = ft.Column(
        [
            txt_nombre,
            drp_tipo,
            drp_puesto,
            txt_titulo,
            ft.Row(
                [
                    ft.ElevatedButton("Actualizar", icon="REFRESH", bgcolor="#9d1d46", color="white", on_click=actualizar_datos),
                    ft.ElevatedButton("Eliminar", icon="REMOVE_CIRCLE", bgcolor="#9d1d46", color="white", on_click=eliminar_datos),
                ]
            )
        ],
        spacing=10,
    )

    second_col = ft.Column([data_table], spacing=10)

    main_row = ft.Row([first_col, second_col], spacing=20)

    page.add(ft.Image(src="logo.png", width=300, height=163))
    page.add(main_row)

    cargar_datos()

ft.app(target=main)