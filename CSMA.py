from SimPy.Simulation import *
from SimPy.SimPlot import *
from random import *
import math
import sys
from Dijkstra import *

class G():

	# Time units are all in mSec
	# DS PHY Characteristics are present in the Standard pg 547
	IFSmechanism = "DIFS"
	CWmechanism = "CW"
	TxOPApplied = 0
	
	numOfNodes = 40												# Mesh Network
	byte = 8.0												# A Byte is a total of 8 bits
	callDurMean = 120000.0									
	queuingThreshold = 200.0								
	callsArrivalRate = 1.0/50.0
	WarmupPeriod = 9000
	ackTimeoutInterval = 0.010
	
	channelBitRate = 5500.0											# 5.5 Mbps or 5500 bits/ms
	PHYhdr = (0.192 + 0.072 + 0.048)*channelBitRate 		
	MAChdr = 34*byte
	IPheader = 20*byte
	UDPheader = 8*byte
	RTPheader = 12*byte
	H = IPheader + UDPheader + RTPheader
	L2header = PHYhdr
	
	# Total packet size = (L2 header: MP or FRF.12 or Ethernet) + (IP/UDP/RTP header) + (voice payload size)
	payload = 160*byte #8184.0						# Voice Payload Size (Bits)
	packetSize =  MAChdr + L2header + H + payload
	dot11ShortRetryLimit = 7.0
	
	DIFS = 0.050
	SIFS = 0.010
	slotTime = 0.020
	delta = 0.00001											# Small Number
	
	ackSize = 14*byte + PHYhdr;								# 112 + 128 bits (30 bytes)
	CWmin = 16.0    # CWmin = 8.0											# Minimum Contention Window size
	CWmax = 128.0    # CWmax = 64.0 											# Maximum Contention Window size
	deltaT = 30 											# Time between two packets transmission 20 ms(Assumed)
	propagationDelay = 0.001								# Propagation delay
	
	AIFS1 = SIFS + 2*slotTime
	AIFS2 = SIFS + 3*slotTime
	AIFS3 = SIFS + 7*slotTime
	
	IFSalpha1 = 0.70
	IFSalpha2 = 0.10
	
	CWalpha1 = 0.70
	CWalpha2 = 0.10
	CWfactor = 2
	
	frequency = 2.4*10**9									# 2.4 GHz
	
	state1freq = 0.0										# Number of times entering state1
	state1time = 0.0										# Amount of time spent in state1
	state2freq = 0.0										# Number of times entering state2
	state2time = 0.0										# Amount of time spent in state2
	state3freq = 0.0										# Number of times entering state3
	state3time = 0.0										# Amount of time spent in state3
	state4freq = 0.0										# Number of times entering state4
	state4time = 0.0										# Amount of time spent in state4
	state5freq = 0.0										# Number of times entering state5
	state5time = 0.0										# Amount of time spent in state5
	state6freq = 0.0										# Number of times entering state6
	state6time = 0.0										# Amount of time spent in state6
	allStatesFreq = 0.0										# Total number of times entering all states
	totalTimeInAllStates = 0.0								# Total amount of time spent in all states
	
	NextState = [[2,3,6],[1,4],[1,2],[2,5,6],[2,4],[1,4]]
	Cum = [[0.2,0.4],[0.5],[0.5],[0.2,0.4],[0.5],[0.5]]
	
	ambientNoise = 2.2019*(10**-014)						# Watt
	transPower = 0.090 										# Watt

	Channel = Resource(numOfNodes)							# Define Channel with a very high capacity
	
	# All the following variables need to be cleared
	startStatsGathering = False
	numOfCalls = 0
	numOfActiveCalls = 0
	simulationStartTime = 0.0
	
	numberOfSuccessfulTransmissions = []
	numberOfPacketsGenerated = []
	numberOfPacketsDropped = []
	numberOfPacketsColliding = []
	
	PassivatedThreads = []
	AssumingChannelFreeList = []
	NodesLocations = []
	Distances = []
	PathLoss = []
	
	TransmissionPower = {}
	QAIFS = {}
	Queues = {}
	NodeTransmitted= {}
	QATxOP = {}
	PacketSoujornTimes = {}
	ONS = {}
	NNS = {}
	
	Queue0 = Resource(1)									# Define Queue
	Queue1 = Resource(1)									# Define Queue
	Queue2 = Resource(1)									# Define Queue
	Queue3 = Resource(1)									# Define Queue
	Queue4 = Resource(1)									# Define Queue
	Queue5 = Resource(1)									# Define Queue
	Queue6 = Resource(1)									# Define Queue
	Queue7 = Resource(1)									# Define Queue
	Queue8 = Resource(1)									# Define Queue
	Queue9 = Resource(1)									# Define Queue
	Queue10 = Resource(1)									# Define Queue
	Queue11 = Resource(1)									# Define Queue
	Queue12 = Resource(1)									# Define Queue
	Queue13 = Resource(1)									# Define Queue
	Queue14 = Resource(1)									# Define Queue
	Queue15 = Resource(1)									# Define Queue
	Queue16 = Resource(1)									# Define Queue
	Queue17 = Resource(1)									# Define Queue
	Queue18 = Resource(1)									# Define Queue
	Queue19 = Resource(1)									# Define Queue
	Queue20 = Resource(1)									# Define Queue
	Queue21 = Resource(1)									# Define Queue
	Queue22 = Resource(1)									# Define Queue
	Queue23 = Resource(1)									# Define Queue
	Queue24 = Resource(1)									# Define Queue
	Queue25 = Resource(1)									# Define Queue
	Queue26 = Resource(1)									# Define Queue
	Queue27 = Resource(1)									# Define Queue
	Queue28 = Resource(1)									# Define Queue
	Queue29 = Resource(1)									# Define Queue
	Queue30 = Resource(1)									# Define Queue
	Queue31 = Resource(1)									# Define Queue
	Queue32 = Resource(1)									# Define Queue
	Queue33 = Resource(1)									# Define Queue
	Queue34 = Resource(1)									# Define Queue
	Queue35 = Resource(1)									# Define Queue
	Queue36 = Resource(1)									# Define Queue
	Queue37 = Resource(1)									# Define Queue
	Queue38 = Resource(1)									# Define Queue
	Queue39 = Resource(1)									# Define Queue
	Queue40 = Resource(1)									# Define Queue
	
	Node0Packets = SimEvent()
	Node1Packets = SimEvent()
	Node2Packets = SimEvent()
	Node3Packets = SimEvent()
	Node4Packets = SimEvent()
	Node5Packets = SimEvent()
	Node6Packets = SimEvent()
	Node7Packets = SimEvent()
	Node8Packets = SimEvent()
	Node9Packets = SimEvent()
	Node10Packets = SimEvent()
	Node11Packets = SimEvent()
	Node12Packets = SimEvent()
	Node13Packets = SimEvent()
	Node14Packets = SimEvent()
	Node15Packets = SimEvent()
	Node16Packets = SimEvent()
	Node17Packets = SimEvent()
	Node18Packets = SimEvent()
	Node19Packets = SimEvent()
	Node20Packets = SimEvent()
	Node21Packets = SimEvent()
	Node22Packets = SimEvent()
	Node23Packets = SimEvent()
	Node24Packets = SimEvent()
	Node25Packets = SimEvent()
	Node26Packets = SimEvent()
	Node27Packets = SimEvent()
	Node28Packets = SimEvent()
	Node29Packets = SimEvent()
	Node30Packets = SimEvent()
	Node31Packets = SimEvent()
	Node32Packets = SimEvent()
	Node33Packets = SimEvent()
	Node34Packets = SimEvent()
	Node35Packets = SimEvent()
	Node36Packets = SimEvent()
	Node37Packets = SimEvent()
	Node38Packets = SimEvent()
	Node39Packets = SimEvent()
	Node40Packets = SimEvent()
	
	NodePackets = {0: Node0Packets ,1: Node1Packets ,2: Node2Packets ,3: Node3Packets ,4: Node4Packets ,5: Node5Packets ,6: Node6Packets ,7: Node7Packets ,8: Node8Packets ,9: Node9Packets, 10: Node10Packets, 11: Node11Packets ,12: Node12Packets ,13: Node13Packets ,14: Node14Packets ,15: Node15Packets ,16: Node16Packets ,17: Node17Packets ,18: Node18Packets ,19: Node19Packets, 20: Node20Packets ,21: Node21Packets ,22: Node22Packets ,23: Node23Packets ,24: Node24Packets ,25: Node25Packets, 26: Node26Packets ,27: Node27Packets ,28: Node28Packets ,29: Node29Packets, 30: Node30Packets, 31: Node31Packets ,32: Node32Packets ,33: Node33Packets ,34: Node34Packets ,35: Node35Packets ,36: Node36Packets ,37: Node37Packets ,38: Node38Packets ,39: Node39Packets, 40: Node40Packets}
	
	SINR_BER_mapping = {5:0.04, 6:0.013, 7:0.0041, 8:0.0013, 9:0.00033, 10:0.00008, 11:0.000015, 12:0.0000027, 13:0.0000005, 14:0.00000005, 15:0.00000001, 16:0.0000000011, 17:0.0000000011}
	qTime = []
	qTimeTime = []
	#QAIFSstatistics = Monitor(name="QAIFS",ylab="QAIFS",tlab="Readings")
	#qTime = Monitor(name="Time packets spent in the queue",ylab="Probability of Delay",tlab="Packet Delay")
	#oneWayDelay = Monitor(name="End-To-End Delay",ylab="One-Way delay (ms)",tlab="Packet Number")
	
	routingTables = {}
	linksMap = []
	dijkstraGraph = Graph()
	dijkstraGraph.nodes = set(range(0, numOfNodes))
#--------------------------------------------------------------------------------------------------------------------
class VoicePacketGenerator(Process):
	# Generates Calls at random according to ITU P59 Voice Model"""
	def __init__(self,srcArg,desArg,callNumArg): # required constructor
		Process.__init__(self) 									# must call parent constructor
		self.callDuration = G.callDurMean						# expovariate(1.0/G.callDurMean)
		self.A = srcArg
		self.B = desArg
		self.callNumber = callNumArg
	def execute(self):
		state = randint(0,6)									# Initial state picked at random
		self.excessA = 0
		self.excessB = 0
		self.callDurationUpTillNow = 0
		
		while(self.callDurationUpTillNow < self.callDuration):
			####state = 6 # CBR VoIP traffic
			if state == 1: # A Talk B Silent
				timeInState= (-.854*math.log(1-uniform(0,1)))*1000
				if ((self.callDurationUpTillNow + timeInState) > self.callDuration):
					timeInState = self.callDuration - self.callDurationUpTillNow
				# Transmit rest of previous burst if there are excess packets
				if self.excessB != 0:
					G.numberOfPacketsGenerated[self.callNumber] += 1
					P = Scheduler(name = "Packet%2.1f"%G.numberOfPacketsGenerated[self.callNumber])
					self.sim.activate(P,P.execute(self.B,self.A,self.excessB,self.callNumber))
					self.excessB = 0
				if self.excessA != 0:
					G.numberOfPacketsGenerated[self.callNumber] += 1
					P = Scheduler(name = "Packet%2.1f"%G.numberOfPacketsGenerated[self.callNumber])
					self.sim.activate(P,P.execute(self.A,self.B,self.excessA,self.callNumber))
				# Generate Packets according to voice burst
				numberOfPackets = int(math.floor((timeInState-self.excessA)/G.deltaT))
				for i in range(numberOfPackets):
					yield hold,self,G.deltaT
					G.numberOfPacketsGenerated[self.callNumber] += 1
					P = Scheduler(name = "Packet%2.1f"%G.numberOfPacketsGenerated[self.callNumber])
					self.sim.activate(P,P.execute(self.A,self.B,self.excessA,self.callNumber))
				if ((timeInState-self.excessA)%G.deltaT != 0):
					self.excessA = G.deltaT - ((timeInState-self.excessA)%G.deltaT)
				else:
					self.excessA = 0
				# Update statistics
				G.state1freq += 1
				G.state1time += timeInState
				G.allStatesFreq += 1
				self.callDurationUpTillNow += timeInState
				G.totalTimeInAllStates += timeInState

			elif state == 2: # Mutual Silence
				timeInState= (-.456*math.log(1-uniform(0,1)))*1000
				if ((self.callDurationUpTillNow + timeInState) > self.callDuration):
					timeInState = self.callDuration - self.callDurationUpTillNow
				# Transmit rest of previous burst if there are excess packets
				if self.excessA != 0:
					G.numberOfPacketsGenerated[self.callNumber] += 1
					P = Scheduler(name = "Packet%2.1f"%G.numberOfPacketsGenerated[self.callNumber])
					self.sim.activate(P,P.execute(self.A,self.B,self.excessA,self.callNumber))
					self.excessA= 0
				if self.excessB != 0:
					G.numberOfPacketsGenerated[self.callNumber] += 1
					P = Scheduler(name = "Packet%2.1f"%G.numberOfPacketsGenerated[self.callNumber])
					self.sim.activate(P,P.execute(self.B,self.A,self.excessB,self.callNumber))
					self.excessB = 0
				# Update statistics
				yield hold,self,timeInState
				G.state2freq += 1
				G.state2time += timeInState
				G.allStatesFreq += 1
				self.callDurationUpTillNow += timeInState
				G.totalTimeInAllStates += timeInState

			elif state == 3: # Pause 1
				timeInState= (-.456*math.log(1-( 0.3551*uniform(0,1))))*1000
				if ((self.callDurationUpTillNow + timeInState) > self.callDuration):
					timeInState = self.callDuration - self.callDurationUpTillNow
				# Transmit rest of previous burst if there are excess packets
				if self.excessA != 0:
					G.numberOfPacketsGenerated[self.callNumber] += 1
					P = Scheduler(name = "Packet%2.1f"%G.numberOfPacketsGenerated[self.callNumber])
					self.sim.activate(P,P.execute(self.A,self.B,self.excessA,self.callNumber)) 
					self.excessA = 0
				yield hold,self,timeInState
				# Update statistics
				G.state3freq += 1
				G.state3time += timeInState
				G.allStatesFreq += 1
				self.callDurationUpTillNow += timeInState
				G.totalTimeInAllStates += timeInState

			elif state == 4: # B Talk A Silent
				timeInState=(-.854*math.log(1-uniform(0,1)))*1000
				if ((self.callDurationUpTillNow + timeInState) > self.callDuration):
					timeInState = self.callDuration - self.callDurationUpTillNow
				# Transmit rest of previous burst if there are excess packets
				if self.excessA != 0:
					G.numberOfPacketsGenerated[self.callNumber] += 1
					P = Scheduler(name = "Packet%2.1f"%G.numberOfPacketsGenerated[self.callNumber])
					self.sim.activate(P,P.execute(self.A,self.B,self.excessA,self.callNumber))
					self.excessA = 0
				if self.excessB != 0:
					G.numberOfPacketsGenerated[self.callNumber] += 1
					P = Scheduler(name = "Packet%2.1f"%G.numberOfPacketsGenerated[self.callNumber])
					self.sim.activate(P,P.execute(self.B,self.A,self.excessB,self.callNumber))
				# Generate Packets according to voice burst
				numberOfPackets = int(math.floor((timeInState-self.excessB)/G.deltaT))
				for i in range(numberOfPackets):
					yield hold,self,G.deltaT
					G.numberOfPacketsGenerated[self.callNumber] += 1
					P = Scheduler(name = "Packet%2.1f"%G.numberOfPacketsGenerated[self.callNumber])
					self.sim.activate(P,P.execute(self.B,self.A,self.excessB,self.callNumber))
				if ((timeInState-self.excessB)%G.deltaT != 0):
					self.excessB = G.deltaT - ((timeInState-self.excessB)%G.deltaT)
				else:
					self.excessB = 0
				# Update statistics
				G.state4freq += 1
				G.state4time += timeInState
				G.allStatesFreq += 1
				self.callDurationUpTillNow += timeInState
				G.totalTimeInAllStates += timeInState

			elif state == 5: # Pause 2
				timeInState= (-.456*math.log(1- (0.3551*uniform(0,1))))*1000
				if ((self.callDurationUpTillNow + timeInState) > self.callDuration):
					timeInState = self.callDuration - self.callDurationUpTillNow
				# Transmit rest of previous burst if there are excess packets
				if self.excessB != 0:
					G.numberOfPacketsGenerated[self.callNumber] += 1
					P = Scheduler(name = "Packet%2.1f"%G.numberOfPacketsGenerated[self.callNumber])
					self.sim.activate(P,P.execute(self.B,self.A,self.excessB,self.callNumber))
					self.excessB = 0
				yield hold,self,timeInState
				# Update statistics
				G.state5freq += 1
				G.state5time += timeInState
				G.allStatesFreq += 1
				self.callDurationUpTillNow += timeInState
				G.totalTimeInAllStates += timeInState

			else: # Double Talk
				timeInState= (-.226*math.log(1-uniform(0,1)))*1000
				if ((self.callDurationUpTillNow + timeInState) > self.callDuration):
					timeInState = self.callDuration - self.callDurationUpTillNow
				# Transmit rest of previous burst if there are excess packets
				if self.excessA != 0:
					G.numberOfPacketsGenerated[self.callNumber] += 1
					P = Scheduler(name = "Packet%2.1f"%G.numberOfPacketsGenerated[self.callNumber])
					self.sim.activate(P,P.execute(self.A,self.B,self.excessA,self.callNumber))
				if self.excessB != 0:
					G.numberOfPacketsGenerated[self.callNumber] += 1
					P = Scheduler(name = "Packet%2.1f"%G.numberOfPacketsGenerated[self.callNumber])
					self.sim.activate(P,P.execute(self.A,self.B,self.excessB,self.callNumber))
					
				# Generate Packets according to voice burst
				numberOfPacketsA = int(math.floor((timeInState-self.excessA)/G.deltaT))
				numberOfPacketsB = int(math.floor((timeInState-self.excessB)/G.deltaT))
				for i in range(min(numberOfPacketsA,numberOfPacketsB)):
					yield hold,self,G.deltaT
					G.numberOfPacketsGenerated[self.callNumber] += 1
					P = Scheduler(name = "Packet%2.1f"%G.numberOfPacketsGenerated[self.callNumber])
					self.sim.activate(P,P.execute(self.A,self.B,self.excessA,self.callNumber))
					G.numberOfPacketsGenerated[self.callNumber] += 1
					P = Scheduler(name = "Packet%2.1f"%G.numberOfPacketsGenerated[self.callNumber])
					self.sim.activate(P,P.execute(self.B,self.A,self.excessB,self.callNumber))
				if (numberOfPacketsA != numberOfPacketsB):
					G.numberOfPacketsGenerated[self.callNumber] += 1
					P = Scheduler(name = "Packet%2.1f"%G.numberOfPacketsGenerated[self.callNumber])
					if (numberOfPacketsA > numberOfPacketsB):	
						self.sim.activate(P,P.execute(self.A,self.B,(self.excessA+G.deltaT),self.callNumber))
					else:
						self.sim.activate(P,P.execute(self.B,self.A,(self.excessB+G.deltaT),self.callNumber))
				if ((timeInState-self.excessA)%G.deltaT != 0):
					self.excessA = G.deltaT - ((timeInState-self.excessA)%G.deltaT)
				else:
					self.excessA = 0
				if ((timeInState-self.excessB)%G.deltaT != 0):
					self.excessB = G.deltaT - ((timeInState-self.excessB)%G.deltaT)
				else:
					self.excessB = 0
				# Update statistics
				G.state6freq += 1
				G.state6time += timeInState
				G.allStatesFreq += 1
				self.callDurationUpTillNow += timeInState
				G.totalTimeInAllStates += timeInState

			# Determine next state
			state = G.NextState[state-1][DetermineNextState(G.Cum[state-1])]
			

		# Stop this call
		del self

