import logging

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(module)-10s | %(message)s'
    )

    # Console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File
    file_handler = logging.FileHandler('logs/pipeline.log')
    file_handler.setFormatter(formatter)

    # Add both to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger