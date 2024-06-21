import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selected_location = None

    def handle_hello(self, e):
        name = self._view.txt_name.value
        if name is None or name == "":
            self._view.create_alert("Inserire il nome")
            return
        self._view.txt_result.controls.append(ft.Text(f"Hello, {name}!"))
        self._view.update_page()

    def fillDDProvider(self):
        provider = self._model.getProvider()
        for p in provider:
            self._view._ddProvider.options.append(ft.dropdown.Option(p))
        self._view.update_page()


    def handleCreaGrafo(self, e):
        provider = self._view._ddProvider.value
        soglia = self._view._txtInDistanza.value
        try:
            soglia = float(soglia)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, soglia inserita non numerica."))
            self._view.update_page()
            return
        if provider is None:
            self._view.txt_result.controls.append(ft.Text("Inserisci un Provider!", color='red'))
            self._view.update_page()
        else:
            self._model.buildGraph(provider, soglia)
            self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente", color='green'))
            self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {len(self._model._grafo.nodes)} nodi, Numero archi: {len(self._model._grafo.edges)}", color='green'))
            self.fillDDTarget()
            self._view.update_page()

    def handleAnalisi(self, e):
        lista, max = self._model.maxVicini()
        self._view.txt_result.controls.append(ft.Text("Vertici con più vicini:"))
        for n in lista:
            self._view.txt_result.controls.append(ft.Text(
                f" {n}, Numero vicini: {max}"))
        self._view.update_page()

    def fillDDTarget(self):
        nodi = self._model._grafo.nodes
        for n in nodi:
            self._view._ddTarget.options.append(ft.dropdown.Option(text=n, data=n, on_click=self.readDDlocation))
        self._view.update_page()

    def handleGetPercorso(self, e):
        self._view.txt_result.controls.clear()
        if len(self._model._grafo.nodes) == 0:
            self._view.txt_result.controls.append(ft.Text("Creare un grafo!", color='red'))
            self._view.update_page()
            return
        if self._selected_location is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare una località!", color='red'))
            self._view.update_page()
            return
        if self._model._maxVicini is None:
            self._view.txt_result.controls.append(ft.Text("Analizzare il grafico!", color='red'))
            self._view.update_page()
            return
        if self._view._txtInStringa.value is None or self._view._txtInStringa.value == '':
            self._view.txt_result.controls.append(ft.Text("Inserire una stringa!", color='red'))
            self._view.update_page()
            return
        componenti = self._model.getPath(self._selected_location, str(self._view._txtInStringa.value))
        if componenti:
            for c in componenti:
                self._view.txt_result.controls.append(ft.Text(f"{c}"))
            self._view.update_page()
            return
        else:
            self._view.txt_result.controls.append(ft.Text("Nessun percorso trovato!", color='red'))
            self._view.update_page()
            return

    def readDDlocation(self, e):
        if e.control.data is None:
            self._selected_location = None
        else:
            self._selected_location = e.control.data