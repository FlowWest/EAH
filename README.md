# EAH

SCRIPTS
For EAH, there are a total of  7 scripts/modules.  You will only need to execute eah.py and  graph_select.py.  You should be able to execute all scripts on the server.

1.	eah.py 
Location on Server:
U:\Scripts\EAH\eah.py
Need to execute from Willow

Purpose:

•	main script that invokes efm.py, lp.py, prob.py, area.py, and graph.py
•	mandatory script input parameters include:
o	 hydrology file
o	 geometry file
o	 path of output directory
o	 timing (start month, start day, end month, end day)
o	 duration
•	optional script input parameters include:
o	species – species name label to output in EAH graph file
o	verbose – Boolean field, if specified,  additional debug files are output in addition to regular script output files 
o	 probability – Boolean field if specified, flow probability uses raw probability distribution as opposed to Log Pearson III 
•	script output result files 
o	CSV file with suffix ilp contains fully interpolated area , flow, probability data used to produce ADF Curve in EAH Graph file
o	CSV file with suffix blp contains brief summary recurrence table of area, flow, probability at common recurrence intervals (1 yr, 2 yr, 5 yr, 10 yr, 50 yr, 200 yr)
o	EAH Graph file

2.	graph_select.py

U:\Scripts\EAH\graph_select.py
Purpose:

•	GUI tool that allows user to compare multiple EAH scenario result files located in specified target directory
Execution:
a.	Change directory to location of EAH scripts:
cd  “C:\Users\SLALONDE\Documents\Python Scripts\EAH>”
b.	Enter command to start script:
python graph_select.py
You should see a new window should appear with title “EAH Graph Selector”.  
c.	In EAH Graph Selector window, click on Select button.
d.	Browse folders and select directory location which has the EAH files to compare
e.	Click on checkboxes to select all applicable hydrology, geometry, duration, and timing parameters to be compared
f.	Click on Apply button.
•	script output result is new EAH graph file containing the combined selected parameters.  Graph files will be saved in the same directory as the directory chosen when clicking Select button 

3.	efm.py
•	script determines annual peak flows based on the constraints of the timing window and duration
4.	lp.py
•	 script calculates the log pearson distribution based on EFM script output (default method)
5.	prob.py
•	 script calculates the probability distribution based on EFM script output (override method)
6.	area.py
•	script calculates area duration frequency (ADF),  expected annual habitat (EAH) values, and recurrence interval tables based on flow distribution and flow to area tables  
7.	graph.py
•	script generates ADF curve  based on area script output
 
