import pythoncom
from win32com.server.exception import COMException
import win32com.server.util
import win32com.client.dynamic
import win32gui
from numpy import random
import time
import csv
import os
import sys
from datetime import datetime,timedelta
from threading import Thread
import copy
from truedata_ws.websocket.TD import TD


path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

from kite_login_example import autologin
from GUI import IV_array_GUI
from Black_Scholes_module import OTW_IV
from Calc_functions import find_IV_past_log,load_IV_past_log,ExpiryCalcInit,formatStrkPr

def datecalc(period,a,b=0):
        if b==0 and a==0:
                return 0
        elif b==0:
                x=datetime.strptime(str(int(19000000+a)),"%Y%m%d")
                return datetime(x.year,x.month,x.day,15,29,59)
        else:
                x=datetime.strptime(str(int(19000000+a))+" "+str(int(b)),"%Y%m%d %H%M%S")
                x=x+timedelta(seconds=period-1)
                if x.hour>15 or (x.hour==15 and x.minute>30):
                        x=datetime(x.year,x.month.x.day,15,29,59)
                return x

        

class PythonUtilities(object):
    _public_methods_=['getIVdata','load_data_log']
    
    _reg_clsid_="{25F32489-9E84-4D9F-8AEB-44DC9B528405}"
    _reg_desc_ =   "Utilities for Extending Amibroker AFL"
    _reg_progid_ = "PyAFL"
    _readonly_attrs_ = ['revision']
    
    _public_attrs_=['NDepVar','ArrayLen','ProbArray',
                    'X_Open','X_High','X_Low','X_Close',
                    'X_Volume','X_OI','IV_log']

    Log=""  # Log may be a  string use to pass text to AFL
    init=0
    optGap=[]
    IV_log=[]
    inst_tkn={}
    kite=0
    kws=0
    td_api=0
    thread=Thread()
    def load_data_log(self):
        if(self.init==0):
                self.init=1
                with open(r'C:\Users\HJ\Desktop\python COM server\log\optionGap.csv','r') as optGap:
                        self.optGap=list(csv.reader(optGap))
                self.td_api = TD('dummy', 'dummy',live_port=None)

                                
        return 1

    def getIVRTdata(self,tickerName,Underlying,Now,optFromStrike,optionType,optionExpiryType,optionExpiryNumber,rollOverPeriod):
            
            ExpiryDate=ExpiryCalcInit(Now,optionExpiryType,optionExpiryNumber)

            if(ExpiryDate-Now.date()<timedelta(rollOverPeriod)):
                    ExpiryDate=ExpiryCalcInit(Now,optionExpiryType,optionExpiryNumber+1)
                    
            for i in range(0,len(self.optGap[0])):
                    if self.optGap[0][i]==tickerName:
                            optionGap=float(self.optGap[1][i])
                            break
            if(optionGap==-1):
                    return 0

            StrkPr=(optionGap*round(Underlying/optionGap))+(optFromStrike*optionGap)
            tickerCur=tickerName+ExpiryDate.strftime("%y%m%d")+formatStrkPr(StrkPr)+optionType
            print(tickerCur)
            OptPr=self.td_api.get_historic_data(tickerCur,start_time=datetime(Now.year,Now.month,Now.day,9,15)
                                            ,end_time=Now,bar_size="tick")
            
            Interest=0
            Dividend=0
            if OptPr==[]:
                    return -1
            else:
                    OptPr=[OptPr[-1]]
                    return round(100*OTW_IV(optionType,Underlying,StrkPr,(ExpiryDate-Now.date()).total_seconds()/31536000,Interest,OptPr[0]['ltp'],Dividend),2)

    def getIVdata(self,tickerName,Underlying,dnum,tnum,period,optFromStrike,optionType,optionExpiryType,optionExpiryNumber,rollOverPeriod,sliceFactor):
        Underlying=list(Underlying)
        dnum=list(dnum)
        tnum=list(tnum)

        

        if sliceFactor<len(Underlying):
                Underlying=Underlying[-int(sliceFactor):]
                dnum=dnum[-int(sliceFactor):]
                tnum=tnum[-int(sliceFactor):]

        if len(Underlying)!=len(dnum) or len(tnum)!=len(dnum):
                return 0
        
        if period>86400:
                return 0
        temp=[period]*len(Underlying)
        
        if period==86400:
                
                BarTimeArray=list(map(datecalc,temp,dnum))
        else:
                BarTimeArray=list(map(datecalc,temp,dnum,tnum))

        del(temp)
                
        with open(r'C:\Users\HJ\Desktop\python COM server\log2\log.csv','w') as file:
                writer=csv.writer(file)
                writer.writerow(Underlying)
                writer.writerow(dnum)
                writer.writerow(tnum)
                
        liveMarket=False
        Now=datetime.now()
        if Now.date()==BarTimeArray[-1].date() and (Now.hour<15 or (Now.hour==15 and Now.minute<=30)):
                liveMarket=True
        
        logged=[] 
        logged.append(load_IV_past_log(self,tickerName+" "+str(int(optFromStrike))+" "+optionType+" "+str(int(optionExpiryType))+str(int(optionExpiryNumber))))
        logged.append(load_IV_past_log(self,tickerName+" "+str(int(optFromStrike))+" "+optionType+" "+str(int(optionExpiryType))+str(int(optionExpiryNumber+1))))
        result=[0]*len(Underlying)
        flag=1
        
        if len(logged[0][1])!=0 or len(logged[1][1])!=0:
                j=[-1,-1]
                switch=0
                for i in range(0,len(Underlying)-1 if (liveMarket and BarTimeArray[-1]>Now) else len(Underlying)):
                        flag=1
                        cur=BarTimeArray[i]
                        
                        if cur==0 or cur.year<2020:
                                flag=0
                                result[i]=result[i-1] if i>0 else 0
                                continue
                                
                        ExpiryDate=ExpiryCalcInit(cur,optionExpiryType,optionExpiryNumber)

                        if(ExpiryDate-cur.date()<timedelta(rollOverPeriod)):
                                switch=1
                        else:
                                switch=0
                                
                        while j[switch]<len(logged[switch][1])-1:
                            j[switch]=j[switch]+1
                            if(logged[switch][1][j[switch]]==cur):
                                    result[i]=logged[switch][2][j[switch]]
                                    if result[i]==0:
                                            result[i]=result[i-1] if i>0 else 0
                                    flag=0
                                    break
                            
                            elif(logged[switch][1][j[switch]]>cur):
                                if j[switch]!=0:
                                    if logged[switch][1][j[switch]-1]<cur:
                                        break
                                    else:
                                        while logged[switch][1][j[switch]-1]>=cur and j[switch]>0:
                                            if(logged[switch][1][j[switch]-1]==cur):
                                                j[switch]=j[switch]-1
                                            j[switch]=j[switch]-1
                                else:
                                    break
                                
                        if flag==1:
                            break
                        
                        
        if not self.thread.is_alive() and flag==1:
                if liveMarket and BarTimeArray[-1]>Now:
                        self.thread=Thread(target=IV_array_GUI,args=(self,tickerName,Underlying[:-1],BarTimeArray[:-1],period,self.optGap,optFromStrike,optionType,optionExpiryType,optionExpiryNumber,rollOverPeriod,))
                else:
                        self.thread=Thread(target=IV_array_GUI,args=(self,tickerName,Underlying,BarTimeArray,period,self.optGap,optFromStrike,optionType,optionExpiryType,optionExpiryNumber,rollOverPeriod,))
                self.thread.start()

        if liveMarket and BarTimeArray[-1]>Now:
                result[-1]=self.getIVRTdata(tickerName,Underlying[-1],Now,optFromStrike,optionType,optionExpiryType,optionExpiryNumber,rollOverPeriod)
                
        return result
 

        
if __name__=='__main__':
    print("Registering COM Server ")
    import win32com.server.register
    win32com.server.register.UseCommandLine(PythonUtilities)

# uncomment out if you want to unregister com server 

##    from win32com.server.register import UnregisterServer
##    UnregisterServer("{25F32489-9E84-4D9F-8AEB-44DC9B528405}")
##    print "Com server unregistered."    

#############################################End Python Code
####################################
