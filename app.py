import flet as ft
from flet_route import Routing,path
#Importar views
from Login import UserLogin #Vista de login
from formCliente import formularioClientes #Vista de formulario de cliente
#Instancia para utilizar la funcion build de login
login = UserLogin()
#Instancia para utilizar build de formulario de cliente
formCliente = formularioClientes()
def main(page: ft.Page):
    #Tema
    page.theme_mode = ft.ThemeMode.LIGHT
    #Tamaño de la ventana
    page.window_width = 900
    page.window_height = 800
    app_routes = [
        path(url="/", clear=True, view=login.build),
        path(url="/formCliente", clear=True, view=formCliente.build),
    ]
    #Funcion para manejar las rutas
    Routing(page=page, app_routes=app_routes)
    
    page.go(page.route)
    #print(page.route)
ft.app(target=main)
#ft.app(target=main, view=ft.AppView.WEB_BROWSER)