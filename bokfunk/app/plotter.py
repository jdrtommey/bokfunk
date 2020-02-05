import copy
from bokeh.layouts import column, layout,row
from bokeh.models import ColumnDataSource
from bokeh.models import ColumnDataSource, Select,Button,DataTable,TableColumn,TextInput
import pandas as pd
class Plotter:
    def __init__(self,looper,figure,inputter):
        """
        contains widgets for generating plot data and saving the output files
        """
        self.looper = looper
        self.figure = figure
        self.inputter = inputter   #converts the data_source into a results dataframe
        self.data_source = pd.DataFrame()
        self.plot_source = ColumnDataSource({})

        res_menu = list(self.looper.get_value(flatten=True).keys())
        self.res_options = Select(title="independant variable",value=res_menu[0], options=res_menu)
        self.res_options.on_change('value',self._res_option_change)

        self.plot_button = Button(label='Plot',button_type = 'success')
        self.plot_button.on_click(self.update_plot)

        self.save_location = TextInput(value="default", title="Save path:")
        self.save_button = Button(label="Save")
        self.save_button.on_click(self._save_click)

        self.update_plot_dataframe()

    def _save_click(self):
        export_loc = self.save_location.value_input
        self.plot_data.to_csv(export_loc, index = None, header=True)

    def update_plot_dataframe(self):
        """
        goes through rows in the data table and computes results
        """
        self.data_source = self.inputter.table_data
        self.plot_data = self.looper.run(self.data_source)

    def _res_option_change(self,attr,old,new):
        self.update_plot()

    def update_plot(self):
        self.update_plot_dataframe()

        y_key = self.res_options.value
        y = self.plot_data[y_key]
        x = self.plot_data.index.tolist()

        self.plot_source.data = dict(x=x,y=y)
        self.figure.line(x='x',y='y',source=self.plot_source)

    def get_widgets(self):
        return column(column(self.plot_button,self.res_options),column(self.save_location,self.save_button))