#-------------------------------------------------------------------------------------------------------------------- 
class IndependentPacketGenerator(Process):
	def __init__(self,srcArg,desArg,callNumArg):				# required constructor
		Process.__init__(self) 									# must call parent constructor
		self.callDuration = G.callDurMean						# expovariate(1.0/G.callDurMean)
		self.A = srcArg
		self.B = desArg
		self.callNumber = callNumArg
	
	def execute(self):
		while (True):
			#yield hold,self,expovariate(1.0/1)
			yield hold,self,3
			P = Scheduler(name = "Packet%2.1f"%G.numberOfPacketsGenerated[self.callNumber])
			self.sim.activate(P,P.execute(self.A,self.B,0,self.callNumber))
			G.numberOfPacketsGenerated[self.callNumber] += 1
#--------------------------------------------------------------------------------------------------------------------
class Scheduler(Process):
	def __init__(self,name="Packet"):
		Process.__init__(self)
		self.name = name
	
	def execute(self,source,destination,excessDelay,callNum):
		yield hold,self,excessDelay
		self.arrTime = now()
		
		SRC = 0 # STAs shall maintain an SRC for each MSDU awaiting transmission
		if len(G.Queues[source].waitQ) >= 100:
			if (G.startStatsGathering) :
				G.numberOfPacketsDropped[callNum] += 1
			return
		
		yield request,self,G.Queues[source]
		if (G.CWmechanism == "CW"): CW = G.CWmin
		if (G.CWmechanism == "QACW"): CW = ComputeQACW(source,callNum)
		
		self.channelFoundIdleForQAIFS = True

		# Check if Node did not transmit earlier
		if G.NodeTransmitted[source] == 0:
			# Check if channel is idle for QAIFS
			if SenseChannelIdle(source):
				AssumeChannelFree(self,source)
				if (G.IFSmechanism == "DIFS"): yield hold,self,G.DIFS
				if (G.IFSmechanism == "QAIFS"): yield hold,self,G.QAIFS[callNum]
				DiscardChannelFreeAssumption(self,source)
				if (self.interrupted() and (self.interruptLeft != 0)):
					self.channelFoundIdleForQAIFS = False
			else: #Channel is not immediately idle
				self.channelFoundIdleForQAIFS = False

		if ((self.channelFoundIdleForQAIFS) and (G.NodeTransmitted[source] == 0) or (G.QATxOP[source] > 0)):
			#G.qTime.observe(now()-self.arrTime)
			PH = PacketHandler(name = self.name)
			self.sim.activate(PH,PH.execute(source,destination,self.arrTime,CW,SRC,callNum))
		else:
			BOP = BackoffProcedure(name = self.name)
			self.sim.activate(BOP,BOP.execute(source,destination,self.arrTime,CW,SRC,callNum))

		yield waitevent,self,G.NodePackets[source]
		G.NodeTransmitted[source] = 1
		yield release,self,G.Queues[source]
