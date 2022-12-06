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
            top_left = self.db.child(self.root).child(process).child("predictions").child("top_left").get().val()
            top_right = self.db.child(self.root).child(process).child("predictions").child("top_right").get().val()
            bottom_left = self.db.child(self.root).child(process).child("predictions").child("bottom_left").get().val()
            bottom_right = self.db.child(self.root).child(process).child("predictions").child("bottom_right").get().val()
            if top_left != -1 and top_right != -1 and bottom_left != -1 and bottom_right != -1:
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

    def upload4Image(self,currentProcess,tl,tr,bl,br):
        try:
            tl_encode = cv2.imencode('.png', tl)[1]
            tr_encode = cv2.imencode('.png', tr)[1]
            bl_encode = cv2.imencode('.png', bl)[1]
            br_encode = cv2.imencode('.png', br)[1]
            
            tl_encode = tl_encode.tobytes()
            tr_encode = tr_encode.tobytes()
            bl_encode = bl_encode.tobytes()
            br_encode = br_encode.tobytes()
            
            tlURL, trURL, blURL, brURL = self.uploadImagesInProcess(currentProcess,tl_encode,tr_encode,bl_encode,br_encode)
            if tlURL and trURL and blURL and brURL:
                self.saveURLs(currentProcess,tlURL,trURL,blURL,brURL)
                self.initPredictionValues(currentProcess)
                return True
            else:
                return False
        except Exception as e:
            print("Process.py (upload4Image) => ", e)
            return False

    def initPredictionValues(self,process):
        try:
            self.db.child(self.root).child(process).child("predictions").child("top_left").set(-1)
            self.db.child(self.root).child(process).child("predictions").child("top_right").set(-1)
            self.db.child(self.root).child(process).child("predictions").child("bottom_left").set(-1)
            self.db.child(self.root).child(process).child("predictions").child("bottom_right").set(-1)
            return True
        except Exception as e:
            print("Process.py (initPredictionValues) => ", e)
            return False

    def saveURLs(self,process,tlURL,trURL,blURL,brURL):
        try:
            self.db.child(self.root).child(process).child("URLs").child("top_left_URL").set(tlURL)
            self.db.child(self.root).child(process).child("URLs").child("top_right_URL").set(trURL)
            self.db.child(self.root).child(process).child("URLs").child("bottom_left_URL").set(blURL)
            self.db.child(self.root).child(process).child("URLs").child("bottom_right_URL").set(brURL)
            return True
        except Exception as e:
            print("Process.py (saveURLs) => ", e)
            return False

    def uploadImagesInProcess(self,process,tl_encode,tr_encode,bl_encode,br_encode):
        try:
            # Uploading Top Portion of Image
            process = str(process)
            top_filename = "top_left_image"
            self.storage.child("ProcessImages").child(process).child(top_filename).put(tl_encode)
            tlURL = self.storage.child("ProcessImages").child(process).child(top_filename).get_url(None)
            
            # Uploading Bottom Portion of Image
            bottom_filename = "top_right_image"
            self.storage.child("ProcessImages").child(process).child(bottom_filename).put(tr_encode)
            trURL = self.storage.child("ProcessImages").child(process).child(bottom_filename).get_url(None)
            
            # Uploading Left Portion of Image
            left_filename = "bottom_left_image"
            self.storage.child("ProcessImages").child(process).child(left_filename).put(bl_encode)
            blURL = self.storage.child("ProcessImages").child(process).child(left_filename).get_url(None)
            
            # Uploading Right Portion of Image
            right_filename = "bottom_right_image"
            self.storage.child("ProcessImages").child(process).child(right_filename).put(br_encode)
            brURL = self.storage.child("ProcessImages").child(process).child(right_filename).get_url(None)
            return tlURL, trURL, blURL, brURL
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
