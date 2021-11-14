import bpy, bmesh 
import os, csv, math 
import time  
from scipy.spatial import distance
from math import radians, degrees, cos, inf 
from mathutils import Vector  
from random import *  
 
tic = time.process_time()
  
NUM_OF_GENERATION_FILES = 100
RESOLUTION = 250 # Build size: height, length, and width (mm)  
FILE_SIZE_LIMIT = 10000000  # 10MB
THRESHOLD_OVERHANG = 45 
 
EXPORT_PATH = "C://Users/jspoh/tmp/Data/ValidatedData/InputParts/"  
DATASET_PATH = "C://Users/jspoh/tmp/Data/ValidatedData/NormalizedFile/"
DATASET_METADATA = DATASET_PATH+"metadata.csv"
''' 
EXPORT_PATH = "C://Users/jspoh/tmp/Data/test/" 
DATASET_PATH = "C:/Users/jspoh/Google Drive/03.Research/8.Journal/2020 BT_Eetimation/Data/Experiment/Case1/"
DATASET_METADATA = "C:/Users/jspoh/Google Drive/03.Research/8.Journal/2020 BT_Eetimation/Data/Experiment/metadata.csv"
'''
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
def updated_dim(obj):
    mx = obj.matrix_world
    minx = min((mx @ v.co)[0] for v in obj.data.vertices)
    maxx = max((mx @ v.co)[0] for v in obj.data.vertices)
    miny = min((mx @ v.co)[1] for v in obj.data.vertices)
    maxy = max((mx @ v.co)[1] for v in obj.data.vertices)
    minz = min((mx @ v.co)[2] for v in obj.data.vertices)
    maxz = max((mx @ v.co)[2] for v in obj.data.vertices)
    d_X = maxx - minx
    d_Y = maxy - miny
    d_Z = maxz - minz 
    return d_X, d_Y, d_Z
# Calculating support volume
def support_volume(part):  
    # Calculate overhang area
    buildOrientationNormal = Vector((0.0, 0.0, 1.0))
    bmPart = bmesh.new()
    bmPart.from_mesh(part.data) 
    supportVolume =0 
    bmPart.faces.ensure_lookup_table()   
    for f in bmPart.faces:   
        global_f_normal = f.normal
        if global_f_normal != Vector((0.0, 0.0, 0.0)):
            theta = global_f_normal.angle(-buildOrientationNormal)    
            if 0 < theta and theta < radians(THRESHOLD_OVERHANG): 
                c = f.calc_center_median() 
                ray_begin_local = part.matrix_world.inverted() @ c 
                direction_local = part.matrix_world.inverted() @ -buildOrientationNormal
                hit_data = part.ray_cast(ray_begin_local, direction_local)      
                if hit_data[0]:    
                    sDistance = distance.euclidean(ray_begin_local, hit_data[1])   
                    supportVolume += sDistance * f.calc_area()  
                else:  
                    ray_begin_local = buildVolume.matrix_world.inverted() @ c  
                    direction_local = buildVolume.matrix_world.inverted() @ -buildOrientationNormal
                    hit_data = buildVolume.ray_cast(ray_begin_local, direction_local)  
                    if hit_data[0]:    
                        sDistance = distance.euclidean(ray_begin_local, hit_data[1])   
                        supportVolume += sDistance * f.calc_area()    
                '''        
                # Leave non-allowable faces as objects for validation
                mesh = bpy.data.meshes.new("m")  # add the new mesh
                obj_f = bpy.data.objects.new(mesh.name, mesh)
                bpy.context.collection.objects.link(obj_f)
                bpy.context.view_layer.objects.active = obj_f
                verts = [] 
                faces = [[]]  
                mat = part.matrix_world   
                for i in range(0, len(f.verts)): 
                    verts.append(mat @ f.verts[i].co)
                    faces[0].append(i)
                edges = []
                mesh.from_pydata(verts, [], faces)  
                '''        
    bmPart.free()  
    return supportVolume
 
# Import file names from a metadata
data_file = []
with open(DATASET_METADATA, newline='') as csvfile:
    spamreader = csv.DictReader(csvfile)
    for row in spamreader: 
        data_file.append({'Id': row['Id'], 'OriginalFileName': row['OriginalFileName']})  

# New file generation
generatedFiles=0
i = 0
metadata=[]
while(generatedFiles<NUM_OF_GENERATION_FILES and i<len(data_file)):
    bpy.ops.object.select_all(action='DESELECT') 
    filePath = DATASET_PATH+data_file[i]["Id"]+".stl" 
    if os.stat(filePath).st_size < FILE_SIZE_LIMIT: # File size check
        # Import a stl file
        bpy.ops.import_mesh.stl(filepath=filePath)  
        print("Imported file name: ", data_file[i]["Id"]) 
        obj = bpy.context.selected_objects[0] 
        obj.select_set(True) 
        
        bpy.ops.object.mode_set( mode = 'OBJECT' )
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS') 
        bpy.ops.object.location_clear() 
         
        # Scaling the size of a geometry
        scaleD = uniform(30,90) 
        obj.scale=((scaleD, scaleD, scaleD))  
        '''     
        # Randomly change the orientation of a model 
        c=0
        v=False
        while v==False and c<30:     
            obj.rotation_euler = (0,0,0) 
            rotateX = round(uniform(-90,90), 2)
            rotateY = round(uniform(-90,90), 2)  
            obj.rotation_euler = (math.radians(rotateX),math.radians(rotateY),0)    
            d_X, d_Y, d_Z = updated_dim(obj)       
            if max(d_X, d_Y, d_Z) < RESOLUTION:
                v=True
                break
            c+=1
        '''    
        obj_alignment(obj) 
        exportPath = EXPORT_PATH+data_file[i]["Id"]+".stl" 
        bpy.ops.export_mesh.stl(filepath=exportPath, use_selection=True) 
        bpy.data.objects.remove(obj) 
        bpy.ops.import_mesh.stl(filepath=exportPath)  
        obj = bpy.context.selected_objects[0] 
        obj.select_set(True)   
        
        fileValidation = True    
        if max(obj.dimensions) > RESOLUTION:
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
            obj_alignment(obj) 
            # Metadata  
            d_X, d_Y, d_Z = obj.dimensions
            bm = bmesh.new()   
            bm.from_mesh(obj.data) 
            sv = support_volume(obj)
            metadata.append({'Id': data_file[i]["Id"], 'OriginalFileName': data_file[i]["OriginalFileName"], 'DimX': round(d_X, 2), 'DimY': round(d_Y, 2), 'DimZ': round(d_Z, 2), 'ModelVolume': round(bm.calc_volume(), 2), 'SupportVolume': round(sv, 2)})
            bm.free()  
            
            print("Generated files: ", generatedFiles, " / file name: ", data_file[i]["Id"]) 
            generatedFiles += 1
        else:
            os.remove(exportPath)
        bpy.data.objects.remove(obj) 
          
    i += 1 

with open(EXPORT_PATH+"metadata_1.csv", mode='w') as csv_file:
    # Write the metadata header into a CSV file
    fieldnames = ['Id', 'OriginalFileName','DimX', 'DimY', 'DimZ', 'ModelVolume','SupportVolume']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()  
    for i in metadata:
        writer.writerow({'Id': i['Id'], 'OriginalFileName': i['OriginalFileName'], 'DimX': i['DimX'], 'DimY': i['DimY'], 'DimZ': i['DimZ'], 'ModelVolume': i['ModelVolume'], 'SupportVolume': i['SupportVolume']})
 
print("Processing time: ", time.process_time() - tic)

