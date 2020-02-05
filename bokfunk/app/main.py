from tornado.ioloop import IOLoop
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.models import ColumnDataSource,Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.layouts import row,column
from bokeh.io import show, output_notebook

from .input import Inputter
from .controller import Controller
from .plotter import Plotter
from ..code import Looper

class BokehFunk:
    def __init__(self,funk,variables,config={}):
        """
        Class to call to enter function.

        Parameters
        ----------
        funk: function
            a function which accepts a dictionary as an argument function(args)
        variables: dict
            the dictionary of arguments which are accepted
        config: dict
            dictionary which contains information about how to display widgets for the arguments
        """

        self.looper = Looper(funk,variables)
        self.config = config
        output_notebook()
        self.launch()

    def launch(self):
        """
        Launch the server and connect to it.
        """
        show(self.modify_doc)

    def modify_doc(self,doc):
        """
        generate the document to serve to the app
        """
        controller = Controller(self.looper,self.config)
        inputter = Inputter(self.looper,controller.total_config)
        fig = figure(width=1000, height=600,y_axis_type="log",toolbar_location="below")
        plotter = Plotter(self.looper,fig,inputter)

        doc.add_root(row(controller.get_widgets(),fig,column(inputter.get_widgets(),plotter.get_widgets())))
        doc.title = "Test Plot"
