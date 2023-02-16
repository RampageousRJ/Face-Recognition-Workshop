# Import libraries
import cv2
import time

# Class creation for easier bundling and functionalities 
class selfie:

    # Function to initialise capture of frames
    def __init__(self):

        self.cap=cv2.VideoCapture(0)
        self.time_started = False
        self.count=1
        self.detect_face()
        
    # Function to capture photo when S is pressed
    def take_snapshot(self,frame):
        
        self.time_started=True
        print("Press S to save the image")
        ch =  cv2.waitKey(3000)  #3000ms
        
        # Saves images named as numbers globally saved 
        if ch==ord('s'):
            cv2.imwrite(str(self.count)+'.png',frame)
            self.count=self.count+1
            print("saved")

    # Function to read video frame-by-frame and process
    def detect_face(self):

        while True:

            ret,frame=self.cap.read()

            if frame is None:
                print("No frame detected! ")

            else:
                gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                haar_cascade = cv2.CascadeClassifier('haarcascades_cuda/haarcascade_frontalface_alt.xml')
                faces_rect = haar_cascade.detectMultiScale(gray_img, scaleFactor=1.05,minNeighbors=9, minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)
                
                # Code for box around face
                for (x, y, w, h) in faces_rect:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), thickness=2)
                
                if len(faces_rect)>0 and self.time_started == False:
                    prev_time=int(time.time())
                    self.take_snapshot(frame)
                
                curr_time=int(time.time())

                if self.time_started:
                    if(curr_time-prev_time>10):
                        self.time_started=False
                        cv2.destroyAllWindows()
                        prev_time=time.time()
                    
            cv2.imshow("Live feed",frame)
            
            # Press Q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

# Object creation for class selfie
if __name__=='__main__':
    selfie()