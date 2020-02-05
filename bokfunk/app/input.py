"""
inputter
"""
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput,FileInput,Button,DataTable,TableColumn,Tabs,Panel
from bokeh.layouts import column, layout,row
import pandas as pd
import numpy as np
import os

class Inputter:
    def __init__(self,looper,config):
        """
        widgets to control a dataframe. Either by a single variable or a file
        """
        self.data_frame = pd.DataFrame(data={})
        self.looper = looper
        self.config = config

        self.table_data = pd.DataFrame()
        self.table_source = ColumnDataSource(self.table_data)
        self.table_columns= []
        self.my_table = DataTable(source = self.table_source,columns = self.table_columns)

        #### Options for input via a single variable
        dependant_menu = self.populate_options()
        self.dep_options = Select(title="Dependant variable",value=dependant_menu[0], options=dependant_menu)
        self.dep_options.on_change('value',self.linear_change)
        self.min_box = TextInput(title="Minimum",value= '1',value_input='1')
        self.min_box.on_change('value_input',self.linear_change)
        self.max_box = TextInput(title="Maximum",value= '10',value_input='10')
        self.max_box.on_change('value_input',self.linear_change)
        self.iter_box = TextInput(title="Iterations",value='100',value_input='100')
        self.iter_box.on_change('value_input',self.linear_change)
        self.plot_button = Button(label="Plot", button_type="success")
        #self.plot_button.on_click(self.plot_button_click)
        linear_widgets = [self.dep_options,self.min_box,self.max_box,self.iter_box]
        linear_widgets_column = column(linear_widgets)
        self.linear_table()

        #### Options for input via a csv file
        self.file_file = TextInput(value="default", title="File path:")
        self.file_button = Button(label="Foo", button_type="success")
        self.file_button.on_click(self._file_button_click)
        file_widgets = [self.file_file,self.file_button]
        file_widgets_column = column(file_widgets)

        ### put widgets into tabs
        panelz =[]
        panelz.append(Panel(child = linear_widgets_column,title='single variable'))
        panelz.append(Panel(child = file_widgets_column,title='File input'))
        self.plot_tabs = Tabs(tabs=panelz)

    def linear_change(self,attr,old,new):
        self.linear_table()

    def linear_table(self):
        try:
            min = eval(self.min_box.value_input)
            max = eval(self.max_box.value_input)
            iter = eval(self.iter_box.value_input)
        except:
            min = 0.0
            max = 1.0
            iter = 0
        data = {self.dep_options.value:np.linspace(min,max,iter) }
        self.table_data = pd.DataFrame(data)
        self._update_table()

    def _file_button_click(self):
        myDirname = os.path.normpath(self.file_file.value_input)
        self.table_data = pd.read_csv(myDirname)
        self._update_table()

    def populate_options(self):
        """
        takes the looper and generates the dependant variable
        """
        dep_var_list =[]
        for key in self.config:
            if self.config[key]['numeric'] == True:
                dep_var_list.append(key)
        return dep_var_list

    def get_widgets(self):

        return column(self.plot_tabs)

    def _update_table(self):
        self.table_columns= []
        self.table_source.data = self.table_data
        for key in self.table_data:
            self.table_columns.append(TableColumn(field = key,title = key))
            self.my_table.columns = self.table_columns
