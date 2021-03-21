from datetime import datetime, timezone
import pytz
from dateutil.tz import tzlocal
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import MDList, TwoLineListItem
from kivy.network.urlrequest import UrlRequest
from interface.form import Form
from constants import Constants
import os

class EntryForm(Form):
    def __init__(self, **kwargs):
        super(EntryForm, self).__init__(form_attrs = {
            "form_name": "entry_form",
            "provider_id": ["ID Proveedor",'int'],
            "provider_name": ["Proveedor",'str'],
            "product_id": ["ID Producto",'int'],
            "product_name":["Producto",'str'],
            "product_description": ["Descripción producto",'str'],
            "entry_date": ["Fecha ingreso",'date'],
            "measure": ["Medida",'str'],
            "quantity": ["Cantidad",'int']
        }, **kwargs)
    pass

class OutForm(Form):
    def __init__(self, **kwargs):
        super(OutForm, self).__init__(form_attrs = {
            "form_name": "out_form",
            "provider_id": ["ID Proveedor","int"],
            "provider_name": ["Proveedor", "str"],
            "product_id": ["ID Producto","int"],
            "product_name":["Producto", "str"],
            "product_description": ["Descripción producto","str"],
            "out_date": ["Fecha salida", "date"],
            "measure": ["Medida","str"],
            "quantity": ["Cantidad", "int"],
            "value": ["Valor", "flt"]
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

class Stock(MDList):
    def __init__(self, **kwargs):
        url = Constants.HOST +'/stock_summary'
        UrlRequest(url=url,on_success=self.parse_json)
        super().__init__(**kwargs)
    def parse_json(self,req, result):
        for i in result["result"]:
            keys = ',   '.join(list(i.keys()))
            values_str = map(lambda x: str(x),list(i.values()))
            values_local = map(self.utc_to_local,values_str)
            self.add_widget(TwoLineListItem(text=keys, secondary_text= ',   '.join(list(values_local)),
            font_style='Caption', secondary_font_style ='Overline'))
    def utc_to_local(self, x):
        resp = None
        try:
            date_record= datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
            utc_datetime = pytz.timezone('UTC').localize(date_record, is_dst=None)
            local_datetime_converted = utc_datetime.astimezone(tz=tzlocal())
            resp = local_datetime_converted.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            resp = x
        return resp

class Entry(MDList):
    def __init__(self, **kwargs):
        url = Constants.HOST +'/entry'
        UrlRequest( url=url, on_success=self.parse_json)
        super().__init__(**kwargs)
    def parse_json(self,req, result):
        for i in result["result"]:
            keys = ',   '.join(list(i.keys()))
            values_str = map(lambda x: str(x),list(i.values()))
            values_local = map(self.utc_to_local,values_str)
            self.add_widget(TwoLineListItem(text=keys, secondary_text= ',   '.join(list(values_local)),
            font_style='Caption', secondary_font_style ='Overline'))
    def utc_to_local(self, x):
        resp = None
        try:
            date_record= datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
            utc_datetime = pytz.timezone('UTC').localize(date_record, is_dst=None)
            local_datetime_converted = utc_datetime.astimezone(tz=tzlocal())
            resp = local_datetime_converted.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            resp = x
        return resp

class Out(MDList):
    def __init__(self, **kwargs):
        url = Constants.HOST +'/out'
        UrlRequest(url=url, on_success=self.parse_json)
        super().__init__(**kwargs)
    def parse_json(self,req, result):
        for i in result["result"]:
            keys = ',   '.join(list(i.keys()))
            values_str = map(lambda x: str(x),list(i.values()))
            values_local = map(self.utc_to_local,values_str)
            self.add_widget(TwoLineListItem(text=keys, secondary_text= ',   '.join(list(values_local)),
            font_style='Caption', secondary_font_style ='Overline'))
    def utc_to_local(self, x):
        resp = None
        try:
            date_record= datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
            utc_datetime = pytz.timezone('UTC').localize(date_record, is_dst=None)
            local_datetime_converted = utc_datetime.astimezone(tz=tzlocal())
            resp = local_datetime_converted.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            resp = x
        return resp

class InventoryApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette="Blue"
        self.theme_cls.primary_hue="A700"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("./interface/inventory.kv")

if __name__ == '__main__':
    InventoryApp().run()