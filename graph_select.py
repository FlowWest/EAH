#!/usr/bin/env python
import wx
import wx.grid as gridlib
import glob
import re
import matplotlib.pyplot as plt
import pandas as pd
from time import strftime
import platform
import os
import itertools
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin


class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
        
class MainWindow(wx.Frame):
     def __init__(self, parent, title):
          wx.Frame.__init__(self, parent, title=title)
          self.Bind(wx.EVT_SIZE, self.OnSize)
          self.panel = wx.ScrolledWindow(self, wx.ID_ANY, style=wx.VSCROLL | wx.ALWAYS_SHOW_SB)
          self.panel.SetScrollRate(1,1)

          self.vSizer = wx.BoxSizer(wx.VERTICAL)
          self.CreateStatusBar()
          
          # Creating the menubar
          menuBar = wx.MenuBar()
          
          # Setting up the menu
          menu = wx.Menu()
          menuAbout = menu.Append(wx.NewId(), "&About", "Information about this program")
          menuExit = menu.Append(wx.NewId(), "E&xit", "Terminate the program")        
          menuBar.Append(menu, "&File")
          self.SetMenuBar(menuBar)
          
          self.label1 = wx.StaticText(self.panel, -1, "Target Directory:", (52,25))
          self.label2 = wx.StaticText(self.panel, -1, "HYDROLOGY SCENARIO", (20,60))
          self.label3 = wx.StaticText(self.panel, -1, "GEOMETRY SCENARIO", (400,60))
          self.label4 = wx.StaticText(self.panel, -1, "DURATION (days)", (600,60))
          self.label5 = wx.StaticText(self.panel, -1, "TIMING (month/day to month/day)", (800,60))
          
          self.browse_button = wx.Button(self.panel, -1, "Select")
          self.apply_button = wx.Button(self.panel, -1, "Apply", pos=(900,200))
          
          self.bitmap1 = None
          self.grid_list = []
          self.gridt_list = []

          # Set events
          self.Bind(wx.EVT_MENU, self.OnAbout)
          self.Bind(wx.EVT_MENU, self.OnExit)
          self.Bind(wx.EVT_BUTTON, self.OnSelect, self.browse_button)
          self.Bind(wx.EVT_BUTTON, self.OnApply, self.apply_button)

          self.label2.Hide()
          self.label3.Hide()
          self.label4.Hide()
          self.label5.Hide()
          self.apply_button.Hide()
          
         # self.Sizer.Add(gr, 1, wx.EXPAND | wx.ALL, 5)
          self.vSizer.Add(self.browse_button, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
          self.panel.SetSizerAndFit(self.vSizer)
          #self.panel.SetSizerAndFit(self.hSizer)
          
     def OnSize(self, e):
         self.panel.SetSize(self.GetClientSize())
         
     def OnAbout(self, e):
          dlg = wx.MessageDialog(self, "Graph Selector Tool", "About Graph Selector", wx.OK)
          dlg.ShowModal()
          

     def OnSelect(self, e):
          dlg = wx.DirDialog(None, "Please select your project directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_CHANGE_DIR)
     
          self.hydro_menu = []
          self.flow_menu = []
          self.duration_menu = []
          self.season_menu = []
          
          self.hydro_cb_list = []
          self.flow_cb_list = []
          self.duration_cb_list = []
          self.season_cb_list = []
          
          self.hydro_sel_list = []
          self.flow_sel_list = []
          self.duration_sel_list = []
          self.season_sel_list = []


          if self.bitmap1 is not None:
              self.bitmap1.Destroy()
              self.bitmap1 = None
              
          for g in self.grid_list:
              g.Destroy()
             
          for gt in self.gridt_list:
              gt.Destroy()
              
          self.grid_list = []
          self.gridt_list = []

          if dlg.ShowModal() == wx.ID_OK:
               self.pathname = dlg.GetPath()
               self.SetStatusText('You selected: %s\n' %self.pathname)
               ss = self.pathname.encode('ascii','ignore') + '/*.csv'
               files = glob.glob(ss)
               
               if platform.system() == 'Windows':
                    regex = re.compile(".*\\\\(.*)_(.*)_(.*)_day_(.*_.*_to_.*_.*)_ilp\.csv")
               else:
                    regex = re.compile(".*/(.*)_(.*)_(.*)_day_(.*_.*_to_.*_.*)_ilp\.csv")
               hydro = [m.group(1) for f in files for m in [regex.search(f)] if m]
               flow = [m.group(2) for f in files for m in [regex.search(f)] if m]
               duration = [m.group(3) for f in files for m in [regex.search(f)] if m]
               duration = map(int, duration)
               season = [m.group(4) for f in files for m in [regex.search(f)] if m]
               self.hydro_menu = list(set(hydro))
               self.flow_menu = list(set(flow))
               self.duration_menu = list(set(duration))
               self.season_menu = list(set(season))
               self.hydro_menu.sort()
               self.flow_menu.sort()
               self.duration_menu.sort()
               self.season_menu.sort()
                              
               #cb = CheckListCtrl(self.panel)
               #cb.InsertColumn(0, 'Hydrology', width=140)
               pos_y = 80
               for h in self.hydro_menu:
                    cb = wx.CheckBox(self.panel, label = str(h), pos=(20, pos_y))
                    #cb.InsertStringItem(sys.maxint, h)     
                    self.hydro_cb_list.append(cb)
                    pos_y += 20
               #self.hSizer.Add(cb, 0, wx.EXPAND | wx.ALL, 5)       
            
               pos_y = 80
               #cb = CheckListCtrl(self.panel)
               #cb.InsertColumn(0, 'Hydraulics', width=140)
               for f in self.flow_menu:
                    cb = wx.CheckBox(self.panel, label = str(f), pos=(400, pos_y))
                    #cb.InsertStringItem(sys.maxint, f) 
                    self.flow_cb_list.append(cb)
                    pos_y += 20
               #self.hSizer.Add(cb, 0, wx.EXPAND | wx.ALL, 5)             
               
               pos_y = 80
               #cb = CheckListCtrl(self.panel)
               #cb.InsertColumn(0, 'Duration', width=140)
               for d in self.duration_menu:
                    cb = wx.CheckBox(self.panel, label = str(d), pos=(600, pos_y))
                    #cb.InsertStringItem(sys.maxint, d)
                    self.duration_cb_list.append(cb)
                    pos_y += 20
               #self.hSizer.Add(cb, 0, wx.EXPAND | wx.ALL, 5) 
               
               pos_y = 80
               #cb = CheckListCtrl(self.panel)
               #cb.InsertColumn(0, 'Timing', width=140)
               for s in self.season_menu:
                    cb = wx.CheckBox(self.panel, label = str(s), pos=(800, pos_y))
                   #cb.InsertStringItem(sys.maxint, s)
                    self.season_cb_list.append(cb)
               #self.hSizer.Add(cb, 0, wx.EXPAND | wx.ALL, 5) 
                    pos_y += 20

          self.label2.Show()
          self.label3.Show()
          self.label4.Show()
          self.label5.Show()
          self.apply_button.Show()
          #w, h  = self.hSizer.GetMinSize()
          #self.panel.SetVirtualSize((w,h))
                  

     def OnApply (self, e):
          sep = os.path.sep
          self.label1.Hide()
          self.label2.Hide()
          self.label3.Hide()
          self.label4.Hide()
          self.label5.Hide()
          self.apply_button.Hide()
      
          # Get values of checkboxes selected
          for cb1 in self.hydro_cb_list:
              cb1.Hide()
              if cb1.GetValue():
                  h = cb1.GetLabel()
                  self.hydro_sel_list.append(h)
          for cb2 in self.flow_cb_list:
              cb2.Hide()
              if cb2.GetValue():
                  f = cb2.GetLabel()
                  self.flow_sel_list.append(f)
          for cb3 in self.duration_cb_list:
              cb3.Hide()
              if cb3.GetValue():
                  d = cb3.GetLabel()
                  self.duration_sel_list.append(d)
          for cb4 in self.season_cb_list:
              cb4.Hide()
              if cb4.GetValue():
                  s = cb4.GetLabel()
                  self.season_sel_list.append(s)

          # create graph using csv files based on checkbox selections
          combo = list(itertools.product(self.hydro_sel_list, self.flow_sel_list, self.duration_sel_list, self.season_sel_list))   
          fig = plt.figure()
          ax = fig.add_subplot(1,1,1)

          for c in combo:
              h = c[0]
              f = c[1]
              d = c[2]
              s = c[3]
              ilp_file = self.pathname + sep + h + "_" + f + "_" + d + "_day_" + s + "_ilp.csv"
              eah_file = self.pathname + sep + h + "_" + f + "_" + d + "_day_" + s + "_blp.csv"
              ilp_check = glob.glob(ilp_file)
              eah_check = glob.glob(eah_file)
              if ilp_check and eah_check:
                  data = pd.read_csv(ilp_file)
                  #print data
                  eah = pd.read_csv(eah_file)
                  #print eah
                  columns = range(7, len(data.columns)-1)
                  
                  for col in columns:
                      #eah_val = eah.iloc[:, [col-6]].values[0]
                      #eah_val = round(eah_val, 2)
                      #species = eah.iloc[:,[col-5]].values[0]
                      species = str(eah.species[0])
                      if species == 'nan':
                          lname = h + '_' + f + '_' + d + 'day_' + s 
                      else:
                          lname = species + '_' + h + '_' + f + '_' + d + 'day_' + s 
                      ax.plot(data['Probability'],data[[col]], label = lname)
         
          box = ax.get_position()
          ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])            
          ax.legend(prop={'size':6}, bbox_to_anchor =(1.4,1.05))
                                             
          title = "ADF Plot"
          fig.suptitle(title)
          plt.xlabel('Probability (1/year)')
          plt.ylabel('Inundated Area (acres)')
          datestamp = strftime("%Y-%m-%d-%H-%M")
          output_file= "EAH_graph_" + datestamp
          fig.savefig(output_file)
          self.SetStatusText('File has been saved: %s\n' %output_file)
          png_file = output_file + ".png"
          png = wx.Image(png_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
          #png.Rescale(50,50)
          self.bitmap1 = wx.StaticBitmap(self, -1, png,size=(png.GetWidth(), png.GetHeight()))
          #self.bitmap1 = wx.StaticBitmap(self, -1, png, style=wx.BITMAP_TYPE_PNG)
          self.vSizer.Add(self.bitmap1, 0, wx.EXPAND | wx.ALL, 5)       

         # create recurrence interval tables using csv files based on checkbox selections         
          colnames = ['Return Period (years)', 'Flow (cfs)', 'Area (acres)', 'Probability', 'EAH (acres)']     
          #row_ix = [1.0101, 2, 5, 10, 25, 50, 100, 200]
          combo = list(itertools.product(self.hydro_sel_list, self.flow_sel_list, self.duration_sel_list, self.season_sel_list)) 

          for c in combo:
              h = c[0]
              f = c[1]
              d = c[2]
              s = c[3]
              ilp_file = self.pathname + sep + h + "_" + f + "_" + d + "_day_" + s + "_ilp.csv"
              eah_file = self.pathname + sep + h + "_" + f + "_" + d + "_day_" + s + "_blp.csv"
              ilp_check = glob.glob(ilp_file)
              eah_check = glob.glob(eah_file)
              if ilp_check and eah_check:
              
                   data = pd.read_csv(ilp_file, index_col=0)
                   eah = pd.read_csv(eah_file, index_col=0)
                   eah = eah.astype(float)
                   row_ix = eah.index.values.tolist()
                   #print row_ix
                   gr_title = 'Recurrence Interval Table: ' + str(h) + '_' + str(f) + '_' + str(d) + '_day' + str(s)
                  
                   gr = gridlib.Grid(self.panel)
                   gr_txt = wx.TextCtrl(self.panel, -1, gr_title, size=(450,-1))
                   self.grid_list.append(gr)
                   self.gridt_list.append(gr_txt)
                   gr.CreateGrid(0, len(colnames))
                   r = 0
                   for i in range(len(colnames)):
                       gr.SetColLabelValue(i, colnames[i])
                       gr.AppendCols(1)
                   for row in row_ix:
                       #print row
                       gr.AppendRows(1)
                       gr.SetCellValue(r, 0, str(row))
                       columns = range(0, 3)
                       for col in columns:
                            #print "COL IS"
                            #print col
                            raw_value = eah.loc[row, [col]].values[0]
                            #print raw_value
                            round_value = int(raw_value)
                            round = format(round_value, ",d")
                            if col == 2:
                                 gr.SetCellValue(r, col+1, str(raw_value))
                            else:
                                 gr.SetCellValue(r, col+1, str(round))
                       r = r + 1
                   eah_val = eah['eah'][row_ix[0]]
                   eah_val = int(eah_val)
                   r_eah_val = format(eah_val, ",d")
                   gr.SetCellValue(0,4,str(r_eah_val))
                   gr.AutoSizeColumns()
                   self.vSizer.Add(gr_txt, 0)
                   self.vSizer.Add(gr, 0, wx.EXPAND | wx.ALL, 5)
                   
          w, h  = self.vSizer.GetMinSize()
          self.panel.SetVirtualSize((w,h))
          self.panel.Refresh
          self.panel.Layout
                   
                            
     def OnExit(self, e):
          self.Close(True)

app = wx.App(False)
frame = MainWindow(None, "EAH Graph Selector").Show()
app.MainLoop()
