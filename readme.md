# Velocity Derivatives from sim racing
This was inspired by the StandUpMaths video on the same subject which can be found here: https://www.youtube.com/watch?v=sB2X5l5CsNs and works on the following basis  
![equation](https://latex.codecogs.com/svg.image?v=\frac{dx}{dt})  
![equation](https://latex.codecogs.com/svg.image?a=\dot{v}=\frac{dv}{dt}=\frac{d^2x}{dt^2})  
![equation](https://latex.codecogs.com/svg.image?\text{jerk}=j=\dot{a}=\frac{d^2v}{dt^2}=\frac{d^3x}{dt^3})  
![equation](https://latex.codecogs.com/svg.image?\text{snap}=s=\dot{j}=\frac{d^3v}{dt^3}=\frac{d^4x}{dt^4})  
![equation](https://latex.codecogs.com/svg.image?\text{crackle}=c=\dot{s}=\frac{d^4v}{dt^4}=\frac{d^5x}{dt^5})  
![equation](https://latex.codecogs.com/svg.image?\text{pop}=p=\dot{c}=\frac{d^5v}{dt^5}=\frac{d^6x}{dt^6})  
In practice, the data is discrete instead of continuous thus writing the derivatives as  
![equation](https://latex.codecogs.com/svg.image?\frac{dv}{dt}=\frac{v_2-v_1}{t_2-t_1}.)  
In Python, this translates to  
```
a = (v[i] - v[i-1])/(t[i] - t[i-1])
```
for an index `i` in a loop running over the range `range(0,len(v))` in which `v` and `t` are arrays containing the velocities and times respectively.

## Requirements
In order to run the this script, please install the following Python libraries:
```
pip install numpy
pip install scipy
pip install pandas
pip install scienceplots
pip install fastf1
```

## Calculations and Data Preparation
### ACTI Data
1. Open Motec to analyse your Assetto Corsa telemetry,
2. select the range you want to analyse,
3. go to file>export and export your data to a `csv` file including both time and distance data
4. open the csv file and delete all rows down to the column headers
5. delete the rows between the header and the first datapoint
6. save as xlsx to the `data` folder
7. add the file name to the `fileList` array in `main.py`
8. run `main.py`

### Formula One Data
The FastF1 library in Python gives you access to all real-life F1 telemetry, including time and velocity data for all laps. This data cannot be used with this script yet but support is planned to be included at some point, preliminary code has been included in the resource but doesn't work yet.