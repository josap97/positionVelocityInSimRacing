import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import vCalc
import os
import fastf1

def savePlot(plot, destination):
        plot.xlabel('Time (s)')
        plot.savefig(destination, dpi=300)
        plot.close()

def dataProcessor(sampleRateOfInterest, t, distance, brake, ax, ay, az, px, py, pz, vx, vy, vz, vrap, throttle, file, useVrap=False):
        if not(os.path.exists('output/' + file)):
                os.makedirs('output/' + file)
        # Save data
        tSave = []
        sampleRatesSave = []
        distanceSave = []
        brakeSave = []
        axSave = []
        aySave = []
        azSave = []
        pxSave = []
        pySave = []
        pzSave = []
        vxSave = []
        vySave = []
        vzSave = []
        vrapSave = []
        throttleSave = []
        vmagSave = []
        amagSave = []
        jerkmagSave = []
        snapmagSave = []
        cracklemagSave = []
        popmagSave = []

        # Filtering
        tFilter = []
        distanceFilter = []
        brakeFilter = []
        axFilter = []
        ayFilter = []
        azFilter = []
        pxFilter = []
        pyFilter = []
        pzFilter = []
        vxFilter = []
        vyFilter = []
        vzFilter = []
        vrapFilter = []
        throttleFilter = []


        print("All data loaded in")

        def printData(freq):

                print("Calculating derivatives")

                if not(useVrap):
                        vArr = np.sqrt(np.sum([np.square(np.asarray(vxFilter)), np.square(np.asarray(vyFilter)), np.square(np.asarray(vzFilter))], axis=0))
                        aArr = np.sqrt(np.sum([np.square(np.asarray(axFilter)), np.square(np.asarray(ayFilter)), np.square(np.asarray(azFilter))], axis=0))
                else:
                        vArr = vrapFilter
                        aArr = np.ones(len(vArr))
                vmag, amag, jerkmag, snapmag, cracklemag, popmag = vCalc.calcDerivives(vArr, aArr, tFilter)

                vCalc.printFigures(tFilter, pxFilter, pyFilter, pzFilter, vmag, amag, jerkmag, snapmag, cracklemag, popmag, file, freq)

                print("Derivatives calculated")

                tSave.append(tFilter)
                vmagSave.append(vmag)
                amagSave.append(amag)
                jerkmagSave.append(jerkmag)
                snapmagSave.append(snapmag)
                cracklemagSave.append(cracklemag)
                popmagSave.append(popmag)

                print("Current calculated derivatives saved to array")

        for freq in sampleRateOfInterest:
                print("------------------------------------------\nProcessing " + str(freq) + " Hz sampling")
                outputStr, tFilter, axFilter, ayFilter, azFilter, vxFilter, vyFilter, vzFilter, vrapFilter, px, py, pz = vCalc.filter(freq, sampleRatesSave, t, ax, ay, az, vx, vy, vz, vrap, px, py, pz)
                if(outputStr != "noMatch") and (outputStr != "freqHighExit"):
                        printData(freq)
                elif(outputStr == "freqHighExit"):
                        break

        def calcError(saveArr, outputAbsolute=False):
                print(saveArr)
                aError = []
                for i in range(0, len(sampleRatesSave)):
                        sampleRate = sampleRatesSave[i]
                        totSamples = int(len(t)/sampleRate)
                        aComp = []
                        tComp = []
                        for j in range(0, totSamples):
                                aComp.append(saveArr[-1][j*sampleRate])
                                tComp.append(t[j*sampleRate])
                        aError.append(np.divide(np.sum(np.abs(np.subtract(saveArr[i], aComp))), len(aComp)))
                print(aError)
                relError = np.divide(aError, max(aError))
                if outputAbsolute:
                        return aError
                else:
                        return relError

        print("Creating error figures")
        plt.figure()
        for i in range(0, len(amagSave)):
                plt.plot(tSave[i], amagSave[i])
                plt.title('Acceleration')
                plt.ylabel('Acceleration (ms${}^{-2}$)')
                plt.legend(sampleRateOfInterest[0:len(amagSave)])
        savePlot(plt, 'output/' + file + '/04_accel_comp.png')

        plt.figure()
        for i in range(0, len(jerkmagSave)):
                plt.plot(tSave[i], jerkmagSave[i])
                plt.title('Jerk')
                plt.ylabel('Jerk (ms${}^{-3}$)')
                plt.legend(sampleRateOfInterest[0:len(jerkmagSave)])
        savePlot(plt, 'output/' + file + '/07_jerk_comp.png')

        plt.figure()
        for i in range(0, len(cracklemagSave)):
                plt.plot(tSave[i], cracklemagSave[i])
                plt.title('Crackle')
                plt.ylabel('Crackle (ms${}^{-5}$)')
                plt.legend(sampleRateOfInterest[0:len(cracklemagSave)])
        savePlot(plt, 'output/' + file + '/09_crackle_comp.png')

        plt.figure()
        plt.plot(sampleRateOfInterest[0:len(amagSave)], calcError(amagSave, True))
        plt.xlabel("Sample Rate")
        plt.ylabel("Total Error")
        plt.title("Acceleration Error")
        plt.savefig('output/' + file + '/04_acceleration_error,png', dpi=300)
        plt.close()

        plt.figure()
        plt.plot(sampleRateOfInterest[0:len(amagSave)], calcError(jerkmagSave, True))
        plt.xlabel("Sample Rate")
        plt.ylabel("Total Error")
        plt.title("Jerk Error")
        plt.savefig('output/' + file + '/07_jerk_error,png', dpi=300)
        plt.close()

        plt.figure()
        plt.plot(sampleRateOfInterest[0:len(amagSave)], calcError(snapmagSave, True))
        plt.xlabel("Sample Rate")
        plt.ylabel("Total Error")
        plt.title("Snap Error")
        plt.savefig('output/' + file + '/08_snap_error,png', dpi=300)
        plt.close()

        plt.figure()
        plt.plot(sampleRateOfInterest[0:len(amagSave)], calcError(cracklemagSave, True))
        plt.xlabel("Sample Rate")
        plt.ylabel("Total Error")
        plt.title("Crackle Error")
        plt.savefig('output/' + file + '/09_crackle_error,png', dpi=300)
        plt.close()

        plt.figure()
        plt.plot(sampleRateOfInterest[0:len(amagSave)], calcError(popmagSave, True))
        plt.xlabel("Sample Rate")
        plt.ylabel("Total Error")
        plt.title("Pop Error")
        plt.savefig('output/' + file + '/10_pop_error,png', dpi=300)
        plt.close()

        plt.figure()
        plt.plot(sampleRateOfInterest[0:len(amagSave)], calcError(amagSave))
        plt.plot(sampleRateOfInterest[0:len(amagSave)], calcError(jerkmagSave))
        plt.plot(sampleRateOfInterest[0:len(amagSave)], calcError(snapmagSave))
        plt.plot(sampleRateOfInterest[0:len(amagSave)], calcError(cracklemagSave))
        plt.plot(sampleRateOfInterest[0:len(amagSave)], calcError(popmagSave))
        plt.legend(['Acceleration', 'Jerk', 'Snap', 'Crackle', 'Pop'])
        plt.xlabel("Sample Rate")
        plt.ylabel("Normalised Total Error")
        plt.title("Combined Derivatives Error")
        plt.savefig('output/' + file + '/11_combined_error,png', dpi=300)
        plt.close()

        print("All figures created, exiting")