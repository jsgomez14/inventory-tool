from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from interface.form import Form

class EntryForm(Form):
    def __init__(self, **kwargs):
        super(EntryForm, self).__init__(form_attrs = {
            "form_name": "entry_form",
            "provider_id": "ID Proveedor",
            "product_id": "ID Producto",
            "product_description": "Descripción producto",
            "entry_date": "Fecha ingreso",
            "measure": "Unidades",
            "quantity": "Cantidad"
        }, **kwargs)
    pass

class OutForm(Form):
    def __init__(self, **kwargs):
        super(OutForm, self).__init__(form_attrs = {
            "form_name": "out_form",
            "provider_id": "ID Proveedor",
            "product_id": "ID Producto",
            "product_description": "Descripción producto",
            "out_date": "Fecha salida",
            "measure": "Unidades",
            "quantity": "Cantidad",
            "value": "Valor"
        }, **kwargs)
    pass

class MainWindow(Screen):
    pass

class OutsView(Screen):
    pass

class EntriesView(Screen):
    pass

class CreateOut(Screen):
    pass

class CreateEntry(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("./interface/inventory.kv")

class InventoryApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    InventoryApp().run()