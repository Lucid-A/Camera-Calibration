import cv2
import numpy as np
import glob

path = "./calib_pic"
grid_len = 26.5 # mm
r, c = 5, 8

# Set parameters to find corner point
# MAX_ITER == 30 or MAX_ERROR <= 0.001
criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001)

# Get Coordinates of corner points
objp = np.zeros((r * c, 3), np.float32)
# Set WCS on checkboard, 
# thus all z value is 0 and only x,y are to be assigned
objp[:, :2] = np.mgrid[0:c, 0:r].T.reshape(-1, 2) * grid_len

obj_points = [] # Store 3D Coord
img_points = [] # Store 2D Coord

imgs = glob.glob(f"{path}/*.png")
#print(f"images = {imgs}")

cnt = 0
for i, fname in  enumerate(imgs):
    print(f"{i:02d}/{len(imgs)}", end=' ')
    img = cv2.imread(fname)
    cv2.imshow(fname, img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    size = gray.shape[::-1]
    ret, corners = cv2.findChessboardCorners(gray, (c,r), None)
    print(ret)
    #print(corners)

    if ret:
        obj_points.append(objp)
        
        corners2 = cv2.cornerSubPix(gray, corners, (5,5), (-1,-1), criteria)
        #print(corners2)

        if [corners2]:
            img_points.append(corners2)
        else:
            img_points.append(corners)

        cv2.drawChessboardCorners(img, (c,r), corners, ret)
        cv2.imshow(fname, img)
        cv2.waitKey(1)

while(True):
    key = cv2.waitKey(1)
    if ord('q') == key:
        break

cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, size, None, None)

# Intrinsic Parameters
print("ret: ", ret)
print("Intrinsic Matrix:\n", mtx)
print("Distortion Coefficients:\n", dist)

# Extrinsic Parameters
#print("Rotation Vectors:\n", rvecs)
#print("Translation Vectors:\n", tvecs)

