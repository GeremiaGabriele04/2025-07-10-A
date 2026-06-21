import datetime
from sqlite3.dbapi2 import Date

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceCategory = None
        self._choiceDataI = None
        self._choiceDataF = None
        self._choiceProdStart = None
        self._choiceProdEnd = None


    def handleCreaGrafo(self, e):
        if self._choiceCategory is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Scegliere una categoria", color="red"))
            self._view.update_page()
            return

        self._choiceDataI = self._view._dp1.value
        self._choiceDataF = self._view._dp2.value
        if self._choiceDataI is None or self._choiceDataF is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Scegliere una dataI e una dataF", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(self._choiceCategory, self._choiceDataI, self._choiceDataF)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Date selezionate:"))
        self._view.txt_result.controls.append(ft.Text(f"Start date: {self._choiceDataI}"))
        self._view.txt_result.controls.append(ft.Text(f"End date: {self._choiceDataF}"))
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))
        self.fillDDProducts()
        self._view.update_page()


    def handleBestProdotti(self, e):
        self._view.txt_result.controls.append(ft.Text("I cinque prodotti più venduti:"))
        for p in self._model.getTop5():
            self._view.txt_result.controls.append(ft.Text(f"{p[0].product_name} with score {p[1]}"))
        self._view.update_page()

    def handleCercaCammino(self, e):
        if self._choiceProdStart is None or self._choiceProdEnd is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Scegliere un prodotto di partenza e uno di arrivo", color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Caricando un cammino....(non è vero, ancora da fare)"))
        self._view.update_page()

    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)

    def fillDDCategory(self):
        allCategory = self._model.getAllCategory()
        for c in allCategory:
            self._view._ddcategory.options.append(ft.dropdown.Option(data=c, key=c.category_name, on_click=self._choiceDDCategory))

    def fillDDProducts(self):
        allProducts = self._model.getAllProducts()
        for p in allProducts:
            self._view._ddProdStart.options.append(ft.dropdown.Option(data=p, key=p.product_name, on_click=self._choiceDDProdStart))
            self._view._ddProdEnd.options.append(ft.dropdown.Option(data=p, key=p.product_name, on_click=self._choiceDDProdEnd))


    def _choiceDDCategory(self, e):
        self._choiceCategory = e.control.data
        print(f"hai selezionato{self._choiceCategory}")

    def _choiceDDProdStart(self, e):
        self._choiceProdStart = e.control.data
        print(f"hai selezionato{self._choiceProdStart}")

    def _choiceDDProdEnd(self, e):
        self._choiceProdEnd = e.control.data
        print(f"hai selezionato{self._choiceProdEnd}")

    def setDataI(self):
        self._choiceDataI = self._view._dp1.value

    def setDataF(self):
        self._choiceDataF = self._view._dp2.value
