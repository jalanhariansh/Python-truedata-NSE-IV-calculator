from scipy.stats import norm
import math


def dOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend):
    ##try:
    return (math.log(UnderlyingPrice / ExercisePrice) + (Interest - Dividend + 0.5 * math.pow(Volatility, 2)) * TimeLeft) / ( Volatility * (math.sqrt(TimeLeft)))
    ##except:
        ##raise NameError(str(UnderlyingPrice)+"    "+str(ExercisePrice)+"    "+str(TimeLeft)+"    "+
                        ##str(Interest)+"    "+str(Volatility)+"   "+str(Dividend))

def NdOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend):
    return math.exp(-math.pow(dOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend), 2) / 2) / (math.sqrt(2 * 3.14159265358979))

def dTwo(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend):
    return dOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend) - Volatility * math.sqrt(TimeLeft)

def NdTwo(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend):
    return norm.cdf(dTwo(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend))

def CallOption(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend):
    return math.exp(-Dividend * TimeLeft) * UnderlyingPrice * norm.cdf(dOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend)) - ExercisePrice * math.exp(-Interest * TimeLeft) * norm.cdf(dOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend) - Volatility * math.sqrt(TimeLeft))

def PutOption(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend):
    return ExercisePrice * math.exp(-Interest * TimeLeft) * norm.cdf(-dTwo(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend)) - math.exp(-Dividend * TimeLeft) * UnderlyingPrice * norm.cdf(-dOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend))

def CallDelta(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend):
    return norm.cdf(dOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend))
    ##CallDelta = norm.cdf((math.log(UnderlyingPrice / ExercisePrice) + (Interest - Dividend) * TimeLeft) / (Volatility * math.sqrt(TimeLeft)) + 0.5 * Volatility * math.sqrt(TimeLeft))
    
def PutDelta(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend):
    return norm.cdf(dOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend)) - 1

def CallTheta(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend):
    CT = -(UnderlyingPrice * Volatility * NdOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend)) / (2 * math.sqrt(TimeLeft)) - Interest * ExercisePrice * math.exp(-Interest * (TimeLeft)) * NdTwo(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend)
    return CT / 365

def OptionGamma(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend):
    return NdOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend) / (UnderlyingPrice * (Volatility * math.sqrt(TimeLeft)))

def Vega(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend):
    return 0.01 * UnderlyingPrice * math.sqrt(TimeLeft) * NdOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend)

def PutTheta(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend):
    PT = -(UnderlyingPrice * Volatility * NdOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend)) / (2 * math.sqrt(TimeLeft)) + Interest * ExercisePrice * math.exp(-Interest * (TimeLeft)) * (1 - NdTwo(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend))
    return PT / 365

def CallRho(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend):
    return 0.01 * ExercisePrice * TimeLeft * math.exp(-Interest * TimeLeft) * norm.cdf(dTwo(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend))

def PutRho(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend):
    return -0.01 * ExercisePrice * TimeLeft * math.exp(-Interest * TimeLeft) * (1 - norm.cdf(dTwo(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend)))

def ImpliedCallVolatility(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Target, Dividend):
    Hi = 5
    Lo = 0
    while((Hi - Lo) > 0.001):
        if(CallOption(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, (Hi + Lo) / 2, Dividend) > Target):
            Hi = (Hi + Lo) / 2
        else:
            Lo = (Hi + Lo) / 2
    return (Hi + Lo) / 2

def ImpliedPutVolatility(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Target, Dividend):
    Hi = 5
    Lo = 0
    while((Hi - Lo) > 0.001):
        if(PutOption(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, (Hi + Lo) / 2, Dividend) > Target):
            Hi = (Hi + Lo) / 2
        else:
            Lo = (Hi + Lo) / 2
    return (Hi + Lo) / 2

