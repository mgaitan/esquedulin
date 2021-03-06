# -*- coding: utf-8 -*-


import wx
import wx.grid
import random
import inspect
import pickle

from MyWidgets import NewEnterHandlingGrid
from AboutFrame import AboutFrame       #la ventana de "Acerca de" donde estamos nosotros
import helpers

from schedulers import Clock

import os

from matplotlib.figure import Figure
import matplotlib
import numpy as np
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx

_path = os.path.abspath(os.path.dirname(__file__)) #la ruta desde donde se ejecuta el programa



class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: GuiMain.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.sizer_4_staticbox = wx.StaticBox(self, -1, "Algoritmos")
        self.sizer_3_staticbox = wx.StaticBox(self, -1, "Procesos")

        self.notebook_1 = wx.Notebook(self, -1, style=0)
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_2 = wx.Panel(self.notebook_1, -1)


        self.stats_text = wx.TextCtrl(self.notebook_1_pane_2, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)

        #self.sizer_8_staticbox = wx.StaticBox(self, -1, "Resultado")

        #self.process_list_widget = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.process_grid = NewEnterHandlingGrid(self)

        self.implemented = helpers.get_implemented()

        self.algorithm_combo = wx.ComboBox(self, -1, "", choices=sorted(self.implemented.keys()))
        self.algorithm_button = wx.Button(self, -1, "ok", style=wx.BU_EXACTFIT)
        self.algorithm_list = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.FULL_REPAINT_ON_RESIZE)
        self.algorithm_list_data = {}

        #matplotlib
        self.figure = Figure()
        self.canvas = FigureCanvas(self.notebook_1_pane_1, -1, self.figure)
        
        #matplolib for stats
        #self.stats_panel = wx.Panel(self.notebook_1_pane_2, -1)
        self.stats_figure = Figure()
        self.stats_canvas = FigureCanvas(self.notebook_1_pane_2, -1, self.stats_figure)
        
        self.clock = Clock()
        self.instances = []


        # Menu Bar
        menues_ids = [wx.NewId() for i in range(10)]
        
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
        wxglade_tmp_menu.Append(menues_ids[7], "&Agregar procesos", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(menues_ids[8], "&Ejecutar todo", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(menues_ids[8], "E&liminar algoritmos seleccionados", "", wx.ITEM_NORMAL)
        self.frame_1_menubar.Append(wxglade_tmp_menu, "&Acciones")

        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(menues_ids[5], u"Índ&ice", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(menues_ids[6], "&Acerca de..", "", wx.ITEM_NORMAL)
        self.frame_1_menubar.Append(wxglade_tmp_menu, "A&yuda")
        self.SetMenuBar(self.frame_1_menubar)
        # Menu Bar end


        # Tool Bar
        self.tools_ids = [wx.NewId() for i in range(13)]
        
        self.frame_1_toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL|wx.TB_DOCKABLE)
        self.SetToolBar(self.frame_1_toolbar)
        self.frame_1_toolbar.AddLabelTool(self.tools_ids[0], "Nuevo", wx.Bitmap("%s/icons/document-new.png" % _path, wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Nuevo archivo", "Crea una nueva secuencia de instrucciones")
        self.frame_1_toolbar.AddLabelTool(self.tools_ids[1], "Abrir", wx.Bitmap("%s/icons/document-open.png" % _path, wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Abrir archivo", "Abre una secuencia de instrucciones de un archivo")
        self.frame_1_toolbar.AddLabelTool(self.tools_ids[2], "Guardar", wx.Bitmap("%s/icons/document-save.png" % _path, wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Guardar", "Guarda la secuencia de instrucciones actual")
        self.frame_1_toolbar.AddLabelTool(self.tools_ids[3], "Guardar como...", wx.Bitmap("%s/icons/document-save-as.png" % _path, wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Guardar como...", "Guarda la secuencia en un nuevo archivo")
        self.frame_1_toolbar.AddSeparator()
        #self.frame_1_toolbar.AddLabelTool(self.tools_ids[4], "Arriba", wx.Bitmap("%s/icons/go-top.png" % _path, wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Subir al tope", "Agrupa y sube las intrucciones selecciones al principio")
        #self.frame_1_toolbar.AddLabelTool(self.tools_ids[5], "Subir", wx.Bitmap("%s/icons/go-up.png" % _path, wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Subir una intrucción", "Sube las instrucciones seleccionadas un paso")
        #self.frame_1_toolbar.AddLabelTool(self.tools_ids[6], "Bajar", wx.Bitmap("%s/icons/go-down.png" % _path, wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Bajar una instrucción", "Baja las intrucciones seleccionadas un paso")
        #self.frame_1_toolbar.AddLabelTool(self.tools_ids[7], "Abajo", wx.Bitmap("%s/icons/go-bottom.png" % _path, wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Bajar al final", "Agrupa y baja las instrucciones seleccionadas al final")
        self.frame_1_toolbar.AddLabelTool(self.tools_ids[8], "Eliminar", wx.Bitmap("%s/icons/list-remove.png" % _path, wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Borrar", "Borra algoritmos seleccionados")
        #self.frame_1_toolbar.AddSeparator()
        self.frame_1_toolbar.AddLabelTool(self.tools_ids[11], u"Añadir procesos aleatorios", wx.Bitmap("%s/icons/wand.png" % _path, wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, u"Añadir procesos aleatorios", u"Añade procesos a la tabla generador aleatoriamente")
        self.frame_1_toolbar.AddSeparator()
        self.frame_1_toolbar.AddLabelTool(self.tools_ids[9], "Ejecutar paso", wx.Bitmap("%s/icons/go-next.png" % _path, wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Ejecutar instrucción", "Ejecuta la siguiente instrucción de la secuencia")
        self.frame_1_toolbar.AddLabelTool(self.tools_ids[12], "Actualizar", wx.Bitmap("%s/icons/view-refresh.png" % _path, wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Actualizar entorno", "Actualiza los registros y el estado de la pila")
        self.frame_1_toolbar.AddLabelTool(self.tools_ids[10], "Ejecutar todo", wx.Bitmap("%s/icons/go-last.png" % _path, wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Ejecutar hasta el final", "Ejecuta los pasos necesarios para finalizar todos los procesos")
        # Tool Bar end
        




        self.Bind(wx.EVT_MENU, self.action_new, id=menues_ids[0])
        self.Bind(wx.EVT_MENU, self.action_open, id=menues_ids[1])
        self.Bind(wx.EVT_MENU, self.action_save, id=menues_ids[2])
        self.Bind(wx.EVT_MENU, self.action_save_as, id=menues_ids[3])
        self.Bind(wx.EVT_MENU, self.action_exit, id=menues_ids[4])
        self.Bind(wx.EVT_MENU, self.actionShowHelp, id=menues_ids[5])
        self.Bind(wx.EVT_MENU, self.actionShowAbout, id=menues_ids[6])
    
        self.Bind(wx.EVT_MENU, self.action_add_random_process, id=menues_ids[7])
        self.Bind(wx.EVT_MENU, self.action_run_all, id=menues_ids[8])
        self.Bind(wx.EVT_MENU, self.action_delete, id=menues_ids[9])


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
        self.titulo = 'Esquedulin'
        self.SetTitle(self.titulo)
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
                                            wx.grid.GridCellNumberEditor(1, 1000),
                                        ]):
                self.process_grid.SetCellEditor(row, col, editor)

        self.algorithm_list.InsertColumn(0,u'Algoritmo')
        self.algorithm_list.SetColumnWidth(0,250)
   
        self.Bind(wx.EVT_TOOL, self.action_new, id=self.tools_ids[0])
        self.Bind(wx.EVT_TOOL, self.action_open, id=self.tools_ids[1])
        self.Bind(wx.EVT_TOOL, self.action_save, id=self.tools_ids[2])
        self.Bind(wx.EVT_TOOL, self.action_save_as, id=self.tools_ids[3])
        #self.Bind(wx.EVT_TOOL, self.action_go_top, id=self.tools_ids[4])
        #self.Bind(wx.EVT_TOOL, self.action_go_up, id=self.tools_ids[5])
        #self.Bind(wx.EVT_TOOL, self.action_go_down, id=self.tools_ids[6])
        #self.Bind(wx.EVT_TOOL, self.action_go_bottom, id=self.tools_ids[7])
        self.Bind(wx.EVT_TOOL, self.action_delete, id=self.tools_ids[8])
        self.Bind(wx.EVT_TOOL, self.action_run_next, id=self.tools_ids[9])
        self.Bind(wx.EVT_TOOL, self.action_run_all, id=self.tools_ids[10])
        self.Bind(wx.EVT_TOOL, self.action_add_random_process, id=self.tools_ids[11])
        self.Bind(wx.EVT_TOOL, self.action_refresh_all, id=self.tools_ids[12])

        #self.stats_grid.CreateGrid(30, 30)
        self.stats_text.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, face="Courier New"))

        self.figure.subplots_adjust(left=0.06, right=0.99, top=0.99, bottom=0.03, hspace=0.06)
        
        self.stats_figure.subplots_adjust(bottom=0.4, wspace=0.3)

    def __do_layout(self):
        # begin wxGlade: GuiMain.__do_layout
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        #sizer_8 = wx.StaticBoxSizer(self.sizer_8_staticbox, wx.VERTICAL)

        sizer_8 = wx.BoxSizer(wx.VERTICAL)
        sizer_9 = wx.BoxSizer(wx.VERTICAL)

        sizer_10 = wx.BoxSizer(wx.VERTICAL)

        sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)


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
        #sizer_1.Add(self.panel_1, 2,  border=5, flag=wx.LEFT | wx.TOP | wx.GROW)
        
        
        sizer_9.Add(self.canvas, 1, border=1, flag=wx.LEFT | wx.TOP | wx.GROW)

#        sizer_10.Add(self.stats_text, 1, border=1, flag=wx.ALL | wx.TOP | wx.GROW)

        sizer_11.Add(self.stats_text, 1, border=5, flag=wx.ALL | wx.TOP | wx.GROW)
        sizer_10.Add(sizer_11, 1, wx.EXPAND, 0)

        sizer_12.Add(self.stats_canvas, 1, border=2, flag=wx.LEFT | wx.TOP | wx.GROW)
        sizer_10.Add(sizer_12, 1, wx.EXPAND, 0)


        self.notebook_1_pane_1.SetSizer(sizer_9)
        self.notebook_1_pane_2.SetSizer(sizer_10)

        self.notebook_1.AddPage(self.notebook_1_pane_1, u"Ploteo")

        self.notebook_1.AddPage(self.notebook_1_pane_2, u"Estadísticas")

        #self.notebook_1.AddPage(self, u"Estadisticas")

        sizer_8.Add(self.notebook_1, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_8, 2, wx.EXPAND, 0)
        
        self.canvas.Fit()

        #sizer_8.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)

        

        

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        self.Centre()
        # end wxGlade

        self.add_toolbar(sizer_9)


# end of class GuiMain

    def add_toolbar(self, sizer):
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        self.toolbar.Realize()
        if wx.Platform == '__WXMAC__':
            # Mac platform (OSX 10.3, MacPython) does not seem to cope with
            # having a toolbar in a sizer. This work-around gets the buttons
            # back, but at the expense of having the toolbar at the top
            self.SetToolBar(self.toolbar)
        else:
            # On Windows platform, default window size is incorrect, so set
            # toolbar width to figure width.
            tw, th = self.toolbar.GetSizeTuple()
            fw, fh = self.canvas.GetSizeTuple()
            # By adding toolbar in sizer, we are able to put it at the bottom
            # of the frame - so appearance is closer to GTK version.
            # As noted above, doesn't work for Mac.
            self.toolbar.SetSize(wx.Size(fw, th))
            sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        # update the axes menu on the toolbar
        self.toolbar.update()



    def action_go_top(self, event):
        pass

    def action_go_up(self, event):
        pass

    def action_go_down(self, event):
        pass

    def action_go_bottom(self, event):
        pass

    def action_delete(self, event):
        """delete selected algorithms"""

        def get_selected_items(list):
            selection = []
            # start at -1 to get the first selected item
            current = -1
            while True:
                next = get_next_selected(list, current)
                if next == -1:
                    return selection
                selection.append(next)
                current = next
        
        def get_next_selected(list, current):
            return list.GetNextItem(current,
                                    wx.LIST_NEXT_ALL,
                                    wx.LIST_STATE_SELECTED) 

        for key in get_selected_items(self.algorithm_list):
            self.algorithm_list_data.pop(self.algorithm_list.GetItemData(key)) #delete from data
            self.algorithm_list.DeleteItem(key) #delete from listctrl
            



    def action_refresh_all(self, event):
        """reset variables an widgets"""

        self.clock.reset()
        self.instances = []
        self.stats_figure.clf()
        self.stats_canvas.draw()
        self.stats_text.Clear()
        self.figure.clf()
        self.canvas.draw()



    def actionShowAbout(self, event): # wxGlade: MainFrame.<event_handler>
        self.about = AboutFrame(None, -1, "")
        self.about.Show(True)

    def actionShowHelp(self, event): # wxGlade: MainFrame.<event_handler>
        pass



    def action_open(self,event):
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
            with open(os.path.join(self.dirname, self.filename),'r') as filehandle:
                data = pickle.load(filehandle)
                self.set_table_process(data[0])     #TODO: need to be more robust
                self.set_algorithm_table(data[1])            

            filehandle.close()
            self.figure.clf()

            # Report on name of latest file read
            self.SetTitle("%s <%s>" % (self.titulo, self.filename))
            
            self.modificado = False

        dlg.Destroy()

    def set_algorithm_table(self, algorithm_table):
        self.algorithm_list_data = algorithm_table
        self.algorithm_list.DeleteAllItems()
        for alg_key in sorted(self.algorithm_list_data.keys()):
            alg_name, params = self.algorithm_list_data[alg_key]
            self.algorithm_list.Append([alg_name + str(params)])  
            #TODO: this is ugly, right?
            self.algorithm_list.SetItemData(self.algorithm_list.GetItemCount() - 1, alg_key)
        
    


    def action_new(self, event): # wxGlade: MainFrame.<event_handler>
        if self.modificado:
            dlg = wx.MessageDialog(None, u'Si no guarda, se perderán permanentemente los cambios realizados\n¿Desea guardar antes?', 
                u'Los cambios no ha sido guardados', 
                style=wx.YES_NO | wx.CANCEL | wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)
                
            selection = dlg.ShowModal()
            if selection == wx.ID_YES:
                self.action_save(event)
            elif selection == wx.ID_CANCEL:
                evtent.Skip()
            dlg.Destroy() 
        
        #clean interface
        self.algorithm_list_data = {}
        self.algorithm_list.DeleteAllItems()
        self.process_grid.ClearGrid()
        self.figure.clear()
        self.filename = None
        self.modified = False
        self.SetTitle(self.titulo)

        


    def action_save_as(self,event):
        """guarda la lista de intrucciones actual dando un nombre nuevo"""
        dlg = wx.FileDialog(self, "Elija un archivo", self.dirname, "", "*.esq", \
                wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            # Open the file for write, write, close
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            self.action_save(event)

        dlg.Destroy()

    def action_save(self,event):
        """guarda la lista de instrucciones en el archivo abierto. Si no existe, 
        abre el dialogo Guardar como"""

        if self.filename is None:
            self.action_save_as(event)
        else:
            data = (self.get_table_process(), self.algorithm_list_data)
            filehandle=open(os.path.join(self.dirname, self.filename),'w')
            pickle.dump(data,filehandle)
            filehandle.close()
            self.SetTitle("%s <%s>" % (self.titulo, self.filename))
            self.modificado = False



    def action_exit(self, event):
        """Salir y cerrar la puerta"""
        self.Close(True)

    def onCloseWindow(self, event):
        """al salir se ejecuta este método que verifica el estado del archivo"""
        if self.modificado:
            #self.action_save(event)
            dlg = wx.MessageDialog(self, "El archivo no se ha guardado\nDesea guardarlo?", "Salir", wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
            answer = dlg.ShowModal()
            dlg.Destroy()
            if answer == wx.ID_YES:
                self.action_save(event)
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
            
            #does this algorithm request parameters?
            for i, arg in enumerate(arg_spec.args[2:]):
                dlg = wx.TextEntryDialog(self, '%s?' % arg, u'Parámentros de %s' % alg_name, 
                                            defaultValue=str(arg_spec.defaults[i+1]))   #first-one not self parameter is None (table_process)
                if dlg.ShowModal()  == wx.ID_OK:
                    params[arg] = dlg.GetValue()        
                else:
                    #canceled
                    return None

            #not allow repeated algorithms
            if (alg_name, params) in self.algorithm_list_data.values():
                wx.Bell()
                return
        
            
            #asociating an entry in the list with a dictionary of algorithm instances 
            while True:
                id = wx.NewId()
                if id not in self.algorithm_list_data.keys():
                    break

            self.algorithm_list_data[ id ] = (alg_name, params)
            self.algorithm_list.Append([alg_name + str(params)])  
            #TODO: this is ugly, right? 
            self.algorithm_list.SetItemData(self.algorithm_list.GetItemCount() - 1, id)

            self.modified = True 
            self.SetTitle(self.GetTitle() + u' *')
            
        else:
            #not valid algorithm
            wx.Bell()
            return
    


    def action_add_random_process(self, event):
        """generate and add random process to grid"""

        dlg = wx.TextEntryDialog(self, '¿Cuántos procesos desea crear?', 'Crear procesos aleatoriamente', defaultValue=u'5')
        while True:
            if dlg.ShowModal()  == wx.ID_OK:               
                v = dlg.GetValue()
                if v.isnumeric():
                    num_of_proc = int(v)
                    break
            else: 
                return None #canceled
        dlg = wx.TextEntryDialog(self, '¿Cual es la duración máxima por proceso?', 'Crear procesos aleatoriamente', defaultValue=u'10')
        while True:
            if dlg.ShowModal()  == wx.ID_OK:               
                v = dlg.GetValue()
                if v.isnumeric():
                    max_duration = int(v)
                    break
            else: 
                return None #canceled


        init_times  = random.sample(range(1, num_of_proc * max_duration), num_of_proc)
        init_times.sort()
        init_times[0] = 0

       
        for i in range(num_of_proc):
            self.process_grid.SetCellValue(i, 0, chr(65 + i)) #name
            self.process_grid.SetCellValue(i, 1, str(init_times.pop(0))) #init
            self.process_grid.SetCellValue(i, 2, str(random.randint(1, max_duration)))
        

    def set_table_process(self, table):
        self.process_grid.ClearGrid()
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
                
    def action_run_next(self, event):
        
        if self.clock.time == 0:
            table = self.get_table_process()
            if not table:
                return
            else:
                for alg_key in sorted(self.algorithm_list_data.keys()):
                    alg_name, params = self.algorithm_list_data[alg_key]
                    
                    algorithm = self.implemented[alg_name](**params)

                    algorithm.set_process_table(table)
                    self.instances.append(algorithm)
        
        if len(self.instances)>0:
            self.clock.inc()
            self.figure.clf()
            for num, alg in enumerate(self.instances):
                alg.step()
                alg.set_ax(self.figure, '%i1%i' % (len(self.instances), num+1))

            self.set_stats(self.instances)
            self.canvas.draw()

    def action_run_all (self,  event):

        table = self.get_table_process()        

        if not table:
            return
        else:
            all = []
            

            for alg_key in sorted(self.algorithm_list_data.keys()):
                alg_name, params = self.algorithm_list_data[alg_key]
                
                algorithm = self.implemented[alg_name](**params)

                algorithm.set_process_table(table)
                all.append(algorithm)

            
            self.figure.clf()

            for num, alg in enumerate(all):
                while len(alg.factory.process_table) != len(alg.finished):  #run until all finish
                    alg.step()
                
        
                
                alg.set_ax(self.figure, '%i1%i' % (len(all), num+1))


            


            self.set_stats(all)
            self.canvas.draw()        

    def set_stats (self, all):
        text = ""
        for alg in all:
            text += "%s\n%s\n\n" % (alg.long_name, "="*len(alg.long_name))
            for p in all[0].get_all_process() :
                text += repr(p) + "\n"
            
            text += "Tr media = %.3f\n" % alg.get_media_tr()
            text += "Tr/Ts media = %.3f\n\n" % alg.get_media_rate()
            text += "%s\n\n" % ("*"*78)

        self.stats_text.Clear()
        self.stats_text.AppendText(text)
        
        ax = self.stats_figure.add_subplot(121)
        y = np.arange(len(all))+.5


        ax.barh(y, [alg.get_media_tr() for alg in reversed(all)], align="center")
        ax.set_yticks(y)
        ax.set_yticklabels([alg.short_name for alg in reversed(all)])
        ax.set_title('Tr medio')
        ax.grid(True)

        ax = self.stats_figure.add_subplot(122)
        ax.barh(y, [alg.get_media_rate() for alg in reversed(all)], align="center")
        ax.set_yticks(y)
        ax.set_yticklabels([alg.short_name for alg in reversed(all)])
        ax.set_title('Tr/Ts medio')
        ax.grid(True)

        self.stats_canvas.draw()
