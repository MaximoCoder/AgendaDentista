#CONEXION A DB
import flet as ft
from flet import Page, Column,Tab, Tabs
from flet_route import Params, Basket
from Clases.controls import *
#Calendario
import calendar
from datetime import datetime, timedelta, date


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
        search_value = str(e.control.value).lower()  # Convertir e.control.value a cadena
        for data_rows in self.dt.rows:
            data_cell = data_rows.cells[1]
            data_rows.visible = (
                True if search_value in str(data_cell.content.value).lower() else False
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
            dlg = ft.AlertDialog(title=ft.Text("Por favor llena todos los campos", color="black"))
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
        ft.DataColumn(ft.Text("#", size=16, color="black", weight="bold")),
        *(ft.DataColumn(ft.Text(index, size=13, color="black", weight="bold")) for index in [nombres_columnas[i] for i in [1,2,3]]), #MUESTRA LAS COLUMNAS DE LA DB
        ft.DataColumn(ft.Text("ACCIONES", size=13, color="black", weight="bold")) #Columna Acciones
    ]
}
class DataTable(ft.DataTable):
    def __init__(self):
        super().__init__(**data_table_style)
        self.data = control.get_data('clientes')
    #Funcion para eliminar un registro
    def delete_data(self, id_cliente):
        self.page.dialog.open = False  # Cerramos el modal de eliminar
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
        self.page.dialog.open = False
        self.page.update()
    
    def show_delete_dialog(self, e):
        #Imprimir el id del cliente seleccionado
        #print("El id del cliente es = ",e.control.data['id_cliente'])
        id_cliente = e.control.data['id_cliente']
        #MODAL PARA ELIMINAR UN REGISTRO
        dlg = ft.AlertDialog(
            title=ft.Text("¿Estas seguro de eliminar este registro?"),
            content=ft.Text("No podras recuperarlo"),
            actions=[
                ft.TextButton("Si, Estoy seguro", on_click=lambda e: self.delete_data(id_cliente)),
                ft.TextButton("Cancelar", on_click=self.close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
    
    #Funcion para editar un registro
    def update_data(self, id_cliente, edit_Name, edit_Email, edit_Tel):
       self.page.dialog.open = False  # Cerramos el modal de editar
       condition = f"id_cliente = {id_cliente}"
       #Muestra mensaje de exito o fallo
       if(control.update_data('clientes', (edit_Name, edit_Email, edit_Tel), condition)):
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
           
    #Modal para editar un registro
    def show_update_dialog(self, e):
        #Imprimir el id del cliente seleccionado
        #print("El id del cliente es = ",e.control.data['id_cliente'])
        # CREATE EDIT INPUT
        edit_Name = ft.TextField(label="Name", autofocus=True,)
        edit_Email = ft.TextField(label="Email", autofocus=True,)
        edit_Tel = ft.TextField(label="Telefono", autofocus=True,)
        dlg = ft.AlertDialog(
            title=ft.Text("Editar cliente"),
            content=Column([
                edit_Name,
                edit_Email,
                edit_Tel
			],
                height=300,
                width=300
            ),
            actions=[
                ft.TextButton("Actualizar", on_click=lambda e: self.update_data(id_cliente, edit_Name.value, edit_Email.value, edit_Tel.value)),
                ft.TextButton("Cancelar", on_click=self.close_dlg), #Reutilizamos la funcion para cerrar modales.
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        #Traer los datos de esa row.
        id_cliente = e.control.data['id_cliente']
        edit_Name.value = e.control.data['nombre_cliente']
        edit_Email.value = e.control.data['email_cliente']
        edit_Tel.value = e.control.data['tel_cliente']
        #Abrir el modal
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    #Funcion para agendar cita
    def schedule_date(self, id_cliente, email_cliente, procedimiento_field, fechaText, horaPicker ):
        self.page.dialog.open = False  # Cerramos el modal de editar
        #Primero mandamos solo los datos de fecha y hora para verificar que no esta encimando un horario ocupado
        check_values = (fechaText, horaPicker)
        if control.check_disponibilidad(check_values):
            # Si la fecha y hora están disponibles, mandamos el resto de los datos
            row_values = (id_cliente, email_cliente, procedimiento_field, fechaText, horaPicker)
            if control.agendar_cita(row_values):
                #print("Cita agendada con éxito.")
                # Muestra una SnackBar si la consulta es exitosa
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("¡Se agendo correctamente la cita!", color="white", weight="bold"),
                    action="Okey!",
                    bgcolor="green",
                    action_color="white",
                    duration=3000)
                self.page.snack_bar.open = True
                self.page.update()
            else:
                #print("No se pudo agendar la cita.")
                # Muestra una SnackBar si la consulta fallo
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("¡Lo sentimos algo salio mal, vuelve a intentarlo!", color="white", weight="bold"),
                    action="Okey!",
                    bgcolor="red",
                    action_color="white",
                    duration=3000)
                self.page.snack_bar.open = True
                self.page.update()
        else:
            #print("La fecha y hora ya están ocupadas.")
            # Muestra una SnackBar si la consulta fallo
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("¡El horario que seleccionaste ya esta ocupado, por favor selecciona otra hora.!", color="white", weight="bold"),
                action="Okey!",
                bgcolor="red",
                action_color="white",
                duration=3000)
            self.page.snack_bar.open = True
            self.page.update()

        
    #Modal de cita    
    def show_schedule_dialog(self, e):
        #self.page.go("/agenda")
        #Traer los datos de esa row.
        id_cliente = e.control.data['id_cliente']
        email_cliente = e.control.data['email_cliente']
        #Create the inputs
            # Cuerpo del formulario
        procedimiento_field = ft.TextField(label="Procedimiento a realizar:",width=300, height=100, color="black")
        procedimiento = ft.Container(
            content=procedimiento_field,
            alignment=ft.alignment.center
        )

        #DATEPICKER

        # Calculate the current date
        current_date = datetime.now()

        # Calculate the last date as the current date plus 3 months
        last_date = current_date + timedelta(days=90)
        #TEXTO PARA MOSTRAR LA FECHA QUE SELECCIONA EL USUARIO
        fechaText = ft.Text(weight=ft.FontWeight.BOLD, size=20, color="black")  

        def change_date(e):
            fechaText.value = f"{fechaPicker.value.date()}"
            e.control.page.update()

        fechaPicker = ft.DatePicker(
            first_date=current_date,
            last_date=last_date,
            on_change=change_date,
        )
        self.page.overlay.append(fechaPicker)

        fecha_button = ft.ElevatedButton(
            "Selecciona la fecha:",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: fechaPicker.pick_date(),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            height=50,
            width=200
        )

        stackFecha = ft.Stack(
            [   
                ft.Row(
                    [fecha_button, fechaText],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ])

        fecha = ft.Container(
            content=stackFecha,
            alignment=ft.alignment.center,
        )
        #TIME PICKER
        timeText = ft.Text(weight=ft.FontWeight.BOLD, size=20, color="black")  
        def change_time(e):
            timeText.value = f"{horaPicker.value}"
            e.control.page.update()

        horaPicker = ft.TimePicker(
            confirm_text="Confirmar",
            error_invalid_text="El tiempo esta fuera de rango",
            help_text="Seleciona un tiempo",
            on_change=change_time,
        )
        self.page.overlay.append(horaPicker)
        time_button = ft.ElevatedButton(
            "Selecciona la hora:",
            icon=ft.icons.ACCESS_TIME_FILLED,
            on_click=lambda _: horaPicker.pick_time(),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            height=50,
            width=200
        )

        
        stackTime = ft.Stack(
            [   
                ft.Row(
                    [time_button, timeText],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ])
        
        hora = ft.Container(
            content=stackTime,
            alignment=ft.alignment.center
        )
        #TIME PICKER
        
        time_button = ft.TextField(
            label="seleccionar hora",
            icon=ft.icons.ACCESS_TIME,
        )
        #Create the dialog
        dlg = ft.AlertDialog(
            title=ft.Text("Agendar Cita"),
            content=Column([
                procedimiento,
                fecha,
                hora,
                
            ],
            height=300,
            width=300
            ),
            actions=[
                ft.TextButton("Agendar", on_click=lambda e:self.schedule_date(id_cliente, email_cliente, procedimiento_field.value, fechaText.value, horaPicker.value)),
                ft.TextButton("Cancelar", on_click=self.close_dlg), #Reutilizamos la funcion para cerrar modales.
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        #Abrir el modal
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def add_data_to_table(self):
        self.rows = []
        for row in self.data:
            data_row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(row['id_cliente'], size=13, color="black")),
                    ft.DataCell(ft.Text(row['nombre_cliente'], size=13, color="black")),
                    ft.DataCell(ft.Text(row['tel_cliente'], size=13, color="black")),
                    ft.DataCell(ft.Text(row['email_cliente'], size=13, color="black")),
                    ft.DataCell(ft.Row([
                        ft.IconButton("edit_calendar_rounded", data=row, icon_color="black", tooltip="Agendar", on_click=self.show_schedule_dialog),
                        ft.IconButton("edit", data=row, icon_color="blue", tooltip="Editar", on_click=self.show_update_dialog),
                        ft.IconButton("delete",data=row, icon_color="red", tooltip="Eliminar", on_click=self.show_delete_dialog),  # Añade un manejador de eventos de clic),
                    ])),
                ]
            ) 
            self.rows.append(data_row)


    #Funcion para que se actualice la tabla con los nuevos registros.
    def refresh_data(self):
        self.data = control.get_data('clientes')
        self.add_data_to_table()
#Clases del calendario
cal = calendar.Calendar()
 # pre-defined calendar maps ...
date_class: dict[int, str] = {
    0: "Lu",
    1: "Ma",
    2: "Mi",
    3: "Ju",
    4: "Vi",
    5: "Sa",
    6: "Do",
}

month_class: dict[int, str] = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}

# Date class to handle calendar logic ...
class Settings:
    # in this class we'll use datetime module to handle dates
    year: int = datetime.now().year
    month: int = datetime.now().month

    # static method to return the !year
    @staticmethod
    def get_year():
        return Settings.year

    # static method to return the !month
    @staticmethod
    def get_month():
        return Settings.month

    # static method to calculate month changes (user event)
    @staticmethod
    def get_date(delta: int):
        # the following logic handles changes in the month
        # if user triggers back, we check the limit of 1 to see ifi t's been passed and handle it accordingly. Same goes ith next trigger...
        if delta == 1:
            if Settings.month + delta > 12:
                Settings.month = 1
                Settings.year += 1
            else:
                Settings.month += 1

        if delta == -1:
            if Settings.month + delta < 1:
                Settings.month = 12
                Settings.year -= 1
            else:
                Settings.month -= 1


# Custom Container class to display days ...
date_box_style = {
    "width": 30,
    "height": 30,
    "alignment": ft.alignment.center,
    "shape": ft.BoxShape("rectangle"),
    "animate": ft.Animation(400, "ease"),
    "border_radius": 5,
}


class DateBox(ft.Container):
    def __init__(
        self,
        day: int,
        date: str = None,
        date_instnace: ft.Column = None,
        task_instance: ft.Column = None,
        opacity_: float | int = None,
    ):
        super(DateBox, self).__init__(
            **date_box_style,
            data=date,
            opacity=opacity_,
            # add a on_click trigger to select days
            on_click=self.selected,
        )

        self.day = day
        self.date_instance = date_instnace
        self.task_instance = task_instance

        self.content = ft.Text(self.day, text_align="center")

    def selected(self, e: ft.TapEvent):
        # becuase each BoxDay has the !grid instance, we can loop over the rows and check to see which day is being clicked and update the UI...
        if self.date_instance:  # to bypass any errors
            # [1:] becuase we skip over the weekday row
            for row in self.date_instance.controls[1:]:
                for date in row.controls:
                    date.bgcolor = "#76ABAE" if date == e.control else None
                    date.border = (
                        ft.border.all(0.5, "#76ABAE") if date == e.control else None
                    )
                    # we can add one more line of code to display the clicked date into the text field

                    if date == e.control:
                        # recall that we passed in a formatted date, under the method called !format_date
                        self.task_instance.date.value = e.control.data

            self.date_instance.update()
            self.task_instance.update()


# Calendar class that sets up UI for year/month/day...
class DateGrid(ft.Column):
    # data grid takes in !year and !month as well as the task manager instance
    def __init__(self, year: int, month: int):
        super(DateGrid, self).__init__()

        self.year = year
        self.month = month
        #self.task_manager = task_instance

        self.date = ft.Text(f"{month_class[self.month]} {self.year}")

        self.year_and_month = ft.Container(
            bgcolor="#76ABAE",
            border_radius=ft.border_radius.only(top_left=10, top_right=10),
            content=ft.Row(
                alignment="center",
                controls=[
                    ft.IconButton(
                        "chevron_left",
                        on_click=lambda e: self.update_date_grid(e, -1),
                    ),
                    ft.Container(
                        width=150, content=self.date, alignment=ft.alignment.center
                    ),
                    ft.IconButton(
                        "chevron_right",
                        on_click=lambda e: self.update_date_grid(e, 1),
                    ),
                ],
            ),
        )

        self.controls.insert(1, self.year_and_month)

        week_days = ft.Row(
            alignment="spaceEvenly",
            controls=[
                DateBox(day=date_class[index], opacity_=0.7) for index in range(7)
            ],
        )

        self.controls.insert(1, week_days)
        self.populate_date_grid(self.year, self.month)

    # this method adds the days of each week accordingly...
    def populate_date_grid(self, year: int, month: int):
        # delete all controls after the list of days of the week row
        del self.controls[2:]

        # Obtén el día actual y las citas
        today = datetime.now().day
        citas = control.get_citas()

        for week in cal.monthdayscalendar(year, month):
            row = ft.Row(alignment="spaceEvenly")
            for day in week:
                if day != 0:
                    date_box = DateBox(day, self.format_date(day), self)

                    # Si el día es hoy, cambia el color de fondo y el borde
                    if day == today and month == datetime.now().month and year == datetime.now().year:
                        date_box.bgcolor = "#76ABAE"
                        date_box.border = ft.border.all(0.5, "#76ABAE")

                    #Si el día tiene una cita, cambia el color de fondo y el borde
                    for cita in citas:
                        cita_date = cita['fecha']  # Asegúrate de que cita['fecha'] es un objeto datetime.date
                        if date(year, month, day) == cita_date:
                            date_box.bgcolor = "#97FEED"
                            date_box.border = ft.border.all(0.5, "#97FEED")

                    row.controls.append(date_box)
                else:
                    row.controls.append(DateBox(" "))

            self.controls.append(row)

    # We need a method to update the UI when user triggers back or next for !month
    def update_date_grid(self, e: ft.TapEvent, delta: int):
        # we need to pass delta (either 1 or -1) to settings and get current year and month changes...
        # The logic is set up, we can trigger the method first ...
        Settings.get_date(delta)  # make sure to pass in delta...

        self.update_year_and_month(
            Settings.get_year(),
            Settings.get_month(),
        )

        self.populate_date_grid(
            Settings.get_year(),
            Settings.get_month(),
        )

        self.page.update()

    # Another helper method to insert the changes post-event trigger
    def update_year_and_month(self, year: int, month: int):
        self.year = year
        self.month = month
        self.date.value = f"{month_class[self.month]} {self.year}"

    # A helper method to format and return the day...
    def format_date(self, day: int):
        return f"{month_class[self.month]} {day}, {self.year}"


# some stylign for the inputs we will use ...
def input_style(height: int):
    return {
        "height": height,
        "focused_border_color": "blue",
        "border_radius": 5,
        "cursor_height": 16,
        "cursor_color": "white",
        "content_padding": 10,
        "border_width": 1.5,
        "text_size": 12,
    }


# Task manager class to handle tasks (if app is a to-do app)
class TaskManager(ft.Column):
    def __init__(self):
        super(TaskManager, self).__init__()

        self.date = ft.TextField(
            label="Date", read_only=True, value=" ", **input_style(38)
        )

        self.controls = [self.date]
#Apartado de agenda
class Agenda(Column):
    def __init__(self):
        super().__init__()
       
        self.date_grid = DateGrid(
            year=Settings.get_year(), month=Settings.get_month()
        )
        # Crear el título
        title = ft.Text("Aqui puedes observar las citas pendientes, Haz click sobre un dia marcado para ver las citas de ese dia.", size=16, text_align="center")
        #self.controls.append(title)
        
        # Crear los rectángulos a la izquierda
        rectangles = ft.Column()
        for _ in range(5):  # Cambia esto por el número de rectángulos que quieras
            rectangles.controls.append(ft.Container(width=200, height=300, bgcolor="lightgrey"))
        
        # Crear la fila con los rectángulos y el calendario
        row = ft.Row(controls=[self.date_grid], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        content = ft.Column(controls=[title, row])
        self.controls.append(content)
    


class formularioClientes(Column):
    def __init__(self):
        super().__init__()
        # Define las pestañas
        agenda = Agenda()
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
                            ft.Row(controls=[agenda]),
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