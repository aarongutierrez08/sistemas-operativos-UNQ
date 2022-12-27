import logging

logger = logging.getLogger("so")

def setupLogger():
    ## Configure Logger
    handler = logging.FileHandler("logs//so.log", mode="w")
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

shellLogger = logging.getLogger("shell")

def setupShellLogger():
    ## Configure shell logger
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    shellLogger.addHandler(handler)
    shellLogger.setLevel(logging.DEBUG)

ganttLogger = logging.getLogger("gantt")

def setupGanttLogger():
    ## Configure gantt logger
    handler = logging.FileHandler("logs//gantt.log", mode="w")
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    ganttLogger.addHandler(handler)
    ganttLogger.setLevel(logging.DEBUG)