import cv2
import threading
import datetime

class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    
    #frame_width = int(cam.get(3))
    #frame_height = int(cam.get(4))
    #videopath='/home/pi/thermal_testing/'
    #duration = 10 #in seconds. This is not exact.
    #end_time= datetime.datetime.now() + datetime.timedelta(seconds=duration)
    #video_cod = cv2.VideoWriter_fourcc(*'XVID')
    #video_output= cv2.VideoWriter(videopath + 'test1.avi',video_cod,10,(frame_width,frame_height))
    
    if cam.isOpened():
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        #video_output.write(frame)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)

# Create threads as follows
thread1 = camThread("Camera 1", '/dev/video2')
thread2 = camThread("Camera 2", '/dev/video0')

thread1.start()
thread2.start()
print()
print("Active threads", threading.activeCount())
