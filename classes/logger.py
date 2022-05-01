import logging
from datetime import datetime

def setup_logger(name, level=logging.DEBUG):
    """To setup as many loggers as you want"""

    tempoAtual= (datetime.now())

    tempoAtual=tempoAtual.strftime("%d_%m_%Y-%H_%M_%S")

    name=name+"-"+str(tempoAtual)

    log_file="logs/"+name+".log"

    formatter = logging.Formatter('%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger