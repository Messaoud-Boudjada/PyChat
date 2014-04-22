#The MIT License (MIT)

#Copyright (c) 2014 Boudjada Messaoud

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import wx,thread,socket
import os,sys
import struct
frame=wx.Frame

class PyChat(frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,title="PyChat",size=(550,430),pos=(500,100),style=wx.SYSTEM_MENU | wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX  ,name=wx.FrameNameStr)
        self.panel=wx.Panel(self)
        self.style=wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
        
        self.font=wx.Font(15, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, underline=False, face="", encoding=wx.FONTENCODING_DEFAULT)
        self.font2=wx.Font(30, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, underline=False, face="", encoding=wx.FONTENCODING_DEFAULT)

        self.text1=wx.TextCtrl(self.panel,pos=(190,90),size=(300,30))
        self.text2=wx.TextCtrl(self.panel,pos=(20,300),size=(350,90),style=wx.TE_MULTILINE | wx.HSCROLL)
        self.text3=wx.TextCtrl(self.panel,pos=(20,125),size=(500,170),style=wx.TE_MULTILINE | wx.HSCROLL|wx.TE_READONLY)
        self.text4=wx.TextCtrl(self.panel,pos=(190,55),size=(300,30))
        
        self.button = wx.Button(self.panel,label="Send",pos=(400,300),size=(100,30))
        self.button1 = wx.Button(self.panel,label="Connect",pos=(400,330),size=(100,30))
        self.button2 = wx.Button(self.panel,label="Help???",pos=(400,360),size=(100,30))
        
        self.SetBackgroundColour((0,200,255))
        
        self.statictext=wx.StaticText(self.panel,-1,"Client IP: ",(20,90))
        self.statictext1=wx.StaticText(self.panel,-1,"Server IP: ",(20,55))
        self.statictext2=wx.StaticText(self.panel,-1,"PyChat",(150,0))

        self.statictext.SetFont(self.font)
        self.statictext1.SetFont(self.font)
        self.statictext2.SetFont(self.font2)
        
        self.statictext.SetBackgroundColour((100,100,255))
        self.statictext1.SetBackgroundColour((100,100,255))
        
        self.statictext.SetForegroundColour((255,255,255))
        self.statictext1.SetForegroundColour((255,255,255))
        
        self.text1.SetBackgroundColour((100,100,100))
        self.text2.SetBackgroundColour((255,255,255))
        self.text3.SetBackgroundColour((100,100,100))
        self.text4.SetBackgroundColour((100,100,100))
        
        self.text1.SetForegroundColour((255,255,255))
        self.text2.SetForegroundColour((0,0,0))
        self.text3.SetForegroundColour((255,255,255))
        self.text4.SetForegroundColour((255,255,255))
        
        self.text1.SetFont(self.font)
        self.text2.SetFont(self.font)
        self.text3.SetFont(self.font)
        self.text4.SetFont(self.font)
        
        self.text2.Bind(wx.EVT_TEXT_ENTER,self.caseb)
        self.button.Bind(wx.EVT_BUTTON,self.caseb)
        self.button1.Bind(wx.EVT_BUTTON,self.connect)
        self.button2.Bind(wx.EVT_BUTTON,self.onhelp)
        self.Bind(wx.EVT_CLOSE,self.onclose)
        
        
    def connect(self,event):
        self.clisock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        host=self.text4.GetValue()
        self.clisock.connect( (host, 2626))
        host,port = self.clisock.getpeername()
        thread.start_new_thread( self.recv,(self,))
        if self.text1.GetValue()== "":
            self.text1.SetValue(host)
        
    def onclose(self,event):
        try :
            self.ip=self.text1.GetValue()
            self.clisock.send(self.ip+" Client lenft")
        except:
            pass
        sys.exit()
        
    def recv(self,event):
        while True:
            data=self.clisock.recv(1050)
            if ":" in data:
                index=data.index(":")
                data=self.text3.GetValue()+"\n"+data
                self.text3.SetValue(data)
                 
    def caseb(self,event):
        self.ip=self.text1.GetValue()
        self.message=self.text2.GetValue()
        self.text2.SetValue("")
        self.text3.SetValue(self.text3.GetValue()+"\n"+self.ip+": "+self.message)
        self.clisock.send(self.ip+self.message)
    def onhelp(self,event):
        content="Hello this software is created by Messaoud BOUDJADA a student \n\
        at University of M'hamed bougerra Institut of electrical and electronic IGEE  Boumerdes Algeria\
        \nThis softwre is a chat app if you want to use it follow the following instruction\
        \n1-->Run the server if you want to use your computer as a server\
        \n2-->Type the server IP adrress in the field provided\
        \n3-->Type the client's ip\
        \n4-->Press Connect\
        \n5-->Type your message in the white field\
        \n6-->Press Send or just press enter to send message\
        \n7-->Email me if you have something messaoudinelec@gmail.com"
        wx.MessageBox(content, 'Help???', 
            wx.OK | wx.ICON_INFORMATION)
            
    
            

if __name__ =='__main__':
    app=wx.PySimpleApp()
    frame=PyChat(parent=None,id=-1)
    frame.Show()
    app.MainLoop()

    
