from tornado.ioloop import IOLoop
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.models import ColumnDataSource,Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.layouts import row
from bokeh.io import show, output_notebook

from .input import Inputter
from .controller import Controller
class BokehFunk:
    def __init__(self,funk,config):
        """
        Class to call to enter function
        """
        self.funk = funk
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

        contoller = Controller()
        inputter = Inputter()
        plot = figure(width=1000, height=600,y_axis_type="log",toolbar_location="below")
        my_data = pd.DataFrame()
        my_source = ColumnDataSource(my_data)

        doc.add_root(row(plot,my_slider))
        doc.title = "Test Plot"
