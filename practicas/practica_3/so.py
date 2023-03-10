#!/usr/bin/env python

from hardware import *
import log



## emulates a compiled program
class Program():

    def __init__(self, name, instructions):
        self._name = name
        self._instructions = self.expand(instructions)

    @property
    def name(self):
        return self._name

    @property
    def instructions(self):
        return self._instructions

    def addInstr(self, instruction):
        self._instructions.append(instruction)

    def expand(self, instructions):
        expanded = []
        for i in instructions:
            if isinstance(i, list):
                ## is a list of instructions
                expanded.extend(i)
            else:
                ## a single instr (a String)
                expanded.append(i)

        ## now test if last instruction is EXIT
        ## if not... add an EXIT as final instruction
        last = expanded[-1]
        if not ASM.isEXIT(last):
            expanded.append(INSTRUCTION_EXIT)

        return expanded

    def __repr__(self):
        return "Program({name}, {instructions})".format(name=self._name, instructions=self._instructions)


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
            #print(pair)
            pcb = pair['pcb']
            instruction = pair['instruction']
            self._currentPCB = pcb
            self._device.execute(instruction)


    def __repr__(self):
        return "IoDeviceController for {deviceID} running: {currentPCB} waiting: {waiting_queue}".format(deviceID=self._device.deviceId, currentPCB=self._currentPCB, waiting_queue=self._waiting_queue)

NEW = "new"
WAITING = "waiting"
READY = "ready"
RUNNING = "running"
TERMINATED = "terminated"

class Loader():
    
    def __init__(self):
        self._lastMemoryDir = 0
    
    @property
    def lastMemoryDir(self):
        return self._lastMemoryDir

    @lastMemoryDir.setter
    def lastMemoryDir_set(self, addr):
        self._lastMemoryDir = addr
        
    def load(self, program):
        # loads the program in main memory
        progSize = len(program.instructions)
        for index in range(0, progSize):
            inst = program.instructions[index]
            HARDWARE.memory.write(index + self._lastMemoryDir, inst)
        self._lastMemoryDir = self._lastMemoryDir + progSize
        return self._lastMemoryDir - progSize

class Dispatcher():
    
    def load(self, pcb):
        log.logger.info("\n Executing program: {name}".format(name=pcb.programName))
        HARDWARE.cpu.pc = pcb.pc
        HARDWARE.mmu.baseDir = pcb.programBaseDir
    
    def save(self, pcb):
        pcb.pc = HARDWARE.cpu.pc
        HARDWARE.cpu.pc = -1
        
class PCB():
    
    def __init__(self, pid, programBaseDir, programName):
        self._pid = pid
        self._programBaseDir = programBaseDir
        self._programName = programName
        self._state = NEW
        self._pc = 0
    
    @property
    def pid(self):
        return self._pid
    
    @property
    def programBaseDir(self):
        return self._programBaseDir
    
    @property
    def programName(self):
        return self._programName
    
    def setState(self, newState):
        self._state = newState
    
    @property
    def pc(self):
        return self._pc
    
    @pc.setter
    def pc(self, newPc):
        self._pc = newPc

class PCBTable():
    
    def __init__(self):
        self._PCBTable = []
        self._newPID = 1
        self._runningPCB = None
    
    def getPCB(self, PID):
        pass
    
    def addPCB(self, PCB):
        self._PCBTable.append(PCB)
        self._newPID = self._newPID + 1
    
    @property
    def runningPCB(self):
        return self._runningPCB
    
    @runningPCB.setter
    def runningPCB(self, newRunningPCB):
        self._runningPCB = newRunningPCB
    
    @property
    def getNewPID(self):
        return self._newPID

class ReadyQueue():
    
    def __init__(self):
        self._readyQueue = []
    
    def addPCB(self, pcb):
        self._readyQueue.append(pcb)
    
    @property
    def readyQueue(self):
        return self._readyQueue

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
        
        if self.kernel.readyQueue.readyQueue:
            pcbToLoad = self.kernel.readyQueue.readyQueue.pop(0)
            self.kernel.pcbTable.runningPCB = pcbToLoad
            pcbToLoad.setState(RUNNING)
            self.kernel.dispatcher.load(pcbToLoad)
        else:
            self.kernel.pcbTable.runningPCB = None
            HARDWARE.cpu.pc = -1
            
        if not (self.kernel.readyQueue.readyQueue) and HARDWARE.ioDevice.is_idle:
            log.logger.info(" Program Finished ")
            HARDWARE.switchOff()
        '''
        if not (self.kernel.readyQueue.readyQueue or self.kernel.ioDeviceController.waiting_queue):
            print(self.kernel.readyQueue.readyQueue)
            print(self.kernel.ioDeviceController.waiting_queue)
            log.logger.info(" Program Finished ")
              ## dejamos el CPU IDLE
            HARDWARE.switchOff()
        
        log.logger.info(" Program Finished ")
        HARDWARE.cpu.pc = -1  ## dejamos el CPU IDLE
        '''

class IoInInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        
        operation = irq.parameters
        pcb = self.kernel.pcbTable.runningPCB
        self.kernel.dispatcher.save(pcb)
        pcb.setState(WAITING)
        self.kernel.ioDeviceController.runOperation(pcb, operation)
        
        if self.kernel.readyQueue.readyQueue:
            pcbToLoad = self.kernel.readyQueue.readyQueue.pop(0)
            self.kernel.pcbTable.runningPCB = pcbToLoad
            self.kernel.dispatcher.load(pcbToLoad)
        else:
            self.kernel.pcbTable.runningPCB = None
            HARDWARE.cpu.pc = -1
        '''
        operation = irq.parameters
        pcb = {'pc': HARDWARE.cpu.pc} # porque hacemos esto ???
        HARDWARE.cpu.pc = -1   ## dejamos el CPU IDLE
        self.kernel.ioDeviceController.runOperation(pcb, operation)
        log.logger.info(self.kernel.ioDeviceController)
        '''


class IoOutInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        
        pcb = self.kernel.ioDeviceController.getFinishedPCB()
        
        if self.kernel.pcbTable.runningPCB:
            pcb.state = READY
            self.kernel.readyQueue.addPCB(pcb)
        else:
            self.kernel.dispatcher.load(pcb)
            self.kernel.pcbTable.runningPCB = pcb
            pcb.setState(RUNNING)
        
        '''
        pcb = self.kernel.ioDeviceController.getFinishedPCB()
        HARDWARE.cpu.pc = pcb['pc']
        log.logger.info(self.kernel.ioDeviceController)
        '''
        

class NewInterruptionHandler(AbstractInterruptionHandler):
    
    def execute(self, irq):
        program = irq.parameters
        pid = self.kernel.pcbTable.getNewPID
        programBaseDir = self.kernel.loader.load(program)
        newPCB = PCB(pid, programBaseDir, program.name)
        self.kernel.pcbTable.addPCB(newPCB)
        
        if self.kernel.pcbTable.runningPCB:
            newPCB.setState(READY)
            self.kernel.readyQueue.addPCB(newPCB)
        else:
            self.kernel.dispatcher.load(newPCB)
            newPCB.setState(RUNNING)
            self.kernel.pcbTable.runningPCB = newPCB

# emulates the core of an Operative System
class Kernel():

    def __init__(self):
        ## setup interruption handlers
        killHandler = KillInterruptionHandler(self)
        HARDWARE.interruptVector.register(KILL_INTERRUPTION_TYPE, killHandler)

        ioInHandler = IoInInterruptionHandler(self)
        HARDWARE.interruptVector.register(IO_IN_INTERRUPTION_TYPE, ioInHandler)

        ioOutHandler = IoOutInterruptionHandler(self)
        HARDWARE.interruptVector.register(IO_OUT_INTERRUPTION_TYPE, ioOutHandler)
        
        newHandler = NewInterruptionHandler(self)
        HARDWARE.interruptVector.register(NEW_INTERRUPTION_TYPE, newHandler)

        ## controls the Hardware's I/O Device
        self._ioDeviceController = IoDeviceController(HARDWARE.ioDevice)

        self._loader = Loader()
        self._dispatcher = Dispatcher()
        self._pcbTable = PCBTable()
        self._readyQueue = ReadyQueue()

    @property
    def ioDeviceController(self):
        return self._ioDeviceController
    
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
    def readyQueue(self):
        return self._readyQueue

    ## emulates a "system call" for programs execution
    '''
        def run(self, program):
        self.load_program(program)
        log.logger.info("\n Executing program: {name}".format(name=program.name))
        log.logger.info(HARDWARE)

        # set CPU program counter at program's first intruction
        HARDWARE.cpu.pc = 0
    '''
    
    def run(self, program):
        newIRQ = IRQ(NEW_INTERRUPTION_TYPE, program)
        HARDWARE.interruptVector.handle(newIRQ)
        log.logger.info(HARDWARE)

    def __repr__(self):
        return "Kernel "
