import cv2
import dlib
import time
import serial
from multiprocessing import Process
import threading
import queue

main_queue = queue.Queue()

####This version tries to improve headnod detections which occured in Mouth_HN2

def detect_mouth_and_headnods():

    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Load the Haar Cascade Classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Load the facial landmark detector
    predictor_path = "./assets/openCV/shape_predictor_68_face_landmarks.dat"
    predictor = dlib.shape_predictor(predictor_path)

    # Define the minimum height of the mouth region relative to the height of the face region
    mouth_height_ratio = 0.01

    # Define the minimum number of consecutive frames needed to detect a head nod
    nod_frames = 3

    # Define the threshold for vertical movement of the face region to be considered a head nod
    nod_threshold = 2 

    # Initialize variables for head nod detection
    nod_count = 0
    last_face_center_y = None

    # Initialize variables for mouth opening time
    mouth_open_start_time = None
    mouth_open = False

    # Initialize serial port to read from
    ser = serial.Serial('COM5', 9600, timeout=1)
    
    while True:

        # Read a frame from the webcam
        ret, frame = cap.read()


        # Check if the frame is read correctly
        if not ret:
            print("Cannot receive frame")
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect the face region in the grayscale frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # Check if a face region is detected
        if len(faces) > 0:
            # Get the largest face region
            largest_face = max(faces, key=lambda x: x[2]*x[3])

            # Extract the region of interest (ROI) corresponding to the face region
            x, y, w, h = largest_face
            face_center_y = y + h // 2
            face_roi = gray[y:y+h, x:x+w]

            # Detect the facial landmarks in the face ROI
            shape = predictor(face_roi, dlib.rectangle(0, 0, w, h))

            # Get the mouth region from the facial landmarks
            mouth_left = shape.part(48).x
            mouth_right = shape.part(54).x
            mouth_top = min(shape.part(60).y, shape.part(61).y, shape.part(62).y, shape.part(63).y, shape.part(64).y)
            mouth_bottom = max(shape.part(65).y, shape.part(66).y, shape.part(67).y)

            # Calculate the height and width of the mouth region relative to the height and width of the face region
            face_height = y + h
            mouth_height = mouth_bottom - mouth_top

            mouth_height_ratio_actual = mouth_height / face_height

            # Draw rectangles around the detected face and mouth regions
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.rectangle(frame, (x + mouth_left, y + mouth_top), (x + mouth_right, y + mouth_bottom), (0, 0, 255), 2)

            # Check if the mouth is open or closed
            if mouth_height_ratio_actual > mouth_height_ratio:
                if not mouth_open:
                    mouth_open_start_time = time.time()
                mouth_open = True
                
            else:
                if mouth_open:
                    mouth_open_duration = time.time() - mouth_open_start_time
                    if mouth_open_duration >= 1:
                        print("Mouth movement")
                        main_queue.put("Mouth movement")
                        #gui.closeTV()
                mouth_open = False

            # Check for head nodding
            if last_face_center_y is not None:
                face_center_y_diff = abs(face_center_y - last_face_center_y)
                if face_center_y_diff > nod_threshold:
                    nod_count += 1
                else:
                    nod_count = 0

                if nod_count == nod_frames:
                    print("Head nod detected")
                    main_queue.put("Head nod detected")
                    #gui.pause_play()
                    nod_count = 0
                    time.sleep(1) # Add a 1 second delay

            last_face_center_y = face_center_y

            s = ser.readline().decode("utf-8")
            if s:
                print(s)
                main_queue.put(s)
                '''
                if (s=="Jaw Clench Detected"):
                    gui.volumeUp()
                elif (s=="Neck Flex Detected"):
                    gui.volumeDown()
                '''


        # Display the frame
        #cv2.imshow("Webcam", frame)

        # Check for user input to quit the program
        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    # Release the webcam and destroy the windows
    cap.release()
    cv2.destroyAllWindows()

'''
if __name__ == '__main__':
    print("Running process_face_inputs.py")
    detect_mouth_and_headnods()
    gui.window.mainloop()

    #guiProcess = Process(target=gui.window.mainloop)
    #openCVProcess = Process(target=detect_mouth_and_headnods)

    #openCVProcess.start()
    #guiProcess.start()
'''