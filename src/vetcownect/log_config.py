import logging


def get_logger(name):
    """
    Get a logger object with the given name.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    file_handler = logging.FileHandler("vetcownect.log")
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger
