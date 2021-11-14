import os
import csv
import bpy, bmesh
import time
tic = time.process_time()
   
OBJ_DIR_PATH = "C://Users/jspoh/tmp/Data/OBJ/"   
VOXELIZER = "C://Users/jspoh/tmp/Voxelizer/voxelizer.exe"  

START_FILE_NO = 0
END_FILE_NO = 100

RESOLUTION = 250 # Build space : height, length, and width (mm)
VOXEL_SIZE = 2 # height=length=width (mm)
INNER_VALUE = 1 # 0 <= INNER_VALUE <= 1

# Voxelization and H5 generation   
command = VOXELIZER + " " + OBJ_DIR_PATH + " " + str(END_FILE_NO) + " " + str(RESOLUTION) + " " + str(VOXEL_SIZE) + " " + str(INNER_VALUE)
print(command)
os.system(command)
 
print("Processing time: ", time.process_time() - tic)
