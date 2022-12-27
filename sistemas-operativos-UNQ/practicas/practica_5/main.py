from hardware import *
from so.so import *
from shell import *
import log
from threading import Thread

##
##  MAIN 
##
             
if __name__ == '__main__':
    
    log.setupLogger()
    log.setupShellLogger()
    log.setupGanttLogger()
    log.logger.info('Starting emulator')
    

    ## setup our hardware and set memory size to 25 "cells"
    HARDWARE.setup(20)

    ## Switch on computer
    HARDWARE.switchOn()

    ## new create the Operative System Kernel
    # "booteamos" el sistema operativo
    
    # instancias de schedulers
    schedulerFCFS = FCFSScheduler()
    #schedulerNPP = NoPreemptivePriorityScheduler()
    #schedulerPP = PreemptivePriorityScheduler()
    #schedulerRR = RoundRobinScheduler(4)
    
    kernel = Kernel(schedulerFCFS)
    
    # Ahora vamos a guardar los programas en el FileSystem
    ##################
    #prg1 = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(1), ASM.IO(), ASM.CPU(2)])
    #prg2 = Program("prg2.exe", [ASM.CPU(4)])
    #prg3 = Program("prg3.exe", [ASM.CPU(3), ASM.IO(), ASM.CPU(1)])
    
    prg1 = Program("prg1.exe", [ASM.CPU(1)])
    prg2 = Program("prg2.exe", [ASM.CPU(1)])
    prg3 = Program("prg3.exe", [ASM.CPU(1)])

    kernel.fileSystem.write("c:/prg1.exe", prg1)
    kernel.fileSystem.write("c:/prg2.exe", prg2)
    kernel.fileSystem.write("c:/prg3.exe", prg3)
    
    # ejecutamos los programas a partir de un "path" (con una prioridad x)
    kernel.run("c:/prg1.exe", 0)
    kernel.run("c:/prg2.exe", 2)
    kernel.run("c:/prg3.exe", 1)
    
    t = Thread(target=shell, args = (kernel, ))
    t.start()