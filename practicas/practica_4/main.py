from hardware import *
from so import *
import log


##
##  MAIN 
##
if __name__ == '__main__':
    log.setupLogger()
    log.logger.info('Starting emulator')

    ## setup our hardware and set memory size to 25 "cells"
    HARDWARE.setup(25)
    '''
    ## Switch on computer
    HARDWARE.switchOn()
    '''
    ## new create the Operative System Kernel
    # "booteamos" el sistema operativo
    kernel = Kernel()
    '''
    ##  create a program
    prg = Program("test.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.IO(), ASM.CPU(3)])
    
    # execute the program
    kernel.run(prg)
    '''
    # Ahora vamos a intentar ejecutar 3 programas a la vez
    ###################
    prg1 = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(2), ASM.IO(), ASM.CPU(2)])
    prg2 = Program("prg2.exe", [ASM.CPU(5)])
    prg3 = Program("prg3.exe", [ASM.CPU(3), ASM.IO(), ASM.CPU(3)])

    # execute all programs
    kernel.run(prg1, 3)  ## 1 = prioridad del proceso
    kernel.run(prg2, 1)  ## 2 = prioridad del proceso
    kernel.run(prg3, 5)  ## 3 = prioridad del proceso


    ## start
    HARDWARE.switchOn()





