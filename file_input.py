from bokeh.layouts import column, layout,row
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput,FileInput,Button,DataTable,TableColumn,Tabs,Panel
from bokeh.plotting import figure
import pandas as pd
from pandas.io.json._normalize import nested_to_record
import copy
import numpy as np
from plotter import get_dictionary

class FilePlotter:
    def __init__(self,function,datasource,dictionary):
        self.function = function
        self.datasource =datasource
        self.dictionary = dictionary

        self.my_data = pd.DataFrame()
        self.table_source = ColumnDataSource(self.my_data)
        self.table_columns= []

        self.my_file = TextInput(value="default", title="File path:")
        self.my_button = Button(label="Foo", button_type="success")
        self.my_table = DataTable(source = self.table_source,columns = self.table_columns)
        self.my_button.on_click(self._button_click)

    def _button_click(self):

        self.my_data = pd.read_csv(self.my_file.value_input)
        self.table_source.data = self.my_data
        self.table_columns= []

        for key in self.my_data:
            self.table_columns.append(TableColumn(field = key,title = key))
            self.my_table.columns = self.table_columns


        foo_dict = copy.deepcopy(self.dictionary)
        flattened_dict = nested_to_record(foo_dict,sep=':')

        results_overall =[]
        for index,row in self.my_data.iterrows():
            for key in self.my_data:
                if key in flattened_dict:
                    get_dictionary(foo_dict,key,row[key])   #updates the variables dictionary if match found
                    
            updated_flat_dict = nested_to_record(foo_dict,sep=':')
            result_dict = self.function(foo_dict)
            flattened_result_dict = nested_to_record(result_dict,sep=':')
            save_dict  = updated_flat_dict.copy()
            save_dict.update(flattened_result_dict)
            results_overall.append(save_dict)

        save_panda = pd.DataFrame(results_overall)
        print(save_panda.head())
    def get_widgets(self):

        widgets = column(self.my_file,self.my_button,self.my_table)
        return widgets


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
