import wx
import wx.lib.platebtn as pbtn
import wx.lib.agw.gradientbutton as gbtn
import serial,time
from threading import *
import os

# Button definitions
ID_START = wx.NewId()
ID_STOP = wx.NewId()

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()
VAL_SERIAL_ID= 222

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data

# Thread class that executes processing
class WorkerThread(Thread):
    """Worker Thread Class."""
    def __init__(self, notify_window):
        """Init Worker Thread Class."""
        self.ar = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=1.0)
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

    def run(self):
    	
        """Run Worker Thread."""
        # This is the code executing in the new thread. Simulation of
        # a long process (well, 10s here) as a simple loop - you will
        # need to structure your processing so that you periodically
        # peek at the abort variable
        infoserial=None
        i=0
        while True:
            infserial=self.ar.readline()
            print infserial
			#self.mensaje.SetLabel(label=(">>>>"+(self.data)))
            if self._want_abort:
                # Use a result of None to acknowledge the abort (of
                # course you can use whatever you'd like or even
                # a separate event type)
                wx.PostEvent(self._notify_window, ResultEvent(None))
                return
        # Here's where the result would be returned (this is an
        # example fixed result of the number 10, but it could be
        # any Python object)
        wx.PostEvent(self._notify_window, ResultEvent(10))

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort

        self._want_abort = 1
        self.ar.close()


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
 		self.ar = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=1.0)
 		
 		#INICIO--------creacion de panel para mostras mensaje
 		self.panel = wx.Panel(self,size=(500,600),pos=(0,140))
 		self.panel.SetBackgroundColour((41, 41, 41))
 		#FIN-------creacion de panel para mostrar mensaje 
 		 
 		#INICIO-------creacion de panel para botones de incio y parada
 		self.panel2 = wx.Panel(self,size=(400,600),pos=(0,0))
 		#self.panel2.SetBackgroundColour((1,1,1))
 		#FIN-------------de creaion de panel para botones 
 		bmpconect = wx.Bitmap("/home/dario/Documentos/code/python/conectar2.png",wx.BITMAP_TYPE_ICON)
 		bmpdisconect = wx.Bitmap("/home/dario/Documentos/code/python/desconectar2.png" ,wx.BITMAP_TYPE_ICON)
 		#INICIO-----------inicio creacion de botones 
 		#self.btnstart=wx.Button(self.panel2,label="conect")#BUTTON start normal
 		self.btnstart=wx.BitmapButton(self.panel2,pos=(0,0),style=1,bitmap=bmpconect)#Button start bmp
 		#self.btnstop=wx.Button(self.panel2,label="stop",pos=(0,40))#Button stop normal
 		self.btnstop=wx.BitmapButton(self.panel2,pos=(0,80),style=1,bitmap=bmpdisconect)#Button stop bmp
 		self.btnstate=wx.Button(self.panel2,label="state",style=5,pos=(100,0))#Button of state


 		self.btnstate.SetBackgroundColour((41,41,41))
 		self.btnstart.SetBackgroundColour((200,200,200))
 		self.btnstop.SetBackgroundColour((100,100,100))
 		#FIN-------------creacion de botones
 
 		self.mensaje = wx.TextCtrl(self.panel,size=(500,400),style=wx.TE_MULTILINE|wx.TE_READONLY)

 		#INICIO------------event hanlder`s
 		self.Bind(wx.EVT_BUTTON,self.start,self.btnstart)
 		self.Bind(wx.EVT_BUTTON,self.stop,self.btnstop)




 		menu_bar = wx.MenuBar()
		edit_menu = wx.Menu()

		#edit_menu.Append(wx.NewId(),"PORTS")
		edit_menu.Append(wx.ID_PREFERENCES)
		edit_menu.Append(wx.ID_FIND)
		menu_bar.Append(edit_menu,"Opcion")
		self.SetMenuBar(menu_bar)


		EVT_RESULT(self,self.OnResult)

 		self.worker = None
 		
	def start(self,event):
		if not self.worker:
			self.mensaje.AppendText('serial\n')	
			self.worker = WorkerThread(self)
			self.btnstate.SetBackgroundColour((20,200,20))
			self.btnstate.SetLabel("Conect")
	def stop(self,event):
		self.btnstate.SetBackgroundColour((200,20,20))
		self.btnstate.SetLabel("Disconect")
		if self.worker:
			#self.ar.close()
			self.worker.abort()
			print "stop Rx data"
		self.worker = None
	def OnResult(self,event):
		if event.data is None:
			self.mensaje.AppendText('SERIAL ')
		else:
			self.mensaje.SetLabel(event.data)
if __name__ =="__main__":
	app = myapp(False)
	app.MainLoop()