#--------------------------------------------------------------------------------------------------------------------
class BackoffProcedure(Process):
	def __init__(self,name="Packet"):
		Process.__init__(self)
		self.name = name
	
	def execute(self,source,destination,arrTime,CW,SRC,callNum):
		#Wait until Channel is Idle For QAIFS
		while (True):
			if SenseChannelIdle(source):
				AssumeChannelFree(self,source)
				G.QAIFS[callNum] = ComputeQAIFS(source,callNum)
				#G.QAIFSstatistics.observe(G.QAIFS[callNum])
				#print G.QAIFS[callNum]
				if (G.IFSmechanism == "DIFS"): yield hold,self,G.DIFS
				if (G.IFSmechanism == "QAIFS"): yield hold,self,G.QAIFS[callNum]
				DiscardChannelFreeAssumption(self,source)
				if ((self.interrupted() == False) or (self.interruptLeft == 0)): break
				G.PassivatedThreads.append(self)
				yield passivate,self #wait for channel to become idle
				G.PassivatedThreads.remove(self)
			else:
				G.PassivatedThreads.append(self)
				yield passivate,self #wait for channel to become idle
				G.PassivatedThreads.remove(self)
			
		#Choose random Value between (0,CW-1) timeSlots and assign it to the backoff counter
		self.BackoffCounter = (randint(0,round(CW-1)))*G.slotTime
		
		# Hold for BackoffCounter amount of time while channel is Idle
		while (True):
			if SenseChannelIdle(source):
				AssumeChannelFree(self,source)
				yield hold,self,self.BackoffCounter
				DiscardChannelFreeAssumption(self,source)
				if ((self.interrupted() == False) or (self.interruptLeft == 0)): break
				G.PassivatedThreads.append(self)
				yield passivate,self #wait for channel to become idle
				G.PassivatedThreads.remove(self)
				self.BackoffCounter = (math.floor(self.interruptLeft/G.slotTime))*G.slotTime #DCF employs a discrete-time backoff scale
						
				#Freeze counter and wait until Channel is Idle For QAIFS and then continue
				while (True):
					if SenseChannelIdle(source):
						AssumeChannelFree(self,source)
						G.QAIFS[callNum] = ComputeQAIFS(source,callNum)
						#G.QAIFSstatistics.observe(G.QAIFS[callNum])
						#print G.QAIFS[callNum],", ",
						#if len(G.Queues[source].waitQ) != 0:
							#print "CQ: ",ComputeCQ(source,callNum),";Source : ",source,"; QAIFS[",callNum,"] ", G.QAIFS[callNum],";BO : ",self.BackoffCounter,"\n"
							

						if (G.IFSmechanism == "DIFS"): yield hold,self,G.DIFS
						if (G.IFSmechanism == "QAIFS"): yield hold,self,G.QAIFS[callNum]
						DiscardChannelFreeAssumption(self,source)
						if ((self.interrupted() == False) or (self.interruptLeft == 0)): break
					G.PassivatedThreads.append(self)
					yield passivate,self #wait for channel to become idle
					G.PassivatedThreads.remove(self)
			else:
				G.PassivatedThreads.append(self)
				yield passivate,self #wait for channel to become idle 
				G.PassivatedThreads.remove(self)
		PH = PacketHandler(name = self.name)
		self.sim.activate(PH,PH.execute(source,destination,arrTime,CW,SRC,callNum))
