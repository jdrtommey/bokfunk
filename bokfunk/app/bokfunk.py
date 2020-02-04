from bokeh.io import curdoc
from bokeh.layouts import column, layout,row
from bokeh.models import ColumnDataSource, Select, Slider, TextInput,FileInput,Button,DataTable,TableColumn,Tabs,Panel,HoverTool
from bokeh.plotting import figure

from controller import generate_widgets,generate_config
from input import Inputter

from function import my_function,variable_dictionary
import numpy as np
import pandas as pd

funk = my_function
variables = variable_dictionary
config = generate_config(variables)
tabs = generate_widgets(config)
def dict_update(attr,old,new):
    for panel in tabs.tabs:
        for widget in panel.child.children:
            name = widget.title.split(':')
            print(name)
            if len(name) == 1:
                if config[panel.title][widget.title]['numeric'] == True:
                    print(widget.value_input)
                    variables[panel.title][widget.title] = float(eval(widget.value_input))
                else:
                    variables[panel.title][widget.title] = widget.value_input
            else:
                if config[panel.title][widget.title]['numeric'] == True:
                    variables[panel.title][name[0]][name[1]] = float(eval(widget.value_input))
                else:
                    variables[panel.title][name[0]][name[1]] = widget.value_input


for panel in tabs.tabs:
    for widget in panel.child.children:
        widget.on_change('value_input',dict_update)

p = figure(width=1000, height=600,y_axis_type="log",toolbar_location="below")
hover=HoverTool(tooltips=[
    ("index", "$index"),
    ("(x,y)", "($x, $y)")
])
p.add_tools(hover)
p.sizing_mode = 'scale_width'

my_data = pd.DataFrame()
my_source = ColumnDataSource(my_data)

my_inputer = Inputter(funk,my_source,p,variables)
display = row(tabs,p,my_inputer.get_widgets())


display.sizing_mode = 'scale_width'

curdoc().add_root(display)
curdoc().title = "BokFunk"
