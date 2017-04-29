# Online-courses-subtitles-topic-classification
## Introduction
This is my undergraduate research project.<br>
As MOOC (Massive Open Online Courses) become more and more popular, we hope to find a way to deliver online courses easier for content providers. It is easy to see that videos alone do not make courses. They need to be carefully edited and supplemented by text materials like subtitles. In many occasions, long videos are edited into small separate segments manually with each talking about a single topic. In this project, we hope to make this process automatic by utilizing NLP and OCR technologies. Currently, we require both the videos and the subtitle. But if good speech recognition methods becomes more available in the future, we might try using only the videos. <br>
## Environment
Tested on Windows 7&8 using Anaconda and Python 3.5<br>
<br>
This project uses:<br>
[PySceneDetect](https://github.com/Breakthrough/PySceneDetect)<br>
[ABBYY](https://github.com/samueltc/ABBYY)<br>
[Keras](https://github.com/fchollet/keras)<br>
## Method
### Preprocessing data
Training data are obtained from scanned textbooks from digital libraries using ABBYY PDF Transformer +, used for educational purpose only. <br>
Original test data are course materials obtained from [Coursera](https://www.coursera.org/learn/jisuanji-biancheng), used for educational purpose only. <br>
<br>
We put the video files of MOOC courses under the 'mp4' directory and the subtitle files under the 'srt' directory. Their names should match. <br>
<br>
We use "CutScene.py" to invoke PySceneDetect which cuts our MOOC videos into scenes, and save the lists of scenes in csv files. The first and last frames of each scene are saved under the main directory. <br>
<br>
We "ExtractTitlesAndCut.py" to cut the subtitles into 5-line text segments. Each represents the sentence in the middle. They are then given slides' titles as filenames. The titles are taken through ABBYY OCR from the images. These text segments will be our test files for classification. <br> 
<br>
### Classification
Classification uses keras. The base code is taken from the [keras blog](https://blog.keras.io/using-pre-trained-word-embeddings-in-a-keras-model.html) <br>
## About OCR
In this project there are two instances where OCR is needed. The first time is when we obtain training data, where we use a commercial software. The second time is when we obtain the titles of each slide from the frames, where we use the API.<br>
Out of all the OCR technologies I've tried, ABBYY (www.ocrsdk.com) provides the most accurate outcomes. I hope they can provide more pages for me to complete this project.
