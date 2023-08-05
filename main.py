import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import fastf1
import vCalc
import proc

try:
        import scienceplots
        plt.style.use(['science', 'notebook'])
except ModuleNotFoundError:
        print("SciencePlots is not installed, will try to make plots without it.")

fileList = ['spa_rss_gtm_mercer_v8_lapLowRes', 'spa_rss_gtm_mercer_v8_lapHighRes', 'silverstone_RSS_FH121']
sampleRateOfInterest = [0.1,0.25,0.5,1,2,10,20,25,50,100,200,250,500,750,1000]          # You can enter as many sample rates (low to high) as you want but more rates require more memory so pls: think of the poor computer
useACTITelem = True                                                                     # Boolean, true only runs through ACTI files, false only runs through defined FastF1 data (not working at the moment)


for file in fileList:
        if(useACTITelem):
                print('==========================\nLoading in data for ' + file + '...')
                WS = pd.read_excel('data/' + file + '.xlsx')
                dataArr = np.array(WS)

                # Calculate x, v, a, jerk, etc
                # Plot against time / outing
                # Calculate data with different sample rates to see the evolution etc

                t = dataArr[:,0]
                distance = dataArr[:,1]
                brake = dataArr[:,19]
                ax = dataArr[:,24]
                ay = dataArr[:,25]
                az = dataArr[:,26]
                px = dataArr[:,32]
                py = dataArr[:,33]
                pz = dataArr[:,34]
                vx = dataArr[:,46]
                vy = dataArr[:,47]
                vz = dataArr[:,48]
                vrap = dataArr[:,65]
                throttle = dataArr[:,111]

                proc.dataProcessor(sampleRateOfInterest, t, distance, brake, ax, ay, az, px, py, pz, vx, vy, vz, vrap, throttle, file)
        else:
                session = fastf1.get_session(2019, 'Silverstone', 'Q')

                session.load()
                fast_leclerc = session.laps.pick_driver('HAM').pick_fastest()
                lapData = fast_leclerc.get_car_data()
                tArr = np.divide(np.asarray(lapData['Time']), 1000000000)
                vCar = np.asarray(lapData['Speed'])
                t = []
                for i in tArr:
                        t.append(float(i))
                brake = np.asarray(lapData['Brake'])
                throttle = np.asarray(lapData['Throttle'])
                px = np.ones(len(vCar))  #lapData['X']
                py = np.ones(len(vCar))  #lapData['Y']
                pz = np.ones(len(vCar))  #lapData['Z']

                proc.dataProcessor(sampleRateOfInterest, t, np.ones(len(vCar)), np.ones(len(vCar)), np.ones(len(vCar)), np.ones(len(vCar)), np.ones(len(vCar)), px, py, pz, np.ones(len(vCar)), np.ones(len(vCar)), np.ones(len(vCar)), vCar, throttle, 'HAM_2019_Silverstone')
