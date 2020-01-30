"""
inputter
"""
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput,FileInput,Button,DataTable,TableColumn,Tabs,Panel
from bokeh.layouts import column, layout,row
from pandas.io.json._normalize import nested_to_record
import copy
import pandas as pd
import numpy as np
import os
class Inputter:
    def __init__(self,function,datasource,figure,dictionary):
        """
        class which contains widgets for generating a dataframe
        """

        self.function = function
        self.datasource = datasource
        self.dictionary = dictionary
        self.figure = figure
        self.table_data = pd.DataFrame()
        self.plot_data = pd.DataFrame()

        self.table_source = ColumnDataSource(self.table_data)
        self.table_columns= []

        self.my_table = DataTable(source = self.table_source,columns = self.table_columns)

        dependant_menu = get_options(self.dictionary) #menu with all the variables of type float or int
        self.dep_options = Select(title="Dependant variable",value=dependant_menu[0], options=dependant_menu)
        res_dic = self.function(self.dictionary)  #run once to get structure of output menu
        res_menu = get_options(res_dic)
        self.res_options = Select(title="independant variable",value=res_menu[0], options=res_menu)

        ##### Widgets for a linear variable
        #self.linear_button = Button(label="Plot", button_type="success")
        #self.linear_button.on_click(self._linear_button_click)
        self.linear_dep_min = TextInput(value="0",value_input="0", title="Minimum")
        self.linear_dep_min.on_change('value_input',self._linear_button_click)
        self.linear_dep_max = TextInput(value="1",value_input="1", title="Maximum")
        self.linear_dep_max.on_change('value_input',self._linear_button_click)
        self.linear_dep_iterations = Slider(start=1, end=10000, value=500, step=5, title="Iterations")
        self.linear_dep_iterations.on_change('value',self._linear_button_click)

        ##### Widgets for file input
        self.file_file = TextInput(value="default", title="File path:")
        self.file_file.on_change('value_input',self._file_button_click)
        #self.file_button = Button(label="Foo", button_type="success")
        #self.file_button.on_click(self._file_button_click)

        ##### tabs widgets
        linear_widgets = [self.dep_options,self.linear_dep_min,self.linear_dep_max,self.linear_dep_iterations]
        linear_widgets_column = column(linear_widgets)

        file_widgets = [self.file_file]
        file_widgets_column = column(file_widgets)
        panelz =[]
        panelz.append(Panel(child = linear_widgets_column,title='single variable'))
        panelz.append(Panel(child = file_widgets_column,title='File input'))
        self.plot_tabs = Tabs(tabs=panelz)

        #####  widgets for plotting
        self.plot_dep_select = Select(title="Dependant variable",value=dependant_menu[0], options=dependant_menu)
        self.plot_button = Button(label = "Plot")
        self.plot_button.on_click(self._plot_button_click)


        #### widgets for saving the output dataframe
        self.save_location = TextInput(value="default", title="Save path:")
        self.save_button = Button(label="Save")
        self.save_button.on_click(self._save_click)


    def _update_table(self):
        self.table_columns= []
        self.table_source.data = self.table_data
        for key in self.table_data:
            self.table_columns.append(TableColumn(field = key,title = key))
            self.my_table.columns = self.table_columns

    def _generate_plot_data(self):
        """
        fills a datatable for a given variable source
        """
        results_overall=[]
        start_dict = copy.deepcopy(self.dictionary)
        flattened_dict = nested_to_record(start_dict,sep=':')
        for index,row in self.table_data.iterrows():
            for key in self.table_data:
                if key in flattened_dict:
                    get_dictionary(start_dict,key,row[key])   #updates the variables dictionary if match found
            updated_flat_dict = nested_to_record(start_dict,sep=':')
            result_dict = self.function(start_dict)
            flattened_result_dict = nested_to_record(result_dict,sep=':')
            save_dict  = updated_flat_dict.copy()
            save_dict.update(flattened_result_dict)
            results_overall.append(save_dict)

        self.plot_data = pd.DataFrame(results_overall)

    def _update_dep_choice(self):
        """
        updates the choices of dependant variable
        """
        dep_mens=[]
        for key in self.table_data:
            if key in get_options(self.dictionary):
                dep_mens.append(key)
        self.plot_dep_select.options=dep_mens

    def _plot_button_click(self):
        self._generate_plot_data()
        plot_y = self.res_options.value
        y = self.plot_data[plot_y]

        if self.plot_tabs.active == 1:
        #    self._file_button_click()
            x = self.plot_data.index.tolist()
        elif self.plot_tabs.active == 0:
        #    self._linear_button_click()
            x = self.table_data[self.table_data.columns[0]]

        print(self.plot_data)
        self.datasource.data = dict(x=x,y=y)
        self.figure.line(x='x',y='y',source=self.datasource)

    def _file_button_click(self,attr,old,new):
        myDirname = os.path.normpath(self.file_file.value_input)

        self.table_data = pd.read_csv(myDirname)
        self._update_dep_choice()
        self._update_table()
        self._generate_plot_data()

    def _linear_button_click(self,attr,old,new):
        dependant_variable = self.dep_options.value
        min = eval(self.linear_dep_min.value_input)
        max = eval(self.linear_dep_max.value_input)
        iterations = self.linear_dep_iterations.value
        x = np.linspace(min,max,iterations)
        self.table_data = pd.DataFrame({dependant_variable:x})
        self._update_dep_choice()
        self._update_table()
        self._generate_plot_data()


    def _save_click(self):
        export_loc = self.save_location.value_input
        self.plot_data.to_csv(export_loc, index = None, header=True)


    def get_widgets(self):
        """
        returns the layout of the classes widgets.
        """

        view = column(self.plot_tabs,self.res_options,self.plot_button,self.my_table,self.save_location,self.save_button)

        return view

def get_options(dictionary):
    """
    goes through input dictionary and returns all the keys which have a float variable type
    """
    menus =[]
    for key in dictionary:
        for variable in dictionary[key]:
            if isinstance(dictionary[key][variable], float) == True or isinstance(dictionary[key][variable], int):
                menus.append(key+":"+variable)
            elif isinstance(dictionary[key][variable], dict):
                for subkey in dictionary[key][variable]:
                    if isinstance(dictionary[key][variable][subkey], float) == True or isinstance(dictionary[key][variable][subkey], int):
                        menus.append(key+":"+variable+':'+subkey)
    return menus

def get_dictionary(dictionary,string_to_split,value):
    """
    given a dicrionaty and a flattened key will change the value in the dictionary
    """
    split = string_to_split.split(':')
    depth = len(split)
    entry = dictionary
    for d in range(depth-1):
        entry = entry[split[d]]
    entry[split[-1]] = value
