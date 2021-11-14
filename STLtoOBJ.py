import os
import csv
import bpy, bmesh
import time
tic = time.process_time()  
## Windows 
STL_DIR_PATH = "C://Users/jspoh/tmp/Data/ValidatedData/InputParts/"   
OBJ_DIR_PATH = "C://Users/jspoh/tmp/Data/OBJ/"    
CSV = STL_DIR_PATH+"metadata_2.csv"   

START_FILE_NO = 0 
END_FILE_NO = 100
  
# Get id and name from a csv file 
STL_name = []
INPUT_COUNT=0
with open(CSV, newline='') as csvFile:
    spamreader = csv.DictReader(csvFile) 
    for row in spamreader: 
        if int(row['Id'])>START_FILE_NO:
            if int(row['Id'])<=END_FILE_NO:
                INPUT_COUNT +=1
                STL_name.append({'Id':row['Id']})   
 
 
# Import STL file  
FILE_COUNT=0              
for f in STL_name:
    print("PartId: ", f['Id']) 
    # export STL to OBJ
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.import_mesh.stl(filepath=STL_DIR_PATH+str(f['Id'])+".stl")      
    obj = bpy.context.selected_objects[0] 
    bpy.ops.export_scene.obj(filepath=OBJ_DIR_PATH+str(f['Id'])+".obj", use_selection=True, axis_forward='-X', axis_up='Z') 
    
    # Remove and import the object
    bpy.data.objects.remove(obj) 
 

print("Processing time: ", time.process_time() - tic)
