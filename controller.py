"""
module takes a dictionary and converts it into a set of widgets with which to control the variables.
"""


from bokeh.layouts import column, layout
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput
from bokeh.models.widgets import Tabs, Panel

widget_list = {'slider':Slider,'textinput':TextInput}

class Controller:
    def __init__(self,variable_dict,config_dict= None):
        """
        takes a dictionary and uses it to generate a set of widgets to control the function.
        Parameters
        ----------
        variable_dict: dict
            dictionary used to generate the widgets
        config_dict: dict
            matching dictionary which contains information about the type of widget to use
        """

        self.variable_dict = variable_dict
        self.config_dict = config_dict

        self.update()

    def update(self):
        """
        updates the widgets
        """
        self.widgets = generate_widgets(self.config_dict)

def generate_config(variable_dict):
    """
    given a variable dictionary will generate a config dictionary which is used to generate the widgets
    """
    config_dict={}

    for key in variable_dict:  ##generates a nested dictionary where each tab is from a dictionary
        config_dict[key] = {}
        for variable in  variable_dict[key]:
            config_dict[key][variable] ={}
            config_dict[key][variable]['widget'] = 'textinput'
            config_dict[key][variable]['args'] = {'title':variable,'value':str(variable_dict[key][variable])}
    return config_dict

def generate_widgets(config):
    """
    Takes a config dictionary and generates the widgets.
    """
    panels=[]
    for i,key in enumerate(config):
        widgets=[]
        for variable in config[key]:
            widgets.append( widget_list[config[key][variable]['widget']](**config[key][variable]['args']) )
        panels.append(Panel(child = column(widgets),title=key))

    tabs = Tabs(tabs=panels)
    return tabs