#--------------------------------------------------------------------------------------------------------------------
class PacketHandler(Process):
	def __init__(self,name="Packet"):
		Process.__init__(self)
		self.name = name

	def execute(self,source,destination,arrTime,CW,SRC,callNum):
		if G.QATxOP[source] <= 0:
			G.QATxOP[source] = ComputeQATxOP(source, callNum)
		else:
			G.QATxOP[source] -= 1
		# Compute Network Status to be transmitted
		self.NS = ComputeCQ(source,callNum)
		
		#print "Call ",callNum," started transmission from source ",source," to destination ",destination," at ",now()
		# Transmit Packet on channel
		G.qTime.append(now()-arrTime)
		G.qTimeTime.append(now())
		yield request,self,G.Channel
		packetTransmissionTime = G.propagationDelay + G.packetSize/G.channelBitRate

		# Update Transmission  Power
		G.TransmissionPower[source] += G.transPower
		# Impose slotTime delay since it takes a slotTime for any node to detect activity on channel
		yield hold,self,G.slotTime-G.delta
		# Interrupt all packets assuming channel busy
		for victimThread in G.AssumingChannelFreeList:
			self.interrupt(victimThread)
		yield hold,self,0.5*packetTransmissionTime-(G.slotTime-G.delta)
		self.collisionAtDestination = CheckSNR(source,destination)
		yield hold,self,0.5*packetTransmissionTime
		
		
		
		#here is where we should update the dijsktraGraph, get the next best hop and retransmit the packet if
		#the current node is not the final destination. Maybe if this is not the final destination we should
		#not hold for packetTransmissionTime (consider that the full package is not transmitted to intermediate nodes)
		#also how would an intermediate node influence transmission power?
		#also we need to consider what happens in case of collision (if ack is not sent, will the package be resent?)
		
		
		
		yield release,self,G.Channel
		# Update Transmission  Power
		G.TransmissionPower[source] -= G.transPower
			
		# activate all passivated threads
		for victim in G.PassivatedThreads:
			reactivate(victim)
		
		# Check if packet latency time has exceeded threshold
		if ((now()-arrTime) >= G.queuingThreshold):
			self.packetDropped = True
			if (G.startStatsGathering) :
				G.numberOfPacketsDropped[callNum] += 1
			G.NodePackets[source].signal()
			#print now()
			return
		
		# Collect statistics
		if (self.collisionAtDestination == True):
			yield hold,self,G.ackTimeoutInterval
			if (G.startStatsGathering) :
				G.numberOfPacketsColliding[callNum] += 1
			G.QAIFS[callNum] = ComputeQAIFS(source,callNum)
			#G.QAIFSstatistics.observe(G.QAIFS[callNum])
			#print G.QAIFS[callNum]
			
			if (G.IFSmechanism == "DIFS"): yield hold,self,G.DIFS
			if (G.IFSmechanism == "QAIFS"): yield hold,self,G.QAIFS[callNum]
			#print "Collision at ",destination," for call ",callNum," from source ",source,"\n"

			G.QATxOP[source] = 0
			SRC += 1
			if CW < G.CWmax:
				CW *= 2
			if (SRC > G.dot11ShortRetryLimit):
				G.numberOfPacketsDropped[callNum] += 1
				G.NodePackets[source].signal()
			else:
				BOP = BackoffProcedure(name = self.name)
				self.sim.activate(BOP,BOP.execute(source,destination,arrTime,CW,SRC,callNum))
		else:
			# No Collision detected
					
			# Nodes Should Update their Network Status upon successful reception
			for i in range(1,G.numOfActiveCalls+1):
				if (G.NNS[i] > G.ONS[i]):
					G.ONS[i] = G.IFSalpha1*G.NNS[i] + (1-G.IFSalpha1)*G.ONS[i]
				else:
					G.ONS[i] = G.IFSalpha2*G.NNS[i] + (1-G.IFSalpha2)*G.ONS[i]
				G.NNS[i] = self.NS
				if G.NNS[i] == 0: G.NNS[i] = 0.0001
			
			#G.oneWayDelay.observe(now()-arrTime)
			# Wait SIFS amount of time before transmitting Ack
			yield hold,self,G.SIFS
			Ack = SendAck(name = self.name)
			self.sim.activate(Ack,Ack.execute(destination,source,arrTime,CW,SRC,callNum))
#--------------------------------------------------------------------------------------------------------------------
class SendAck(Process):
	def __init__(self,name="Packet"):
		Process.__init__(self)
		self.name = name

	def execute(self,source,destination,arrTime,CW,SRC,callNum):
		# Transmit Packet on channel
		yield request,self,G.Channel
		ackTransmissionTime = G.propagationDelay + G.ackSize/G.channelBitRate

		# Update Transmission Power
		G.TransmissionPower[source] += G.transPower

		# interrupt all packets assuming channel busy
		for victimThread in G.AssumingChannelFreeList:
			self.interrupt(victimThread)
		yield hold,self,ackTransmissionTime
		yield release,self,G.Channel
		
		# Update Transmission Power
		G.TransmissionPower[source] -= G.transPower
			
		# activate all passivated threads
		for victim in G.PassivatedThreads:
			reactivate(victim)
		
		# Collect statistics
		G.numberOfSuccessfulTransmissions[callNum] += 1
		G.NodePackets[destination].signal()
		G.PacketSoujornTimes[callNum].append(now()-arrTime)
