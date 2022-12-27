from hardware import *

NEW = "new"
WAITING = "waiting"
READY = "ready"
RUNNING = "running"
TERMINATED = "terminated"

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

class PCB():
    
    def __init__(self, pid, pageTable, programPath, priority):
        self._pid = pid
        self._pageTable = pageTable
        self._programPath = programPath
        self._state = NEW
        self._pc = 0
        self._originalPriority = priority
        self._currentPriority = priority
        
    def __lt__(self, other):
        return self._currentPriority < other.currentPriority
    
    @property
    def pid(self):
        return self._pid
    
    @property
    def pageTable(self):
        return self._pageTable
    
    @pageTable.setter
    def pageTable(self, newPageTable):
        self._pageTable = newPageTable
    
    @property
    def programPath(self):
        return self._programPath
    
    def setState(self, newState):
        self._state = newState
    
    @property
    def currentPriority(self):
        return self._currentPriority
    
    @currentPriority.setter
    def currentPriority(self, newPriority):
        self._currentPriority = newPriority
    
    @property
    def originalPriority(self):
        return self._originalPriority
    
    @property
    def pc(self):
        return self._pc
    
    @pc.setter
    def pc(self, newPc):
        self._pc = newPc

class PCBTable():
    
    def __init__(self):
        self._PCBTable = []
        self._newPID = 0
        self._runningPCB = None
    
    def getPCB(self, PID):
        pass
    
    def addPCB(self, PCB):
        self._PCBTable.append(PCB)
    
    @property
    def runningPCB(self):
        return self._runningPCB
    
    @runningPCB.setter
    def runningPCB(self, newRunningPCB):
        self._runningPCB = newRunningPCB
        if self._runningPCB:
            self._runningPCB.setState(RUNNING)
    
    @property
    def getNewPID(self):
        self._newPID = self._newPID + 1
        return self._newPID