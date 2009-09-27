#!/usr/bin/env python

""" 
  PyPose: Bioloid pose system for arbotiX robocontroller
  Copyright (c) 2008,2009 Michael E. Ferguson.  All right reserved.

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software Foundation,
  Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import wx
import project
from ToolPane import ToolPane
from ax12 import *

###############################################################################
# Sequence editor window
class SeqEditor(ToolPane):
    """ editor for the creation of sequences. """
    BT_MOVE_UP = 101
    BT_MOVE_DN = 102
    BT_RELAX = 103
    BT_RUN = 104
    BT_HALT = 105 
    BT_SEQ_ADD = 106
    BT_SEQ_REM = 107
    BT_TRAN_ADD = 108
    BT_TRAN_REM = 109

    ID_SEQ_BOX = 110
    ID_TRAN_BOX = 111
    ID_TRAN_POSE = 112
    ID_TRAN_TIME = 113

    def __init__(self, parent, port=None):
        ToolPane.__init__(self, parent, port) 
        self.curseq = ""
        self.curtran = -1

        sizer = wx.GridBagSizer(10,10)
    
        # sequence editor, goes in a box:
        temp = wx.StaticBox(self, -1, 'edit sequence')
        temp.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        editBox = wx.StaticBoxSizer(temp,orient=wx.VERTICAL)
        seqEditSizer = wx.GridBagSizer(5,5)
        
        # transitions list
        temp = wx.StaticText(self, -1, "transitions:")
        temp.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        seqEditSizer.Add(temp, (0,0), wx.GBSpan(1,1), wx.TOP,10)
        self.tranbox = wx.ListBox(self, self.ID_TRAN_BOX)
        seqEditSizer.Add(self.tranbox, (1,0), wx.GBSpan(5,1), wx.EXPAND|wx.ALL) 
        # and add/remove
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.Button(self, self.BT_TRAN_ADD, 'new'))
        hbox.Add(wx.Button(self, self.BT_TRAN_REM, 'delete'))     
        seqEditSizer.Add(hbox,(6,0),wx.GBSpan(1,1),wx.ALIGN_CENTER)
        
        # pose name & delta-T
        seqEditSizer.Add(wx.StaticText(self, -1, "pose:"), (1,1))
        self.tranPose = wx.ComboBox(self, self.ID_TRAN_POSE, choices=self.parent.project.poses.keys())
        seqEditSizer.Add(self.tranPose, (1,2))
        seqEditSizer.Add(wx.StaticText(self, -1, "delta-T:"), (2,1))
        self.tranTime = wx.SpinCtrl(self, self.ID_TRAN_TIME, '1000', min=1, max=5000)
        seqEditSizer.Add(self.tranTime, (2,2))
        # buttons to move transition up/down
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.Button(self, self.BT_MOVE_UP, 'move up'))
        hbox.Add(wx.Button(self, self.BT_MOVE_DN, 'move down'))     
        seqEditSizer.Add(hbox,(4,1),wx.GBSpan(1,2),wx.ALIGN_CENTER|wx.BOTTOM,10)
        # grid it
        editBox.Add(seqEditSizer)
        sizer.Add(editBox, (0,0), wx.GBSpan(1,1), wx.EXPAND)

        # list of sequences
        self.seqbox = wx.ListBox(self, self.ID_SEQ_BOX, choices=self.parent.project.sequences.keys())
        sizer.Add(self.seqbox, (0,1), wx.GBSpan(1,1), wx.EXPAND) 
        # and add/remove
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.Button(self, self.BT_SEQ_ADD, 'add'))
        hbox.Add(wx.Button(self, self.BT_SEQ_REM, 'remove'))     
        sizer.Add(hbox,(1,1),wx.GBSpan(1,1),wx.ALIGN_CENTER)

        # toolbar
        toolbar = wx.Panel(self, -1)
        toolbarsizer = wx.BoxSizer(wx.HORIZONTAL)
        toolbarsizer.Add(wx.Button(toolbar, self.BT_RELAX, 'relax'),1)
        toolbarsizer.Add(wx.Button(toolbar, self.BT_RUN, 'run'),1)         
        toolbarsizer.Add(wx.Button(toolbar, self.BT_HALT, 'halt'),1)
        toolbar.SetSizer(toolbarsizer)
        sizer.Add(toolbar, (1,0), wx.GBSpan(1,1), wx.ALIGN_CENTER)

        self.SetSizerAndFit(sizer)

        wx.EVT_BUTTON(self, self.BT_RELAX, self.parent.doRelax)    
        wx.EVT_BUTTON(self, self.BT_RUN, self.runSeq)    
        wx.EVT_BUTTON(self, self.BT_HALT, self.haltSeq) 
        wx.EVT_BUTTON(self, self.BT_SEQ_ADD, self.addSeq)
        wx.EVT_BUTTON(self, self.BT_SEQ_REM, self.remSeq)   
        wx.EVT_LISTBOX(self, self.ID_SEQ_BOX, self.doSeq)
        wx.EVT_BUTTON(self, self.BT_MOVE_UP, self.moveUp)
        wx.EVT_BUTTON(self, self.BT_MOVE_DN, self.moveDn)
        wx.EVT_BUTTON(self, self.BT_TRAN_ADD, self.addTran)
        wx.EVT_BUTTON(self, self.BT_TRAN_REM, self.remTran)   
        wx.EVT_LISTBOX(self, self.ID_TRAN_BOX, self.doTran)
        
        wx.EVT_COMBOBOX(self, self.ID_TRAN_POSE, self.updateTran)
        wx.EVT_SPINCTRL(self, self.ID_TRAN_TIME, self.updateTran)
     
    def save(self):            
        if self.curseq != "":
            self.parent.project.sequences[self.curseq] = sequence()
            for i in range(self.tranbox.GetCount()):
                self.parent.project.sequences[self.curseq].append(self.tranbox.GetString(i).replace(",","|"))               
   
    ###########################################################################
    # Sequence Manipulation
    def doSeq(self, e=None):
        """ save previous sequence changes, load a sequence into the editor. """
        if e.IsSelection():
            self.save()            
            self.curseq = str(e.GetString())
            self.curtran = -1
            for i in range(self.tranbox.GetCount()):
                self.tranbox.Delete(0)      # TODO: There has got to be a better way to do this??
            for transition in self.parent.project.sequences[self.curseq]:
                self.tranbox.Append(transition.replace("|",","))
            self.tranPose.SetValue("")
            self.tranTime.SetValue(500)
            self.parent.sb.SetStatusText('now editing sequence: ' + self.curseq)

    def addSeq(self, e=None):       
        """ create a new sequence. """
        if self.parent.project.name != "":
            dlg = wx.TextEntryDialog(self,'Sequence Name:', 'New Sequence Settings')
            dlg.SetValue("")
            if dlg.ShowModal() == wx.ID_OK:
                self.seqbox.Append(dlg.GetValue())
                self.parent.project.sequences[dlg.GetValue()] = project.sequence("")
                dlg.Destroy()
        else:
            dlg = wx.MessageDialog(self, 'Please create a new robot first.', 'Error', wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
    def remSeq(self, e=None):
        """ remove a sequence. """
        if self.curseq != "":
            dlg = wx.MessageDialog(self, 'Are you sure you want to delete this sequence?', 'Confirm', wx.OK|wx.CANCEL|wx.ICON_EXCLAMATION)
            if dlg.ShowModal() == wx.ID_OK:
                # this order is VERY important!
                v = self.seqbox.FindString(self.curseq)
                del self.parent.project.sequences[self.curseq]
                self.seqbox.Delete(v)
                self.curseq = ""
                dlg.Destroy()

    ###########################################################################
    # Transition Manipulation
    def doTran(self, e=None):
        """ load a transition into the editor. """
        if e.IsSelection():
            if self.curseq != "":
                self.curtran = e.GetInt()
                v = str(e.GetString())   
                self.tranPose.SetValue(v[0:v.find(",")])
                self.tranTime.SetValue(int(v[v.find(",")+1:]))
            
    def addTran(self, e=None):       
        """ create a new transtion in this sequence. """
        if self.curseq != "":
            if self.curtran != -1:
                self.tranbox.Insert("none,500",self.curtran+1)
            else:
                self.tranbox.Append("none,500")
    def remTran(self, e=None):
        """ remove a sequence. """
        if self.curseq != "" and self.curTran != -1:
            dlg = wx.MessageDialog(self, 'Are you sure you want to delete this transition?', 'Confirm', wx.OK|wx.CANCEL|wx.ICON_EXCLAMATION)
            if dlg.ShowModal() == wx.ID_OK:
                self.tranbox.Delete(self.curtran)
                self.curtran = -1
                self.tranPose.SetValue("")
                self.tranTime.SetValue(500)
                dlg.Destroy()

    def moveUp(self, e=None):
        if self.curtran > 0:
            self.tranbox.Delete(self.curtran)
            self.curtran = self.curtran - 1
            self.tranbox.Insert(self.tranPose.GetValue() + "," + str(self.tranTime.GetValue()), self.curtran)
            self.tranbox.SetSelection(self.curtran)
    def moveDn(self, e=None):
        if self.curtran < self.tranbox.GetCount()-1:
            self.tranbox.Delete(self.curtran)
            self.curtran = self.curtran + 1
            self.tranbox.Insert(self.tranPose.GetValue() + "," + str(self.tranTime.GetValue()), self.curtran)   
            self.tranbox.SetSelection(self.curtran)
    def updateTran(self, e=None):
        if self.curtran != -1:
            self.tranbox.Delete(self.curtran)
            self.tranbox.Insert(self.tranPose.GetValue() + "," + str(self.tranTime.GetValue()), self.curtran)
            print "Updated: " + self.tranPose.GetValue() + "," + str(self.tranTime.GetValue()), self.curtran
            self.tranbox.SetSelection(self.curtran)

    def extract(self, li):
        """ extract x%256,x>>8 for every x in li """
        out = list()
        for i in li:
            out = out + [i%256,i>>8]
        return out        

    def runSeq(self, e=None):
        """ download poses, seqeunce, and send. """
        self.save() # save sequence            
        if self.port != None and self.curseq != "":
            poseDL = dict()     # key = pose name, val = index, download them after we build a transition list
            tranDL = list()     # list of bytes to download
            for t in self.parent.project.sequences[self.curseq]:  
                p = t[0:t.find("|")]                    # pose name
                dt = int(t[t.find("|")+1:])             # delta-T
                if p not in poseDL.keys():
                    poseDL[p] = len(poseDL.keys())      # get ix for pose
                # create transition values to download
                tranDL.append(poseDL[p])                # ix of pose
                tranDL.append(dt%256)                   # time is an int (16-bytes)
                tranDL.append(dt>>8)
            tranDL.append(255)      # notice to stop
            tranDL.append(0)        # time is irrelevant on stop    
            tranDL.append(0)
            # set pose size -- IMPORTANT!
            print "Setting pose size at " + str(self.parent.project.count)
            self.port.execute(253, 7, [self.parent.project.count])
            # send poses            
            for p in poseDL.keys():
                print "Sending pose " + str(p) + " to position " + str(poseDL[p])
                self.port.execute(253, 8, [poseDL[p]] + self.extract(self.parent.project.poses[p])) 
            print "Sending sequence: " + str(tranDL)
            # send sequence and play            
            self.port.execute(253, 9, tranDL) 
            self.port.execute(253, 10, list())
            self.parent.sb.SetStatusText('Playing Sequence: ')
    def haltSeq(self, e=None):
        """ send halt message ("H") """ 
        if self.port != None:
            self.port.ser.write("H")

NAME = "sequence editor"
STATUS = "please create or select a sequence to edit..."