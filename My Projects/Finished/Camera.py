"""
Created on Sun 09 Jun 17:34 2019
Finished on
@author: Cpt.Ender
"""
import cv2

# Creating an object
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not camera.isOpened():
    print("Camera could not open")

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while True:

    check, frame = camera.read()  # check = True/False
    if check:
        cv2.imshow("Video", cv2.flip(frame, 1))
        out.write(frame)

    Key = cv2.waitKey(1)
    if Key == ord('q'):
        print("Camera window closed")
        camera.release()
        break


# Ending program and closing the output file
out.release()
cv2.destroyAllWindows()
