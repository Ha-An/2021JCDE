# Neural network-based build time estimation for additive manufacturing 
Oh, Y., Sharp, M., Sprock, T., & Kwon, S. (2021). Neural network-based build time estimation for additive manufacturing: a performance comparison. Journal of Computational Design and Engineering, 8(5), 1243-1256, https://doi.org/10.1093/jcde/qwab044


# (Phase 1) Input generation

**Requirements**
* BLENDER 2.82 & PYTHON 3.7.4 (embeded script)
* Input 3D model files (from BAUMANN DATASET) 
* A metadata file 
  - Build time is calculated by the CURA engine
* Voxelization.exe 

**How to run**

* The code of the following files should be sequentially run in the Python script embedded in Blender 2.82
  - (Step 1) PartNormalization.py
  - (Step 2) PartGeneration.py
  - (Step 3) BuildTimeEstimation(CURA).py
  - (Step 4) STLtoOBJ.py 
  - (Step 5) Voxelization.py 

# (Phase 2) Build time estimation based on neural networks

**Requirements**


**How to run**
