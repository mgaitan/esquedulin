#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.grid as gridlib

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


class NewEnterHandlingGrid(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        
        self.data = {}


    def update_data(self):
        pass


    def OnKeyDown(self, evt):
        if evt.GetKeyCode() != wx.WXK_RETURN:
            evt.Skip()
            return
        if evt.ControlDown():   # the edit control needs this key
            evt.Skip()
            return
        self.DisableCellEditControl()
        success = self.MoveCursorRight(evt.ShiftDown())
        if not success:
            newRow = self.GetGridCursorRow() + 1
            if newRow < self.GetTable().GetNumberRows():
                self.SetGridCursor(newRow, 0)
                self.MakeCellVisible(newRow, 0)
            else:
                # this would be a good place to add a new row if your app
                # needs to do that
                pass


class MplPanel(wx.Panel): 
    def __init__(self, *arg, **kwds):
        wx.Panel.__init__(self, *arg, **kwds)
        self.figure = Figure()
        self.canvas = FigureCanvas(self, wx.ID_ANY, self.figure)
        
        
