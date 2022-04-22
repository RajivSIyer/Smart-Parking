"""
@author: Rajiv.S.Iyer

"""
import sys
import os
import smartparkapp  as SMApp
from datetime import datetime, date, timedelta

#All GLobals:-
main_license=""
entrytimestamp=0
exittimestamp=0

def getcommandline():
    global main_license
    global entrytimestamp
    global exittimestamp
    
    if len(sys.argv) < 3:
        main_license = str(input("Ënter car license number(Default = MH04FA488): "))
        main_license = main_license.strip()
        if main_license == "":
            #main_license = 'MH43FO4596'
            main_license = 'MH04FA488'
        print(main_license)

    else:    
        if  len(sys.argv) % 2 == 0:
            print("Error, Invalid number of arguments.")
            return False
        
        for i in range(1, len(sys.argv)):
            if sys.argv[i] == "-l":
                main_license = sys.argv[i+1]
                i=i+1
                continue
            if sys.argv[i] == "-ent":
                entrytime_str = sys.argv[i+1]
                datetime_endt = datetime.strptime(entrytime_str, '%d-%m-%Y %H:%M:%S')
                entrytimestamp = datetime_endt.timestamp()
                i=i+1
                continue
            if sys.argv[i] == "-ext":
                exittime_str = sys.argv[i+1]
                datetime_exdt = datetime.strptime(exittime_str, '%d-%m-%Y %H:%M:%S')
                exittimestamp = datetime_exdt.timestamp()
                i=i+1
                continue
            
    if SMApp.IsCarParked(main_license):
        if exittimestamp==0:
            print("Looks like this car " + main_license + " is already parked.")
            exittime_str = str(input("Please enter Exit time(Default-Hit 'enter' for current time + 1 hour: "))
            exittime_str = exittime_str.strip()
            if exittime_str == "":
                now = datetime.now()
                exittimestamp = datetime.timestamp(now + timedelta(hours=1))
            else:
                datetime_exdt = datetime.strptime(exittime_str, '%d-%m-%Y %H:%M:%S')
                exittimestamp = datetime_exdt.timestamp()

    else:
        if entrytimestamp == 0:
            entrytime_str = str(input("Please enter Entry time(Default-Hit 'enter' for current time: "))
            entrytime_str = entrytime_str.strip()
            if entrytime_str == "":
                now = datetime.now()
                entrytimestamp = datetime.timestamp(now)
            else:
                datetime_endt = datetime.strptime(entrytime_str, '%d-%m-%Y %H:%M:%S')
                entrytimestamp = datetime_endt.timestamp()
        
    return True

#------------------------------------------MAIN PROGRAM----------------------------------

#SMApp.UpdateAllMemberActivityTimeValues()
#SMApp.CleanupAllActivityRecords()
#SMApp.UpdateSpotStatusFromActivity()
#SMApp.CalcAllMemberMedianAndAverage()

carimagedict = {  
                "MH04FA488"   :	"IMG20200213094639.jpg",
                "MH04DJ0746"  :	"IMG20200213094917.jpg",
                "MH46N4312"   :	"IMG20200213095153.jpg",
                "MH46AU1589"  :	"IMG20200213095237.jpg",
                "MH46W1408"   :	"IMG20200213095309.jpg",
                "MH43AW2192"  :	"IMG20200213095926.jpg",
                "MH43QT9987"  : "Mahindra Verito.jpg"
            }



if getcommandline()==False:
    sys.exit()

if main_license in carimagedict:
    local_carimage = "./Images/" + carimagedict[main_license]
else:
    local_carimage = "./Images/" + "outsidercar.jpg"

print(os. getcwd())

if SMApp.IsCarParked(main_license):  
    SMApp.RegisterCarExit(main_license, exittimestamp)
else:
    print(entrytimestamp)
    print(main_license)
    y=SMApp.RegisterCarEntry(main_license, entrytimestamp,local_carimage) 