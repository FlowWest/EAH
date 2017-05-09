# EAH

## Disclaimer: 
This code was developed by FlowWest, LLC with some funding provider by American Rivers. We have not updated or maintained this code since August 2014. Use of this code is “at your own risk” and FlowWest, LLC is not responsible for the results of any analyses conducted using this code or any derivatives of this code. FlowWest could support use of this code through a contract with any entity requiring implementation support or further code development. Any changes to this code must be posted to GitHub so that FlowWest, LLC can continue to refine and improve the code as future needs arise.

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

