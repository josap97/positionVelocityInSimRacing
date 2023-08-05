import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import proc

def filter(frequency, sampleRatesSave, t, ax, ay, az, vx, vy, vz, vrap, px, py, pz):
        outputStr = ""
        # Define Filter Array
        tFilter = []
        axFilter = []
        ayFilter = []
        azFilter = []
        vxFilter = []
        vyFilter = []
        vzFilter = []
        pxFilter = []
        pyFilter = []
        pzFilter = []
        vrapFilter = []
        for i in range(0,2000):
                if(t[i]>=1):
                        break
        if frequency <= i:
                sampleRate = i/frequency
                if (round(sampleRate) == sampleRate):
                        sampleRate = int(sampleRate)
                        totSamples = int(len(t)/sampleRate)
                        sampleRatesSave.append(sampleRate)
                        for i in range(0, totSamples):
                                tFilter.append(t[i*sampleRate])
                                axFilter.append(ax[i*sampleRate])
                                ayFilter.append(ay[i*sampleRate])
                                azFilter.append(az[i*sampleRate])
                                vxFilter.append(vx[i*sampleRate])
                                vyFilter.append(vy[i*sampleRate])
                                vzFilter.append(vz[i*sampleRate])
                                vrapFilter.append(vrap[i*sampleRate])
                                pxFilter.append(px[i*sampleRate])
                                pyFilter.append(py[i*sampleRate])
                                pzFilter.append(pz[i*sampleRate])
                else:
                        outputStr = "noMatch"
        else:
                print("Analyis exited, requested frequency is larger than the reported frequency. Unfortunately, I cannot create data out of nothing...")
                outputStr = "freqHighExit"
        vrapFilter = np.divide(vrapFilter, 3.6)
        return outputStr, tFilter, axFilter, ayFilter, azFilter, vxFilter, vyFilter, vzFilter, vrapFilter, px, py, pz

def calcDerivives(vel,accel,time):
        vmag = vel
        amag = []
        jerkmag = []
        snapmag = []
        cracklemag = []
        popmag = []

        amag.append(accel[0])
        jerkmag.append(0)
        snapmag.append(0)
        cracklemag.append(0)
        popmag.append(0)
        for i in range(1, len(time)):
                amag.append((vmag[-1] - vmag[-2])/(time[i]-time[i-1]))
                jerkmag.append((amag[-1] - amag[-2])/(time[i]-time[i-1]))
                snapmag.append((jerkmag[-1] - jerkmag[-2])/(time[i]-time[i-1]))
                cracklemag.append((snapmag[-1] - snapmag[-2])/(time[i]-time[i-1]))
                popmag.append((cracklemag[-1] - cracklemag[-2])/(time[i]-time[i-1]))

        return vmag, amag, jerkmag, snapmag, cracklemag, popmag

def printFigures(time, px, py, pz, vmag, amag, jerkmag, snapmag, cracklemag, popmag, file, freq):
        currFolder = 'output/' + file + '/f' + str(freq) + '/'
        if not(os.path.exists(currFolder)):
                os.makedirs(currFolder)

        plt.figure()
        plt.plot(px, py)
        plt.title('GPS')
        proc.savePlot(plt, currFolder + '00_2D_distanceplot.png')
        print("00 GPS figure created")

        plt.figure()
        plt.plot(time, vmag)
        plt.title('Speed')
        plt.ylabel('Speed (ms${}^{-1}$)')
        proc.savePlot(plt, currFolder + '03_speed_plot.png')
        print("03 speed figure created")

        plt.figure()
        plt.plot(time, amag)
        plt.title('Acceleration')
        plt.ylabel('Acceleration (ms${}^{-2}$)')
        proc.savePlot(plt, currFolder + '04_accel_plot.png')
        print("04 acceleration figure created")

        plt.figure()
        plt.plot(time, np.multiply(amag,9.81))
        plt.title('Longitudinal G-Forces')
        plt.ylabel('Acceleration (G)')
        proc.savePlot(plt, currFolder + '06_gforce_plot.png')
        print("06 Longitudinal G-Force figure created")

        plt.figure()
        plt.plot(time, jerkmag)
        plt.title('Jerk')
        plt.ylabel('Jerk (ms${}^{-3}$)')
        proc.savePlot(plt, currFolder + '07_jerk_plot.png')
        print("07 jerk figure created")

        plt.figure()
        plt.plot(time, snapmag)
        plt.title('Snap')
        plt.ylabel('Snap (ms${}^{-4}$)')
        proc.savePlot(plt, currFolder + '08_snap_plot.png')
        print("08 Snap figure created")

        plt.figure()
        plt.plot(time, cracklemag)
        plt.title('Crackle')
        plt.ylabel('Crackle (ms${}^{-5}$)')
        proc.savePlot(plt, currFolder + '09_crackle_plot.png')
        print("09 Crackle figure created")

        plt.figure()
        plt.plot(time, popmag)
        plt.title('Pop')
        plt.ylabel('Pop (ms${}^{-6}$)')
        proc.savePlot(plt, currFolder + '10_pop_plot.png')
        print("10 Pop figure created")

        plt.figure()
        plt.plot(time, vmag)
        plt.plot(time, amag)
        plt.plot(time, jerkmag)
        plt.plot(time, snapmag)
        plt.plot(time, cracklemag)
        plt.plot(time, popmag)
        plt.title('$v,a,$ Jerk, Snap, Crackle, Pop')
        plt.ylabel('Derivative')
        proc.savePlot(plt, currFolder + '11_all_plot.png')
        print("11 combined figure created")