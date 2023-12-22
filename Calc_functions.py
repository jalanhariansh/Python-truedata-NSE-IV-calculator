import os
import sys
from numpy import random
from datetime import datetime,timedelta
import csv

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

from Black_Scholes_module import OTW_IV

import sys
import time


from datetime import datetime,timedelta

def ExpiryCalcInit(DateOfCur,OptExpPeriod,OptExpNumber):
    if(OptExpPeriod==0):
        ExpiryDate=DateOfCur+timedelta(7*(OptExpNumber-1))
        ExpiryDate=ExpiryDate+timedelta(10-ExpiryDate.weekday() if ExpiryDate.weekday()>3 else 3-ExpiryDate.weekday())
        ExpiryDate = ExpiryDate.date()

    if(OptExpPeriod==1):
        ExpiryDate=DateOfCur+timedelta(10-DateOfCur.weekday() if DateOfCur.weekday()>3 else 3-DateOfCur.weekday())
        ExpiryDate = datetime(ExpiryDate.year, ExpiryDate.month, ExpiryDate.day, 15, 30, 0)

        i=0
        
        while(i!=OptExpNumber):
            while ExpiryDate.month==(ExpiryDate+timedelta(7)).month:
                ExpiryDate=ExpiryDate+timedelta(7)
            i=i+1
            ExpiryDate=ExpiryDate+timedelta(7)
            
        ExpiryDate=ExpiryDate-timedelta(7)

        ExpiryDate = ExpiryDate.date()

    ##check from datatbase if market was closed that day

    return ExpiryDate

def formatStrkPr(Strkpr):
    return '%g'%(Strkpr)
    
def OTW_IV_array(self,tickerName,Underlying,DateTime,period,optGap,OptFromStrike,OptType,OptExpPeriod,OptExpNumber,rollOver,countChanged,editChanged):
    if len(Underlying)!=len(DateTime):
        return 998
    try:
        Interest=0
        Dividend=0
        
        
        optionGap=-1
        
        for i in range(0,len(optGap[0])):
            if optGap[0][i]==tickerName:
                optionGap=float(optGap[1][i])
                break
        
        if(optionGap==-1):
            return ""
        

        logged=[]
        logged.append(load_IV_past_log(self,tickerName+" "+str(int(OptFromStrike))+" "+OptType+" "+str(int(OptExpPeriod))+str(int(OptExpNumber))))
        logged.append(load_IV_past_log(self,tickerName+" "+str(int(OptFromStrike))+" "+OptType+" "+str(int(OptExpPeriod))+str(int(OptExpNumber+1))))
        
        k=0

        with open(r'C:\Users\HJ\Desktop\python COM server\log2\IV_log_log.csv','a',newline='') as file:
                        writer=csv.writer(file)
                        writer.writerow(logged[0][1])
                        writer.writerow(logged[0][2])
                        writer.writerow(DateTime)
                        writer.writerow([])

        with open(r'C:\Users\HJ\Desktop\python COM server\log2\full_log.csv','a',newline="") as file:
            writer=csv.writer(file)
            writer.writerow([])
            writer.writerow([])
            
        ExpiryCalc=ExpiryCalcInit(DateTime[0],OptExpPeriod,OptExpNumber)
        
        j=[-1,-1]
        switch=0
                    
        for i in range(0,len(Underlying)):
            countChanged.emit(i+1)
            editChanged.emit(str(DateTime[i]))
            cur=DateTime[i]
            
            if cur==0 or cur.year<2020:
                continue
              
            flag=0

            if(cur.date()>ExpiryCalc):
                ExpiryCalc=ExpiryCalcInit(cur.date(),OptExpPeriod,OptExpNumber)
            
            if(ExpiryCalc-cur.date()<timedelta(rollOver)):
                switch=1
                ExpiryDate=ExpiryCalcInit(cur.date(),OptExpPeriod,OptExpNumber+1)
            else:
                switch=0
                ExpiryDate=ExpiryCalc
                
                
            while j[switch]<len(logged[switch][1])-1:
                j[switch]=j[switch]+1
                
                if(logged[switch][1][j[switch]]==cur):
                    flag=1
                    break
                elif(logged[switch][1][j[switch]]>cur):
                    if j[switch]!=0:
                        if logged[switch][1][j[switch]-1]<cur:
                            break
                        else:
                            while logged[switch][1][j[switch]]>cur and j[switch]>0:
                                j[switch]=j[switch]-1
                    else:
                        break
                    
            
            if(j[switch]==len(logged[switch][1])-1):
                j[switch]=j[switch]+1
                        
            if flag==1:
                continue
            
            StrkPr=(optionGap*round(Underlying[i]/optionGap))+(OptFromStrike*optionGap)
            
            tickerCur=tickerName+ExpiryDate.strftime("%y%m%d")+formatStrkPr(StrkPr)+OptType
            
            OptPr=[]
            
            
            if period>=86400:
                OptPr=self.td_api.get_historic_data(tickerCur,start_time=datetime(cur.year,cur.month,cur.day,15)
                                                    ,end_time=cur.date()+timedelta(1),bar_size="1min")
                if OptPr!=[]:
                    OptPr=[OptPr[-1]]
                
            else:
                OptPr=self.td_api.get_historic_data(tickerCur,start_time=cur-timedelta(minutes=1)
                                                ,end_time=cur,bar_size="1min")
                
    ##            try:
            logged[switch][1].insert(j[switch],DateTime[i])
            if OptPr==[]:
                logged[switch][2].insert(j[switch],0)
            else:
                logged[switch][2].insert(j[switch],round(100*OTW_IV(OptType,Underlying[i],StrkPr,(ExpiryDate-cur.date()).total_seconds()/31536000,Interest,OptPr[0]['c'],Dividend),2))
                
