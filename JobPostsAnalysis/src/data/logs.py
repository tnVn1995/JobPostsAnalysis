import os
import logging

def log(path, filename, level):
    """[Create a log file to record the experiment's logs]
    
    Arguments:
        path {string} -- path to the directory
        filename {string} -- file name
        level {str} -- level of logging, one of (critical, info, debug, warning)
    
    Returns:
        [obj] -- [logger that record logs]
    """
    loggers = {'info':logging.INFO, 'critical':logging.CRITICAL, 'debug':logging.DEBUG, 'warning':logging.WARNING, 'error':logging.ERROR}
    # check if the file exist
    log_file = os.path.join(path, filename)

    if not os.path.isfile(log_file):
        open(log_file, "w+").close()

    console_logging_format = "%(levelname)s %(message)s"
    file_logging_format = "%(levelname)s: %(asctime)s: %(message)s"

    # configure logger
    logging.basicConfig(level=loggers[level], format=console_logging_format)
    logger = logging.getLogger()
    
    # create a file handler for output file
    handler = logging.FileHandler(log_file)

    # set the logging level for log file
    handler.setLevel(logging.INFO)
    
    # create a logging format
    formatter = logging.Formatter(file_logging_format)
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    return logger


if __name__ == "__main__":
    pass