#--------------------------------------------------------------------------------------------------------------------
class CallsGenerator(Process):
	def execute(self,numOfCalls,s,IFSalpha1,IFSalpha2,IFSmechanism,CWalpha1,CWalpha2,CWmechanism,CWfactor,TxOPApplied):
		InitializeGlobals()
		G.numOfCalls = numOfCalls
		
		G.IFSalpha1 = IFSalpha1
		G.IFSalpha2 = IFSalpha2
		G.IFSmechanism = IFSmechanism
		
		G.CWalpha1 = CWalpha1
		G.CWalpha2 = CWalpha2
		G.CWmechanism = CWmechanism
		G.CWfactor = CWfactor
		G.TxOPApplied = TxOPApplied
		
		FormulateNetwork(G.numOfNodes)
		
		ComputeDistances(G.numOfNodes)
		#we create the DijkstraGraph with the calculated weights for each edge
		#for now we use the distance (but i guess it should be a function between distance, pathloss and transmission power)
		CreateDijkstraGraph(G.numOfNodes, G.Distances)
		ConstructPathLossList(G.numOfNodes)
		GenerateQueuingSystems()
		GenerateNodesTransmissionStatus(G.numOfNodes)
		GenerateQATxOPStatus(G.numOfNodes)
		InitializeNodeTransmissionPower(G.numOfNodes)
		InitializeStatistics(numOfCalls)
		InitializePacketSoujornTimes(numOfCalls)

		for callNumber in range(1,numOfCalls+1):
			# Pick Source
			seed(s+callNumber)
			src = randint(0,G.numOfNodes-1)
			dst = randint(0,G.numOfNodes-1)
			while dst == src:
				dst = randint(0,G.numOfNodes-1)
			g = VoicePacketGenerator(src,dst,callNumber)		# instantiate a new object of type PacketGenerator
#			g = IndependentPacketGenerator(src,dst,callNumber)	# instantiate a new object of type IndependentPacketGenerator
			activate(g,g.execute())								# mark thread as runnable when first created
			InitializeCallNetworkParams(callNumber)
			G.numOfActiveCalls += 1
			holdingTime = expovariate(G.callsArrivalRate)
			yield hold,self,holdingTime

		# Wait a random amount of time after all calls start and then set Flag to enable stats gathering
		yield hold,self,G.WarmupPeriod
		# Set Flag to enable stats gathering
		G.startStatsGathering = True
		if G.startStatsGathering == True:
			G.simulationStartTime = now()
#--------------------------------------------------------------------------------------------------------------------
class Packet():
	def __init__(self,packetType): # required constructor
		self.type = packetType
#--------------------------------------------------------------------------------------------------------------------
#def InitializeGlobals():
	# Do nothing
#--------------------------------------------------------------------------------------------------------------------
def SenseChannelIdle(node):
# The DSSS PHY shall provide the capability to perform CCA according to at least one of the following three methods:
	# CCA Mode 1: Energy above threshold. CCA shall report a busy medium upon detection of any energy above the ED threshold.
	# CCA Mode 2: CS only. CCA shall report a busy medium only upon detection of a DSSS signal. This signal may be above or below ED threshold.
	# CCA Mode 3: CS with energy above threshold. CCA shall report a busy medium upon detection of a DSSS signal with energy above ED threshold.
	# Page 573 is the rest
	for Node in G.TransmissionPower:
		if G.TransmissionPower[Node] != 0:
			return False
	return True
#--------------------------------------------------------------------------------------------------------------------
def DetermineNextState(args):
	probability = uniform(0,1)
	for index in range(len(args)):
		if probability < args[index]:
			return index
	return len(args)
#--------------------------------------------------------------------------------------------------------------------
def CheckSNR(source,destination):
	# If destination is transmitting then there will be collision
	if G.TransmissionPower[destination] != 0:
		return True
				
	# Compute SINR
	receivedPower = G.TransmissionPower[source]/G.PathLoss[source-1][destination-1]
	interference = 0
	for node in range(G.numOfNodes):
		if (node != source) and (node != destination):
			if G.PathLoss[node-1][destination-1] == 0:
				print (node != source) and (node != destination)
				print "ERROR : Source ", source, " destination : ", destination, " node : ", node
				print (node != destination)
				print G.PathLoss
				print G.NodesLocations
			interference += G.TransmissionPower[node]/G.PathLoss[node-1][destination-1]
	SINR = receivedPower/(G.ambientNoise + interference)
	# Compute BER from SINR_BER curve/table
	SINR_dB = 10*(math.log10(SINR))
	if SINR_dB < 5:
		return True
	if SINR_dB > 17:
		return False
		
	BER = G.SINR_BER_mapping[math.ceil(SINR_dB)]
	# Compute PER assuming bit independence
	PER = 1 - (1-BER)**G.packetSize
	
	# Determine if there is collision
	probability = uniform(0,1)
	if probability < PER:
		return True
	else:
		return False
#--------------------------------------------------------------------------------------------------------------------
def AssumeChannelFree(self,node):
	G.AssumingChannelFreeList.append(self)
#--------------------------------------------------------------------------------------------------------------------
def DiscardChannelFreeAssumption(self,node):
	G.AssumingChannelFreeList.remove(self)
#--------------------------------------------------------------------------------------------------------------------
def ComputePathLoss(distance,frequency=G.frequency):
	c = (2.99792458)*(10**8)
	pi= 22.0/7
	return ((4*pi*distance*frequency)/c)**2
#--------------------------------------------------------------------------------------------------------------------
def FormulateNetwork(numOfNodes,xGridSpan=500,yGridSpan=500):
	for i in range(numOfNodes):
		G.NodesLocations.append((randint(1,xGridSpan),randint(1,yGridSpan)))
		
		
def ComputeDistances(numOfNodes):
	tempList = []
	for column in range(numOfNodes):
		for row in range(numOfNodes):
			if column == row:
				tempList.append(0)
			else:
				tempList.append(math.sqrt((G.NodesLocations[column][0]-G.NodesLocations[row][0])**2 + (G.NodesLocations[column][1]-G.NodesLocations[row][1])**2))
		G.Distances.append(tempList)
		tempList = []


def CreateDijkstraGraph(numOfNodes, edgeWeights):
	#we reset the dijkstraGraph in case the weights have changed
	dijkstraGraph = Graph()
	dijkstraGraph.nodes = set(range(0, numOfNodes))
	
	#we add each edge (between all the nodes) with their corresponding weight to the dijkstraGraph
	for i in range(numOfNodes):
		for j in range(i, numOfNodes):		
			G.dijkstraGraph.add_edge(i, j, edgeWeights[i][j])
	
	#just a test, print the shortest path between node 1 and node 10
	print shortest_path(G.dijkstraGraph, 1, 10)

