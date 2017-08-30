import logging


class Logger:
    logging.basicConfig(filename="logs.log",
                        level=logging.INFO,
                        format="%(levelname)s %(asctime)s - %(message)s %(funcName)s",
                        filemode='w')
    logger = logging.getLogger()
