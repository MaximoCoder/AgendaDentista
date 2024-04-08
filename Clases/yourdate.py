import flet as ft
from flet import *
from .datepicker import DatePicker
from .selection_type import SelectionType
from datetime import datetime

class Yourdate(ft.UserControl):
    def __init__(self,page):
        super().__init__()
        self.page = page
        self.datepicker = None
        self.holidays = [
            datetime(2024, 1, 1),  # Año Nuevo
            datetime(2024, 2, 5),  # Día de la Constitución
            datetime(2024, 3, 18),  # Natalicio de Benito Juárez
            datetime(2024, 5, 1),  # Día del Trabajo
            datetime(2024, 9, 16),  # Día de la Independencia
        ]

        self.locales = ["es", "en"]
        self.selected_locale = None

        #Your selected date
        #self.you_select_date = ft.Text(size=20, weight="bold")

        self.locales_opts = []
        for l in self.locales_opts:
            self.locales_opts.append(ft.dropdown.Option(l))

        #Modal por input date
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Selecciona la fecha"),
            actions = [
                ft.TextButton("Cancelar", on_click=self.cancel_dlg),
                ft.TextButton("Confirmar", on_click=self.confirm_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            actions_padding=5,
            content_padding=0
        )

        #Textfield
        self.tf = ft.TextField(
            label="Selecciona la fecha",
            dense = True,
            width=300, height=100, color="black"
        )
        #Icon inside textfield
        self.calendar_icon = ft.TextButton(
            icon=ft.icons.CALENDAR_MONTH,
            on_click=self.open_dlg_modal,
            height=50,
            width=85,
            right=0,
            style = ft.ButtonStyle(
                padding=Padding(4, 0, 0, 0),
                shape={
                    MaterialState.DEFAULT:RoundedRectangleBorder(radius=1)
                }
            )

        )
        #Stick both texfield and icon
        self.st = ft.Stack([
            self.tf,
            self.calendar_icon
        ])
        self.from_to_text = ft.Text(visible=False, size=20, weight="bold")
    def build(self):
        return Column([
            #Show input date
            self.st,
            self.from_to_text,
            #self.you_select_date
        ])
    
    #Function for open and close modal
    def confirm_dlg(self, e):
        selected_date = self.datepicker.selected_data[0] if len(self.datepicker.selected_data) > 0 else None;
        # Check if selected_date is a datetime object
        if isinstance(selected_date, datetime):
            # Convert to format DD/MM/YYYY
            selected_data_str  = selected_date.strftime("%d/%m/%Y")
        else:
            selected_data_str = None
        formated_date = self._format_date(selected_data_str)
        self.tf.value = formated_date
        # Close modal
        self.dlg_modal.open = False
        self.page.update()


    def cancel_dlg(self, e):
        self.dlg_modal.open = False
        self.page.update()

    #OPEN MODAL
    def open_dlg_modal(self, e):
        self.selected_locale = "es"  # Set the locale to Spanish
        self.datepicker = DatePicker(
            #SHOW HOUR OR MINUTE
            #hour_minute=True,
            selected_date=None,
            #This for single input
            #You can add 0. AND FOR MULTIPLE
            #you can add 1 For date range picker
            #And for Multiple input date you can add 2
            selection_type=int(0),
            #Holidays
            holidays=self.holidays,
            #SHOW 3 MONTH 
            show_three_months=False,
            locale = self.selected_locale
        )
        self.page.dialog = self.dlg_modal
        self.dlg_modal.content = self.datepicker
        self.dlg_modal.open = True
        self.page.update()

    def _format_date(self, date_str):
        if date_str:
            return date_str
        else:
            return ""
  