"""
Serial monitor open source for microcontrollers
----------------------------------------

This App was created utilizing wxptython and pyserial


The actual App still find in a version 1.


Copyright (c) 2020,Dario jose artega villalba , All rights reserved.
"""

import wx
import wx.lib.platebtn as pbtn
import wx.lib.agw.gradientbutton as gbtn
import serial,time
import threading
import os
import sys 

class myapp(wx.App):
 	def OnInit(self):
 		self.frame = Myframe(None,title="Smon")
 		self.frame.SetMaxSize(wx.Size(500,600))
		self.frame.SetMinSize(wx.Size(500,600))
 		self.SetTopWindow(self.frame)
 		self.frame.Show()
 		return True
class Myframe(wx.Frame):	
 	def __init__(self,parent,id=wx.ID_ANY,title="",pos=wx.DefaultPosition,size=(500,600),style=wx.DEFAULT_FRAME_STYLE,name="FrameMONITORSerial"):
 		super(Myframe,self).__init__(parent,id,title,pos,size,style,name)
 		
 		
 		#INICIO--------creacion de panel para mostras mensaje
 		self.panel = wx.Panel(self,size=(500,600),pos=(0,200))
 		self.panel.SetBackgroundColour(("#FFFFFF"))
 		#FIN-------creacion de panel para mostrar mensaje 
 		 
 		#INICIO-------creacion de panel para botones de incio y parada
 		self.panel2 = wx.Panel(self,size=(500,200),pos=(0,0))
 		self.panel2.SetBackgroundColour(("#FFFFFF"))
 		#FIN-------------de creaion de panel para botones 
 		bmpstart = wx.Bitmap('/home/dario/Documentos/Repos/serial-monitor-in-wxpython/image/conectar2.png',wx.BITMAP_TYPE_ANY)
 		bmpstop  = wx.Bitmap('/home/dario/Documentos/Repos/serial-monitor-in-wxpython/image/desconectar2.png',wx.BITMAP_TYPE_ANY)
 		bmpsend  = wx.Bitmap('/home/dario/Documentos/Repos/serial-monitor-in-wxpython/image/send.png',wx.BITMAP_TYPE_ANY)
 		#INICIO-----------inicio creacion de botones 
 		Ports =  u"/dev/ttyACM0|/devTttyACM1|/dev/ttyACM2".split("|")
 		baud = 	 u"9600|16000|202000".split("|")
 		self.btnConect=wx.Button(self.panel2,label="Abrir",size=(80,40),pos=(5,5))
 		self.btnDisconect=wx.Button(self.panel2,label="Cerrar",size=(80,40),pos=(94,5))
 		self.Cbbox_ports = wx.ComboBox(self.panel2,value="",choices=Ports,size=(120,25),style=wx.CB_READONLY,pos=(350,15))	
 		self.Cbbox_baud = wx.ComboBox(self.panel2,value="EmptyString",choices=baud,size=(120,25),style=wx.CB_READONLY,pos=(350,65))


 		self.btnConect.SetBackgroundColour("#008db1")
 		self.btnDisconect.SetBackgroundColour("#008db1")
 		self.Cbbox_ports.SetBackgroundColour("#008db1")
 		self.Cbbox_baud.SetBackgroundColour("#008bd1")
 		#FIN-------------creacion de botones
 
 		self.mensaje_serial = wx.TextCtrl(self.panel,size=(500,330),style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.mensaje_serial.SetBackgroundColour("#232323") 		
 		#self.Controls_port = wx.StaticText(self.panel2,label="Controls port",pos=(90,60))

 		self.Txinput= wx.TextCtrl(self.panel,size=(400,30),pos=(0,339))
 		self.Txinput.SetBackgroundColour("#232323")
 		#INICIO------------event hanlder`s
 		self.Bind(wx.EVT_BUTTON,self.Conect,self.btnConect)
 		self.Bind(wx.EVT_BUTTON,self.Discone,self.btnDisconect)
 		

 		self.serial_state=0 #FLAG STATE CONECTION
 		redir = RedirectText(self.mensaje_serial)
		sys.stdout=redir
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<parte^grafica
	def flag(self,val):
		self.serial_state=val
	def open_COM(self,):
	 		if self.serial_state==0:
	 			try: 
	 				self.arduino_conf= serial.Serial("/dev/ttyACM0",9600,timeout=1)
	 				self.serial_state=1
	 				self.btnStart_Com = wx.Button(self.panel2,label="Start comunication",size=(168,50),pos=(5,60))
	 				self.btnStart_Com.SetBackgroundColour("#008db1")
	 				self.Bind(wx.EVT_BUTTON,self.run_,self.btnStart_Com)
	 				self.btnSend = wx.Button(self.panel,label="SEND",pos=(400,339))
	 				self.btnSend.SetBackgroundColour("#008db1")
	 				self.Bind(wx.EVT_BUTTON,self.send_,self.btnSend)
	 			except:
	 				wx.MessageBox('Primero conecte el dispositivo serial', 'Info',wx.OK | wx.ICON_INFORMATION)
	 				self.serial_state=0
	def close_COM(self):
		self.arduino_conf.close()
		self.dead=True

	def COM_SERIAL_RX(self):
		self.dead=False
 		while (not self.dead):
 			while True:
 				self.data=self.arduino_conf.readline()
 				print (self.data)
 	def COM_SERIAL_TX(self):
 			data = "hola mundo"
 			self.arduino_conf.write(b"%s"%data)

	def Conect(self, event):
			self.open_COM()
			#self.COM_SERIAL_RX()
	def Discone(self,event):
		try :
			self.close_COM()
			self.flag(0)
			print("COM serial closed")
			self.btnStart.Destroy()
		except AttributeError:
			print "Primero conectece"

	def run_(self,event):
		self.s=threading.Thread(target=self.COM_SERIAL_RX)
		self.s.start()
	def send_(self,event):
		self.COM_SERIAL_TX()



class RedirectText(object):
    def __init__(self, aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self, string):
        wx.CallAfter(self.out.WriteText, string)



if __name__ =="__main__":
	app = myapp(False)
	app.MainLoop()