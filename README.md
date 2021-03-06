# Neural network-based build time estimation for additive manufacturing 
Oh, Y., Sharp, M., Sprock, T., & Kwon, S. (2021). Neural network-based build time estimation for additive manufacturing: a performance comparison. Journal of Computational Design and Engineering, 8(5), 1243-1256, https://doi.org/10.1093/jcde/qwab044


# (Phase 1) Input generation

**Requirements**
* BLENDER 2.82 & PYTHON 3.7.4 (embeded script), https://www.blender.org/download/releases/2-82/
* 3D model files (We used Baumann's dataset, https://doi.org/10.3390/data3010005) 
* Voxelization.exe, https://drive.google.com/file/d/15MQk9bI3UP7zcChl9Rj6KzI77ybdFGPQ/view?usp=sharing
  - https://github.com/soonjokwon/VOX4AM
* The CURA engine & a config file for a 3D printer

**How to run**

* The code of the following files should be sequentially run in the Python script embedded in Blender 2.82
  - (Step 1) PartNormalization.py
  - (Step 2) PartGeneration.py
  - (Step 3) BuildTimeCaluculation(CURA).py
  - (Step 4) STLtoOBJ.py 
  - (Step 5) Voxelization.py 

# (Phase 2) Build time estimation based on neural networks

**Requirements** 
* Tensorflow 2.2.0; Python 3.6.9; Keras 2.3.0
* A dataset for metadata (a CSV file)
  - This is generated in Phase 1
* A voxelization dataset (a H5 file) 
  - This is generated in Phase 1

**How to run**

* The code runs on Google Colab, https://colab.research.google.com/drive/1xMy7s4hVNjw2u3koOJSOAFGp-53vvcfC?usp=sharing
  - ANN with RFs
  - CNN with voxels
  - ANN with voxels
