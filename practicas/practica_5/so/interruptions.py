import log
from hardware import *
from so.pcb import *

## emulates the  Interruptions Handlers
class AbstractInterruptionHandler():
    
    def __init__(self, kernel):
        self._kernel = kernel

    @property
    def kernel(self):
        return self._kernel

    def execute(self, irq):
        log.logger.error("-- EXECUTE MUST BE OVERRIDEN in class {classname}".format(classname=self.__class__.__name__))

class KillInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        
        pcb = self.kernel.pcbTable.runningPCB
        self.kernel.dispatcher.save(pcb)
        pcb.state = TERMINATED
        
        self.kernel.memoryManager.free(pcb.pageTable)
        
        if self.kernel.scheduler.readyQueue:
            pcbToLoad = self.kernel.scheduler.getNext()
            if pcbToLoad.pageTable:
                self.kernel.pcbTable.runningPCB = pcbToLoad
                self.kernel.dispatcher.load(pcbToLoad)
            else:
                pcbToLoad.pageTable = self.kernel.loader.load(pcbToLoad.programPath)
                self.kernel.pcbTable.runningPCB = pcbToLoad
                self.kernel.dispatcher.load(pcbToLoad)
        else:
            self.kernel.pcbTable.runningPCB = None
            
        #if (not self.kernel.scheduler.readyQueue) and (HARDWARE.ioDevice.is_idle) and (HARDWARE.cpu.pc == -1):
        #    log.logger.info(" Program Finished ")
        #    HARDWARE.switchOff()

class IoInInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        
        operation = irq.parameters
        pcb = self.kernel.pcbTable.runningPCB
        self.kernel.dispatcher.save(pcb)
        pcb.setState(WAITING)
        self.kernel.pcbTable.runningPCB = None
        self.kernel.ioDeviceController.runOperation(pcb, operation)
        pcbsToReadyQueue = []
           
        while self.kernel.scheduler.readyQueue:
            pcbToLoad = self.kernel.scheduler.getNext()
            if pcbToLoad.pageTable:
                self.kernel.pcbTable.runningPCB = pcbToLoad
                self.kernel.dispatcher.load(pcbToLoad)
                break
            else:
                pcbToLoad.pageTable = self.kernel.loader.load(pcbToLoad.programPath)
                if pcbToLoad.pageTable:
                    self.kernel.pcbTable.runningPCB = pcbToLoad
                    self.kernel.dispatcher.load(pcbToLoad)
                    break
                else:
                    pcbsToReadyQueue.append(pcbToLoad)

        if pcbsToReadyQueue:
            for p in pcbsToReadyQueue:
                self.kernel.scheduler.addPCB(p)

class IoOutInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        pcbInCPU = self.kernel.pcbTable.runningPCB
        pcbToAdd = self.kernel.ioDeviceController.getFinishedPCB()
        
        if self.kernel.pcbTable.runningPCB:
            if self.kernel.scheduler.mustExpropiate(pcbInCPU, pcbToAdd):
                self.kernel.dispatcher.save(pcbInCPU)
                self.kernel.scheduler.addPCB(pcbInCPU)
                
                self.kernel.dispatcher.load(pcbToAdd)
                self.kernel.pcbTable.runningPCB = pcbToAdd
            else:
                self.kernel.scheduler.addPCB(pcbToAdd)
        else:
            self.kernel.dispatcher.load(pcbToAdd)
            self.kernel.pcbTable.runningPCB = pcbToAdd

class NewInterruptionHandler(AbstractInterruptionHandler):
    
    def execute(self, irq):
        parameters = irq.parameters
        programPath = parameters['programPath']
        priority = parameters['priority']
        pid = self.kernel.pcbTable.getNewPID
        pageTable = self.kernel.loader.load(programPath)
        newPCB = PCB(pid, pageTable, programPath, priority)
        self.kernel.pcbTable.addPCB(newPCB)
        
        if self.kernel.pcbTable.runningPCB or not newPCB.pageTable:
            self.kernel.scheduler.addPCB(newPCB)
        else:
            self.kernel.dispatcher.load(newPCB)
            self.kernel.pcbTable.runningPCB = newPCB
            
class TimeoutInterruptionHandler(AbstractInterruptionHandler):
    
    def execute(self, irq):
        
        if self.kernel.scheduler.readyQueue:
            pcbToAdd = self.kernel.pcbTable.runningPCB
            self.kernel.dispatcher.save(pcbToAdd)
            self.kernel.scheduler.addPCB(pcbToAdd)
            
            pcbsToReadyQueue = []
            
            while self.kernel.scheduler.readyQueue:
                pcbToLoad = self.kernel.scheduler.getNext()
                if pcbToLoad.pageTable:
                    self.kernel.pcbTable.runningPCB = pcbToLoad
                    self.kernel.dispatcher.load(pcbToLoad)
                    break
                else:
                    pcbToLoad.pageTable = self.kernel.loader.load(pcbToLoad.programPath)
                    if pcbToLoad.pageTable:
                        self.kernel.pcbTable.runningPCB = pcbToLoad
                        self.kernel.dispatcher.load(pcbToLoad)
                        break
                    else:
                        pcbsToReadyQueue.append(pcbToLoad)

            if pcbsToReadyQueue:
                for p in pcbsToReadyQueue:
                    self.kernel.scheduler.addPCB(p)
        else:
            HARDWARE.timer.reset()

class StatInterruptionHandler(AbstractInterruptionHandler):

    def __init__(self, kernel):
        super().__init__(kernel)
        HARDWARE.cpu.enable_stats = True
        self._gantt = []
        self._headersGantt = ["ticks"]
        
    def execute(self, irq):
        self._headersGantt.append(HARDWARE.clock.currentTick)
        existingPCB = None
        
        if self.kernel.pcbTable.runningPCB:
            for prg in self._gantt:
                if prg[0] == self.kernel.pcbTable.runningPCB.programPath:
                    existingPCB = self.kernel.pcbTable.runningPCB.programPath
                    prg.append(HARDWARE.clock.currentTick)
                else:
                    prg.append("-")
                    
            if not existingPCB:
                self._gantt.append([self.kernel.pcbTable.runningPCB.programPath])
                ticks = len(self._headersGantt) - 2
                while ticks > 0:
                    self._gantt[-1].append("-")
                    ticks -= 1
                self._gantt[-1].append(HARDWARE.clock.currentTick)
        
        else:
            for prg in self._gantt:
                 prg.append("-")
            
        log.ganttLogger.info(tabulate(self._gantt, headers = self._headersGantt))