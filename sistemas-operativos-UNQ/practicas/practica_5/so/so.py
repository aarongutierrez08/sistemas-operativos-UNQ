#!/usr/bin/env python

from log import *
from hardware import *
from so.schedulers import *
from so.interruptions import *

## emulates an Input/Output device controller (driver)
class IoDeviceController():

    def __init__(self, device):
        self._device = device
        self._waiting_queue = []
        self._currentPCB = None
    
    @property
    def waiting_queue(self):
        return self._waiting_queue

    def runOperation(self, pcb, instruction):
        pair = {'pcb': pcb, 'instruction': instruction}
        # append: adds the element at the end of the queue
        self._waiting_queue.append(pair)
        # try to send the instruction to hardware's device (if is idle)
        self.__load_from_waiting_queue_if_apply()

    def getFinishedPCB(self):
        finishedPCB = self._currentPCB
        self._currentPCB = None
        self.__load_from_waiting_queue_if_apply()
        return finishedPCB

    def __load_from_waiting_queue_if_apply(self):
        if (len(self._waiting_queue) > 0) and self._device.is_idle:
            ## pop(): extracts (deletes and return) the first element in queue
            pair = self._waiting_queue.pop(0)
            pcb = pair['pcb']
            instruction = pair['instruction']
            self._currentPCB = pcb
            self._device.execute(instruction)


    def __repr__(self):
        return "IoDeviceController for {deviceID} running: {currentPCB} waiting: {waiting_queue}".format(deviceID=self._device.deviceId, currentPCB=self._currentPCB, waiting_queue=self._waiting_queue)

class Loader():
    
    def __init__(self, fileSystem, memoryManager):
        self._memoryDir = 0
        self._fileSystem = fileSystem
        self._memoryManager = memoryManager
        
    @property
    def memoryDir(self):
        return self._memoryDir
        
    def load(self, path):
        # loads the program in main memory
        frameSize = HARDWARE.mmu.frameSize
        prg = self._fileSystem.read(path)
        prgSize = len(prg.instructions)
        requiredFrames = prgSize // frameSize
        if prgSize % frameSize:
            requiredFrames = requiredFrames + 1
        # alloc() 
        # si hay la cantidad requerida de frames disponibles los retorna
        # sino retorna una lista vacias
        allocFrames = self._memoryManager.alloc(requiredFrames)

        if allocFrames:
            for i in range(0, prgSize):
                inst = prg.instructions[i]
                self._memoryDir = (allocFrames[i // frameSize] * frameSize) + i % frameSize
                HARDWARE.memory.write(self._memoryDir, inst)
            log.logger.info(HARDWARE)
            
        return allocFrames           

class Dispatcher():
    
    def load(self, pcb):
        log.logger.info("\n Executing program: {name}".format(name=pcb.programPath))
        HARDWARE.cpu.pc = pcb.pc
        HARDWARE.mmu.resetTLB()
        prgSize = len(pcb.pageTable)
        for index in range(0, prgSize):
            HARDWARE.mmu.setPageFrame(index, pcb.pageTable[index])
        HARDWARE.timer.reset()
    
    def save(self, pcb):
        pcb.pc = HARDWARE.cpu.pc
        HARDWARE.cpu.pc = -1
        
class MemoryManager():
    
    def __init__(self, freeFrames = []):
        
        self._freeFrames = freeFrames
        
        freeFramesAmount = HARDWARE.memory.size // HARDWARE.mmu.frameSize
        
        if not self._freeFrames:
            self._freeFrames = list(range(freeFramesAmount))
    
    def alloc(self, amount):
        frames = self._freeFrames[:amount]
        if len(frames) == amount:
            del self._freeFrames[:amount]
        else:
            frames = []
        return frames
    
    def free(self, frames):
        self._freeFrames.extend(frames)
    
    @property
    def freeFrames(self):
        return self._freeFrames

class FileSystem():
    
    def __init__(self):
        self._fileSystem = dict()
    
    def write(self, path, prg):
        self._fileSystem[path] = prg
    
    def read(self, path):
        return self._fileSystem[path]

# emulates the core of an Operative System
class Kernel():

    def __init__(self, scheduler):
        
        HARDWARE.mmu.frameSize = 4
        
        ## setup interruption handlers
        killHandler = KillInterruptionHandler(self)
        HARDWARE.interruptVector.register(KILL_INTERRUPTION_TYPE, killHandler)

        ioInHandler = IoInInterruptionHandler(self)
        HARDWARE.interruptVector.register(IO_IN_INTERRUPTION_TYPE, ioInHandler)

        ioOutHandler = IoOutInterruptionHandler(self)
        HARDWARE.interruptVector.register(IO_OUT_INTERRUPTION_TYPE, ioOutHandler)
        
        newHandler = NewInterruptionHandler(self)
        HARDWARE.interruptVector.register(NEW_INTERRUPTION_TYPE, newHandler)
        
        timeoutHandler = TimeoutInterruptionHandler(self)
        HARDWARE.interruptVector.register(TIMEOUT_INTERRUPTION_TYPE, timeoutHandler)
        
        statHandler = StatInterruptionHandler(self)
        HARDWARE.interruptVector.register(STAT_INTERRUPTION_TYPE, statHandler)

        ## controls the Hardware's I/O Device
        self._ioDeviceController = IoDeviceController(HARDWARE.ioDevice)

        self._fileSystem = FileSystem()
        #self._memoryManager = MemoryManager([8, 5, 3, 4, 0, 1, 6, 7, 9, 2])
        self._memoryManager = MemoryManager()
        self._loader = Loader(self._fileSystem, self._memoryManager)
        self._dispatcher = Dispatcher()
        self._pcbTable = PCBTable()
        self._scheduler = scheduler

    @property
    def ioDeviceController(self):
        return self._ioDeviceController
    
    @property
    def fileSystem(self):
        return self._fileSystem
    
    @property
    def memoryManager(self):
        return self._memoryManager
    
    @property
    def loader(self):
        return self._loader
    
    @property
    def dispatcher(self):
        return self._dispatcher
    
    @property
    def pcbTable(self):
        return self._pcbTable
    
    @property
    def scheduler(self):
        return self._scheduler

    ## emulates a "system call" for programs execution
    def run(self, programPath, priority):
        parameters = {'programPath': programPath, 'priority': priority}
        newIRQ = IRQ(NEW_INTERRUPTION_TYPE, parameters)
        HARDWARE.interruptVector.handle(newIRQ)

    def __repr__(self):
        return "Kernel "
