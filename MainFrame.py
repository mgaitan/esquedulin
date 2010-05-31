# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Wed May 26 23:57:42 2010

import wx
import wx.grid
import random
import inspect
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

from MyWidgets import NewEnterHandlingGrid, MplPanel
from AboutFrame import AboutFrame       #la ventana de "Acerca de" donde estamos nosotros
import helpers

from matplotlib.figure import Figure

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: GuiMain.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.sizer_4_staticbox = wx.StaticBox(self, -1, "Algoritmos")
        self.sizer_3_staticbox = wx.StaticBox(self, -1, "Procesos")
        #self.process_list_widget = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.process_grid = NewEnterHandlingGrid(self)

        self.implemented = helpers.get_implemented()

        self.algorithm_combo = wx.ComboBox(self, -1, "", choices=sorted(self.implemented.keys()))
        self.algorithm_button = wx.Button(self, -1, "ok", style=wx.BU_EXACTFIT)
        self.algorithm_list = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.FULL_REPAINT_ON_RESIZE)
        self.algorithm_list_data = {}

        self.panel_1 = MplPanel(self, -1)

        # Menu Bar
        menues_ids = [wx.NewId() for i in range(7)]
        
        self.frame_1_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(menues_ids[0], "&Nuevo", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(menues_ids[1], "&Abrir", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(menues_ids[2], "&Guardar", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(menues_ids[3], "Guardar como...", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(menues_ids[4], "&Salir", "", wx.ITEM_NORMAL)
        self.frame_1_menubar.Append(wxglade_tmp_menu, "&Archivo")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(menues_ids[5], u"Índ&ice", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(menues_ids[6], "&Acerca de..", "", wx.ITEM_NORMAL)
        self.frame_1_menubar.Append(wxglade_tmp_menu, "A&yuda")
        self.SetMenuBar(self.frame_1_menubar)
        # Menu Bar end



        self.Bind(wx.EVT_MENU, self.actionNew, id=menues_ids[0])
        self.Bind(wx.EVT_MENU, self.actionOpen, id=menues_ids[1])
        self.Bind(wx.EVT_MENU, self.actionSave, id=menues_ids[2])
        self.Bind(wx.EVT_MENU, self.actionSaveAs, id=menues_ids[3])
        self.Bind(wx.EVT_MENU, self.actionExit, id=menues_ids[4])
        self.Bind(wx.EVT_MENU, self.actionShowHelp, id=menues_ids[5])
        self.Bind(wx.EVT_MENU, self.actionShowAbout, id=menues_ids[6])



        self.__set_properties()
        self.__do_layout()
        # end wxGlade


       
        self.Bind(wx.EVT_TEXT_ENTER, self.action_add_algorithm, self.algorithm_button)
        self.Bind(wx.EVT_BUTTON, self.action_add_algorithm, self.algorithm_button)
        # end wxGlade

        self.doiexit = wx.MessageDialog( self, u'Desea salir? \n',
                        "Saliendo...", wx.YES_NO)
       
        self.dirname = ''
        self.filename = None
        self.modificado = False

    def __set_properties(self):
        # begin wxGlade: GuiMain.__set_properties
        self.SetTitle("frame_1")
        self.SetBackgroundColour(wx.Colour(230, 221, 213))
        
        # end wxGlade
        self.process_grid.CreateGrid(15, 3)
        self.process_grid.SetRowLabelSize(0) #hide it
        col_labels = {0: 'name', 1: 'init_time', 2: 'estimated_duration'}
        for k,v in col_labels.items():
            self.process_grid.SetColLabelValue(k,v)
        
        for row in range(15):
            for col, editor in enumerate([  wx.grid.GridCellTextEditor(), 
                                            wx.grid.GridCellNumberEditor(0, 1000), 
                                            wx.grid.GridCellNumberEditor(0, 1000),
                                        ]):
                self.process_grid.SetCellEditor(row, col, editor)

        self.algorithm_list.InsertColumn(0,u'Algoritmo')
        self.algorithm_list.SetColumnWidth(0,250)
   

    def __do_layout(self):
        # begin wxGlade: GuiMain.__do_layout
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.StaticBoxSizer(self.sizer_4_staticbox, wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.StaticBoxSizer(self.sizer_3_staticbox, wx.HORIZONTAL)
        sizer_3.Add(self.process_grid, 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_6.Add(self.algorithm_combo, 3, wx.TOP, 3)
        sizer_6.Add(self.algorithm_button, 0, wx.RIGHT, 0)
        sizer_5.Add(sizer_6, 0, wx.EXPAND, 0)
        sizer_7.Add(self.algorithm_list, 1, wx.EXPAND, 0)
        sizer_5.Add(sizer_7, 1, wx.EXPAND, 0)
        sizer_4.Add(sizer_5, 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        sizer_1.Add(self.panel_1, 2, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        self.Centre()
        # end wxGlade

# end of class GuiMain




    def actionShowAbout(self, event): # wxGlade: MainFrame.<event_handler>
        self.about = AboutFrame(None, -1, "")
        self.about.Show(True)

    def actionShowHelp(self, event): # wxGlade: MainFrame.<event_handler>
        pass



    def actionOpen(self,event):
        # In this case, the dialog is created within the method because
        # the directory name, etc, may be changed during the running of the
        # application. In theory, you could create one earlier, store it in
        # your frame object and change it when it was called to reflect
        # current parameters / values
        dlg = wx.FileDialog(self, "Elija un archivo", self.dirname, "", "*.esq", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()

            # Open the file, read the contents and set them into
            # the text edit window
            filehandle=open(os.path.join(self.dirname, self.filename),'r')
            lista = pickle.load(filehandle)
            
            #update list
            self.instructionsList.updateList(lista)

            filehandle.close()

            # Report on name of latest file read
            self.SetTitle("%s <%s>" % (self.titulo, self.filename))
            
            self.modificado = False
            self.updateStatusBar(u"Archivo %s abierto correctamente" % self.filename)
        dlg.Destroy()


    def actionNew(self, event): # wxGlade: MainFrame.<event_handler>
        if self.modificado:
            dlg = wx.MessageDialog(None, u'Si no guarda, se perderán permanentemente los cambios realizados\n¿Desea guardar antes?', 
                u'Los cambios no ha sido guardados', 
                style=wx.YES_NO | wx.CANCEL | wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)
                
            selection = dlg.ShowModal()
            if selection == wx.ID_YES:
                self.actionSave(event)
            elif selection == wx.ID_CANCEL:
                evtent.Skip()
            dlg.Destroy() 
        
        self.instructionsList.DeleteAllItems()
        self.filename = None
        self.SetTitle(self.titulo)



    def actionSaveAs(self,event):
        """guarda la lista de intrucciones actual dando un nombre nuevo"""
        dlg = wx.FileDialog(self, "Elija un archivo", self.dirname, "", "*.fpu", \
                wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            # Open the file for write, write, close
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            self.actionSave(event)
            
        # Get rid of the dialog to keep things tidy
        dlg.Destroy()

    def actionSave(self,event):
        """guarda la lista de instrucciones en el archivo abierto. Si no existe, 
        abre el dialogo Guardar como"""

        if self.filename is None:
            self.actionSaveAs(event)
        else:
            list = self.instructionsList.get_list()
            filehandle=open(os.path.join(self.dirname, self.filename),'w')
            pickle.dump(list,filehandle)
            filehandle.close()
            self.SetTitle("%s <%s>" % (self.titulo, self.filename))
            self.modificado = False
            
            self.updateStatusBar(u"Archivo %s guardado" % filename)
        return



    def actionExit(self, event):
        """Salir y cerrar la puerta"""
        self.Close(True)

    def onCloseWindow(self, event):
        """al salir se ejecuta este método que verifica el estado del archivo"""
        if self.modificado:
            #self.actionSave(event)
            dlg = wx.MessageDialog(self, "El archivo no se ha guardado\nDesea guardarlo?", "Salir", wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
            answer = dlg.ShowModal()
            dlg.Destroy()
            if answer == wx.ID_YES:
                self.actionSave(event)
            elif answer == wx.ID_NO:
                self.Destroy() # frame
        else:
            dlg = wx.MessageDialog(self, "Desea salir?", "Salir", wx.YES_NO | wx.ICON_QUESTION)
            answer = dlg.ShowModal()
            dlg.Destroy()
            if answer == wx.ID_YES:
                self.Destroy()

    def action_add_algorithm(self, event):
        alg_name = self.algorithm_combo.GetValue()
        if alg_name in self.implemented.keys():
            alg = self.implemented[alg_name]
            arg_spec = inspect.getargspec(getattr(alg, '__init__'))
            params = {}
            
            #this algorithm request parameters
            for i, arg in enumerate(arg_spec.args[2:]):
                dlg = wx.TextEntryDialog(self, '%s?' % arg, u'Parámentros de %s' % alg_name, 
                                            defaultValue=str(arg_spec.defaults[i+1]))   #first-one not self parameter is None (table_process)
                if dlg.ShowModal()  == wx.ID_OK:
                    params[arg] = dlg.GetValue()        
                else:
                    #canceled
                    return None

            #asociating an entry in the list with a dictionary of algorithm instances 
            id = wx.NewId()
            self.algorithm_list_data[ id ] = (alg_name, params)
            self.algorithm_list.Append([alg_name + str(params)])  
            #TODO: this is ugly, right?
            self.algorithm_list.SetItemData(self.algorithm_list.GetItemCount() - 1, id)
            
        else:
            #not valid algorithm
            wx.Bell()
            return
    


    def action_add_random_process(self, event):
        dlg = wx.TextEntryDialog(self, '¿Cuántos procesos desea crear?', 'Crear procesos aleatoriamente', defaultValue=u'5')
        while True:
            if dlg.ShowModal()  == wx.ID_OK:               
                v = dlg.GetValue()
                if v.isnumeric():
                    num_of_proc = int(v)
                    break
            else: 
                return None #canceled
        dlg = wx.TextEntryDialog(self, '¿Que promedio de duración máxima por proceso?', 'Crear procesos aleatoriamente', defaultValue=u'2')
        while True:
            if dlg.ShowModal()  == wx.ID_OK:               
                v = dlg.GetValue()
                if v.isnumeric():
                    media_duration = int(v)
                    break
            else: 
                return None #canceled


        init_times  = random.sample(range(1, num_of_proc * media_duration), num_of_proc)
        init_times.sort()
        init_times[0] = 0

       
        for i in range(num_of_proc):
            self.process_grid.SetCellValue(i, 0, chr(65 + i)) #name
            self.process_grid.SetCellValue(i, 1, str(init_times.pop(0))) #init
            self.process_grid.SetCellValue(i, 2, str(random.randint(1, max_duration)))
        

    def set_table_process(self, table):
        table.sort(key=lambda k: k['order']) #ordering
        for row, p in enumerate(table):
            for col, col_key in enumerate(['name', 'init_time', 'estimated_duration']):
                self.process_grid.SetCellValue(row, col, str(p[col_key]))
        
    

    def get_table_process(self):
        table = []
        for row in range(self.process_grid.GetNumberRows()):
            try:
                n = self.process_grid.GetCellValue(row, 0)
                it = int(self.process_grid.GetCellValue(row, 1))
                ed = int(self.process_grid.GetCellValue(row, 2))
                p = dict(name=n, init_time=it, estimated_duration=ed, order=row)
                table.append(p)
            except:
                pass
        return table
                
            
    def run (self):
        from settings import TABLE_PROC

        all = []
        for alg_key in sorted(self.algorithm_list_data.keys()):
            alg_name, params = self.algorithm_list_data[alg_key]
            
            algorithm = self.implemented[alg_name](params)
            algorithm.set_process_table(TABLE_PROC)
            all.append(algorithm)

        
        self.panel_1.canvas.figure.clf()

        for num, alg in enumerate(all):
            time = alg.total_estimated_duration #10
            print 'time', time
            for i in range(time) :
                alg.step()
        

            alg.set_ax(self.panel_1.figure, '%i1%i' % (len(all), num+1))
    
        self.panel_1.figure.canvas.draw()



        return 
        
            
            
