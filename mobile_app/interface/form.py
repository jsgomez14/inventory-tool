from os import name
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton
from datetime import datetime, timezone
import json


class Form(MDGridLayout):
    def __init__(self, form_attrs, **kwargs):
        super(Form, self).__init__(**kwargs)
        self.cols = 1
        self.form = MDGridLayout()
        self.form.cols = 2
        self.form_attrs = form_attrs
        self.text_inputs = {}
        self.search_btn = {}
        for key,value in form_attrs.items():
            if key == 'form_name':
                self.form_name = form_attrs[key]
            elif key in ['product_id','provider_id']:
                self.form.add_widget(MDLabel(text=value[0]+':'))
                self.text_inputs[key] = MDTextField(multiline=False, text='' if 'date' not in key else datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.search_btn[key] = MDRectangleFlatButton(text='Buscar '+value[0],size_hint_x= None,font_size=10)
                self.search_btn[key].bind(on_release = self.search)
                search_lo = MDGridLayout()
                search_lo.cols = 2
                search_lo.add_widget(self.text_inputs[key])
                search_lo.add_widget(self.search_btn[key])
                self.form.add_widget(search_lo)
            else:
                self.form.add_widget(MDLabel(text=value[0]+':'))
                self.text_inputs[key] = MDTextField(multiline=False, text='' if 'date' not in key else datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.form.add_widget(self.text_inputs[key])
        self.add_widget(self.form)

        self.submit =  MDRectangleFlatButton(text='Crear', font_size=40, pos_hint= {'center_x':0.5, 'center_y':0.1},size_hint_x= None)
        self.submit.bind(on_release = self.submit_form)
        self.add_widget(self.submit)

    def search(self, instance):
        key = instance.text
        
        url = None
        if key == 'Buscar ID Proveedor':
            ti_key ='provider_id'
            id = '?id='+self.text_inputs[ti_key].text
            url = 'http://localhost:5000'+'/provider'+id
        elif key == 'Buscar ID Producto':
            ti_key='product_id'
            id = '?id='+self.text_inputs['product_id'].text
            url = 'http://localhost:5000'+'/product'+id
        if self.text_inputs[ti_key].text != '': UrlRequest(url, on_success=self.parse_object)
    
    def parse_object(self,req,result):
        if 'provider' in req.url:
            self.text_inputs['provider_name'].text = result["result"][0]['name']
        elif 'product' in req.url:
            self.text_inputs['product_name'].text = result["result"][0]['name']
            self.text_inputs['product_description'].text = result["result"][0]['description']
            self.text_inputs['measure'].text = result["result"][0]['measure']

    def convert(self,k,v):
        value = None
        try:
            if self.form_attrs[k][1] == 'int':
                value = int(v)
            elif self.form_attrs[k][1] == 'flt':
                value = float(v)
            elif self.form_attrs[k][1] == 'date':
                value = v
                datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            else:
                value = v
        except:
            raise
        return [k,value]

    def submit_form(self, instance):
        print("pressed")
        form_name = self.form_name
        text_inputs = self.text_inputs
        
        for key, value in self.text_inputs.items():
            if self.text_inputs[key].text == '':
                return
        try:
            resp_dic = {}
            for k,v in text_inputs.items():
                record=self.convert(k,v.text)
                resp_dic[record[0]]=record[1]
            texts = json.dumps(resp_dic)
        except:
            return
                
        if form_name == 'entry_form':
            url = 'http://localhost:5000'+'/entry'
        elif form_name == 'out_form':
            url = 'http://localhost:5000'+'/out'
        
            
        headers = {"Content-type": "application/json","Accept": "text/plain"}
        req = UrlRequest(url,req_headers=headers,req_body=texts,on_failure= self.fail,on_success=self.success, on_error=self.error)
        for key, value in self.text_inputs.items():
            self.text_inputs[key].text = '' if 'date' not in key else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    def success(sefl,req, result):
        print('success')

    def fail(self, req,result):
        print('fail')

    def error(self, req,error):
        print("error")
        print(error)
