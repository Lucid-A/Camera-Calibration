import cv2

path = "./calib_pic"
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("Cannot open camera!")
    exit()

name = "720P Cam"
cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)

cnt = 0
while(True):
    ret, frame = cam.read()

    if not ret:
        print("Can't receive frame (stream ended?). Exiting...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow(name, frame)
    key = cv2.waitKey(1)
    if ord('q') == key:
        print("Exit by keyboard.")
        break
    elif ord('p') == key:
        pic = f"{cnt}.png"
        ret = cv2.imwrite(f"{path}/{pic}", frame)
        if ret:
            print(f"Picture is saved to \"{path}/{pic}\"")
            cnt = cnt + 1
        else:
            print("Save picture failed!")

cam.release()
cv22.destroyAllWindows()
