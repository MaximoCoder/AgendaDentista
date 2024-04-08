import flet as ft 
from flet import Column, Page
from flet_route import Params, Basket
#traer la clase de la conexion a la base de datos
from Clases.conexionDB import *
#Traer la clase de login del index
from Clases.usuario import *
class UserLogin(Column):
    def _init_(self):
        super()._init_()
    #lO QUE HICE FUE AÑADIR EL PARAMETRO PAGE PARA QUE LO RECONOCIERA Y LUEGO PASARSELO 
    def login_form(self, page):
        # Encabezado del formulario
        title_text = ft.Container(
            padding=ft.padding.only(top=20),
            content=ft.Text(value="Inicia sesion", size=60, color="black"),
            alignment=ft.alignment.center,

        )

        # Cuerpo del formulario
        username_field = ft.TextField(label="Nombre de usuario", autofocus=True, width=350, height=100, color="black")
        username = ft.Container(
            content=username_field,
            alignment=ft.alignment.center
        )
        password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=350, height=100, color="black")
        password = ft.Container(
            content=password_field,
            alignment=ft.alignment.center
        )

        # Función para manejar el inicio de sesión
        def handleLogin(e):
            user = username_field.value
            passw = password_field.value
            if user == "" or passw == "":
                dlg = ft.AlertDialog(title=ft.Text("Porfavor llena todos los campos", color="black"))
                page.dialog = dlg
                dlg.open = True
                page.update()
            elif Login.authenticate(user, passw):
                #Redireccionar
                page.go("/formCliente")
            else:
                dlg = ft.AlertDialog(title=ft.Text("Credenciales incorrectas", color="black"))
                page.dialog = dlg
                dlg.open = True
                page.update()
        # Botón para iniciar sesión
        login_button = ft.Container(
            content= ft.FilledButton(
                text="Login",
                on_click=handleLogin,  
                width=300,
                height=50,
            ),
            alignment=ft.alignment.center
        ) 

        return ft.Column(
            controls=[
                title_text, 
                username, 
                password, 
                login_button
            ],
            #alignment=ft.Alignment.center
        )

    def build(self, page: ft.Page, params=Params, basket=Basket):
        return ft.View(
            '/',
            controls=[
                self.login_form(page)
            ],
            bgcolor="white"
        )