# ctcalibration
Calibrates the intensity values between two tif sequences, for known z intervals of the same material

## axial_sym
Calibration is performed by assuming samples have axial symmetry. Therefore, different materials are considered only in the z direction

**Inputs**
axial_sym(input_folder1, input_folder2, save, bit32, *interval)

- input_folder1: folder where the reference tif sequence is stored
- input_folder2: folder where the other tif sequence is stored
- save: boolean value:
  - *True*: saves the calibrated tif sequence in a output_folder
  - *False*: does not save anything
- bit32: boolean value. Works only if *save* is set to *True*:
  - *True*: saves the calibrated tif sequence in a 32-bit format
  - *False*: saves the calibrated tif sequence in a 8-bit format
- *interval: z interval to be used for calibration. This is a list expecting 4 elements: [z1_ini, z1_fin, z2_ini, z2_fin]
  - z1_ini: initial z for interval in sequence 1
  - z1_fin: final z for interval in sequence 1
  - z2_ini: initial z for interval in sequence 2
  - z2_fin: final z for interval in sequence 2

  **Outputs*
  It returns a numpy array of the calibrated sequence:
  - 1st dimension: z direction
  - 2nd/3rd dimension: x and y direction

  ## **How to use it**
  **1. Install the following python libraries:**
  - scipy
  - cv2

  **2. Download calibration.py**
  In your working folder download the file *calibration.py*

  **3. Store the 2 input tif sequences in appropriate folders**
  In your working directory create two input folders (i.e. *s1* and *s2*) and store your original tif sequences.

  **4. Code example**
  ```
  >>> import calibration as cal

  >>> data_output = cal.axial_sym('s1', 's2', True, True, [1,100,1,100])

  ```

  For more examples see the file **example.py**