YOLO BYPASS FOR AMERICAN RIVERS	
Input Files
Directory with Input Hydrology and Geometry Files
Z:\Projects\Yolo Bypass\Alternatives\EAH Inputs
Hydrology CSV Files:  YoloBypassBaseline, YoloBypassNotch, YoloBypassNotchFeb15, YoloBypassNotchMarch1, YoloBypassNotchMarch15, YoloBypassNotchMarch31, YoloBypassNotchApril15, YoloBypassNotchMay1, YoloBypassNotchMay15
Geometry/FTA CSV Files:  sac_fta, sac_fta_depth_1feet
Raw Verona Gage Data File
Z:\Projects\Yolo Bypass\Alternatives\EAH Inputs\Gage\Verona_USGS_Daily_Discharge.xlsx
Modelling Spreadsheet
Z:\Projects\Yolo Bypass\Alternatives\20140904 YoloBypassInflowCalcs.xlsx
Methodology Outline
..\Yolo Bypass\Yolo Bypass Hydrology Spreadsheet Notes.docx
Script Execution
To run all scenarios: 
a.	From Windows Start Menu on Seth’s machine, type “cmd” in textbox labeled “Search programs and files”
b.	In DOS window, type yolowrap.bat and hit Enter 
Results will be saved in the following directory ..\Yolo Bypass\Scenario Runs\20140908
Results
Summary of All Scenario Results 
Z:\Projects\Yolo Bypass\Alternatives\EAH Results\20140827 YoloBypassResultSummary.xlsx
Powerpoint Slides for 9/3/14 Meeting
Z:\Projects\Yolo Bypass\Alternatives\EAH Results\140902Yolo_MT.pptx
Directory with Individual Result Files
..\Yolo Bypass\Scenario Runs\20140826
CVFPP San Joaquin Dos Rios/Three Amigos
Input Files
Directory with Input Hydrology and Geometry Files
Z:\Projects\CVFPP Phase 2\LSJR Analysis\EAH\Dos Rios Three Amigos\Inputs
Hydrology CSV Files:  SJRhydrology1940, SJRandTLRhydrology1940, TLRhydrology1940
Geometry/FTA CSV Files:  DosRiosSJRbaseline, DosRiosSJRalternative, ThreeAmigosSJRbaseline, ThreeAmigosSJRalternative, ThreeAmigosSJRandTLRbaseline, ThreeAmigosSJRandTLRalternative
Raw Gage Data Files
Z:\Projects\CVFPP Phase 2\LSJR Analysis\EAH\Dos Rios Three Amigos\Inputs\Gage\sanjoaquin_newman_raw_usgs.txt
Z:\Projects\CVFPP Phase 2\LSJR Analysis\EAH\Dos Rios Three Amigos\Inputs\Gage\tulomne_merced_raw_usgs.txt
Script Execution
1)	Create new FTA csv files based on hydraulic model FTA tables provided by Devinder at DWR.  Confirm with Mark whether any scenario requires only using Tulomne River hydrology.
2)	Create output directory for the model run 
a.	mkdir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908"
3)	Change directory to location of EAH script
a.	cd  “C:\Users\SLALONDE\Documents\Python Scripts\EAH>”
4)	Execute EAH scripts for Dos Rios breach sites using SJR hydrology
C:\Users\SLALONDE\Documents\Python Scripts\EAH>python eah.py -hfile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\SJRhydrology1940.csv" -afile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\DosRiosSJRbaseline.csv" -odir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908" -smo 1 -sda 1 -emo 6 -eda 15 -durations 7 10
C:\Users\SLALONDE\Documents\Python Scripts\EAH>python eah.py -hfile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\SJRhydrology1940.csv" -afile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\DosRiosSJRalternative.csv" -odir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908" -smo 1 -sda 1 -emo 6 -eda 15 -durations 7 10
C:\Users\SLALONDE\Documents\Python Scripts\EAH>python eah.py -hfile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\SJRhydrology1940.csv" -afile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\DosRiosSJRbaseline.csv" -odir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908" -smo 11 -sda 1 -emo 6 -eda 15 -durations 7 10
C:\Users\SLALONDE\Documents\Python Scripts\EAH>python eah.py -hfile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\SJRhydrology1940.csv" -afile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\DosRiosSJRalternative.csv" -odir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908" -smo 11 -sda 1 -emo 6 -eda 15 -durations 7 10
C:\Users\SLALONDE\Documents\Python Scripts\EAH>python eah.py -hfile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\SJRhydrology1940.csv" -afile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\DosRiosSJRbaseline.csv" -odir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908" -smo 1 -sda 21 -emo 7 -eda 7 -durations 7 10
C:\Users\SLALONDE\Documents\Python Scripts\EAH>python eah.py -hfile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\SJRhydrology1940.csv" -afile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\DosRiosSJRalternative.csv" -odir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908" -smo 1 -sda 21 -emo 7 -eda 7 -durations 7 10
5)	Execute EAH scripts for Three Amigos breach sites using SJR hydrology
C:\Users\SLALONDE\Documents\Python Scripts\EAH>python eah.py -hfile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\SJRhydrology1940.csv" -afile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\ThreeAmigosSJRbaseline.csv" -odir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908" -smo 1 -sda 1 -emo 6 -eda 15 -durations 7 10
C:\Users\SLALONDE\Documents\Python Scripts\EAH>python eah.py -hfile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\SJRhydrology1940.csv" -afile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\ThreeAmigosSJRalternative.csv" -odir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908" -smo 1 -sda 1 -emo 6 -eda 15 -durations 7 10
C:\Users\SLALONDE\Documents\Python Scripts\EAH>python eah.py -hfile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\SJRhydrology1940.csv" -afile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\ThreeAmigosSJRbaseline.csv" -odir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908" -smo 11 -sda 1 -emo 6 -eda 15 -durations 7 10
C:\Users\SLALONDE\Documents\Python Scripts\EAH>python eah.py -hfile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\SJRhydrology1940.csv" -afile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\ThreeAmigosSJRalternative.csv" -odir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908" -smo 11 -sda 1 -emo 6 -eda 15 -durations 7 10
C:\Users\SLALONDE\Documents\Python Scripts\EAH>python eah.py -hfile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\SJRhydrology1940.csv" -afile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\ThreeAmigosSJRbaseline.csv" -odir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908" -smo 1 -sda 21 -emo 7 -eda 7 -durations 7 10
C:\Users\SLALONDE\Documents\Python Scripts\EAH>python eah.py -hfile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\SJRhydrology1940.csv" -afile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\ThreeAmigosSJRalternative.csv" -odir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908" -smo 1 -sda 21 -emo 7 -eda 7 -durations 7 10

