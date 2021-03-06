import numpy as np
from keras.models import model_from_json
import operator
import cv2



json_file = open("model-bw.json", "r")
model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(model_json)

loaded_model.load_weights("model-bw.h5")
print("Loaded model from disk")

cap = cv2.VideoCapture(0)

#dictionary
categories = {0: 'ZERO',
              1: 'ONE', 
              2: 'TWO', 
              3: 'THREE', 
              4: 'FOUR', 
              5: 'FIVE', 
              6: 'SIX' ,
              7: 'SEVEN' ,
              8: 'EIGHT' , 
              9: 'NINE'}

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    
    # Coordinates of the ROI
    x1 = int(0.5*frame.shape[1])
    y1 = 10
    x2 = frame.shape[1]-10
    y2 = int(0.5*frame.shape[1])

    cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,255,0) ,2)

    roi = frame[y1:y2, x1:x2]
    

    roi = cv2.resize(roi, (300, 300)) 
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, test_image = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY)
    cv2.imshow("Binary", test_image)
    test_image = cv2.resize(roi, (64, 64)) 

    result = loaded_model.predict(test_image.reshape(1, 64, 64, 1))
    prediction = {'ZERO': result[0][0], 
                  'ONE': result[0][1], 
                  'TWO': result[0][2],
                  'THREE': result[0][3],
                  'FOUR': result[0][4],
                  'FIVE': result[0][5],
                  'SIX': result[0][6],
                  'SEVEN': result[0][7],
                  'EIGHT': result[0][8],
                  'NINE': result[0][9]
                  }

    prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
    

    cv2.putText(frame, prediction[0][0], (x2-170, y2+30), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,0), 2)    
    cv2.imshow("Frame", frame)
    
    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == 27: # esc key
        break
        
 
cap.release()
cv2.destroyAllWindows()
