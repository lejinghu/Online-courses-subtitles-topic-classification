import os
import pysrt
from datetime import datetime
for fname in os.listdir('./mp4'):
    csvname=fname[:-3]+"csv"
    os.system(".\\scenedetect -i .\\mp4\\"+fname+" -co .\\csv\\"+csvname+" -d content -df 4 -t 25")
for csvfile in os.listdir('./csv'):
    file=open(csvfile)
    lines=file.readlines()
    timecut=lines[0]
    timecut=timecut.strip()
    timelist=timecut.split(',')
    time_list=[]
    for cut in timelist:
        a = datetime.strptime(cut, '%H:%M:%S.%f')
        time_list.append(a)
        
    cutsub=[]
    for i in range(0,len(time_list)):
        cutsub.append([])
    srtfile=csvfile[:-3]+"srt"
    srt=pysrt.open(".\\srt\\"+srtfile)
    for line in srt:
        start_time=str(line.start)
        end_time=str(line.end)
        text=str(line.text).strip()
        text=text.replace('\n','')
        start_time=datetime.strptime(start_time, '%H:%M:%S,%f')
        end_time=datetime.strptime(end_time, '%H:%M:%S,%f')
        for i in range(0,len(time_list)):
            if((i==0 and start_time<time_list[1]) or (i==(len(time_list)-1) and start_time>=time_list[i]) or (start_time>=time_list[i] and start_time<time_list[i+1])):
                cutsub[i].append(text)
                break
    for x in cutsub:
        print (x)