6)	Execute EAH scripts for Three Amigos breach sites using combined SJR and TLR hydrology
C:\Users\SLALONDE\Documents\Python Scripts\EAH>python eah.py -hfile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\SJRandTLRhydrology1940.csv" -afile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\ThreeAmigosSJRandTLRbaseline.csv" -odir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908" -smo 1 -sda 1 -emo 6 -eda 15 -durations 7 10
C:\Users\SLALONDE\Documents\Python Scripts\EAH>python eah.py -hfile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\SJRandTLRhydrology1940.csv" -afile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\ThreeAmigosSJRandTLRalternative.csv" -odir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908" -smo 1 -sda 1 -emo 6 -eda 15 -durations 7 10
C:\Users\SLALONDE\Documents\Python Scripts\EAH>python eah.py -hfile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\SJRandTLRhydrology1940.csv" -afile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\ThreeAmigosSJRandTLRbaseline.csv" -odir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908" -smo 11 -sda 1 -emo 6 -eda 15 -durations 7 10
C:\Users\SLALONDE\Documents\Python Scripts\EAH>python eah.py -hfile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\SJRandTLRhydrology1940.csv" -afile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\ThreeAmigosSJRandTLRalternative.csv" -odir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908" -smo 11 -sda 1 -emo 6 -eda 15 -durations 7 10
C:\Users\SLALONDE\Documents\Python Scripts\EAH>python eah.py -hfile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\SJRandTLRhydrology1940.csv" -afile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\ThreeAmigosSJRbaseline.csv" -odir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908" -smo 1 -sda 21 -emo 7 -eda 7 -durations 7 10
C:\Users\SLALONDE\Documents\Python Scripts\EAH>python eah.py -hfile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\SJRandTLRhydrology1940.csv" -afile "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\ThreeAmigosSJRandTLRalternative.csv" -odir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908" -smo 1 -sda 21 -emo 7 -eda 7 -durations 7 10

Result Files
Summary of All Scenario Results 
Z:\Projects\CVFPP Phase 2\LSJR Analysis\EAH\Dos Rios Three Amigos\Results\20140825_DosRios_ThreeAmigos_EAH_Summary.xlsx
Directory with Individual Result Files
..\CVFPP\SJR\Dos Rios_3 Amigos\20140825
 

CVFPP San Joaquin Firebaugh
Input Files
Directory with Input Hydrology and Geometry Files
Z:\Projects\CVFPP Phase 2\LSJR Analysis\EAH\Firebaugh\Inputs
Hydrology CSV Files:  MendotaModel, MendotaHistorical
Geometry/FTA CSV Files:  Eco1Baseline, Eco1Alternative, Eco2Baseline, Eco2Alternative, Eco3Baseline, Eco3Alternative, Eco4Baseline, Eco4Alternative, Eco5Baseline, Eco5Alternative, Eco6Baseline, Eco6Alternative
Script Execution
1)	Confirm with Mark what scenarios require rerunning.
2)	Create output directory for the model run 
a.	mkdir "C:\Users\SLALONDE\Documents\CVFPP\SJR\Dos Rios_3 Amigos\20140908"
3)	Change directory to location of EAH script
a.	cd  “C:\Users\SLALONDE\Documents\Python Scripts\EAH>”
4)	Execute EAH scripts for Dos Rios breach sites using SJR hydrology

