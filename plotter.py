"""
module which returns ColumnDataSource for plotting.
"""
from bokeh.models.widgets import Select,TextInput,Slider,Button
from bokeh.layouts import column, layout,row
import numpy as np
import copy
class Plotter:
    def __init__(self,variables,function,datasource,figure):
        """
        class contains all the widgets for plotting the function against one of the dependant variables
        """
        self.function = function
        self.variables = variables
        self.datasource = datasource
        self.figure = figure
        dependant_menu = get_options(variables) #menu with all the variables of type float or int
        self.dep_options = Select(title="Dependant variable",value=dependant_menu[0], options=dependant_menu)
        self.dep_min = TextInput(value="0", title="Minimum")
        self.dep_max = TextInput(value="1", title="Maximum")
        self.dep_iterations = Slider(start=1, end=10000, value=1, step=5, title="Iterations")

        res_dic = self.function(self.variables)  #run once to get structure of output menu
        res_menu = get_options(res_dic)
        self.res_options = Select(title="independant variable",value=res_menu[0], options=res_menu)
        self.button = Button(label="Plot", button_type="success")
        self.button.on_click(self._on_click)


    def get_widgets(self):
        dep_values = column(self.dep_min,self.dep_max,self.dep_iterations)
        dep_widgets = column(self.dep_options,dep_values)
        control_widgets = column(dep_widgets,self.res_options)
        return column(control_widgets,self.button)

    def _on_click(self):
        """
        function called when button clicked
        """
        plot_dict = copy.deepcopy(self.variables)

        dependant_variable = self.dep_options.value
        key = dependant_variable.split(':')[0]
        variable = dependant_variable.split(':')[1]
        min = eval(self.dep_min.value_input)
        max = eval(self.dep_max.value_input)
        iterations = self.dep_iterations.value

        x = np.linspace(min,max,iterations)
        res = self.res_options.value
        res_key = res.split(':')[0]
        res_variable = res.split(':')[1]
        y=[]
        for value in x:
            get_dictionary(plot_dict,dependant_variable,value)
            results = self.function(plot_dict)
            y.append(results[res_key][res_variable])
        y = np.asarray(y)

        self.datasource.data = dict(x=x,y=y)
        self.figure.line(x='x',y='y',source=self.datasource)
        print(plot_dict)

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
    split = string_to_split.split(':')
    depth = len(split)
    entry = dictionary
    for d in range(depth-1):
        entry = entry[split[d]]
    entry[split[-1]] = value
