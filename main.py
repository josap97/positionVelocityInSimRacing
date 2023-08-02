import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

try:
        import scienceplots
        plt.style.use(['science', 'notebook'])
except ModuleNotFoundError:
        print("SciencePlots is not installed, will try to make plots without it.")

fileList = ['spa_rss_gtm_mercer_v8_lapLowRes', 'spa_rss_gtm_mercer_v8_lapHighRes', 'silverstone_RSS_FH121']
sampleRateOfInterest = [0.1,0.25,0.5,1,2,10,20,25,50,100,200,250,500,750,1000]      # You can enter as many sample rates (low to high) as you want but more rates require more memory so pls: think of the poor computer

for file in fileList:
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

        def filter(frequency):
                outputStr = ""
                # Define Filter Array
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
                                        distanceFilter.append(distance[i*sampleRate])
                                        brakeFilter.append(brake[i*sampleRate])
                                        axFilter.append(ax[i*sampleRate])
                                        ayFilter.append(ay[i*sampleRate])
                                        azFilter.append(az[i*sampleRate])
                                        pxFilter.append(px[i*sampleRate])
                                        pyFilter.append(px[i*sampleRate])
                                        pzFilter.append(pz[i*sampleRate])
                                        vxFilter.append(vx[i*sampleRate])
                                        vyFilter.append(vy[i*sampleRate])
                                        vzFilter.append(vz[i*sampleRate])
                                        vrapFilter.append(vrap[i*sampleRate])
                                        throttleFilter.append(throttle[i*sampleRate])
                        else:
                                outputStr = "noMatch"
                else:
                        print("Analyis exited, requested frequency is larger than the reported frequency. Unfortunately, I cannot create data out of nothing...")
                        outputStr = "freqHighExit"
                vrapFilter = np.divide(vrapFilter, 3.6)
                return outputStr, tFilter, distanceFilter, brakeFilter, axFilter, ayFilter, azFilter, pxFilter, pyFilter, pzFilter, vxFilter, vyFilter, vzFilter, vrapFilter, throttleFilter


        print("All data loaded in")

        def savePlot(plot, destination):
                plot.xlabel('Time (s)')
                plot.savefig(destination, dpi=300)
                plot.close()

        def printData(freq):
                currFolder = 'output/' + file + '/f' + str(freq) + '/'
                if not(os.path.exists(currFolder)):
                        os.makedirs(currFolder)
                # Output Arrays
                vmag = []
                amag = []
                jerkmag = []
                snapmag = []
                cracklemag = []
                popmag = []

                plt.figure()
                plt.plot(pxFilter, pyFilter)
                plt.title('GPS')
                savePlot(plt, currFolder + '00_2D_distanceplot.png')
                print("00 GPS figure created")

                plt.figure()
                axes = plt.axes(projection='3d')
                axes.plot3D(pxFilter, pyFilter, pzFilter, 'gray')
                savePlot(plt, currFolder + '01_3D_distanceplot.png')
                print("01 3D GPS Figure created, it may be a bit wonkey")

                print("Calculating derivatives")

                vmag.append(np.sqrt(vxFilter[0]**2 + vyFilter[0]**2 + vzFilter[0]**2))
                amag.append(np.sqrt(axFilter[0]**2 + ayFilter[0]**2 + azFilter[0]**2))
                jerkmag.append(0)
                snapmag.append(0)
                cracklemag.append(0)
                popmag.append(0)
                for i in range(1, len(tFilter)):
                        vmag.append(np.sqrt(vxFilter[i]**2 + vyFilter[i]**2 + vzFilter[i]**2))
                        #amag.append(np.sqrt(axFilter[i]**2 + ayFilter[i]**2 + azFilter[i]**2))
                        amag.append((vmag[-1] - vmag[-2])/(tFilter[i]-tFilter[i-1]))
                        jerkmag.append((amag[-1] - amag[-2])/(tFilter[i]-tFilter[i-1]))
                        snapmag.append((jerkmag[-1] - jerkmag[-2])/(tFilter[i]-tFilter[i-1]))
                        cracklemag.append((snapmag[-1] - snapmag[-2])/(tFilter[i]-tFilter[i-1]))
                        popmag.append((cracklemag[-1] - cracklemag[-2])/(tFilter[i]-tFilter[i-1]))

                print("Derivatives calculated")

                tSave.append(tFilter)
                vmagSave.append(vmag)
                amagSave.append(amag)
                jerkmagSave.append(jerkmag)
                snapmagSave.append(snapmag)
                cracklemagSave.append(cracklemag)
                popmagSave.append(popmag)

                print("Current calculated derivatives saved to array")
                
                plt.figure()
                plt.plot(tFilter, vmag)
                plt.title('Speed')
                plt.ylabel('Speed (ms${}^{-1}$)')
                savePlot(plt, currFolder + '03_speed_plot.png')
                print("03 speed figure created")

                plt.figure()
                plt.plot(tFilter, amag)
                plt.title('Acceleration')
                plt.ylabel('Acceleration (ms${}^{-2}$)')
                savePlot(plt, currFolder + '04_accel_plot.png')
                print("04 acceleration figure created")

                plt.figure()
                plt.plot(tFilter, ayFilter)
                plt.title('Longitudinal Acceleration')
                plt.ylabel('Acceleration (ms${}^{-2}$)')
                savePlot(plt, currFolder + '05_accel_long_plot.png')
                print("05 Longitudinal acceleration figure created")

                plt.figure()
                plt.plot(tFilter, np.multiply(ayFilter,9.81))
                plt.title('Longitudinal G-Forces')
                plt.ylabel('Acceleration (G)')
                savePlot(plt, currFolder + '06_gforce_plot.png')
                print("06 Longitudinal G-Force figure created")

                plt.figure()
                plt.plot(tFilter, jerkmag)
                plt.title('Jerk')
                plt.ylabel('Jerk (ms${}^{-3}$)')
                savePlot(plt, currFolder + '07_jerk_plot.png')
                print("07 jerk figure created")

                plt.figure()
                plt.plot(tFilter, snapmag)
                plt.title('Snap')
                plt.ylabel('Snap (ms${}^{-4}$)')
                savePlot(plt, currFolder + '08_snap_plot.png')
                print("08 Snap figure created")

                plt.figure()
                plt.plot(tFilter, cracklemag)
                plt.title('Crackle')
                plt.ylabel('Crackle (ms${}^{-5}$)')
                savePlot(plt, currFolder + '09_crackle_plot.png')
                print("09 Crackle figure created")

                plt.figure()
                plt.plot(tFilter, popmag)
                plt.title('Pop')
                plt.ylabel('Pop (ms${}^{-6}$)')
                savePlot(plt, currFolder + '10_pop_plot.png')
                print("10 Pop figure created")

                plt.figure()
                plt.plot(tFilter, vmag)
                plt.plot(tFilter, amag)
                plt.plot(tFilter, jerkmag)
                plt.plot(tFilter, snapmag)
                plt.plot(tFilter, cracklemag)
                plt.plot(tFilter, popmag)
                plt.title('$v,a,$ Jerk, Snap, Crackle, Pop')
                plt.ylabel('Derivative')
                savePlot(plt, currFolder + '11_all_plot.png')
                print("11 combined figure created")

        for freq in sampleRateOfInterest:
                print("------------------------------------------\nProcessing " + str(freq) + " Hz sampling")
                outputStr, tFilter, distanceFilter, brakeFilter, axFilter, ayFilter, azFilter, pxFilter, pyFilter, pzFilter, vxFilter, vyFilter, vzFilter, vrapFilter, throttleFilter = filter(freq)
                if(outputStr != "noMatch") and (outputStr != "freqHighExit"):
                        printData(freq)
                elif(outputStr == "freqHighExit"):
                        break

        def calcError(saveArr, outputAbsolute=False):
                aError = []
                for i in range(0, len(sampleRatesSave)):
                        freq = sampleRateOfInterest[i]
                        sampleRate = sampleRatesSave[i]
                        totSamples = int(len(t)/sampleRate)
                        aComp = []
                        tComp = []
                        for j in range(0, totSamples):
                                aComp.append(saveArr[-1][j*sampleRate])
                                tComp.append(t[j*sampleRate])
                        #aSqDiff = np.square(np.subtract(saveArr[i], aComp))
                        #aError.append(np.sqrt(np.divide(np.sum(aSqDiff, axis = 0), len(saveArr[i]))))
                        aError.append(np.divide(np.sum(np.abs(np.subtract(saveArr[i], aComp))), len(aComp)))
                #print(sampleRatesSave)
                #print(aError)
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