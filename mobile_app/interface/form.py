from os import name
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton
from datetime import datetime, timezone
from kivy.network.urlrequest import UrlRequest
import json


class Form(MDGridLayout):
    def __init__(self, form_attrs, **kwargs):
        super(Form, self).__init__(**kwargs)
        self.cols = 1
        self.form = MDGridLayout()
        self.form.cols = 2

        self.text_inputs = {}
        for key,value in form_attrs.items():
            if key == 'form_name':
                self.form_name = form_attrs[key]
            else:
                self.form.add_widget(MDLabel(text=value+':'))
                self.text_inputs[key] = MDTextField(multiline=False, text='' if 'date' not in key else datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.form.add_widget(self.text_inputs[key])
        self.add_widget(self.form)

        self.submit =  MDRectangleFlatButton(text='Crear', font_size=40, pos_hint= {'center_x':0.5, 'center_y':0.1},size_hint_x= None)
        self.submit.bind(on_press = self.pressed)
        self.add_widget(self.submit)

    def pressed(self, instance):
        print("pressed")
        form_name = self.form_name
        text_inputs = self.text_inputs

        if form_name == 'entry_form':
            url = 'localhost:5000'+'/entry'
        elif form_name == 'out_form':
            url = 'localhost:5000'+'/out'
        texts = json.dumps({k:v.text for k,v in text_inputs.items()})
            
        headers = {'Content-type': 'application/json','Accept': '*/*'}
        req = UrlRequest(url,req_headers=headers,req_body=texts)
        #TODO: revisar error en request
        #process fields, send to mongo.
        
        for key in self.text_inputs.items(): #TODO: revisar error key "ProviderId"
            self.text_inputs[key].text = '' if 'date' not in key else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        