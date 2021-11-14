import os
import csv
import time   
tic = time.process_time() 

INPUT_METADATA = "C://Users/jspoh/tmp/Data/ValidatedData/InputParts/metadata_1.csv"   
OUTPUT_METADATA = "C://Users/jspoh/tmp/Data/ValidatedData/InputParts/metadata_2.csv"  
PATH_STL = "C://Users/jspoh/tmp/Data/ValidatedData/InputParts/"
PRUSA_SLICER = "C://Users/jspoh/tmp/Slicer/prusa-slicer-console.exe"
CURA_SLICER = 'C://Users/jspoh/tmp/Slicer/Cura/CuraEngine.exe slice -v '
STL_EXTENSION = ".stl" 
OUTPUT_PATH = "C://Users/jspoh/tmp/Data/Gcode/"  

# Read an input metadata
metadata = []
with open(INPUT_METADATA, newline='') as csvfile:
    spamreader = csv.DictReader(csvfile)
    for row in spamreader: 
        metadata.append({'Id':row['Id'], 
        'OriginalFileName':row['OriginalFileName'], 
        'DimX':row['DimX'], 'DimY':row['DimY'], 'DimZ':row['DimZ'], 
        'ModelVolume':row['ModelVolume'],
        'SupportVolume':row['SupportVolume']}) 
        
## Cura #################################################################################
Cura=[]  
CONFIG_FILE = ' -j C://Users/jspoh/tmp/Slicer/Cura/resources/definitions/ultimaker_original.def.json'
OPTION = ' -s layer_height=0.2 -s support_enable=true -s fill_outline_gaps=True ' 
# Toolpath generation based on PrusaSlicer  
for d in metadata:            
    INPUT = ' -l '+PATH_STL+d["Id"]+'".stl"' 
    OUTPUT = ' -o '+OUTPUT_PATH+d["Id"]+'".gcode"'
    command = CURA_SLICER+CONFIG_FILE+OPTION+OUTPUT+INPUT
    os.system(command)        

## Create a new metadata including build time ====================================================  
BT_FILE_EXTENSION = ".gcode"    
## Read the gcode and find an estimation time 
find_string_PT=";TIME_ELAPSED:"      
with open(OUTPUT_METADATA, mode='w') as csv_file:
    fieldnames = ['Id', 'OriginalFileName', 'DimX', 'DimY', 'DimZ', 'ModelVolume','SupportVolume', 'PrintingTime(Cura)', 'MaterialUsed(Cura)']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for d in metadata:            
        FILE_NAME = d["Id"]   
        path = OUTPUT_PATH+FILE_NAME+BT_FILE_EXTENSION 
        PrintingTime=0 
        try: 
            with open(path) as infile:
                for line in infile: 
                    if find_string_PT in line:      
                        BT_str = line.split(':') 
                        PrintingTime = float(BT_str[1].split('\n')[0]) 
                if PrintingTime != 0:
                    writer.writerow({'Id': d["Id"], 
            'OriginalFileName': d["OriginalFileName"], 
            'DimX': d["DimX"], 'DimY': d["DimY"], 'DimZ': d["DimZ"], 
            'ModelVolume': d["ModelVolume"], 
            'SupportVolume': d["SupportVolume"], 
            'PrintingTime(Cura)': PrintingTime, 
            'MaterialUsed(Cura)': 0}) 
        except:
            print("ERROR:",d["Id"])
 
 
print("Processing time: ", time.process_time() - tic)
