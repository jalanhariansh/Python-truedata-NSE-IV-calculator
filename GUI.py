from datetime import datetime
import sys
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import (QWidget,QApplication, QDialog,QLabel,
                             QProgressBar, QPushButton)

from Calc_functions import OTW_IV_array
from Black_Scholes_module import OTW_IV
from kite_login_example import autologin
import csv
from datetime import datetime,timedelta
import time

class External(QThread):
    """
    Runs a counter thread.
    """
    countChanged = pyqtSignal(int)
    editChanged = pyqtSignal(str)

    parObj=0
    tickerName=0
    Underlying=0
    DateTime=0
    period=0
    optGap=0
    OptFromStrike=0
    OptType=0
    OptExpPeriod=0
    OptExpNumber=0
    rollOver=0
    
    def __init__(self,Inps,parent=None):
        super().__init__()
        self.parObj=Inps[0]
        self.tickerName=Inps[1]
        self.Underlying=Inps[2]
        self.DateTime=Inps[3]
        self.period=Inps[4]
        self.optGap=Inps[5]
        self.OptFromStrike=Inps[6]
        self.OptType=Inps[7]
        self.OptExpPeriod=Inps[8]
        self.OptExpNumber=Inps[9]
        self.rollOver=Inps[10]
        
        
        
    def run(self):
        OTW_IV_array(self.parObj,self.tickerName,self.Underlying,self.DateTime,self.period,self.optGap,self.OptFromStrike,self.OptType,self.OptExpPeriod,self.OptExpNumber,self.rollOver,self.countChanged,self.editChanged)

        
class Actions(QDialog):
    def __init__(self,value):
        super().__init__()
        self.var=value
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.var[1])
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # enable custom window hint
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)

        # disable (but not hide) close button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        
        self.progress = QProgressBar(self)
        self.progress.setGeometry(30, 40, 200, 25)
        self.progress.setStyleSheet(" QProgressBar { border: 2px solid grey; border-radius: 0px; text-align: center; } QProgressBar::chunk {background-color: #3add36; width: 1px;}")
        self.progress.setMaximum(len(self.var[2]))
        
        self.base_label = QLabel('Downloading Data for:', self)
        self.base_label.setGeometry(30,70,200,25)

        self.var_label = QLabel('BaseMessage', self)
        self.var_label.setGeometry(30,90,200,15)
        
        self.show()
        
        
        
        self.calc = External(self.var)
        self.calc.finished.connect(self.look)
        self.calc.countChanged.connect(self.onCountChanged)
        self.calc.editChanged.connect(self.onabc)
        
        self.calc.start()

    def look(self):
        QApplication.quit()
        
    def onCountChanged(self, value):
        self.progress.setValue(value)

    def onabc(self,value):
        self.var_label.setText(value)

    def closeEvent(self, evnt):
        evnt.ignore()

            
def IV_array_GUI(self,tickerName,Underlying,DateTime,period,optGap,OptFromStrike,OptType,OptExpPeriod,OptExpNumber,rollOver):
    app = QApplication(sys.argv)
    demo=Actions([self,tickerName,Underlying,DateTime,period,optGap,OptFromStrike,OptType,OptExpPeriod,OptExpNumber,rollOver])
    sys.exit(app.exec_())
