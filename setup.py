from setuptools import setup,find_packages

setup(

   name='bokfunk',
   version='0.1',
   description='wrapper to iterate a functions input variables, with Bokeh app for visualisation',
   author='J.D.R Tommey',
   author_email='ucapdrt@ucl.ac.uk',
   url="https://github.com/jdrtommey/bokfunk",
   packages=find_packages(),  #same as name
   install_requires=['numpy','scipy','pandas'], #external packages as dependencies

)
