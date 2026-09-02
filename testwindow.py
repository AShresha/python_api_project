class TenMinutesData:
    def __init__(self):
        self.T_10M = 2
        self.RH_10M = 539

TenMinutesData = TenMinutesData()
#print(TenMinutesData.T_10M)

class HourData:
    def __init__(self):
        self.T_1H = 505
        self.RH_1H = 540

HourData = HourData()

class compareparams:
    def __init__(self):
        TenMinutesData.T_10M = HourData.T_1H

        

parameterTest = print("Enter a parameter code:", input())
if parameterTest == TenMinutesData.T_10M:
    print(compareparams)


    


#print(TenMinutesData.T_10M