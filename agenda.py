import flet as ft 
from flet import Column, Page
from flet_route import Params, Basket
#traer la clase de la conexion a la base de datos
from Clases.conexionDB import *
#CLASE DE DATE PICKER
from Clases.yourdate import Yourdate
class Agenda(Column):
    def _init_(self):
        super()._init_()
    #Funcion para ir a formCliente
    def goBack(self, e, page):
        page.go("/formCliente")

    #lO QUE HICE FUE AÑADIR EL PARAMETRO PAGE PARA QUE LO RECONOCIERA Y LUEGO PASARSELO 
    def agendaForm(self, page):
        # Encabezado del formulario
        title_text = ft.Container(
            padding=ft.padding.only(top=15),
            content=ft.Text(value="Agenda una cita", size=50, color="black"),
            alignment=ft.alignment.center,
        )

        # Cuerpo del formulario
        procedimiento_field = ft.TextField(label="Procedimiento a realizar:",width=300, height=100, color="black")
        procedimiento = ft.Container(
            content=procedimiento_field,
            alignment=ft.alignment.center
        )
        fecha_field = (Yourdate(self.page))
        fecha = ft.Container(
            content=fecha_field,
            alignment=ft.alignment.center
        )
        hora_field = ft.TextField(label="Hora de la cita:", width=300, height=90, color="black")
        hora = ft.Container(
            content=hora_field,
            alignment=ft.alignment.center
        )
        
        # Botones para cancelar operación o agendar
        cancelarButton = ft.Container(
            content=ft.FilledButton(
                text="Cancelar",
                on_click=lambda e: self.goBack(e, page),
                width=140,
                height=50,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                )
            ),
            padding=ft.padding.only(right=16),  # Agrega espacio a la derecha
        )

        confirmarButton = ft.Container(
            content=ft.FilledButton(
                text="Agendar",
                width=140,
                height=50,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                )
            ),
            padding=ft.padding.only(left=16),  # Agrega espacio a la izquierda
        )
        
        botones = ft.Row(
            controls=[cancelarButton, confirmarButton],
            alignment=ft.MainAxisAlignment.CENTER,  # Centrar los botones horizontalmente
            spacing=32,  # Agrega espacio entre los botones
        )

        return ft.Column(
            controls=[
                title_text, 
                procedimiento, 
                fecha,
                hora, 
                botones
            ],
            #alignment=ft.Alignment.center
        )

    def build(self, page: ft.Page, params=Params, basket=Basket):
        column = self.agendaForm(page) 
        return ft.View(
            '/agenda',
            controls=[
                column
            ],
        )