def OTW_BlackScholes(callputstock, Output, UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend):
    
    ## Stock Calculations
    if(callputstock[:1]=="s"):
        ## Stock Output
        if((Output[:1]).lower()=="p"):
            return UnderlyingPrice

        elif((Output[:1]).lower()=="d"):
            return 1
            
        elif((Output[:1]).lower()=="g"):
            return 0
            
        elif((Output[:1]).lower()=="t"):
            return 0

        elif((Output[:1]).lower()=="v"):
            return 0

        elif((Output[:1]).lower()=="r"):
            return 0
        ##End Stock Output
    ##End Stock Calculations

    ## Call Option Calculations

    elif(callputstock[:1]=="c"):
        ## Call Option Output
        if((Output[:1]).lower()=="p"):
            return math.exp(-Dividend * TimeLeft) * UnderlyingPrice * norm.cdf(dOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend)) - ExercisePrice * math.exp(-Interest * TimeLeft) * norm.cdf(dOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend) - Volatility * math.sqrt(TimeLeft))
        elif((Output[:1]).lower()=="d"):
             return norm.cdf(dOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend))
        elif((Output[:1]).lower()=="g"):
            return NdOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend) / (UnderlyingPrice * (Volatility * math.sqrt(TimeLeft)))
        elif((Output[:1]).lower()=="t"):
            CT = -(UnderlyingPrice * Volatility * NdOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend)) / (2 * math.sqrt(TimeLeft)) - Interest * ExercisePrice * math.exp(-Interest * (TimeLeft)) * NdTwo(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend)
            return CT / 365
        elif((Output[:1]).lower()=="v"):
            return 0.01 * UnderlyingPrice * math.sqrt(TimeLeft) * NdOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend)
        elif((Output[:1]).lower()=="r"):
            return 0.01 * ExercisePrice * TimeLeft * math.exp(-Interest * TimeLeft) * norm.cdf(dTwo(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend))

        ##End Call Output
    ##End Call Option Calculations

    ## Put Option Calculations
    if(callputstock[:1]=="p"):
	## Put Option Output
        if((Output[:1]).lower()=="p"):
            result = ExercisePrice * math.exp(-Interest * TimeLeft) * norm.cdf(-dTwo(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend)) - math.exp(-Dividend * TimeLeft) * UnderlyingPrice * norm.cdf(-dOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend))
        elif((Output[:1]).lower()=="d"):
            result = norm.cdf(dOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend)) - 1
        elif((Output[:1]).lower()=="g"):
            result = NdOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend) / (UnderlyingPrice * (Volatility * math.sqrt(TimeLeft)))
        elif((Output[:1]).lower()=="t"):
            PT = -(UnderlyingPrice * Volatility * NdOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend)) / (2 * math.sqrt(TimeLeft)) + Interest * ExercisePrice * math.exp(-Interest * (TimeLeft)) * (1 - NdTwo(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend))
            return PT/365
        elif((Output[:1]).lower()=="v"):
            return 0.01 * UnderlyingPrice * math.sqrt(TimeLeft) * NdOne(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend)
        elif((Output[:1]).lower()=="r"):
            return -0.01 * ExercisePrice * TimeLeft * math.exp(-Interest * TimeLeft) * (1 - norm.cdf(dTwo(UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Volatility, Dividend)))
        ##End Put Output
    ##End Put Option Calculations

def OTW_IV(CallPut, UnderlyingPrice, ExercisePrice, TimeLeft, Interest, Target, Dividend):
    
    if((CallPut[:1]).lower()=="c"):
        Hi = 5
        Lo = 0
        while((Hi - Lo) > 0.0001):
            if(OTW_BlackScholes("c", "p", UnderlyingPrice, ExercisePrice, TimeLeft, Interest, (Hi + Lo) / 2, Dividend) > Target):
                Hi = (Hi + Lo) / 2
            else:
                Lo = (Hi + Lo) / 2
        return (Hi + Lo) / 2
    
    elif((CallPut[:1]).lower()=="p"):
        Hi = 5
        Lo = 0
        while((Hi - Lo) > 0.0001):
            if(OTW_BlackScholes("p", "p", UnderlyingPrice, ExercisePrice, TimeLeft, Interest, (Hi + Lo) / 2, Dividend) > Target):
                Hi = (Hi + Lo) / 2
            else:
                Lo = (Hi + Lo) / 2
        return (Hi + Lo) / 2

