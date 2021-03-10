from os import name
from kivy.core import text
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from datetime import datetime, timezone


class Form(GridLayout):
    def __init__(self, form_attrs, **kwargs):
        super(Form, self).__init__(**kwargs)
        self.cols = 1
        self.form = GridLayout()
        self.form.cols = 2

        self.text_inputs = {}
        for key,value in form_attrs.items():
            if key == 'form_name':
                self.form_name = form_attrs[key]
            else:
                self.form.add_widget(Label(text=value+':'))
                self.text_inputs[key] = TextInput(multiline=False, text='' if 'date' not in key else datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.form.add_widget(self.text_inputs[key])
        self.add_widget(self.form)

        self.submit =  Button(text='Crear', font_size=40)
        self.submit.bind(on_press = self.pressed)
        self.add_widget(self.submit)

    def pressed(self, instance):
        print("pressed")
        form_name = self.form_name
        text_inputs = self.text_inputs

        #process fields, send to mongo.
        
        for key in self.text_inputs.items():
            self.text_inputs[key].text = '' if 'date' not in key else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        