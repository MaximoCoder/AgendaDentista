#CONEXION A DB
import flet as ft
from flet import Page, Column,Tab, Tabs
from flet_route import Params, Basket
from Clases.controls import *
#INSTANCIA PARA UTILIZAR LOS CONTROLES
control = Controls()
# Nombre de la tabla
nombre_tabla = "clientes"
# Obtener los nombres de las columnas
nombres_columnas = control.obtenerNombresColumnas(nombre_tabla)
#Style attributes for header class
header_style= {
      "height": 60,
      "bgcolor": "#76ABAE",
      "border_radius": ft.border_radius.only(top_left=15, top_right=15),
      "padding": ft.padding.only(left=15, right=15),
}
#Method that creates and return textfield
def search_field(function: callable):
      return ft.TextField(
            border_color="transparent",
            width=350,
            height=20,
            text_size=15,
            content_padding=0,
            cursor_color="white",
            cursor_width=1,
            color="white",
            hint_text="Search",
            on_change=function
      )
#Method that adds a container to the search field
def search_bar(control: ft.TextField):
      return ft.Container(
            bgcolor="white10",
            border_radius=6,
            opacity=0,
            animate_opacity=300,
            padding=8,
            content = ft.Row(
                  spacing=10,
                  vertical_alignment="center",
                  controls=[
                        ft.Icon(
                              name=ft.icons.SEARCH_ROUNDED,
                              size=20,
                              opacity=0.85
                        ),
                        control
                  ]
            )

      )
#Define header class
class Header(ft.Container):
    def __init__(self, page,dt: ft.DataTable):
        super().__init__(**header_style,
                         on_hover=self.toggle_search 
                         )
        #Define attributes
        self.dt = dt
        self.page = page  # Store the 'page' parameter for later use
        #Create a textfield for search
        self.search_value = search_field(self.filter_data)
        #Create a search box
        self.search = search_bar(self.search_value)
        #Define other class attributes
        self.name = ft.Text("MBCMPRUASN", color="white", size=18, weight=700)
        self.logout = ft.IconButton(icon=ft.icons.LOGOUT, icon_color="white", tooltip="Cerrar sesion", on_click=self.logOut, width=40)
        #Compile the attributes
        self.content = ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                self.name,
                self.search, 
                self.logout
            ]
        )
    #Method that log out
    def logOut(self, e: ft.TapEvent):
        #VALIDAR SI SE HACE CLICK
        self.page.go("/")  # Use the stored 'page' for redirecting
    #Method that toggle search bar visibility
    def toggle_search(self, e: ft.HoverEvent):
        #SE MUESTRA SI HACES HOVER Y SI NO SE OCULTA
        self.search.opacity = 1 if e.data == 'true' else 0
        self.search.update()
    #Define a placeholder method for filter data
    def filter_data(self, e):
        for data_rows in self.dt.rows:
            data_cell = data_rows.cells[0]
            data_rows.visible = (
                True
                if e.control.value.lower() in data_cell.content.value.lower()
                else False
            )
            data_rows.update()
#Define form class styling and attributes
form_style = {
    "border_radius": 8,
    "border": ft.border.all(1, "#ebebeb"),
    "bgcolor": "white10",
    "padding": 15,
}
#Method that creates and return textfield
def text_field():
    return ft.TextField(
        border_color="transparent",
        height=30,
        text_size=15,
        content_padding=0,
        cursor_color="black",
        cursor_width=1,
        color="black",
    )
    
#Defin e a container to mantain the textfield
def text_field_container(
    expand: bool | int, name: str, control: ft.TextField
):
    return ft.Container(
        expand=expand,
        height=45,
        bgcolor="#ebebeb",
        border_radius=6,
        padding=8,
        content=ft.Column(
            spacing=1,
            controls=[
                ft.Text(
                    value = name, 
                    size=9,
                    color="black",
                    weight="bold"
                ),
                control
            ]
        )
    )
