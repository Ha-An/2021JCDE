import bpy, bmesh 
import os, csv, math 
import time  
from scipy.spatial import distance
from math import radians, degrees, cos, inf 
from mathutils import Vector  
 
tic = time.process_time()
  
NUM_OF_GENERATION_FILES = 3000
RESOLUTION = 250 # Build size: height, length, and width (mm) 
NORMALIZATION_SCALING_SIZE= 1 
FILE_SIZE_LIMIT = 10000000  # 10MB 

# BUMANN DATASET  
DATASET_PATH = "C://Users/jspoh/tmp/Data/Baumann/"
DATASET_METADATA = "C://Users/jspoh/tmp/Data/Baumann/metadata/fileName.csv"
EXPORT_PATH = "C://Users/jspoh/tmp/Data/ValidatedData/NormalizedFile/" 

# build platform
buildVolume = bpy.context.scene.objects["BuildVolume"]       

def obj_alignment(obj):
    # Move the center of a geometry to the world origin
    bpy.ops.object.mode_set( mode = 'OBJECT' )
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS') 
    bpy.ops.object.location_clear()
    # Align the model onto the XY plane and z-axis  
    mx = obj.matrix_world
    minz = min((mx @ v.co)[2] for v in obj.data.vertices)
    mx.translation.z -= minz  

# Import file names from a metadata
data_file = []
with open(DATASET_METADATA, newline='') as csvfile:
    spamreader = csv.DictReader(csvfile)
    for row in spamreader: 
        data_file.append({'fileName':row['FilePath']})  

# New file generation
generatedFiles=0
i = 0
metadata=[]
while(generatedFiles<NUM_OF_GENERATION_FILES and i<len(data_file)):
    bpy.ops.object.select_all(action='DESELECT') 
    filePath = DATASET_PATH+data_file[i]["fileName"]
    
    if os.stat(filePath).st_size < FILE_SIZE_LIMIT: # File size check
        fileValidation = True
        # Import a stl file
        bpy.ops.import_mesh.stl(filepath=filePath)  
        print("Imported file name: ", data_file[i]["fileName"])
        obj = bpy.context.selected_objects[0] 
        obj.select_set(True) 
        
        # Scale the size of a geometry
        maxD = max(obj.dimensions)
        for j in range(0, len(obj.dimensions)):
            if obj.dimensions[j] == maxD:
                obj.dimensions[j] = NORMALIZATION_SCALING_SIZE
        for j in range(0, len(obj.scale)):
            if obj.scale[j] != 1.0:
                scaleD = obj.scale[j]
        obj.scale=((scaleD, scaleD, scaleD)) 
        
        # Too thin and long models are excluded
        if maxD >0:
            maxD = max(obj.dimensions)
            minD = min(obj.dimensions)
            if minD/maxD <0.15:
                fileValidation=False 
            
        # Checking a manifold geometry        
        bm = bmesh.new()        
        bm.from_mesh(obj.data)           
        bm.edges.ensure_lookup_table()        
        for e in bm.edges:            
            if e.is_manifold==False:                
                fileValidation=False    
                break 
        if bm.calc_volume() ==0:
            fileValidation=False  
        bm.free()  
        # Generating a new file    
        if fileValidation:              
            # File generation  
            obj_alignment(obj)
            bpy.ops.export_mesh.stl(filepath=EXPORT_PATH+str(generatedFiles+1)+".stl", use_selection=True)  
            bpy.ops.import_mesh.stl(filepath=EXPORT_PATH+str(generatedFiles+1)+".stl") 
            obj1 = bpy.context.selected_objects[0] 
            obj1.select_set(True)  
            d_X, d_Y, d_Z = obj1.dimensions
            # Metadata  
            metadata.append({'Id': generatedFiles+1, 'OriginalFileName': data_file[i]["fileName"], 'DimX': round(d_X, 2), 'DimY': round(d_Y, 2), 'DimZ': round(d_Z, 2)})
            bm.free() 
            bpy.data.objects.remove(obj1) 
            
            print("Generated files: ", generatedFiles, " / file name: ", data_file[i]["fileName"]) 
            generatedFiles += 1
        bpy.data.objects.remove(obj)  
    i += 1 

with open(EXPORT_PATH+"metadata.csv", mode='w') as csv_file:
    # Write the metadata header into a CSV file
    fieldnames = ['Id', 'OriginalFileName','DimX', 'DimY', 'DimZ']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()  
    for i in metadata:
        writer.writerow({'Id': i['Id'], 'OriginalFileName': i['OriginalFileName'], 'DimX': i['DimX'], 'DimY': i['DimY'], 'DimZ': i['DimZ']})

print("Processing time: ", time.process_time() - tic)
