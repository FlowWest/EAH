# EAH

## Disclaimer: 
Software and scripts developed by FlowWest, LLC are provided "AS IS" without any warranty or support. FlowWest, LLC assumes no responsibility or liability for the use of the software or scripts, and conveys no license or title under any patent or copyright right to the product. FlowWest, LLC reserves the right to make changes to the software or scripts without notification.

The EAH python scripts were developed by FlowWest, LLC with partial funding provided by American Rivers. FlowWest, LLC has not updated or maintained the EAH python scripts since August 2014. FlowWest, LLC could provide support, customization, or further development of the EAH python scripts through a contract with any entity requiring such support.

FlowWest, LLC requests that any changes to the EAH python scripts be posted to GitHub so that FlowWest, LLC can build on any improvements as future needs arise.

## SCRIPTS
For EAH, there are a total of  7 scripts/modules.  You will only need to execute eah.py and  graph_select.py.

### eah.py

##### Purpose:

*	main script that invokes efm.py, lp.py, prob.py, area.py, and graph.py
* mandatory script input parameters include:
  * hydrology file
  * geometry file
  * path of output directory
  * timing (start month, start day, end month, end day)
  * duration
* optional script input parameters include:
  * species – species name label to output in EAH graph file
  * verbose – Boolean field, if specified,  additional debug files are output in addition to regular script output files 
  * probability – Boolean field if specified, flow probability uses raw probability distribution as opposed to Log Pearson III 
* script output result files 
  * CSV file with suffix ilp contains fully interpolated area , flow, probability data used to produce ADF Curve in EAH Graph file
  * CSV file with suffix blp contains brief summary recurrence table of area, flow, probability at common recurrence intervals (1 yr, 2 yr, 5 yr, 10 yr, 50 yr, 200 yr)
  * EAH Graph file

***

### graph_select.py

##### Purpose:

* GUI tool that allows user to compare multiple EAH scenario result files located in specified target directory

###### Execution:
a.	Change directory to location of EAH scripts

b.	Enter command to start script: `python graph_select.py`. You should see a new window should appear with title “EAH Graph Selector”.  

c.	In EAH Graph Selector window, click on Select button.

d.	Browse folders and select directory location which has the EAH files to compare

e.	Click on checkboxes to select all applicable hydrology, geometry, duration, and timing parameters to be compared

f.	Click on Apply button.

* script output result is new EAH graph file containing the combined selected parameters.  Graph files will be saved in the same directory as the directory chosen when clicking Select button 

***

### efm.py

* script determines annual peak flows based on the constraints of the timing window and duration

***

### lp.py

* script calculates the log pearson distribution based on EFM script output (default method)

***

### prob.py

* script calculates the probability distribution based on EFM script output (override method)

***

### area.py

* script calculates area duration frequency (ADF),  expected annual habitat (EAH) values, and recurrence interval tables based on flow distribution and flow to area tables  

***

### graph.py

* script generates ADF curve  based on area script output

