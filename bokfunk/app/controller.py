"""
module takes a dictionary and converts it into a set of widgets with which to control the variables.
"""
from bokeh.layouts import column, layout
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput
from bokeh.models.widgets import Tabs, Panel

WIDGET_LIST = {'slider':Slider,'textinput':TextInput}

class Controller:
    def __init__(self,looper,config={}):
        """
        class which contains widgets for updating the dictionary
        """
        self.looper = looper
        self.given_config = config
        self.total_config = self.gen_config()
        self.gen_widgets()
    def gen_config(self):
        """
        generates a dictionary which contains information about each of the widgets.

        dictionary of the form,
        total_config:
                flattened_key:
                    name: 'textinput'
                    numeric: True
                    args:
                        title: abcs
                        value_input: 5
                        value: 5
        """
        total_config = {}
        for key in self.looper.flattened_dict:
            value = self.looper.flattened_dict[key]
            if key in self.given_config:
                total_config[key] = self.given_config[key]
            else:
                total_config[key] = {'widget':'textinput','args':{'title':key,'value_input':str(value),'value':str(value)}}

            if isinstance(value,float) or isinstance(value,int):
                total_config[key]['numeric'] = True
            else:
                total_config[key]['numeric'] = False

        return total_config

    def gen_widgets(self):
        """
        populates the controllers widgets
        """
        self.widgets_list =[]
        for key in self.total_config:
            widget_type = self.total_config[key]['widget']
            args = self.total_config[key]['args']
            widget =  WIDGET_LIST[widget_type](**args)
            if widget_type == 'textinput':
                change_var = 'value_input'
            elif widget_type == 'slider':
                change_var = 'value'
            widget.on_change(change_var,self.dict_update)

            self.widgets_list.append(widget ) # generates a widget from the allowed list of widgets

    def get_widgets(self):
        """
        takes the list of widgets and divides them into tabs. The depth says how deep inot the
        """
        panels = []

        for key in self.looper.args_dictionary:
            tab_widgets=[]
            for widget in self.widgets_list:
                if widget.title.split(':')[0] == key:
                    tab_widgets.append(widget)
            panels.append(Panel(child = column(tab_widgets),title=key))

        tabs = Tabs(tabs=panels)
        return  tabs

    def update(self):
        self.gen_widgets()
        tabs = self.populate_frames()
        return tabs


    def dict_update(self,attr,old,new):
        for widget in self.widgets_list:
            if self.total_config[widget.title]['widget'] == 'textinput':
                if self.total_config[widget.title]['numeric'] == True:
                    value = float(eval(widget.value_input))
                else:
                    value = widget.value_input
            elif self.total_config[widget.title]['widget'] == 'slider':
                value = widget.value
            self.looper.update_dictionary(widget.title,value)
