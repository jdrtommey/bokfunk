from bokeh.io import curdoc
from bokeh.layouts import column, layout,row
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput,FileInput,Button,DataTable,TableColumn,Tabs,Panel
from bokeh.plotting import figure
from controller import generate_widgets,generate_config
from plotter import Plotter,get_dictionary
from file_input import FilePlotter
from function import my_function,variable_dictionary
import yaml
import base64
import pandas as pd
from pandas.io.json._normalize import nested_to_record
import copy
import numpy as np


from input import Inputter
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

p = figure(width=1000, height=600,y_axis_type="log")
p.sizing_mode = 'scale_width'
data = dict(x=[],y=[])
datasource = ColumnDataSource(data)

#plotter = get_plotter(variables,my_function)
plotter = Plotter(variables,funk,datasource,p)
plotter.sizing_mode = 'scale_width'


my_data = pd.DataFrame()
my_source = ColumnDataSource(my_data)
my_columns= []

my_file = TextInput(value="default", title="File path:")
my_button = Button(label="Foo", button_type="success")
my_table = DataTable(source = my_source,columns = my_columns)
tab3 =column(my_file,my_button,my_table)
def button_click():
    my_data = pd.read_csv(my_file.value_input)
    my_source.data = my_data
    my_columns =[]
    for key in my_data:
        my_columns.append(TableColumn(field = key,title = key))
        my_table.columns = my_columns

    foo_dict = copy.deepcopy(variables)
    test_dict = nested_to_record(foo_dict,sep=':')
    print(test_dict)

    y = []
    x=[]
    for index,row in my_data.iterrows():
        for key in my_data:
            if key in test_dict:
                get_dictionary(foo_dict,key,row[key])
                y.append(funk(foo_dict)['result']['key_rate'])
                x.append(index)
    y = np.asarray(y)
    x = np.asarray(x)
    datasource.data = dict(x=x,y=y)
    p.line(x='x',y='y',source=datasource)
    print(y)




my_button.on_click(button_click)

fplotter = FilePlotter(funk,my_source,variables)

my_inputer = Inputter(funk,my_source,p,variables)
panelz =[]
panelz.append(Panel(child = plotter.get_widgets(),title='single variable'))
panelz.append(Panel(child = fplotter.get_widgets(),title='File input'))
plot_tabs = Tabs(tabs=panelz)
display = row(tabs,p,my_inputer.get_widgets())


display.sizing_mode = 'scale_width'

curdoc().add_root(display)
curdoc().title = "BokFunk"
