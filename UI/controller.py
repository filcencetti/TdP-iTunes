import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        if self._view._txtInDurata.value is None or self._view._txtInDurata.value == "":
            self._view.create_alert(f"Inserire un valore nella casella di testo!!!")
            return

        try:
            max_lenght = int(self._view._txtInDurata.value)
        except:
            self._view.create_alert(f"Inserire un valore numerico nella casella di testo!!!")
            return

        self._model.buildGraph(max_lenght)
        self.fillDDAlbum()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente!!!"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model._graph.number_of_nodes()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model._graph.number_of_edges()}"))
        self._view.update_page()

    def fillDDAlbum(self):
        myValuesDD = list(map(lambda x: ft.dropdown.Option(data=x, key=x.Title, on_click=self.read_DD_value), self._model._graph.nodes()))
        self._view._ddAlbum.options = myValuesDD

    def read_DD_value(self, e):
        self.album = e.control.data

    def handleAnalisiComp(self, e):
        lengh_conn_comp, sum_min_album = self._model.getConnComp(self.album)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Componente connessa - {self.album}"))
        self._view.txt_result.controls.append(ft.Text(f"Dimensione componenete: {lengh_conn_comp}"))
        self._view.txt_result.controls.append(ft.Text(f"Durata componente: {sum_min_album}"))
        self._view.update_page()

    def handleGetSetAlbum(self, e):
        if self._view._txtInSoglia.value is None or self._view._txtInSoglia.value == "":
            self._view.create_alert(f"Inserire un valore nella casella di testo!!!")
            return

        try:
            max_min = int(self._view._txtInSoglia.value)
        except:
            self._view.create_alert(f"Inserire un valore numerico nella casella di testo!!!")
            return

        self._model.getSet(max_min)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Set di {len(self._model.best_sol)} album:"))
        for album in self._model.best_sol:
            self._view.txt_result.controls.append(ft.Text(f"{album}"))
        self._view.update_page()