# Advanced-Control-of-the-FASTBLADE-Facility
This folder presents a summary of the work carried out in a final year mechanical engineering thesis exploring advanced control options for the FASTBLADE facility.  Please cite me if you intend to use information stored in this repository.

The work conducted was divided into two streams.

# Research Question 1 (Optimising Test Design)- Can the position and angle of discrete loads be optimised to best represent continuous load distributions whilst maintaining regions of interest (upper and lower bounds)?

# Research Question 2 (Adaptive Control)- Can a machine learning model (MLM) obtained from outputs of FASTBLADE’s Simulink model be used to adapt loading frequencies to maintain a constant amplitude fatigue test as specimen stiffness decays within a flowrate limited system?

Files For Research Question 1:
1) 1D Loading Distribution Optimiser
Optimal spanwise placements of discrete laods are selected to best replicate desired loading distributions.

2) 2D Loading Distribution Optimiser
Optimal spanwise placements and angles of inclined discrete loads are selected to best replicate loading distributions in two dimensions.

Note that the Graphical User Interface was not included in this repository since it cannot be made publicly available at this time

Files For Research Question 2:
1) Exporting_Simulink_Datasets_to_CSVs
This MATLAB file can be used to export a folder of datasets from FASTBLADE's Simulink model to CSVs.

2) Automated Upload of CSVs to Database
This python file automates the upload of a folder of CSV files derived from FASTBLADE's Simulink model outputs into a research database.

3) Signal Analysis to Determine Gains & Lags
This file performs signal analysis on desired and applied load signals stored in the research database created. Lag and Gain values are determined for every data set.

4) Regression Models to Predict Gain
This file creates a series of regression models that predict values of gain for the FASTBLADE system using four inputs.

5) Regression Models to Predict Lag
This file creates a series of regression models that predict values of lag for the FASTBLADE system using four inputs.

6) Adaptive Control for 40% Decay
This file demonstrates a foundation for an adaptive control system for the FASTBLADE facility. A machine learning model is
used to adapt control throttle and loading frequencies to ensuring gain values are maintained and loading criteria 
is met.
