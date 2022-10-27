import picamera
from time import sleep
from datetime import datetime, timedelta
import io
import subprocess
from PIL import Image
from subprocess import call
from multiprocessing import Process
import sounddevice as sd
import soundfile as sf
from gpiozero import MotionSensor
import RPi.GPIO as GPIO
import logging
import gpiozero as gz

MotionDetected = False

#set pin that pir sensor is connected to 
pir = MotionSensor(4)

#allow pir to settle
sleep(5)
print('Ready!')

#set directory for videos and audio
audiopath= "/home/pi/testing/"
videopath= "/home/pi/testing/"

#record temp in log file
temp = gz.CPUTemperature().temperature

#start recording a circular stream that keeps 20 seconds of video
camera = picamera.PiCamera()
camera.resolution=(1280, 720)
stream = picamera.PiCameraCircularIO(camera, seconds=20)
camera.start_recording(stream, format='h264')


#parameters for audio recording
samplerate = 250000 #in Hz
duration = 10 #in seconds


# function for recording video
def save_video():
    logging.basicConfig(filename='NatBatVideo.log', format='%(filename)s [%(lineno)d] %(message)s',
                        level=logging.INFO)
    videofilename = "Video-" + datetime.now().strftime("%d.%m.%Y-%H.%M.%S") +".h264"
    camera.wait_recording(10)
    stream.copy_to(videopath + videofilename, seconds=20) #set number of seconds that need to be copied to video
    start_time = datetime.now() - timedelta(seconds=20)
    start = start_time.strftime('%Y-%m-%d %H-%M-%S')
    end_time = datetime.now()
    end = end_time.strftime('%Y-%m-%d %H-%M-%S')
    logging.info("%s ~ %s (%f) %s" %(start, end,(end_time-start_time).total_seconds(), temp))
    print("Video Recording finished!")
    sleep(2)


# function for recording audio
def record_audio():
    #Use the date and time to name the audio file
    audioname = audiopath +"Audio-" + Time.strftime("%d.%m.%Y-%H.%M.%S") +".wav"
    #record a 10 second audio file
    soundcommand= ['rec', '-c' ,'1', '-r', '250000', audioname, 'trim', '0', '10']
    call(soundcommand)
    
def FindTheTime():
    #get the time so video can be named
    Time = datetime.now()
    return Time

# while loop that uses PIR motion detection
try:
    while True:
        logging.basicConfig(filename='NatBatVideo.log', format='%(filename)s [%(lineno)d] %(message)s',
                        level=logging.INFO)

        pir.wait_for_motion()
        
        print("Motion detected. Started recording a video.")
        Time = FindTheTime()
        Process(target= save_video).start()
        Process(target= record_audio).start() 
        sleep(11)
        print("Video recorded.")
        print("Audio recorded.")
finally:
    camera.stop_recording()

