"""
module takes a dictionary and converts it into a set of widgets with which to control the variables.
"""
from bokeh.layouts import column, layout
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput
from bokeh.models.widgets import Tabs, Panel

widget_list = {'slider':Slider,'textinput':TextInput}

def generate_config(variable_dict):
    """
    given a variable dictionary will generate a config dictionary which is then used to generate the widgets
    """
    config_dict={}

    for key in variable_dict:  ##generates a nested dictionary where each tab is from a dictionary
        config_dict[key] = {}
        for variable in  variable_dict[key]:
            if isinstance(variable_dict[key][variable],dict):
                for subvar in variable_dict[key][variable]:
                    config_var = variable+':'+subvar
                    config_dict[key][config_var] = {}
                    config_dict[key][config_var]['widget'] = 'textinput'   #default to textinput
                    if isinstance(variable_dict[key][variable][subvar],float) or isinstance(variable_dict[key][variable][subvar],int):
                        config_dict[key][config_var]['numeric'] = True
                    else:
                        config_dict[key][config_var]['numeric'] = False
                    config_dict[key][config_var]['args'] = {'title':config_var,'value_input':str(variable_dict[key][variable][subvar]),'value':str(variable_dict[key][variable][subvar])}
            else:
                config_dict[key][variable] = {}
                config_dict[key][variable]['widget'] = 'textinput'   #default to textinput
                if isinstance(variable_dict[key][variable],float) or isinstance(variable_dict[key][variable],int):
                    config_dict[key][variable]['numeric'] = True
                else:
                    config_dict[key][variable]['numeric'] = False
                config_dict[key][variable]['args'] = {'title':variable,'value_input':str(variable_dict[key][variable]),'value':str(variable_dict[key][variable])}
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
