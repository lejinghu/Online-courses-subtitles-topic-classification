# Online-courses-subtitles-topic-classification
This project uses:<br>
PySceneDetect: https://github.com/Breakthrough/PySceneDetect<br>
ABBYY: https://github.com/samueltc/ABBYY<br>
<br>
In the 'preprocess' directory, we put the video files of MOOC courses under the 'mp4' directory and the subtitle files under the 'srt' directory. Their names should match.<br>
<br>
"CutScene.py" is a command to use PySceneDetect in order to cut our MOOC videos into scenes and find out the time of the cuts. The images are then generated under the main directory.<br>
<br>
When using "ExtractTitlesAndCut.py", the subtitles are first cut into 5-line text segments, each one representing the sentence in the middle. Then they are given slides' titles as filenames, which are taken through ABBYY OCR from the video images.<br> 
<br>
These text segments will be our test files for classification.<br>