#Define form class
class formClient(ft.Container):
    def __init__(self, page,  dt: ft.DataTable):
        super().__init__(**form_style)
        #Define attributes
        self.dt = dt
        self.page = page  # Store the 'page' parameter for later use
        #Define the num of rows for textfields
        self.row1_value = text_field()
        self.row2_value = text_field()
        self.row3_value = text_field()
        
        #Define and contain the textfields
        self.row1 = text_field_container(True, "Nombre", self.row1_value)
        self.row2 = text_field_container(True, "Email", self.row2_value)
        self.row3 = text_field_container(True, "Telefono", self.row3_value)
        

        #Button to submit
        self.submit = ft.ElevatedButton(
            text="Añadir",
            style=ft.ButtonStyle(
                shape={"": ft.RoundedRectangleBorder(radius=8)},
            ),
            on_click=self.submit_data
        )
        #Compile the attributes
        self.content = ft.Column(
            expand=True,
            controls=[
                ft.Row(controls=[ft.Text("Llena los campos con los datos del cliente", size=20, color="black")]),
                ft.Row(controls=[self.row1, self.row2]),
                ft.Row(controls=[self.row3]),
                ft.Row(controls=[self.submit], alignment="end")
            ]
        )
    #Enviar los datos a la base de datos
    def submit_data(self,e:ft.TapEvent=None):
        self.row_values = (self.row1_value.value, self.row2_value.value, self.row3_value.value)
        #print(self.row_values)
        # Validar si los campos no están vacíos
        if all(self.row_values):
            if control.submit_data(e, self.row_values):  # Si submit_data devuelve True
                #Mostrar que se insertó
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("¡Se guardo correctamente el cliente!", color="white", weight="bold"),
                    action="Okey!",
                    bgcolor="green",
                    action_color="white",
                    duration=3000)
                self.page.snack_bar.open = True
                self.dt.refresh_data()  # Actualizar la tabla de datos
                self.clear_inputs()  # Llamar a clear_inputs
                self.page.update()  # Actualizar la página
            else:
                #Mostrar que no se insertó
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Hubo un problema al guardar el registro.", color="white", weight="bold"),
                    action="Okey!",
                    bgcolor="red",
                    action_color="white",
                    duration=3000)
                self.page.snack_bar.open = True
                self.page.update()
        else:
            dlg = ft.AlertDialog(title=ft.Text("Por favor llena todos los campos", color="white"))
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()
    
    #Method for delete user input after submit
    def clear_inputs(self):
        #Borra los valores de los campos
        self.row1_value.value = ""
        self.row2_value.value = ""
        self.row3_value.value = ""
        self.content.update()