#--------------------------------------------------------------------------------------------------------------------
def InitializeNodeTransmissionPower(numOfNodes):
	for i in range(numOfNodes):
		G.TransmissionPower[i] = 0
#--------------------------------------------------------------------------------------------------------------------
def ConstructPathLossList(numOfNodes):
	tempList = []
	for x in range(numOfNodes):
		for y in range(numOfNodes):
			tempList.append(ComputePathLoss(G.Distances[x][y]))
		G.PathLoss.append(tempList)
		tempList = []
#--------------------------------------------------------------------------------------------------------------------
def PlotNetwork(numOfNodes):
	tempList = []
	plt=SimPlot()
	plt.root.title("The plot")
	objects = []
	for i in range(numOfNodes):
		tempList.append([G.NodesLocations[i][0],G.NodesLocations[i][1]])
	dots = plt.makeSymbols(tempList,color="green",size=2,marker='circle',windowsize=(1000,600))
	objects.append(dots)
	for i in range(numOfNodes):
		for j in range(i, numOfNodes):	
			src = [G.NodesLocations[i][0],G.NodesLocations[i][1]]
			dst = [G.NodesLocations[j][0],G.NodesLocations[j][1]]
			#objects.append(plt.makeLine([src,dst],splinesteps=20,color="blue",width=2))
	obj=plt.makeGraphObjects(objects)
	frame=Frame(plt.root)                               
	graph=plt.makeGraphBase(frame,1000,600, title="Network")      
	graph.pack()                                        
	graph.draw(obj)                                     
	frame.pack()                                     
	plt.mainloop()
#--------------------------------------------------------------------------------------------------------------------
def GenerateQueuingSystems():
	G.Queues = {0: G.Queue0 ,1: G.Queue1 , 2: G.Queue2 , 3:G.Queue3 , 4:G.Queue4 , 5: G.Queue5 , 6: G.Queue6 , 7:G.Queue7 , 8:G.Queue8 , 9: G.Queue9, 10: G.Queue10, 11: G.Queue11, 12: G.Queue12 , 13:G.Queue13 , 14:G.Queue14 , 15: G.Queue15 , 16: G.Queue16 , 17:G.Queue17 , 18:G.Queue18 , 19: G.Queue19, 20: G.Queue20, 21: G.Queue21 , 22: G.Queue22 , 23:G.Queue23 , 24:G.Queue24 , 25: G.Queue25 , 26: G.Queue26 , 27:G.Queue27 , 28:G.Queue28 , 29: G.Queue29, 30: G.Queue30, 31: G.Queue31, 32: G.Queue32 , 33:G.Queue33 , 34:G.Queue34 , 35: G.Queue35 , 36: G.Queue36 , 37:G.Queue37 , 38:G.Queue38 , 39: G.Queue39, 40: G.Queue40} 
#--------------------------------------------------------------------------------------------------------------------
def GenerateNodesTransmissionStatus(numOfNodes):
	for i in range(numOfNodes):
		G.NodeTransmitted[i] = 0
#--------------------------------------------------------------------------------------------------------------------
def GenerateQATxOPStatus(numOfNodes):
	for i in range(numOfNodes):
		G.QATxOP[i] = 0
#--------------------------------------------------------------------------------------------------------------------
def InitializeStatistics(numOfCalls):
	for i in range(0,numOfCalls+1):
		G.numberOfSuccessfulTransmissions.append(0)
		G.numberOfPacketsGenerated.append(0)
		G.numberOfPacketsDropped.append(0)
		G.numberOfPacketsColliding.append(0)

#--------------------------------------------------------------------------------------------------------------------
def InitializeCallNetworkParams(callNumber):
	G.QAIFS[callNumber] = G.DIFS
	G.ONS[callNumber] = 0.0001 #Very Small Number
	G.NNS[callNumber] = 0.0001 #Very Small Number
#--------------------------------------------------------------------------------------------------------------------
def ComputeQACW(source,callNum):
	alpha1 = 0.75
	alpha2 = 0.25
	G.CWfactor = 2
	CQ = ComputeCQ(source,callNum)
	if (CQ == 0) :
		return G.CWmin
		
	QAF = min(1,((alpha1*CQ)/(alpha2*G.NNS[callNum] + (1-alpha2)*G.ONS[callNum])))

	QACW = G.CWmin + (1-QAF)*(G.CWfactor*G.CWmin-G.CWmin)

	return QACW
#--------------------------------------------------------------------------------------------------------------------
def ComputeQAIFS(source,callNum):
	alpha1 = 0.75
	alpha2 = 0.25
	CQ = ComputeCQ(source,callNum)
	if (CQ == 0) :
		return G.AIFS1
		
	QAF = min(1,((alpha1*CQ)/(alpha2*G.NNS[callNum] + (1-alpha2)*G.ONS[callNum])))

	QAIFS = G.AIFS1 + (1-QAF)*(G.AIFS3-G.AIFS1) - ((G.AIFS1 + (1-QAF)*(G.AIFS3-G.AIFS1))%(G.SIFS))

	return QAIFS
#--------------------------------------------------------------------------------------------------------------------
def ComputeQATxOP(source,callNum):
	alpha1 = 0.75
	alpha2 = 0.25
	TxOPmin = 1
	TxOPmax = 20 # Theoretically 20
	CQ = ComputeCQ(source,callNum)
	if (CQ == 0) :
		return 0
		
	QAF = min(1,((alpha1*CQ)/(alpha2*G.NNS[callNum] + (1-alpha2)*G.ONS[callNum])))

	QATxOP = math.floor(TxOPmin + (QAF)*(TxOPmax-TxOPmin))

	if G.TxOPApplied : return QATxOP
	else: return 0
#--------------------------------------------------------------------------------------------------------------------
def ComputeCQ(source,callNum):
	CQ = 0

	if len(G.PacketSoujornTimes[callNum]) == 0:
		averageSoujornTime = 0
	else:
		averageSoujornTime = sum(G.PacketSoujornTimes[callNum])/len(G.PacketSoujornTimes[callNum])
	
	for i in range(len(G.Queues[source].waitQ)):
		TIQ = now() - G.Queues[source].waitQ[i].arrTime	# Time in Queue	
		CQ += TIQ + (i*averageSoujornTime) # Current Queue Status

	return CQ
#--------------------------------------------------------------------------------------------------------------------
def InitializePacketSoujornTimes(numOfCalls):
	for i in range(1,numOfCalls+1):
		G.PacketSoujornTimes[i] = []
