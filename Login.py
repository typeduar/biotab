import flet as ft
import crud

# Función principal de la aplicación
def main(page: ft.Page):
    # Definir el tamaño de la ventana (opcional)
    # page.window_width = 400
    #page.window_height = 400
    page.window_maximized = True
    page.title = "Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    #page.bgcolor = "#9c1d46"

    # Función para manejar el login cuando se presiona el botón
    def login(e):
        # Obtener valores de los TextFields
        username = username_input.value
        password = password_input.value

        # Validación de ejemplo
        if username == "admin" and password == "1234":
            # Cambiar a la siguiente página si el login es exitoso
            #status_message.value = "¡Login exitoso! Redirigiendo..."
            #status_message.color = ft.colors.GREEN

            # Actualizar la página antes de redirigir
            #page.update()

            # Esperar un poco antes de redirigir (opcional)
            page.clean()
            crud.main(page)
            page.update()
            # page.window_destroy()  # Cierra la ventana actual de Flet

            # Ejecutar el archivo UI.py
            # os.system("python crud.py")
        else:
            # Mostrar mensaje de error si las credenciales no son correctas
            status_message.value = "Credenciales incorrectas. Inténtalo de nuevo."
            status_message.color = ft.colors.RED

        # Actualizar la página
        page.update()

    # Campo de texto para el nombre de usuario
    username_input = ft.TextField(label="Usuario", width=300)

    # Campo de texto para la contraseña
    password_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)

    # Botón de login
    login_button = ft.ElevatedButton(text="Iniciar sesión", on_click=login)

    # Mensaje de estado (para mostrar errores o éxito)
    status_message = ft.Text(value="", color=ft.colors.RED)

    # Contenedor principal, centrado tanto vertical como horizontalmente
    container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Sistema de Login", size=24, weight="bold", color=ft.colors.DEEP_ORANGE_ACCENT),
                username_input,
                password_input,
                login_button,
                status_message
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center
    )

    # Añadir el contenedor a la página
    page.add(container)

# Ejecutar la aplicación de Flet
ft.app(target=main)