#Datatable styles and attributes
data_table_style = {
    "expand": True,
    "border_radius": 8,
    "border": ft.border.all(2, "#ebebeb"),
    "horizontal_lines": ft.border.BorderSide(1, "#ebebeb"),
    "columns": [
        #Traer los datos de la base de datos(los titulos de las columnas)
        ft.DataColumn(ft.Text(index, size=13, color="black", weight="bold"))
        for index in [nombres_columnas[i] for i in [1,2,3] ] #MUESTRA SOLO 4 COLUMNAS NOMBRE, TELEFONO, CORREO Y ACCIONES
    ] + [ft.DataColumn(ft.Text("ACCIONES", size=13, color="black", weight="bold"))] #Columna Acciones
}
class DataTable(ft.DataTable):
    def __init__(self):
        super().__init__(**data_table_style)
        self.data = control.get_data('clientes')
    #Funcion para eliminar un registro
    def delete_data(self, id_cliente):
        control.delete_data('clientes', f"id_cliente = {id_cliente}")
        self.refresh_data()
        # Muestra una SnackBar si la consulta es exitosa
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("¡Registro eliminado con éxito!", color="white", weight="bold"),
            action="Okey!",
            bgcolor="green",
            action_color="white",
            duration=3000)
        self.page.snack_bar.open = True
        self.page.update()

    #Funcion para abrir modal para eliminar un registro
    def close_dlg(self, e):
        self.dlg_modal.open = False
        self.page.update()
    def show_alert_dialog(self, id_cliente):
        self.dlg_modal = ft.AlertDialog(
            title=ft.Text("¿Estas seguro de eliminar este registro?"),
            #content=ft.Text("No podras recuperarlo"),
            actions=[
                ft.TextButton("Si, Estoy seguro", on_click=lambda e: self.delete_data(id_cliente)),
                ft.TextButton("Cancelar", on_click=self.close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        #self.page.update()
    
    #Funcion para editar un registro
    def update_data(self, id_cliente, row1_value, row2_value, row3_value):
       condition = f"id_cliente = {id_cliente}"
       #Muestra mensaje de exito o fallo
       if(control.update_data('clientes', (row1_value, row2_value, row3_value), condition)):
            self.refresh_data()
            # Muestra una SnackBar si la consulta es exitosa
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("¡Registro actualizado con éxito!", color="white", weight="bold"),
                action="Okey!",
                bgcolor="green",
                action_color="white",
                duration=3000)
            self.page.snack_bar.open = True
            self.page.update()
       else:
            # Muestra una SnackBar si la consulta fallo
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("¡Lo sentimos algo salio mal, vuelve a intentarlo!", color="white", weight="bold"),
                action="Okey!",
                bgcolor="red",
                action_color="white",
                duration=3000)
            self.page.snack_bar.open = True
            self.page.update()
           
    def add_data_to_table(self):
        self.rows = []
        for row in self.data:
            id_cliente = row['id_cliente']
            data_row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(row['nombre_cliente'], size=13, color="black")),
                    ft.DataCell(ft.Text(row['tel_cliente'], size=13, color="black")),
                    ft.DataCell(ft.Text(row['email_cliente'], size=13, color="black")),
                    ft.DataCell(ft.Row([
                        ft.IconButton("edit_calendar_rounded", icon_color="black", tooltip="Agendar"),
                        ft.IconButton("edit", icon_color="blue", tooltip="Editar", on_click=lambda e: self.update_data(id_cliente)),
                        ft.IconButton("delete", icon_color="red", tooltip="Eliminar", on_click=lambda e: self.show_alert_dialog(id_cliente)),  # Añade un manejador de eventos de clic),
                    ])),
                ]
            ) 
            self.rows.append(data_row)


    #Funcion para que se actualice la tabla con los nuevos registros.
    def refresh_data(self):
        self.data = control.get_data('clientes')
        self.add_data_to_table()

class formularioClientes(Column):
    def __init__(self):
        super().__init__()
        # Define las pestañas
        self.table = DataTable()  
        self.tabs = Tabs(
            selected_index=0,
            expand=True,
            animation_duration=300,
            label_color="black",
            tabs=[
                ft.Tab(
                    text="Clientes",
                    icon=ft.icons.PEOPLE_ROUNDED,
                    content=ft.Column(
                        scroll="auto",
                        expand=True,  
                        controls=[ft.Row(controls=[self.table])], #tabla de clientes
                    ),
                ), 
                ft.Tab(
                    text="Agenda",
                    icon=ft.icons.CALENDAR_MONTH_ROUNDED,
                    content=ft.Column(
                        scroll="auto",
                        expand=True,
                        controls=[
                            ft.Text("Agenda", size=20, color="black")
                        ],
                    ),        
                ), 
            ],
        )
    def main(self, page):
        page.title = "Registro"         
        self.header = Header(page, dt=self.table)
        self.form = formClient(page, dt=self.table)   

        column = ft.Column(
                expand=True,
                controls=[
                    #Header
                    self.header,
                    ft.Divider(height=2, color="transparent"),
                    #Form 
                    self.form,
                    ft.Divider(height=2, color="transparent"),
                    #Table
                    ft.Row(
                        controls=[self.tabs], expand=True #tabla
                    ),
                ],
            )
        
        self.table.add_data_to_table()
        # Actualizar la tabla con los nuevos datos
        self.table.refresh_data()
        return column
    #Regresa la vista
    def build(self, page: ft.Page, params=Params, basket=Basket):
        column = self.main(page) 
        return ft.View(
            "/formCliente",
            controls=[
                column
            ],
            bgcolor="white"
        )