from CSMA import *
from time import strftime
#--------------------------------------------------------------------------------------------------------------------
def main():
	#collidedPackets = Monitor(name="Colliding packets",ylab="Percentage of collided packets",tlab="Number of simultaneous calls")
	#plt=SimPlot()
	debugFileName = 'Debug ' + str(strftime("%m-%d-%y %H_%M_%S")) + '.log'
	fsockDebug = open(debugFileName, 'w')
	resultsFileName = 'Results ' + str(strftime("%m-%d-%y %H_%M_%S")) + '.log'
	fsockResults = open(resultsFileName, 'w')
	simulationStartTime = now()
	
	IFSmechanism = "DIFS"
	CWmechanism = "CW"
	TxOPApplied = 0

	backOffWindow = "Variable Backoff Window"
	seedType = "Variable Seed"
	
	numOfSamples   = 1
	maxNumOfCalls  = 40
	simulationTime = 2000.0
	
###	sys.stdout = fsockResults
	#print "Simulation started at ",simulationStartTime
	#print IFSmechanism
	#print backOffWindow
	#print seedType
	
	#for numOfCalls in range(maxNumOfCalls,maxNumOfCalls+1):
	numOfCalls = maxNumOfCalls
	print "Number of Calls is		: ",maxNumOfCalls
	print "Number of Nodes is		: ",G.numOfNodes
	print "Simulation Length		: ", simulationTime
	
	IFSalpha1 = [0.75]
	IFSalpha2 = [0.03]

	CWalpha1 = [0.85]#[0.85,0.85,0.85,0.85]
	CWalpha2 = [0.1]#[0.05,0.10,0.05,0.10]
	CWfactor = [2]#[2,2,3,3]
	
	for alphaCounter in range(0,len(CWalpha1)):
		CollidingPacketsPercentage = []
		DroppedPacketsPercentage = []
		cumPacketsDropped = []
		cumSuccessfulTransmissions = []

		for i in range(0,numOfCalls+1):
			cumPacketsDropped.append(0)
			cumSuccessfulTransmissions.append(0)

		for trialNum in range(1,numOfSamples+1):

			###sys.stdout = fsockDebug
			###sys.stdout = fsockResults
			
			seed = int(strftime("%S"))%5

			initialize()												# required for all simulation programs

			generate = CallsGenerator()
			activate(generate,generate.execute(numOfCalls,seed,IFSalpha1[0],IFSalpha2[0],IFSmechanism,CWalpha1[alphaCounter],CWalpha2[alphaCounter],CWmechanism,CWfactor[alphaCounter],TxOPApplied))
			simulate(until=simulationTime)
			
			simulationDuration = (simulationTime-G.simulationStartTime)
			
			#print "Number of packets generated is	: ", G.numberOfPacketsGenerated[1:]

			#print "Number of packets succ trans is	: ", G.numberOfSuccessfulTransmissions[1:]

			#print "Number of Packets dropped is : ", G.numberOfPacketsDropped[1:]

			#print "Number of Packets colliding is ", G.numberOfPacketsColliding[1:]
			
			CollidingPacketsP = float(sum(G.numberOfPacketsColliding[1:]))/(sum(G.numberOfPacketsColliding[1:])+sum(G.numberOfSuccessfulTransmissions[1:]) - 0.00000001)
			
			#print "Percentage of Colliding Packets is ", CollidingPacketsP
			CollidingPacketsPercentage.append(CollidingPacketsP)

			DroppedPacketsP = float(sum(G.numberOfPacketsDropped[1:]))/(sum(G.numberOfPacketsDropped[1:])+sum(G.numberOfSuccessfulTransmissions[1:]))
			
			#print "QAIFS mean: ", G.QAIFSstatistics.mean()
			
			#if math.sqrt(G.QAIFSstatistics.mean()) > 0.06 : print "QAIFS std: ", math.sqrt(G.QAIFSstatistics.var())
			
			DroppedPacketsPercentage.append(DroppedPacketsP)

			#print "-------------------------------------------------------------------------------------"
			
			cumPacketsDropped += G.numberOfPacketsDropped
			cumSuccessfulTransmissions += G.numberOfSuccessfulTransmissions
			
			for callNum in range(1,numOfCalls+1):

