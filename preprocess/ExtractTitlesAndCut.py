from ABBYY import CloudOCR
from PIL import Image
import sys, os, re
from io import BytesIO
import shutil
import pysrt
from datetime import datetime

def extract_and_ocr(filename, region):
    image = Image.open(filename)
    region_data = image.crop(region)

    tempfile=BytesIO()
    tempfile.seek(0)
    region_data.save(tempfile,"JPEG")
    file={'temp.jpg': tempfile.getvalue()}
    ocr_engine = CloudOCR(application_id='', password='')
    result = ocr_engine.process_and_download(file, profile='documentConversion',exportFormat='txtUnstructured', language='ChinesePRC,English')
    x=result['txtUnstructured'].read()
    return x

    
all_titles={}


for file in os.listdir('.'):
    if(file.find("Scene-1-OUT.jpg")!=-1):
        course_name_regex='[\d]+-[\d]+'
        course_name=re.findall(course_name_regex,file)
        title_num_regex='-([\d]+)-'
        title_num=re.findall(title_num_regex,file)
        title=extract_and_ocr(file,(240,0,960,65))
        all_titles[str(course_name[0])]={}
        all_titles[str(course_name[0])][int(title_num[0])]=str(title,encoding='UTF-8-sig')
        #newf=open("title/"+str(course_name[0])+".txt","ab")
        #newf.write((title_num[0]+' ').encode(encoding='UTF-8'))
        #newf.write(title+('\n').encode(encoding='UTF-8'))
        #newf.close()

for file in os.listdir('.'):
    if(file.find("IN.jpg")!=-1):
        course_name_regex='[\d]+-[\d]+'
        course_name=re.findall(course_name_regex,file)
        title_num_regex='-([\d]+)-'
        title_num=re.findall(title_num_regex,file)
        title=extract_and_ocr(file,(240,0,960,65))
        all_titles[str(course_name[0])][int(title_num[0])]=str(title,encoding='UTF-8-sig')
        #newf=open("title/"+str(course_name[0])+".txt","ab")
        #newf.write((title_num[0]+' ').encode(encoding='UTF-8'))
        #newf.write(title+('\n').encode(encoding='UTF-8'))
        #newf.close()       

print(all_titles)
TEST_DATA_DIR = "srt/"
all_files=sorted(os.listdir(TEST_DATA_DIR))
if(os.path.exists("srtcut/")==False):
    os.mkdir("./"+"srtcut")	
for j in range(len(all_files)):
    if(os.path.exists("srtcut/"+(all_files[j][:-4]))==True):
        shutil.rmtree("srtcut/"+(all_files[j][:-4]))
        print ("DEL "+all_files[j][:-4])
    os.mkdir("srtcut/"+all_files[j][:-4])

file_num=0
for fname in (all_files):#for each srt file, find the csv file which contains the cuts
    file=open(".\\csv\\"+fname[:-3]+"csv")
    lines=file.readlines()
    timecut=lines[0]
    timecut=timecut.strip()
    timelist=timecut.split(',')
    time_list=[]
    for cut in timelist:
        a = datetime.strptime(cut, '%H:%M:%S.%f')
        time_list.append(a)
    texts = []
    tnames= []
    lines=pysrt.open(TEST_DATA_DIR+fname)
    tt=[]
    for i in range(len(lines)-4):
        tt=[]
        tt.append(lines[i].text)
        tt.append(lines[i+1].text)
        tt.append(lines[i+2].text)
        tt.append(lines[i+3].text)
        tt.append(lines[i+4].text)
        texts.append(tt)

        line=lines[i+2]
        start_time=str(line.start)
        start_time=datetime.strptime(start_time, '%H:%M:%S,%f')
        if(start_time<time_list[0]):
            tnames.append(0)
        elif(start_time>time_list[len(time_list)-1]):
            tnames.append(len(time_list))
        else:
            for ti in range(0,len(time_list)):
                if((start_time>=time_list[ti] and start_time<time_list[ti+1])):
                    tnames.append(ti+1)
                    break
    
    for i in range(len(texts)):
        fff=int(tnames[i])+1
        f_name=str(fname)
        title=all_titles[f_name[:-4]][fff]
        unnamed=r'\\|\/|\:|\*|\?|\"|\<|\>|\|\||\n|\r|\t|\''
        title=re.sub(unnamed,' ',title)
        xxx=open("srtcut/"+f_name[:-4]+"/"+str(i)+"_"+title+".txt","w")
        for text in texts[i]:
            xxx.write(text+'\n')

