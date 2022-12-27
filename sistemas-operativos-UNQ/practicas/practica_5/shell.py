import log
from threading import Lock
from hardware import *
from so.pcb import *

def shell(kernel):
    lock = Lock()
    lock.acquire()
    log.shellLogger.info('SHELL ON')
    cmd = "nothing"
    while cmd[0] != "EXIT":
        log.shellLogger.info('tip  \'RUN\'  to run a new program')
        log.shellLogger.info('tip  \'KILL\' to kill current program')
        log.shellLogger.info('tip  \'EXIT\' to switch off the hardware and exit the shell')
        cmd = input().upper().split()
        if cmd[0] == "RUN":
            log.shellLogger.info('order: *programName* *instructions* *programPath* *priority*')
            cmd = input().split()
            try:
                programName = cmd[0].lower()
                programPath = cmd[-2].lower()
                try:
                    priority = int(cmd[-1])
                except:
                    log.shellLogger.exception("priority is not a number")
                    continue
                instructions = []
                for inst in cmd[1:-2]:
                    if inst.upper() == "CPU":
                        instructions.append(ASM.CPU(1))
                    elif inst.upper() == "IO":
                        instructions.append(ASM.IO())
                    else:
                        instructions = []
                        break
                if instructions:
                    prg = Program(programName, instructions)
                    kernel.fileSystem.write(programPath, prg)
                    kernel.run(programPath, priority)
                else:
                    log.shellLogger.error("bad instructions parameters, try again")
                    continue
            except:
                log.shellLogger.exception("bad parameters, try again")
        elif cmd[0] == "KILL":
            if kernel.pcbTable.runningPCB:
                currentPrg = kernel.pcbTable.runningPCB.programPath
                killIRQ = IRQ(KILL_INTERRUPTION_TYPE)
                HARDWARE.interruptVector.handle(killIRQ)
                log.shellLogger.info('current program {prg} killed'.format(prg = currentPrg))
            else:
                log.shellLogger.error('current program no exist')
        elif cmd[0] == "EXIT":
            HARDWARE.switchOff()
            log.shellLogger.info('hardware switch off')
            log.shellLogger.info("SHELL OFF")
                
    lock.release()