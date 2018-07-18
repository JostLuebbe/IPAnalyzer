import logging as lg
import os
import sys


def logging_setup_main():
    if not os.path.exists('./output'):
        os.makedirs('./output')

    stream_log_format = lg.Formatter(
        '[%(asctime)s] [%(threadName)s] [%(levelname)-9s] %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S%p'
    )
    file_log_format = lg.Formatter(
        "[%(asctime)s] [%(threadName)s] [%(levelname)-9s]: %(message)s",
        datefmt='%m/%d/%Y %I:%M:%S%p'
    )

    stream_handler = lg.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(stream_log_format)

    file_handler = lg.FileHandler(
        os.getcwd() + '\output\ip_format.log',
        mode='w'
    )
    file_handler.setFormatter(file_log_format)

    main_logger = lg.getLogger()
    main_logger.setLevel(lg.INFO)
    main_logger.addHandler(stream_handler)
    main_logger.addHandler(file_handler)
