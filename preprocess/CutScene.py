import os
import pysrt
from datetime import datetime
for fname in os.listdir('./mp4'):
    csvname=fname[:-3]+"csv"
    os.system(".\\PyScene\\scenedetect -i .\\mp4\\"+fname+" -co .\\csv\\"+csvname+" -d content -df 3 -t 20 -q -si")