#--------------------------------------------------------------------------------------------------------------------
def InitializeGlobals():
	# All the following variables need to be cleared
	G.startStatsGathering = False
	G.numOfCalls = 0
	G.numOfActiveCalls = 0
	G.simulationStartTime = 0.0
	
	G.numberOfSuccessfulTransmissions = []
	G.numberOfPacketsGenerated = []
	G.numberOfPacketsDropped = []
	G.numberOfPacketsColliding = []
	
	G.PassivatedThreads = []
	G.AssumingChannelFreeList = []
	G.NodesLocations = []
	G.Distances = []
	G.PathLoss = []
	
	G.TransmissionPower.clear()
	G.QAIFS.clear()
	G.Queues.clear()
	G.NodeTransmitted.clear()
	G.PacketSoujornTimes.clear()
	G.ONS.clear()
	G.NNS.clear()
	
	G.Queue0 = Resource(1)									# Define Queue
	G.Queue1 = Resource(1)									# Define Queue
	G.Queue2 = Resource(1)									# Define Queue
	G.Queue3 = Resource(1)									# Define Queue
	G.Queue4 = Resource(1)									# Define Queue
	G.Queue5 = Resource(1)									# Define Queue
	G.Queue6 = Resource(1)									# Define Queue
	G.Queue7 = Resource(1)									# Define Queue
	G.Queue8 = Resource(1)									# Define Queue
	G.Queue9 = Resource(1)									# Define Queue
	G.Queue10 = Resource(1)									# Define Queue
	G.Queue11 = Resource(1)									# Define Queue
	G.Queue12 = Resource(1)									# Define Queue
	G.Queue13 = Resource(1)									# Define Queue
	G.Queue14 = Resource(1)									# Define Queue
	G.Queue15 = Resource(1)									# Define Queue
	G.Queue16 = Resource(1)									# Define Queue
	G.Queue17 = Resource(1)									# Define Queue
	G.Queue18 = Resource(1)									# Define Queue
	G.Queue19 = Resource(1)									# Define Queue
	G.Queue20 = Resource(1)									# Define Queue
	G.Queue21 = Resource(1)									# Define Queue
	G.Queue22 = Resource(1)									# Define Queue
	G.Queue23 = Resource(1)									# Define Queue
	G.Queue24 = Resource(1)									# Define Queue
	G.Queue25 = Resource(1)									# Define Queue
	G.Queue26 = Resource(1)									# Define Queue
	G.Queue27 = Resource(1)									# Define Queue
	G.Queue28 = Resource(1)									# Define Queue
	G.Queue29 = Resource(1)									# Define Queue
	G.Queue30 = Resource(1)									# Define Queue
	G.Queue31 = Resource(1)									# Define Queue
	G.Queue32 = Resource(1)									# Define Queue
	G.Queue33 = Resource(1)									# Define Queue
	G.Queue34 = Resource(1)									# Define Queue
	G.Queue35 = Resource(1)									# Define Queue
	G.Queue36 = Resource(1)									# Define Queue
	G.Queue37 = Resource(1)									# Define Queue
	G.Queue38 = Resource(1)									# Define Queue
	G.Queue39 = Resource(1)									# Define Queue
	G.Queue40 = Resource(1)									# Define Queue
	
	G.Node0Packets = SimEvent()
	G.Node1Packets = SimEvent()
	G.Node2Packets = SimEvent()
	G.Node3Packets = SimEvent()
	G.Node4Packets = SimEvent()
	G.Node5Packets = SimEvent()
	G.Node6Packets = SimEvent()
	G.Node7Packets = SimEvent()
	G.Node8Packets = SimEvent()
	G.Node9Packets = SimEvent()
	G.Node10Packets = SimEvent()
	G.Node11Packets = SimEvent()
	G.Node12Packets = SimEvent()
	G.Node13Packets = SimEvent()
	G.Node14Packets = SimEvent()
	G.Node15Packets = SimEvent()
	G.Node16Packets = SimEvent()
	G.Node17Packets = SimEvent()
	G.Node18Packets = SimEvent()
	G.Node19Packets = SimEvent()
	G.Node20Packets = SimEvent()
	G.Node21Packets = SimEvent()
	G.Node22Packets = SimEvent()
	G.Node23Packets = SimEvent()
	G.Node24Packets = SimEvent()
	G.Node25Packets = SimEvent()
	G.Node26Packets = SimEvent()
	G.Node27Packets = SimEvent()
	G.Node28Packets = SimEvent()
	G.Node29Packets = SimEvent()
	G.Node30Packets = SimEvent()
	G.Node31Packets = SimEvent()
	G.Node32Packets = SimEvent()
	G.Node33Packets = SimEvent()
	G.Node34Packets = SimEvent()
	G.Node35Packets = SimEvent()
	G.Node36Packets = SimEvent()
	G.Node37Packets = SimEvent()
	G.Node38Packets = SimEvent()
	G.Node39Packets = SimEvent()
	G.Node40Packets = SimEvent()
	
	G.NodePackets = {0: G.Node0Packets ,1: G.Node1Packets ,2: G.Node2Packets ,3: G.Node3Packets ,4: G.Node4Packets ,5: G.Node5Packets ,6: G.Node6Packets ,7: G.Node7Packets ,8: G.Node8Packets ,9: G.Node9Packets, 10: G.Node10Packets, 11: G.Node11Packets ,12: G.Node12Packets ,13: G.Node13Packets ,14: G.Node14Packets ,15: G.Node15Packets ,16: G.Node16Packets ,17: G.Node17Packets ,18: G.Node18Packets ,19: G.Node19Packets, 20: G.Node20Packets ,21: G.Node21Packets ,22: G.Node22Packets ,23: G.Node23Packets ,24: G.Node24Packets ,25: G.Node25Packets, 26: G.Node26Packets ,27: G.Node27Packets ,28: G.Node28Packets ,29: G.Node29Packets, 30: G.Node30Packets, 31: G.Node31Packets ,32: G.Node32Packets ,33: G.Node33Packets ,34: G.Node34Packets ,35: G.Node35Packets ,36: G.Node36Packets ,37: G.Node37Packets ,38: G.Node38Packets ,39: G.Node39Packets, 40: G.Node40Packets}
	
	#G.QAIFSstatistics.reset()
	#G.qTime.reset()
	#G.oneWayDelay.reset()
#--------------------------------------------------------------------------------------------------------------------
