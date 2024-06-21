import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP - Esame del 14/09/2022"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # title
        self._title = ft.Text("TdP - Esame del 14/09/2022", color="red", size=24)
        self._page.controls.append(self._title)

        #ROW1
        self._txtInDistanza = ft.TextField(label="Distanza")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo",
                                               on_click=self._controller.handleCreaGrafo)
        row1 = ft.Row([
            ft.Container(self._txtInDistanza, width=300),
            ft.Container(self._btnCreaGrafo, width=300)
        ], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        #ROW2
        self._ddProvider = ft.Dropdown(label="Provider")
        self._controller.fillDDProvider()
        self._btnAnalisi = ft.ElevatedButton(text = "Analisi Grafo",
                                                 on_click=self._controller.handleAnalisi)

        row2 = ft.Row([
            ft.Container(self._ddProvider, width=300),
            ft.Container(self._btnAnalisi, width=300)
        ], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        #ROW3
        self._txtInStringa = ft.TextField(label="Stringa")
        self._btnSetPercorso = ft.ElevatedButton(text="Calcola Percorso",
                                               on_click=self._controller.handleGetPercorso)
        row3 = ft.Row([
            ft.Container(self._txtInStringa, width=300),
            ft.Container(self._btnSetPercorso, width=300)
        ], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)
        self._ddTarget = ft.Dropdown(label="Target")
        row4 = ft.Row([
            ft.Container(self._ddTarget, width=300)],  alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row4)
        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()