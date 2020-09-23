from  PyQt5.QtWidgets  import * 
from  PyQt5.uic  import  loadUi

from  matplotlib.backends.backend_qt5agg  import  ( NavigationToolbar2QT  as  NavigationToolbar )
from scipy.io.wavfile import read
from scipy.fftpack import fft, fftfreq, fftshift, ifft
from scipy.signal import hilbert
from scipy.integrate import cumtrapz

import  numpy  as  np 
import  random

fft_ = lambda t, y: (fftshift(fftfreq(y.shape[0], t[1]-t[0])), fftshift(fft(y))/y.shape[0])
global Signal, Range, MSignal, MRange

class  MatplotlibWidget ( QMainWindow ):
    def  __init__ ( self ):
        """ 
        Loads the .ui file and associates certain widgets with specific functions 
        """
    
        QMainWindow . __init__ ( self )

        loadUi ( "UI files/Testv2.ui" , self )

        self . setWindowTitle ( "Modulador de Señales" )

        self . pushButton . clicked . connect ( self . update_graph )
        
        self . pushButtonWGN . clicked . connect ( self . WGN )
        
        self . actionImport . triggered . connect(self.openFileNameDialog)
        
        self . actionSin_60Hz . triggered . connect(self.DummyImport)
        
        self . actionAM . triggered . connect(self.modAM)
        
        self . addToolBar ( NavigationToolbar ( self . MplWidget . canvas ,  self ))
        
    def DummyImport(self):
        global Range
        global Signal
        
        Range=np.linspace(0, 3, 1000*3)
        Signal=np.sin(60 * Range * 2 * np.pi)+1
        W, Freq=fft_(Range, Signal)
        
        self . MplWidget . canvas . figure . clear()
        
        a = self . MplWidget . canvas . figure . add_subplot (211)
        a.plot( Range ,  Signal )
        a.grid(True)
        a.set_xlabel("Time [s]")
        
        b=self . MplWidget . canvas . figure . add_subplot (212)
        b.plot( W ,  Freq )
        b.grid(True)
        b.set_xlabel("Frequency [Hz]")
        
        self . MplWidget . canvas . draw ()
        
    def  update_graph ( self ):
        global Range
        global Signal
        
        W, Freq=fft_(Range, Signal)
        
        self . MplWidget . canvas . figure . clear()
        
        a = self . MplWidget . canvas . figure . add_subplot (211)
        a.plot( Range ,  Signal )
        a.grid(True)
        a.set_xlabel("Time [s]")
        
        b=self . MplWidget . canvas . figure . add_subplot (212)
        b.plot( W ,  Freq )
        b.grid(True)
        b.set_xlabel("Frequency [Hz]")
        
        self . MplWidget . canvas . draw ()
        
    def WGN (self):
        global Signal
        
        Noise=np.random.normal(0, 0.1, size=Signal.shape)
        Signal=Signal+Noise
        W, Freq=fft_(Range, Signal)
        
        self . MplWidget . canvas . figure . clear()
        
        a = self . MplWidget . canvas . figure . add_subplot (211)
        a.plot( Range ,  Signal )
        a.grid(True)
        a.set_xlabel("Time [s]")
        
        b=self . MplWidget . canvas . figure . add_subplot (212)
        b.plot( W ,  Freq )
        b.grid(True)
        b.set_xlabel("Frequency [Hz]")
        
        self . MplWidget . canvas . draw ()
        
    def openFileNameDialog(self):
        global Range
        global Signal
        
        options = QFileDialog.Options()
        SignalFile, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Txt Files (*.txt);;Wav Files (*.wav)", options=options)
        
        if SignalFile:
            if (SignalFile.find(".wav")!=-1):
                Data=read(SignalFile)
                Signal=np.array(Data[1],dtype=float)
                Range=np.linspace(0,len(Signal)/Data[0],len(Signal))
            else:
                Signal=np.genfromtxt(SignalFile,delimiter='\t',skip_header=0)[:,1]
                Range=np.genfromtxt(SignalFile,delimiter='\t',skip_header=0)[:,0]
                
            W, Freq=fft_(Range, Signal)
            
            self . MplWidget . canvas . figure . clear()
            
            a = self . MplWidget . canvas . figure . add_subplot (211)
            a.plot( Range ,  Signal )
            a.grid(True)
            a.set_xlabel("Time [s]")
            
            b=self . MplWidget . canvas . figure . add_subplot (212)
            b.plot( W ,  Freq )
            b.grid(True)
            b.set_xlabel("Frequency [Hz]")
            
            self . MplWidget . canvas . draw ()
                
    def modAM(self):
        global Signal
        global MSignal
        global Range
        global MRange
        MRange=Range
        fc=300
        Carrier=np.sin(fc * Range * 2 * np.pi)
        MSignal=(Signal)*Carrier
        MW, MFreq=fft_(MRange, MSignal)
        W, Freq=fft_(Range, Signal)
        self . MplWidget . canvas . figure . clear()
        a = self . MplWidget . canvas . figure . add_subplot (221)
        a.plot( Range ,  Signal )
        a.grid(True)
        a.set_xlabel("Time [s]")
        b=self . MplWidget . canvas . figure . add_subplot (223)
        b.plot( W ,  Freq )
        b.grid(True)
        b.set_xlabel("Frequency [Hz]")
        c = self . MplWidget . canvas . figure . add_subplot (222)
        c.plot( MRange ,  MSignal )
        c.grid(True)
        c.set_xlabel("Time [s]")
        d=self . MplWidget . canvas . figure . add_subplot (224)
        d.plot( MW ,  MFreq )
        d.grid(True)
        d.set_xlabel("Frequency [Hz]")
        self . MplWidget . canvas . draw ()
        
app  =  QApplication ([]) 
window  =  MatplotlibWidget () 
window . show () 
app . exec_ ()