##                writer.writerow([str(cur),Underlying[i],StrkPr,str(ExpiryDate),OptPr[0]['c']])

    ##            except:
    ##                result[i]=result[i-1]
            
            
            
        update_IV_log(self,tickerName+" "+str(int(OptFromStrike))+" "+OptType+" "+str(int(OptExpPeriod))+str(int(OptExpNumber)),logged[0])
        update_IV_log(self,tickerName+" "+str(int(OptFromStrike))+" "+OptType+" "+str(int(OptExpPeriod))+str(int(OptExpNumber+1)),logged[1])
    except Exception as e:
        with open(r'C:\Users\HJ\Desktop\python COM server\log2\logError.csv','w') as file:
            writer=csv.writer(file)
            writer.writerow([e])
        raise NameError()
                
def find_IV_past_log(IV_log,ticker):
    for i in range(0,len(IV_log)):
        if IV_log[i][0]==ticker:
            return i
    return -1

def date_parser(date):
    return datetime.strptime(date,"%Y-%m-%d %H:%M:%S")

def load_IV_past_log(self,ticker):
    result=[]
    
    if find_IV_past_log(self.IV_log,ticker)!=-1:
            return self.IV_log[find_IV_past_log(self.IV_log,ticker)]
    
    else:
        try:
            with open(r'C:\Users\HJ\Desktop\python COM server\log\\'+ticker+'.csv','r') as file:
                a=list(csv.reader(file))
                a=[ticker,list(map(date_parser,a[0])),list(map(float,a[1]))]
                self.IV_log.append(a)
                result=a
        except:
            result=[ticker,[],[]]
            self.IV_log.append(result)
            

    return result

def update_IV_log(self,ticker,log):
    tickIndex=find_IV_past_log(self.IV_log,ticker)
    
    self.IV_log[tickIndex][1]=log[1]
    self.IV_log[tickIndex][2]=log[2]

    with open(r'C:\Users\HJ\Desktop\python COM server\log\\'+ticker+'.csv','w',newline='') as file:
        writer=csv.writer(file)
        writer.writerow(log[1])
        writer.writerow(log[2])
