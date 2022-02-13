# bpho-graphing

Information:

  Graphing software for the BPhO Computational Physics Challenge
  More Info at: https://www.bpho.org.uk

Installation Instructions:

   - Install Python 3.10+ - https://www.python.org/downloads/

   - Install Required Packages

      Required Packages:
       - numpy
       - scipy
       - matplotlib
       - PyQt6

      For information on how to install packages go to https://packaging.python.org/en/latest/tutorials/installing-packages/
      
Usage:
   To use the software import download the data as a csv.
   Ensure the spreadsheet you download has the headers on the top row as otherwise the software won't be able to read it.
   All spreadsheet software will this it as an option. It is likely under file-export or file-download in the menu bar.
   
   Then run graphing.py and select "Open" at the top of the window.
   
   Select the file you want to graph.
   
   Select the columns you want to plot in the dropdowns labelled "x-val" and "y-val".
   
   Click "Add Plot"
   
   To save the file click the save icon in the bottom left of the window with the graph.
  
Customising The Software:

 - To add more plot types (eg. scatter, line) edit plotting_functions.py
 - To add more modelling options edit model_functions.py
 - To add more functions to edit the data before plotting it edit transformation_functions.py
