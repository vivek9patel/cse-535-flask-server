from helpers.datetime import getCurrentTimeStamp
import base64
import cv2

class Process:
    def __init__(self, firebase):
        self.db = firebase.database()
        self.firebase = firebase
        self.storage = firebase.storage()
        self.root = "process"
    
    def start(self):
        try:
            processCountNode = self.firebase.database().child(self.root).child("process_info").child("currentProcess")
            processStatusNode = self.firebase.database().child(self.root).child("process_info").child("status")
            previousState = processStatusNode.get().val()
            # if previousState == "ideal" or previousState == None:
            if True:
                newProcess = 1
                oldProcess = processCountNode.get().val()
                if oldProcess:
                    newProcess = oldProcess + 1
                self.setProcessNumber(newProcess)
                self.setState("started")
                return newProcess
            else:
                raise Exception("Previous process is not yet completed!")
        except Exception as e:
            print("Process.py (start) => ", e)
            return None
    
    def setPrediction(self,process,portion,prediction):
        try:
            self.db.child(self.root).child(process).child("predictions").child(portion).set(prediction)
            self.checkAllPrediction(process)
            return True
        except Exception as e:
            print("Process.py (setPrediction) => ", e)
            return False
    
    def checkAllPrediction(self,process):
        try:
            top = self.db.child(self.root).child(process).child("predictions").child("top").get().val()
            bottom = self.db.child(self.root).child(process).child("predictions").child("bottom").get().val()
            left = self.db.child(self.root).child(process).child("predictions").child("left").get().val()
            right = self.db.child(self.root).child(process).child("predictions").child("right").get().val()
            if top != -1 and bottom != -1 and left != -1 and right != -1:
                self.setState("photosPredicted")
                return True
            else:
                return False
        except Exception as e:
            print("Process.py (checkAllPrediction) => ", e)
            return False

    def setProcessNumber(self, number):
       self.db.child(self.root).child("process_info").child("currentProcess").set(number)

    def setState(self, state):
        # States of a Process:
        # 1: "ideal" -> Process completed/New process not started
        # 2: "started" -> New Process has been started
        # 3: "photosUploaded" -> 4 portion of image has been uploaded and can be streamed to clientMobile
        # 4: "photosPredicted" -> 4 images has been predicted and prediction has been stored in DB
        # After the last state, the process becomes "ideal" again
        try:
            self.db.child(self.root).child("process_info").child("status").set(state)
            return True
        except Exception as e:
            print("Process.py (setState) => ", e)
            return False

    def upload4Image(self,currentProcess,top,bottom,left,right):
        try:
            top_encode = cv2.imencode('.png', top)[1]
            bottom_encode = cv2.imencode('.png', bottom)[1]
            left_encode = cv2.imencode('.png', left)[1]
            right_encode = cv2.imencode('.png', right)[1]
            
            top_encode = top_encode.tobytes()
            bottom_encode = bottom_encode.tobytes()
            left_encode = left_encode.tobytes()
            right_encode = right_encode.tobytes()
            
            topURL, bottomURL, leftURL, rightURL = self.uploadImagesInProcess(currentProcess,top_encode,bottom_encode,left_encode,right_encode)
            if topURL and bottomURL and leftURL and rightURL:
                self.saveURLs(currentProcess,topURL,bottomURL,leftURL,rightURL)
                self.initPredictionValues(currentProcess)
                return True
            else:
                return False
        except Exception as e:
            print("Process.py (upload4Image) => ", e)
            return False

    def initPredictionValues(self,process):
        try:
            self.db.child(self.root).child(process).child("predictions").child("top").set(-1)
            self.db.child(self.root).child(process).child("predictions").child("bottom").set(-1)
            self.db.child(self.root).child(process).child("predictions").child("left").set(-1)
            self.db.child(self.root).child(process).child("predictions").child("right").set(-1)
            return True
        except Exception as e:
            print("Process.py (initPredictionValues) => ", e)
            return False

    def saveURLs(self,process,topURL,bottomURL,leftURL,rightURL):
        try:
            self.db.child(self.root).child(process).child("URLs").child("topURL").set(topURL)
            self.db.child(self.root).child(process).child("URLs").child("bottomURL").set(bottomURL)
            self.db.child(self.root).child(process).child("URLs").child("leftURL").set(leftURL)
            self.db.child(self.root).child(process).child("URLs").child("rightURL").set(rightURL)
            return True
        except Exception as e:
            print("Process.py (saveURLs) => ", e)
            return False

    def uploadImagesInProcess(self,process,topb64,bottomb64,leftb64,rightb64):
        try:
            # Uploading Top Portion of Image
            process = str(process)
            top_filename = "top_image"
            self.storage.child("ProcessImages").child(process).child(top_filename).put(topb64)
            topURL = self.storage.child("ProcessImages").child(process).child(top_filename).get_url(None)
            
            # Uploading Bottom Portion of Image
            bottom_filename = "bottom_image"
            self.storage.child("ProcessImages").child(process).child(bottom_filename).put(bottomb64)
            bottomURL = self.storage.child("ProcessImages").child(process).child(bottom_filename).get_url(None)
            
            # Uploading Left Portion of Image
            left_filename = "left_image"
            self.storage.child("ProcessImages").child(process).child(left_filename).put(leftb64)
            leftURL = self.storage.child("ProcessImages").child(process).child(left_filename).get_url(None)
            
            # Uploading Right Portion of Image
            right_filename = "right_image"
            self.storage.child("ProcessImages").child(process).child(right_filename).put(rightb64)
            rightURL = self.storage.child("ProcessImages").child(process).child(right_filename).get_url(None)
            return topURL, bottomURL, leftURL, rightURL
        except Exception as e:
            print("Process.py (uploadImagesInProcess) => ", e)
            return None

    def end(self):
        try:
            self.setState("ideal")
            return True
        except Exception as e:
            print("Process.py (start) => ", e)
            return False
