import heapq
from so.interruptions import *
import log

class AbstractScheduler():
    
    def __init__(self):
        self._readyQueue = []
        
    def addPCB(self, pcb):
        log.logger.error("-- ADDPCB MUST BE OVERRIDEN in class {classname}".format(classname=self.__class__.__name__))
        
    def getNext(self):
        log.logger.error("-- GETNEXT MUST BE OVERRIDEN in class {classname}".format(classname=self.__class__.__name__))
        
    def mustExpropiate(self, pcbInCPU, pcbToAdd):
        log.logger.error("-- MUSTEXPROPIATE MUST BE OVERRIDEN in class {classname}".format(classname=self.__class__.__name__))
    
    @property
    def readyQueue(self):
        return self._readyQueue
    
class FCFSScheduler(AbstractScheduler):
    
    def addPCB(self, pcb):
        self._readyQueue.append(pcb)
        pcb.setState(READY)
        
    def getNext(self):
        return self._readyQueue.pop(0)
    
    def mustExpropiate(self, pcbInCPU, pcbToAdd):
        return False
        
class NoPreemptivePriorityScheduler(AbstractScheduler):

    def addPCB(self, pcb):
        heapq.heappush(self._readyQueue, pcb)
        pcb.setState(READY)
        pcb.currentPriority = pcb.originalPriority

    def getNext(self):
        nextPCB = self._readyQueue.pop(0)
        readyQueueSize = len(self._readyQueue)
        for index in range(0, readyQueueSize):
            self._readyQueue[index].currentPriority = self._readyQueue[index].currentPriority - 1
        return nextPCB
    
    def mustExpropiate(self, pcbInCPU, pcbToAdd):
        return False
            
class PreemptivePriorityScheduler(NoPreemptivePriorityScheduler):
    
    def mustExpropiate(self, pcbInCPU, pcbToAdd):
        return pcbToAdd.currentPriority < pcbInCPU.currentPriority
    
class RoundRobinScheduler(FCFSScheduler):
    
    def __init__(self, quantum):
        super().__init__()
        HARDWARE.timer.quantum = quantum