#				print "Percentage of packets lost for call ", callNum , " is : ", (G.numberOfPacketsDropped[callNum])/(G.numberOfSuccessfulTransmissions[callNum]+G.numberOfPacketsDropped[callNum]+0.0)
				
				cumPacketsDropped[callNum] += G.numberOfPacketsDropped[callNum]
				
				cumSuccessfulTransmissions[callNum] += G.numberOfSuccessfulTransmissions[callNum]
			
			#print "-------------------------------------------------------------------------------------"

#			for i in range(len(G.qTime)):
#				print G.qTime[i]
#			for i in range(len(G.qTime)):
#				print G.qTimeTime[i]

			#print "Packet rate (packets/second)	is : ", (sum(G.numberOfPacketsGenerated)*1000)/(simulationDuration*numOfCalls)
			print "Average throughput is		: ", (sum(G.numberOfSuccessfulTransmissions)*(G.payload/G.channelBitRate))/simulationDuration
			
			#print "Mean queue time is		: ", G.qTime.mean()
			
			#print "Average One Way Delay time is	: ", G.oneWayDelay.mean()
			
			#collidedPackets.observe(percentageOfLostPackets,numOfCalls)
			#plt.plotLine(G.oneWayDelay,smooth=True,windowsize=(1000,600))
			#plt.mainloop()

		###print "-------------------------------------------------------------------------------------"
		###print "====================================================================================="
				
		###print "IFSalpha1		: ", IFSalpha1[0]
		###print "IFSalpha2		: ", IFSalpha2[0]
		
		###print "CWalpha1			: ", CWalpha1[alphaCounter]
		###print "CWalpha2			: ", CWalpha2[alphaCounter]
		###print "CWfactor			: ", CWfactor[alphaCounter]
		
		for callNum in range(1,numOfCalls+1):
			allPackets = cumSuccessfulTransmissions[callNum]+cumPacketsDropped[callNum]+0.0
			print "Percentage of packets lost for call ", callNum , " is : ", (cumPacketsDropped[callNum])/allPackets if allPackets > 0 else 0.0
	
		print "Colliding Packets' Percentages :", CollidingPacketsPercentage
		print "Dropped Packets' Percentages :",	DroppedPacketsPercentage
		print "-------------------------------------------------------------------------------------"
		print "====================================================================================="
	
#	plt.plotBars(G.qTime,windowsize=(1000,600))
#	plt.plotScatter(collidedPackets,windowsize=(1000,600))
#	plt.plotLine(G.successTrans,smooth=True,windowsize=(1000,600))
#	plt.plotLine(G.droppedPackets,smooth=True,windowsize=(1000,600))
#	plt.plotLine(G.QAIFSstatistics,smooth=True,windowsize=(1000,600))
#	plt.mainloop()
	
#	print "\nFrequency Averages are:"
#	print "A Talk B Silent is				: %6.4f"%(float(G.state1freq)/G.allStatesFreq)
#	print "Mutual Silence is				: %6.4f"%(float(G.state2freq)/G.allStatesFreq)
#	print "Pause (State3) is				: %6.4f"%(float(G.state3freq)/G.allStatesFreq)
#	print "B Talk A Silent is				: %6.4f"%(float(G.state4freq)/G.allStatesFreq)
#	print "Pause (State5) is				: %6.4f"%(float(G.state5freq)/G.allStatesFreq)
#	print "Double Talk is					: %6.4f"%(float(G.state6freq)/G.allStatesFreq)
	
#	print "\nTime Averages are :"
#	print "A Talk B Silent is				: %6.4f"%(G.state1time/G.totalTimeInAllStates)
#	print "Mutual Silence is				: %6.4f"%(G.state2time/G.totalTimeInAllStates)
#	print "B Talk A Silent is				: %6.4f"%(G.state4time/G.totalTimeInAllStates)
#	print "Pause (State5) is				: %6.4f"%(G.state5time/G.totalTimeInAllStates)
#	print "Double Talk is					: %6.4f"%(G.state6time/G.totalTimeInAllStates)
#--------------------------------------------------------------------------------------------------------------------
	print "Simulation ended at ", now()
	print "Simulation ended in ", now()-simulationStartTime
	PlotNetwork(G.numOfNodes)
main();
